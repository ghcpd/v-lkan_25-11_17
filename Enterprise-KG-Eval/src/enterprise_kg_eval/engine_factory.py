"""Factory helpers for pluggable extraction engines."""

from __future__ import annotations

from typing import Dict, Type

from .engines.base import ExtractionEngine
from .engines.regex_engine import RegexExtractionEngine


ENGINE_REGISTRY: Dict[str, Type[ExtractionEngine]] = {
    "regex": RegexExtractionEngine,
}


def get_engine(name: str) -> ExtractionEngine:
    """Return an engine implementation by key."""
    key = name.lower()
    if key not in ENGINE_REGISTRY:
        supported = ", ".join(sorted(ENGINE_REGISTRY))
        raise ValueError(f"Unsupported engine '{name}'. Available: {supported}")
    return ENGINE_REGISTRY[key]()

