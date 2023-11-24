r"""
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import aiohttp

from pyconiq.constants import PYCONIQ_API_BASE
from pyconiq.constants import PYCONIQ_API_KEY_STATIC
from pyconiq.integrations.base import BaseIntegration


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

    async def request(
        self,
        amount: int,
        pos: str,
        currency: str = "EUR",
        description: str | None = None,
        reference: str | None = None,
    ):
        r""""""
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
            headers={"Authorization": f"Bearer {self._key}"},
            json=payload,
        ) as response:
            print(response.status)
            print(await response.json())
