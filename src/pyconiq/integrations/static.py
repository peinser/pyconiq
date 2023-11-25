r"""
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import aiohttp

from pyconiq.constants import PYCONIQ_API_BASE
from pyconiq.constants import PYCONIQ_API_KEY_STATIC
from pyconiq.integrations.base import BaseIntegration
from pyconiq.integrations.base import Transaction
from pyconiq.integrations.base import TransactionStatus


if TYPE_CHECKING:
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
                self._handle_api_error(
                    status=status,
                    payload=await response.json(),
                    transaction=transaction,
                )
                # Note, this line won't be reached as an exception will be thrown.

        # Set the transaction to CANCELLED.
        transaction.status = TransactionStatus.CANCELLED

    async def create(
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
