r"""
Abstract definition of a Payconiq integration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pyconiq.merchant import BaseMerchant


class BaseIntegration:
    def __init__(self, merchant: BaseMerchant):
        super().__init__()
        self._merchant = merchant

    @property
    def merchant(self) -> BaseMerchant:
        return self._merchant
