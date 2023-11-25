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
your account. This involves your mobile phone number, address, Tax ID (if availablef)
amongst others. The onboarding procedure it outlined
[here](https://developer.payconiq.com/online-payments-dock/).

Once onboarded by the support team, you'll most likely have access to the
`EXT` infrastructure. This means you have access to the necessary API keys and unique
merchant identifier. In the wild, the most common integration a consumer will experience
(we think) is the _Static QR_ code integration. This QR code is uniquely tied to a
specific _Point of Sale_ (PoS) of a merchant. Meaning, a Point of Sale is uniquely
identified by the tuple (Merchant ID and PoS ID), the latter is in _your_ control.

**Important**: the infrastructure supporting the External build is switched off
each day from 21h30(CET) to 6h00 (CET) and during the weekends from Friday 21h30 (CET)
until Monday 6h00 (CET).

Detailed information regarding the Payconiq's API specification can be found
[here](https://developer.payconiq.com/online-payments-dock/).

## Roadmap

Currently, only the [Static QR](https://developer.payconiq.com/online-payments-dock/#payconiq-instore-v3-static-qr-sticker) code integration is supported.
In the near future,
we intent to support the [Invoice](https://developer.payconiq.com/online-payments-dock/#payconiq-invoice-v3-invoice) integration.
