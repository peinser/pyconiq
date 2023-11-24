r"""
Abstract definition of a Payconiq integration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pyconiq.concepts import Merchant


class BaseIntegration:
    def __init__(self, merchant: Merchant, key: str, base: str):
        super().__init__()
        self._base = base
        self._merchant = merchant
        self._key = key

    @property
    def base(self) -> str:
        return self._base

    @property
    def merchant(self) -> Merchant:
        return self._merchant
