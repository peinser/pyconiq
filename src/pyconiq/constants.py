r"""
A set of final variables that are constant with respect to the runtime of the
program executing this module. All constants have default values, which can be `None`.

Constants:

  PYCONIQ_DEFAULT_MERCHANT
    Holds the default merchant identifier to be used within `pyconiq`. If no such
    environment variable is specified, it's default value will be None.

  PYCONIQ_BASE
    The base endpoint to use when interacting with Payconiq's servers. If no
    environment variable is specified, it's default value is `https://payconiq.com`.

  PYCONIQ_API_KEY_STATIC
  PYCONIQ_API_KEY_INVOICE
  PYCONIQ_API_KEY_RECEIPT
  PYCONIQ_API_KEY_APP2APP
    Default API keys that will be used in the corresponding intergrations. If the
    environment variable has not been provided, the respective default will be `None`.
"""

from __future__ import annotations

import os


PYCONIQ_API_KEY_STATIC: str | None = os.getenv("PYCONIQ_API_KEY_STATIC", None)
PYCONIQ_API_KEY_INVOICE: str | None = os.getenv("PYCONIQ_API_KEY_INVOICE", None)
PYCONIQ_API_KEY_RECEIPT: str | None = os.getenv("PYCONIQ_API_KEY_RECEIPT", None)
PYCONIQ_API_KEY_APP2APP: str | None = os.getenv("PYCONIQ_API_KEY_APP2APP", None)

PYCONIQ_DEFAULT_MERCHANT: str | None = os.getenv("PYCONIQ_DEFAULT_MERCHANT", None)

PYCONIQ_API_BASE: str = os.getenv("PYCONIQ_API_BASE", "https://api.payconiq.com")
PYCONIQ_BASE: str = os.getenv("PYCONIQ_BASE", "https://payconiq.com")
