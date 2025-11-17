import json
from pathlib import Path


def write_entities(path, entities):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump({'entities': entities}, f, indent=2)


def write_relations(path, relations):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump({'relations': relations}, f, indent=2)
