from typing import List, Dict, Any
from .base_engine import BaseEngine


class MLEngine(BaseEngine):
    """Simple placeholder ML engine: rule-based but with different scoring.
    Could be extended to load ML models.
    """

    def extract_entities(self, text: str, entity_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        # For this placeholder, just return empty list — could be implemented with a trained model
        return []

    def extract_relations(self, text: str, entities: List[Dict[str, Any]], relation_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        return []
