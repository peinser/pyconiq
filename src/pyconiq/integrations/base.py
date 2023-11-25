r"""
Abstract definition of a Payconiq integration.
"""

from __future__ import annotations

import functools

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

import ujson

from pyconiq.exceptions import UnknownTransactionStatusError


if TYPE_CHECKING:
    from typing import Any
    from typing import Final

    from pyconiq.concepts import Merchant


class BaseIntegration(ABC):
    def __init__(self, merchant: Merchant, key: str, base: str):
        super().__init__()
        self._base = base
        self._merchant = merchant
        self._key = key

    @functools.cached_property
    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._key}"}

    @property
    def base(self) -> str:
        return self._base

    @property
    def merchant(self) -> Merchant:
        return self._merchant

    @abstractmethod
    async def create(self, *args: Any, **kwargs: Any) -> Transaction:
        raise NotImplementedError

    @abstractmethod
    async def cancel(self, transaction: Transaction) -> None:
        raise NotImplementedError


class TransactionStatus(StrEnum):
    AUTHORIZATION_FAILED: Final = "AUTHORIZATION_FAILED"
    AUTHORIZED: Final = "AUTHORIZED"
    CANCELLED: Final = "CANCELLED"
    EXPIRED: Final = "EXPIRED"
    FAILED: Final = "FAILED"
    IDENTIFIED: Final = "IDENTIFIED"
    PENDING: Final = "PENDING"
    SUCCEEDED: Final = "SUCCEEDED"

    @staticmethod
    def parse(state: dict[str, Any]) -> TransactionStatus:
        r"""
        Returns a TransactionStatus instance based on the raw state of a Transaction.
        """
        status = state.get("status", None)

        assert status is not None

        status = status.upper()

        if status not in TransactionStatus:
            raise UnknownTransactionStatusError(
                f"{status} is not a valid transaction status."
            )

        return TransactionStatus[status]


@dataclass
class TransactionLinks:
    cancel: str | None
    deeplink: str | None
    self: str | None
    qr: str | None

    KEY_LINKS: Final = "_links"
    KEY_CANCEL: Final = "cancel"
    KEY_DEEPLINK: Final = "deeplink"
    KEY_SELF: Final = "self"
    KEY_QR: Final = "qrcode"
    KEY_HREF: Final = "href"

    @staticmethod
    def parse(state: dict[str, Any]) -> TransactionLinks:
        r"""
        Utility method that parses the specified transaction state into a
        TransactionLinks data class for easy link accessability.
        """
        links = state.get(TransactionLinks.KEY_LINKS, {})

        cancel = links.get(TransactionLinks.KEY_CANCEL, {}).get(
            TransactionLinks.KEY_HREF, None
        )

        deeplink = links.get(TransactionLinks.KEY_DEEPLINK, {}).get(
            TransactionLinks.KEY_HREF, None
        )

        self = links.get(TransactionLinks.KEY_SELF, {}).get(
            TransactionLinks.KEY_HREF, None
        )

        qr = links.get(TransactionLinks.KEY_QR, {}).get(TransactionLinks.KEY_HREF, None)

        return TransactionLinks(
            cancel=cancel,
            deeplink=deeplink,
            self=self,
            qr=qr,
        )


class Transaction:
    def __init__(
        self,
        integration: BaseIntegration,
        **kwargs: Any,
    ) -> None:
        self._integration = integration
        self._state = kwargs
        self.links = TransactionLinks.parse(kwargs)

    @functools.cached_property
    def id(self) -> str:
        identifier = self._state.get("paymentId")
        assert identifier is not None
        return identifier

    @property
    def status(self) -> str:
        return TransactionStatus.parse(self._state)

    @status.setter
    def status(self, status: TransactionStatus) -> None:
        self._state["status"] = status

    @property
    def reference(self) -> str | None:
        return self._state.get("reference", None)

    @property
    def json(self) -> dict:
        return self._state

    def pending(self) -> bool:
        return self.status == TransactionStatus.PENDING

    def succeeded(self) -> bool:
        return self.status == TransactionStatus.SUCCEEDED

    async def cancel(self) -> None:
        await self._integration.cancel(self)

    def __str__(self) -> str:
        return ujson.dumps(
            self._state,
            escape_forward_slashes=False,
            encode_html_chars=False,
        )
