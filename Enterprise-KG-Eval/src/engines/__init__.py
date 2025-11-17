"""Extraction engines module (pluggable architecture)."""

from .base import BaseExtractionEngine
from .regex_engine import RegexExtractionEngine

__all__ = [
    "BaseExtractionEngine",
    "RegexExtractionEngine",
]
