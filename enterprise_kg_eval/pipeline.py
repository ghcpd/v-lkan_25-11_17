"""Top-level orchestration for each extraction pipeline."""

from __future__ import annotations

from typing import Iterable, List

from .models import EntityRecord, RelationRecord
from .engines.base import BaseExtractionEngine


class EntityExtractionPipeline:
    """Wraps an engine so pipelines stay consistent."""

    def __init__(self, engine: BaseExtractionEngine):
        self.engine = engine

    def run(self, documents: Iterable[object]) -> List[EntityRecord]:
        return self.engine.extract_entities(documents)


class RelationExtractionPipeline:
    """Create relations from the previously extracted entities."""

    def __init__(self, engine: BaseExtractionEngine):
        self.engine = engine

    def run(self, entities: List[EntityRecord]) -> List[RelationRecord]:
        return self.engine.extract_relations(entities)
