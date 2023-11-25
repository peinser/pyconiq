r"""
Abstract definition of a Payconiq integration.
"""

from __future__ import annotations

import functools

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from http import HTTPStatus
from typing import TYPE_CHECKING

import aiohttp
import ujson

from pyconiq.exceptions import ForbiddenTransactionError
from pyconiq.exceptions import PayconiqTechnicalError
from pyconiq.exceptions import PayconiqUnavailableError
from pyconiq.exceptions import RateLimitError
from pyconiq.exceptions import UnauthorizedError
from pyconiq.exceptions import UnknownTransactionError
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

    def _handle_api_error(
        self,
        status: int,
        payload: dict[str, Any],
        transaction: Transaction | str,
    ) -> None:
        r"""
        Procedure that handles the specified HTTP error given a certain transaction
        or transaction identifier. Calling this method will always throw an exception.
        In particular, this is an internal method that will be called whenever an
        API error has been detected.
        """
        match status:
            case HTTPStatus.UNAUTHORIZED:
                raise UnauthorizedError(payload, self)
            case HTTPStatus.FORBIDDEN:
                raise ForbiddenTransactionError(payload, self)
            case HTTPStatus.NOT_FOUND:
                raise UnknownTransactionError(payload, transaction)
            case HTTPStatus.TOO_MANY_REQUESTS:
                raise RateLimitError(payload)
            case HTTPStatus.INTERNAL_SERVER_ERROR:
                raise PayconiqTechnicalError(payload)
            case HTTPStatus.SERVICE_UNAVAILABLE:
                raise PayconiqUnavailableError(payload)
            case _:
                raise Exception(payload)

    async def _transaction_state(self, transaction: str) -> dict[str, Any]:
        r"""
        Fetches a state object from Payconiq based on the provided transaction
        identifier. If any error occurs, one of the common `pyconiq` exceptions
        will be thrown. In particular, those defined in `_handle_api_error`.
        """
        assert transaction is not None and isinstance(transaction, str)

        async with aiohttp.ClientSession() as session, session.get(
            url=f"{self._base}/v3/payments/{transaction}",
            headers=self._headers,
        ) as response:
            payload = await response.json()
            if not response.ok:
                self._handle_api_error(
                    status=response.status,
                    payload=payload,
                    transaction=transaction,
                )
                # Note, this line won't be reached as an exception will be thrown.

            return payload

    @property
    def base(self) -> str:
        return self._base

    @property
    def merchant(self) -> Merchant:
        return self._merchant

    @abstractmethod
    async def cancel(self, transaction: Transaction) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args: Any, **kwargs: Any) -> Transaction:
        raise NotImplementedError

    async def update(
        self,
        transaction: Transaction,
    ) -> None:
        r"""
        Synchronizes the state of the specified transaction with Payconiq. Note that,
        if any API error occurs, an exception will be thrown corresponding to the
        API error of interest.
        """
        transaction.state = await self._transaction_state(transaction.id)

    async def details(
        self,
        transaction: str,
    ) -> Transaction:
        r"""
        Fetches a transactions based on the specified transaction or payment identifier.
        """
        return Transaction(
            integration=self,
            **await self._transaction_state(transaction),
        )


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
    def terminal(value: TransactionStatus) -> bool:
        r"""
        Indicates whether a transaction state carries the mark `terminal`. A
        transaction marked `terminal` implies that the transaction does not
        changes state. That is, the state is final.
        """
        return value in {
            TransactionStatus.CANCELLED,
            TransactionStatus.EXPIRED,
            TransactionStatus.FAILED,
            TransactionStatus.SUCCEEDED,
        }

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
    def status(self) -> TransactionStatus:
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

    @property
    def state(self) -> dict[str, Any]:
        return self._state

    @state.setter
    def state(self, state: dict[str, Any]) -> None:
        assert state is not None
        self._state = state

    def expired(self) -> bool:
        return self.status == TransactionStatus.EXPIRED

    def pending(self) -> bool:
        return self.status == TransactionStatus.PENDING

    def succeeded(self) -> bool:
        return self.status == TransactionStatus.SUCCEEDED

    def cancelled(self) -> bool:
        return self.status == TransactionStatus.CANCELLED

    def terminal(self) -> bool:
        return TransactionStatus.terminal(self.status)

    async def cancel(self) -> None:
        await self._integration.cancel(self)

    async def update(self) -> None:
        await self._integration.update(self)

    def __str__(self) -> str:
        return ujson.dumps(
            self._state,
            escape_forward_slashes=False,
            encode_html_chars=False,
        )
