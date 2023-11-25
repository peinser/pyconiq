r"""
"""

from __future__ import annotations

import functools

from dataclasses import dataclass
from enum import StrEnum
from http import HTTPStatus
from typing import TYPE_CHECKING

import aiohttp
import ujson

from pyconiq.constants import PYCONIQ_API_BASE
from pyconiq.constants import PYCONIQ_API_KEY_STATIC
from pyconiq.exceptions import ForbiddenTransactionError
from pyconiq.exceptions import PayconiqTechnicalError
from pyconiq.exceptions import PayconiqUnavailableError
from pyconiq.exceptions import RateLimitError
from pyconiq.exceptions import TransactionNotPendingError
from pyconiq.exceptions import UnauthorizedError
from pyconiq.exceptions import UnknownTransactionError
from pyconiq.exceptions import UnknownTransactionStatusError
from pyconiq.integrations.base import BaseIntegration


if TYPE_CHECKING:
    from typing import Any
    from typing import Final

    from pyconiq.concepts import Merchant


class StaticIntegration(BaseIntegration):
    def __init__(
        self,
        merchant: Merchant,
        key: str | None = PYCONIQ_API_KEY_STATIC,
        base: str = PYCONIQ_API_BASE,
        callback: str | None = None,
    ) -> None:
        assert key is not None
        super().__init__(merchant=merchant, key=key, base=base)

        self._callback = callback

    @property
    def callback(self) -> str | None:
        return self._callback

    async def cancel(
        self,
        transaction: Transaction,
    ) -> None:
        r"""
        Cancels the specified transaction.

        Returns True on success, `False` otherwise.
        """
        endpoint = transaction.links.cancel
        assert endpoint is not None

        async with aiohttp.ClientSession() as session, session.delete(
            url=endpoint,
            headers=self._headers,
        ) as response:
            if not response.ok:
                status = response.status
                payload: dict[str, Any] = await response.json()
                match status:
                    case HTTPStatus.UNAUTHORIZED:
                        raise UnauthorizedError(payload, self)
                    case HTTPStatus.FORBIDDEN:
                        raise ForbiddenTransactionError(payload, self)
                    case HTTPStatus.NOT_FOUND:
                        raise UnknownTransactionError(payload, transaction)
                    case HTTPStatus.UNPROCESSABLE_ENTITY:
                        raise TransactionNotPendingError(payload, transaction)
                    case HTTPStatus.TOO_MANY_REQUESTS:
                        raise RateLimitError(payload)
                    case HTTPStatus.INTERNAL_SERVER_ERROR:
                        raise PayconiqTechnicalError(payload)
                    case HTTPStatus.SERVICE_UNAVAILABLE:
                        raise PayconiqUnavailableError(payload)
                    case _:
                        raise Exception(payload)

        # Set the transaction to CANCELLED.
        transaction.status = TransactionStatus.CANCELLED

    async def request(
        self,
        amount: int,
        pos: str,
        currency: str = "EUR",
        description: str | None = None,
        reference: str | None = None,
    ) -> Transaction:
        r"""
        Method that registeres a Payment Request with Payconiq. The
        caller should provide the `amount` _in EUROCENTS_, the identifier
        of the Point of Sale (PoS) and currency. Note that, the currency
        can only be EUR as of this time. In addition, an optinal transaction
        description and reference can be provided. The reference is of
        particular importance, as this corresponds to the banking reference
        that will be injected in your transaction.
        """

        assert all([amount > 0, pos is not None, currency == "EUR"])

        payload = {
            "amount": amount,
            "currency": currency,
            "posId": pos,
        }

        if description:
            payload["description"] = description

        if reference:
            payload["reference"] = reference

        async with aiohttp.ClientSession() as session, session.post(
            url=f"{self._base}/v3/payments/pos",
            headers=self._headers,
            json=payload,
        ) as response:
            assert response.status == 201  # Payment Request created.
            return Transaction(
                integration=self,
                **await response.json(),
            )


@dataclass
class TransactionLinks:
    cancel: str | None
    deeplink: str | None
    qr: str | None

    KEY_LINKS: Final = "_links"
    KEY_CANCEL: Final = "cancel"
    KEY_DEEPLINK: Final = "deeplink"
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

        qr = links.get(TransactionLinks.KEY_QR, {}).get(TransactionLinks.KEY_HREF, None)

        return TransactionLinks(cancel=cancel, deeplink=deeplink, qr=qr)


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


class Transaction:
    def __init__(
        self,
        integration: StaticIntegration,
        **kwargs,
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
