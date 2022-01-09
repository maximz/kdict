"""Ndict."""

__author__ = """Maxim Zaslavsky"""
__email__ = "maxim@maximz.com"
__version__ = "0.0.1"

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

# Make the ndict class importable via the module, so users can write "from ndict import ndict" instead of "from ndict.ndict import ndict"
from .ndict import ndict
