"""Smoke tests covering the entity/relation pipelines."""

from pathlib import Path

from enterprise_kg_eval.config_loader import ConfigLoader
from enterprise_kg_eval.data_loader import load_documents
from enterprise_kg_eval.engines import RegexExtractionEngine
from enterprise_kg_eval.pipeline import (
    EntityExtractionPipeline,
    RelationExtractionPipeline,
)


def test_pipeline_extracts_all_entity_types():
    repo_root = Path(__file__).resolve().parents[1]
    loader = ConfigLoader(repo_root)
    entity_defs = loader.load_entity_definitions(repo_root / "entities.json")
    relation_defs = loader.load_relation_definitions(repo_root / "relations.json")
    documents = load_documents(repo_root / "documents.txt")

    engine = RegexExtractionEngine(entity_defs, relation_defs)
    entity_pipeline = EntityExtractionPipeline(engine)
    entities = entity_pipeline.run(documents)

    found_types = {entity.type for entity in entities}
    assert set(entity_defs.keys()).issubset(found_types), "Missing entity types"
    assert len(entities) >= len(entity_defs), "Not enough entity rows extracted"

    relation_pipeline = RelationExtractionPipeline(engine)
    relations = relation_pipeline.run(entities)

    assert len(relations) >= len(relation_defs), "Expected a relation per definition"
