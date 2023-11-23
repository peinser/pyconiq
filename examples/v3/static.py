r"""
Examples that demonstrates the usage of pyconiq to handle Static QR stickers.

Payconiq developer documentation for Static QR stickers in API v3:
developer.payconiq.com/online-payments-dock/#creating-the-payconiq-static-qr-code
"""
from __future__ import annotations

import asyncio

import uvloop


async def main() -> None:
    pass


with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
    runner.run(main())
