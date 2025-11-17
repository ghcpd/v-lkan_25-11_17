from pathlib import Path

from src.enterprise_kg_eval.config_loader import (
    load_config,
    load_entity_schema,
    load_relation_schema,
)


ROOT = Path(__file__).resolve().parents[1]


def test_entity_schema_has_person():
    schema = load_entity_schema(ROOT / "entities.json")
    assert "Person" in schema
    assert len(schema["Person"]) >= 1


def test_relation_schema_count():
    schema = load_relation_schema(ROOT / "relations.json")
    assert len(schema) >= 30
    assert schema["works_at"] == ["Person", "Company"]


def test_load_config_returns_both():
    config = load_config(ROOT / "entities.json", ROOT / "relations.json")

    assert "Company" in config.entities
    assert "develops" in config.relations
