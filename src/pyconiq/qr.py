r"""
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import qrcode  # type: ignore[import-untyped]

from pyconiq.constants import PYCONIQ_BASE


if TYPE_CHECKING:
    from pyconiq.integrations.base import BaseIntegration


def static(
    pos: str,
    integration: BaseIntegration,
    border: int = 1,
    box_size: int = 10,
    error_correction: int = qrcode.constants.ERROR_CORRECT_L,
) -> qrcode.QRCode:
    r"""
    Generates a static QR code for the Payconiq Instore (v3) API integrations. These
    QR codes are integrated close to the point of sale. In fact, they are inherently
    tied to the location and specifically identifiers the point of sale.
    """
    assert pos is not None and integration is not None

    # Generate the data that we are going to encode in the QR code.
    data = f"{PYCONIQ_BASE}/l/1/{integration.profile}/{pos}".upper()

    # Generate the actual QR code.
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )

    qr.add_data(data)
    qr.make(fit=True)

    return qr
