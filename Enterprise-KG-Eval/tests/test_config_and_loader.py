from enterprise_kg_eval.config import load_config
from enterprise_kg_eval.data_loader import load_documents

def test_load_config_entities():
    cfg = load_config('entities.json')
    assert isinstance(cfg, dict)


def test_load_documents():
    docs = load_documents('documents.txt')
    assert isinstance(docs, list)
    assert len(docs) > 0
