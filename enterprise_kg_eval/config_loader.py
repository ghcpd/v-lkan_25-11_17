import json
from pathlib import Path
from typing import Dict, Any


def load_json(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with p.open("r", encoding="utf-8") as fh:
        return json.load(fh)


class ConfigLoader:
    def __init__(self, entities_path: str, relations_path: str):
        self.entities_path = entities_path
        self.relations_path = relations_path

    def load_entities(self) -> Dict[str, Any]:
        return load_json(self.entities_path)

    def load_relations(self) -> Dict[str, Any]:
        return load_json(self.relations_path)
