"""Mocked ML-driven extraction that decorates regex output."""

from __future__ import annotations

from typing import Iterable, List

from ..models import EntityRecord, RelationRecord
from .base import BaseExtractionEngine
from .regex_engine import RegexExtractionEngine


class MLEngine(BaseExtractionEngine):
    """A skeletal ML engine that reuses regex heuristics with extra signals."""

    def __init__(self, entity_definitions: dict, relation_definitions: dict) -> None:
        super().__init__(entity_definitions, relation_definitions)
        self._backbone = RegexExtractionEngine(entity_definitions, relation_definitions)

    def extract_entities(
        self,
        documents: Iterable[str | object],
    ) -> List[EntityRecord]:
        entities = self._backbone.extract_entities(documents)
        for index, entity in enumerate(entities):
            confidence = round(0.55 + (index % 5) * 0.05, 2)
            entity.metadata.setdefault("ml_signals", {})["confidence"] = confidence
            entity.metadata["ml_signals"]["model"] = "mock-tree-forest"
        return entities

    def extract_relations(self, entities: List[EntityRecord]) -> List[RelationRecord]:
        relations = self._backbone.extract_relations(entities)
        for idx, relation in enumerate(relations):
            relation.metadata.setdefault("ml_signals", {})["confidence"] = round(
                0.5 + (idx % 3) * 0.1, 2
            )
            relation.metadata["ml_signals"]["model"] = "mock-tree-forest"
        return relations
