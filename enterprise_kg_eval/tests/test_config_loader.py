from enterprise_kg_eval.config_loader import ConfigLoader
from pathlib import Path


def test_load_configs():
    base = Path(__file__).resolve().parents[2]
    entities_path = base / 'entities.json'
    relations_path = base / 'relations.json'
    loader = ConfigLoader(str(entities_path), str(relations_path))
    entities = loader.load_entities()
    relations = loader.load_relations()
    assert isinstance(entities, dict)
    assert isinstance(relations, dict)
    assert 'Person' in entities
    assert 'works_at' in relations
