r"""
Examples that demonstrates the usage of pyconiq to handle Static QR stickers.

Payconiq developer documentation for Static QR stickers in API v3:
developer.payconiq.com/online-payments-dock/#creating-the-payconiq-static-qr-code
"""

from __future__ import annotations

import asyncio

import pyconiq.qr  # type: ignore[import-untyped]
import uvloop


async def main() -> None:
    # First, we need a QR code that is associated with our PoS (point of sale).
    # In this case, the identifier of the PoS is `test`.
    qr = pyconiq.qr.static(pos="test")
    # Show the QR code in the terminal.
    qr.print_ascii(tty=True)

    # Initiate a payment request.
    # TODO Implement


with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
    runner.run(main())
