<div align="center">
  <img src="https://github.com/peinser/pyconiq/actions/workflows/docs.yml/badge.svg">
  <img src="https://github.com/peinser/pyconiq/actions/workflows/image.yml/badge.svg">
  <img src="https://github.com/peinser/pyconiq/actions/workflows/pypi.yml/badge.svg">
  <img src="https://badgen.net/badge/license/Apache-2.0/blue">
  <img src="https://img.shields.io/pypi/v/pyconiq">
  <img src="https://badgen.net/badge/code%20style/black/black">
  <img src="https://img.shields.io/docker/v/peinser/pyconiq">
</div>

<p align="center">
   <img src="docs/assets/logo.png" height=100%>
</p>

--------------------------------------------------------------------------------

_Unofficial_ `async` Python module to interface with the payment processor
[Payconiq](https://www.payconiq.com/).

## Introduction

> [!WARNING]
> This is an initial PoC and integration of the module. The API will most likely change in future releases.

### Installation

The module can be directly installed through pip:

```bash
pip install pyconiq
```

For development purposes, and once the project cloned or the codespace ready,
you can install the project
dependencies. You can use the `dev` extra to install the development
dependencies.

```bash
poetry install --with=dev
```

Or using pip:

```bash
pip install -e .[dev]
```

### Getting started

Before you can integrate your application with [Payconiq](https://www.payconiq.com/),
you need access to a so-called _Merchant_ profile. The process of onboarding with
Payconiq, both for their development (`EXT`) and production (`PROD`) environment
involves opening a support ticket (e-mail) and exchanging some information to setup
your account. In particular, your mobile phone number, address, Tax ID (if availablef),
and company name amongst others. The onboarding procedure is outlined
[here](https://developer.payconiq.com/online-payments-dock/).

> [!IMPORTANT]
> You will have to provide a _default_ callback URL to the support team that Payconiq will use to send updates regarding payment requests and transactions.

Once onboarded by the support team, you'll most likely have access to the
`EXT` infrastructure. This means you have access to the necessary API keys and unique
merchant identifier. In the wild, the most common integration a consumer will experience
(we think) is the _Static QR_ code integration. This QR code is uniquely tied to a
specific _Point of Sale_ (PoS) of a merchant. Meaning, a Point of Sale is uniquely
identified by the tuple (Merchant ID and PoS ID), the latter is in _your_ control.

### Environment variables

`pyconiq` supports to inject several runtime defaults through environment variables.
This is especially useful when targetting the `EXT` infrastructure compared to the
_default_ `PROD` infrastructure.

| Variable | Default | Context |
|---|---|---|
| `PYCONIQ_BASE` | `https://payconiq.com` | TODO |
| `PYCONIQ_API_BASE` | `https://api.payconiq.com` | The primary API endpoint of Payconiq (or some mock service). By default this variable will target the Payconiq production environment. For the `EXT` environment this variable should be set to `https://api.ext.payconiq.com`. Note that setting this environment variable is not necessary. It can be defined in the codebase when allocating specific integrations. |
| `PYCONIQ_DEFAULT_MERCHANT` | `None` | Default Merchant ID that will be used when allocating merchants. |
| `PYCONIQ_API_KEY_STATIC` | `None` | Default API key for the Static QR code integration. |
| `PYCONIQ_API_KEY_INVOICE` | `None` | Default API key for the Invoice integration whenever no key is manually specified. |
| `PYCONIQ_API_KEY_RECEIPT` | `None` | Default API key for the Receipt integration whenever no key is manually specified. |
| `PYCONIQ_API_KEY_APP2APP` | `None` | Default API key for the App2App integration whenever no key is manually specified. |                                                                                                                                                                                    |

### Example

First, before you use the [Static QR](https://developer.payconiq.com/online-payments-dock/#payconiq-instore-v3-static-qr-sticker)
integration, you need a QR code for your customers to scan. You can obtain this QR
code through Payconiq's API. However, `pyconiq` provides a utility to generate
this on the fly for you, with various error correction levels and customization options.
This functionality is powered by the awesome [`qrcode`](https://github.com/lincolnloop/python-qrcode) module.

```python
import pyconiq.qr

# Assign a unique identifier to your point of sale.
# This is managed by us, the merchant.
point_of_sale_id = "test"

# Set your merchant configuration, this will implicetly use the
# `PYCONIQ_DEFAULT_MERCHANT` environment variable for populating
# the merchant identifier.
merchant = pyconiq.merchant()

# Alternatively, the merchant can be generated as.
merchant = pyconiq.merchant(merchant_id="YourMerchantIdentifier")

# Second, we need a QR code that is associated with our PoS (point of sale).
# In this case, the identifier of the PoS is `test`.
qr = pyconiq.qr.static(merchant=merchant, pos=point_of_sale_id)
# Show the QR code in the terminal.
qr.print_ascii(tty=True)
```

this produces the following QR code (in your terminal) for our test Merchant;

```console
█▀▀▀▀▀▀▀██▀█████▀▀▀█▀█▀▀▀▀█▀▀▀▀▀▀▀█
█ █▀▀▀█ █▄ ▀ ▄█▀█▀█▄█▀  ███ █▀▀▀█ █
█ █   █ █▄▄▀▄▀▀▀▀▄▄▄▀▀▀▄▀▀█ █   █ █
█ ▀▀▀▀▀ █ █ █▀▄ ▄ █▀█▀▄ █ █ ▀▀▀▀▀ █
█▀▀▀▀▀█▀▀▀▀▀█ ▄▀ █▀▄▄▀▄▀▄█▀█▀█▀█▀██
█▀▄██▄█▀██ █▀▀██▄▄█ ▄█ ▀▄▄▄▄██▀▄ ▄█
███ ▄▀▀▀██ ▄ ██▄█ ▀▀▄▀▄█ ▀▄█  ▀▄███
█  █▀▄▀▀▀█▄▄█▄   ▀██▄█  ▄▄▀ ▀▀██ ▄█
████▄  ▀██▀ █ ▄▀ █▀ █ ▄▀█▄▀▄▀ █▄▀██
█▄ █▄▄ ▀▀▄█▀▀▀██▄▄▄▀▄▀▄█▄▄█▄█▀ █ ▄█
█▀█▀▀▄▀▀▄▄ █ ██▄█▄▀▄█ ▄█ ▀ ▄▀ █▄▀██
█ █▄▀▄▄▀  ▄▀█▄   █▀ ▄█▄▄▄ ▀ █▀ █ ▄█
█ █ █▀▄▀ █▄▀█ ▄▀  ▀ ▀▀▄▄▀▀   ▀ ▄█▀█
█▀▀▀▀▀▀▀█ █▄▀▀██▀  ▄▄█▄ ▀ █▀█ █ ▀▄█
█ █▀▀▀█ █▀▀  ██▄▀▀▀█▄▀▄▄▄ ▀▀▀ ▄▄▀▄█
█ █   █ █ █▀█▄  ▀ ██▄█   █▄▀▄▄▀ ▄▄█
█ ▀▀▀▀▀ █ ▄▄█ ▄▀ ▄▀▄▀▀▄██▀ ▄▀▀ ▄▀██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
```

Once the QR code has been generated, we can now create payment requests (which we
call transactions internally). Such requests are allocated through "Integrations".
For this particular type, we're using a `StaticIntegration`, which corresponds to the
integration supported the previously generated static QR code.

```python
# Initiate a payment request with a static QR integration.
integration = StaticIntegration(merchant=merchant)
transaction = await integration.create(
  amount=2000,  # IMPORTANT: Amount is in Eurocent
  pos=point_of_sale_id,
  reference="PYCONIQ TEST",  # Reference that will appear as a reference in the bank log.
)
```

> [!TIP]
> You can specify custom Callback URL's using the `callback` parameter when creating transactions.

At this point, the transaction has been allocated and is currently in a `PENDING` state.
For the Static QR integration, transactions remain in a `PENDING` state for about 2
minutes before expiring. Updates regarding payment information will be provided through
the callback URL. However, if you're simply testing locally, you can poll the status
of the transaction like this:

```python
#Just scan the QR code now.
while not transaction.terminal():  # Is the transaction in a `terminal` state?
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
```

> [!IMPORTANT]
> The infrastructure supporting the External build is switched off each day from 21h30(CET) to 6h00 (CET) and during the weekends from Friday 21h30 (CET) until Monday 6h00 (CET).

Detailed information regarding the Payconiq's API specification can be found
[here](https://developer.payconiq.com/online-payments-dock/).

## Roadmap

Currently, only the [Static QR](https://developer.payconiq.com/online-payments-dock/#payconiq-instore-v3-static-qr-sticker) code integration is supported.
In the near future,
we intent to support the [Invoice](https://developer.payconiq.com/online-payments-dock/#payconiq-invoice-v3-invoice) integration.
