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

TODO

Detailed information regarding the Payconiq's API specification can be found
[here](https://developer.payconiq.com/online-payments-dock/).

## Roadmap

TODO
