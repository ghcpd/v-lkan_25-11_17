"""Unit tests verifying that the writer enforces the schema."""

import json
from pathlib import Path

from enterprise_kg_eval.models import EntityRecord, RelationRecord
from enterprise_kg_eval.writer import UnifiedWriter


def _sample_metadata(component: str) -> dict:
    return {
        "engine": "test",
        "component": component,
        "generated_at": "2025-01-01T00:00:00Z",
        "source_documents": ["documents.txt"],
        "document_count": 1,
    }


def test_writer_can_persist_entities(tmp_path: Path):
    writer = UnifiedWriter()
    entity = EntityRecord(
        id="Person-1",
        type="Person",
        attributes={"name": "Jane Doe", "age": 30, "position": "Engineer", "department": "Engineering"},
        source_sentence="Jane Doe, age 30, works at Example as an Engineer.",
    )
    destination = tmp_path / "entities_output.json"
    writer.write("entities", [entity], _sample_metadata("entities"), destination)
    assert destination.exists()
    payload = json.loads(destination.read_text(encoding="utf-8"))
    assert payload["component"] == "entities"
    assert payload["results"][0]["type"] == "Person"


def test_writer_can_persist_relations(tmp_path: Path):
    writer = UnifiedWriter()
    relation = RelationRecord(
        id="works_at-1",
        type="works_at",
        subject_id="Person-1",
        object_id="Company-1",
        metadata={"confidence": 0.75},
    )
    destination = tmp_path / "relations_output.json"
    writer.write("relations", [relation], _sample_metadata("relations"), destination)
    assert destination.exists()
    payload = json.loads(destination.read_text(encoding="utf-8"))
    assert payload["component"] == "relations"
    assert payload["results"][0]["type"] == "works_at"
