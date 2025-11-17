from enterprise_kg_eval.data_loader import DataLoader
from pathlib import Path


def test_data_loader_loads():
    base = Path(__file__).resolve().parents[2]
    docs = base / 'documents.txt'
    loader = DataLoader(str(docs))
    items = loader.load()
    assert isinstance(items, list)
    assert len(items) > 10
    assert all(isinstance(x, str) for x in items)
