"""Entity extraction pipeline orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .config_loader import EntitySchema
from .data_loader import Document
from .engines.base import ExtractionEngine
from .models import EntityPrediction


@dataclass
class EntityExtractionResult:
    document: Document
    predictions: List[EntityPrediction]


class EntityExtractionPipeline:
    """Coordinates document loading and entity extraction."""

    def __init__(self, engine: ExtractionEngine) -> None:
        self.engine = engine

    def run(
        self, documents: Sequence[Document] | Iterable[Document], entity_schema: EntitySchema
    ) -> List[EntityExtractionResult]:
        results: List[EntityExtractionResult] = []
        for document in documents:
            predictions = self.engine.extract_entities(document, entity_schema)
            results.append(EntityExtractionResult(document=document, predictions=predictions))
        return results

