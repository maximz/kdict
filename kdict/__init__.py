"""Kdict."""

__author__ = """Maxim Zaslavsky"""
__email__ = "maxim@maximz.com"
__version__ = "__version__ = '0.1.0'"

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

# Make the kdict class importable via the module, so users can write "from kdict import kdict" instead of "from kdict.core import kdict"
from .core import kdict
