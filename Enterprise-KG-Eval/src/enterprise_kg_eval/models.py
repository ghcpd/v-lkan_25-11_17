"""Dataclasses describing standardized prediction outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class EntityPrediction:
    entity_type: str
    text: str
    start: int
    end: int
    confidence: float
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class RelationPrediction:
    relation_type: str
    source: str
    target: str
    evidence: str
    confidence: float
    attributes: Dict[str, str] = field(default_factory=dict)

