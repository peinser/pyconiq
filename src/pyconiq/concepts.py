r"""
A set of base concepts used throughout `pyconiq` and utility functions to allocate them.
"""

from __future__ import annotations

from pyconiq.constants import PYCONIQ_DEFAULT_MERCHANT


def merchant(merchant_id: str | None = PYCONIQ_DEFAULT_MERCHANT) -> Merchant:
    assert merchant_id is not None
    return Merchant(merchant_id=merchant_id)


class Merchant:
    def __init__(self, merchant_id: str):
        super().__init__()
        self._id = merchant_id

    @property
    def id(self) -> str:
        return self._id
