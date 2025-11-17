"""Relation extraction pipeline orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .config_loader import RelationSchema
from .engines.base import ExtractionEngine
from .entity_pipeline import EntityExtractionResult
from .models import RelationPrediction


@dataclass
class RelationExtractionResult:
    document_id: str
    relations: List[RelationPrediction]


class RelationExtractionPipeline:
    """Runs relation extraction based on prior entity predictions."""

    def __init__(self, engine: ExtractionEngine) -> None:
        self.engine = engine

    def run(
        self,
        entity_results: Sequence[EntityExtractionResult] | Iterable[EntityExtractionResult],
        relation_schema: RelationSchema,
    ) -> List[RelationExtractionResult]:
        results: List[RelationExtractionResult] = []
        for entity_result in entity_results:
            relations = self.engine.extract_relations(
                entity_result.document, entity_result.predictions, relation_schema
            )
            results.append(
                RelationExtractionResult(
                    document_id=entity_result.document.document_id, relations=relations
                )
            )
        return results

