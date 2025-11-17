"""Pipeline modules for entity and relation extraction."""

from .entity_pipeline import EntityExtractionPipeline
from .relation_pipeline import RelationExtractionPipeline

__all__ = [
    "EntityExtractionPipeline",
    "RelationExtractionPipeline",
]
