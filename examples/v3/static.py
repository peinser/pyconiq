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

    # Note, you should set the environment variables.
    # !!! Important !!!
    # - PYCONIQ_DEFAULT_MERCHANT
    # - PYCONIQ_PAYMENT_PROFILE_STATIC

    # Set your merchant configuration.
    merchant = pyconiq.merchant()

    # Initiate a payment request with a static QR integration.
    integration = StaticIntegration(merchant=merchant)

    # Second, we need a QR code that is associated with our PoS (point of sale).
    # In this case, the identifier of the PoS is `test`.
    qr = pyconiq.qr.static(integration=integration, pos=point_of_sale_id)
    # Show the QR code in the terminal.
    qr.print_ascii(tty=True)
    qr.make_image().save("static.png")

    # Create a new payment request.
    transaction = await integration.create(
        amount=2000,  # In Eurocent
        pos=point_of_sale_id,
        reference="PYCONIQ TEST",
    )

    # It is also possible to fetch a transaction by its ID. (re-use ID for ease).
    transaction = await integration.details(transaction.id)
    pprint.pprint(transaction.json, compact=True, indent=2)

    # You can also update the state of a transaction. This can be done through
    # the integration interface as.
    await integration.update(transaction)

    # Or simply directly through the transaction object.
    await transaction.update()

    # Enough demonstrations :) Just scan the QR code now.
    while not transaction.terminal():
        await asyncio.sleep(1)
        await transaction.update()

    if transaction.expired():
        print("Failed to pay on time :(")
    elif transaction.succeeded():
        print("Paid!")
    elif transaction.cancelled():
        print("The transaction was cancelled!")
    else:
        print("Some other status :/")


with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
    runner.run(main())
