from typing import List, Dict, Any


class BaseEngine:
    """Abstract base class for extraction engines."""

    def extract_entities(self, text: str, entity_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    def extract_relations(self, text: str, entities: List[Dict[str, Any]], relation_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError()
