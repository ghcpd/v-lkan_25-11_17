"""Extraction engine interface and helpers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List, Dict

from ..models import EntityRecord, RelationRecord


class BaseExtractionEngine(ABC):
    """Defines the public surface of any extraction engine."""

    def __init__(
        self,
        entity_definitions: Dict[str, list],
        relation_definitions: Dict[str, list],
    ):
        self.entity_definitions = entity_definitions
        self.relation_definitions = relation_definitions

    @abstractmethod
    def extract_entities(
        self,
        documents: Iterable[str | None],
    ) -> List[EntityRecord]:
        """Extract structured entities from a document stream."""

    @abstractmethod
    def extract_relations(self, entities: List[EntityRecord]) -> List[RelationRecord]:
        """Extract relations after entity extraction completes."""
