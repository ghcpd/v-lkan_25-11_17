"""Abstract base classes for extraction engines."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from ..config_loader import EntitySchema, RelationSchema
from ..data_loader import Document
from ..models import EntityPrediction, RelationPrediction


class ExtractionEngine(ABC):
    """Defines the interface for pluggable extraction engines."""

    @abstractmethod
    def extract_entities(
        self, document: Document, entity_schema: EntitySchema
    ) -> List[EntityPrediction]:
        """Return extracted entities for a document."""

    @abstractmethod
    def extract_relations(
        self,
        document: Document,
        entity_predictions: List[EntityPrediction],
        relation_schema: RelationSchema,
    ) -> List[RelationPrediction]:
        """Return extracted relations for a document."""

