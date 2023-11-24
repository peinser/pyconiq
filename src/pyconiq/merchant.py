r"""
Payconiq is a payment service that enables you to receive payments based on a QR code.
Your customers scan this QR code via the Payconiq By Bancontact app or other payment
apps supporting Payconiq on their smartphone and then confirm the amount to be paid.
The payments are then transferred - individually or grouped - to your bank account.
A merchant is a central concept. It defines the way your clients, Payconiq and you
- the merchant - interact with each other.
"""

from __future__ import annotations


class BaseMerchant:
    def __init__(self, merchant_id: str):
        super().__init__()
        self._id = merchant_id

    @property
    def id(self) -> str:
        return self._id
