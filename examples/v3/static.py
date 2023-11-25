r"""
Examples that demonstrates the usage of pyconiq to handle Static QR stickers.

Payconiq developer documentation for Static QR stickers in API v3:
developer.payconiq.com/online-payments-dock/#creating-the-payconiq-static-qr-code
"""

from __future__ import annotations

import asyncio
import pprint

import pyconiq  # type: ignore[import-untyped]
import pyconiq.qr  # type: ignore[import-untyped]
import uvloop

from pyconiq.integrations.static import (  # type: ignore[import-untyped]
    StaticIntegration,
)


async def main() -> None:
    # Assign a unique identifier to your point of sale.
    point_of_sale_id = "test"

    # Set your merchant configuration.
    merchant = pyconiq.merchant(merchant_id="655dd4b3748285422d94a48b")

    # Second, we need a QR code that is associated with our PoS (point of sale).
    # In this case, the identifier of the PoS is `test`.
    qr = pyconiq.qr.static(merchant=merchant, pos=point_of_sale_id)
    # Show the QR code in the terminal.
    qr.print_ascii(tty=True)

    # Initiate a payment request with a static QR integration.
    integration = StaticIntegration(merchant=merchant)
    transaction = await integration.create(
        amount=2000,  # In Eurocent
        pos=point_of_sale_id,
        reference="PYCONIQ TEST",
    )

    # Object denoting the current state of the payment.
    pprint.pprint(transaction.json, compact=True, indent=2)

    # Cancel the pending transaction.
    await transaction.cancel()
    print(transaction.status)


with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
    runner.run(main())
