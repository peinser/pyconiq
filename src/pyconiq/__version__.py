r"""
Returns the current version of the `pyconiq` module through the `__version__` variable.
"""

from __future__ import annotations

from importlib.metadata import version


__version__ = version("pyconiq")
