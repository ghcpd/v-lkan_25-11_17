"""LLM-inspired stub engine wrapping the regex extractor."""

from __future__ import annotations

from typing import Iterable, List

from ..models import EntityRecord, RelationRecord
from .base import BaseExtractionEngine
from .regex_engine import RegexExtractionEngine


class LLMStubEngine(BaseExtractionEngine):
    """Simulates an LLM focusing on concise, structured responses."""

    def __init__(self, entity_definitions: dict, relation_definitions: dict) -> None:
        super().__init__(entity_definitions, relation_definitions)
        self._backbone = RegexExtractionEngine(entity_definitions, relation_definitions)

    def extract_entities(
        self,
        documents: Iterable[str | object],
    ) -> List[EntityRecord]:
        entities = self._backbone.extract_entities(documents)
        for entity in entities:
            entity.metadata.setdefault("llm", {})["summary"] = (
                f"{entity.type} from stub LLM"
            )
            entity.metadata["llm"]["confidence"] = 0.7
        return entities

    def extract_relations(self, entities: List[EntityRecord]) -> List[RelationRecord]:
        relations = self._backbone.extract_relations(entities)
        for relation in relations:
            relation.metadata.setdefault("llm", {})["source"] = "stub-prompt"
        return relations
