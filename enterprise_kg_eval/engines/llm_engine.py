from typing import List, Dict, Any
from .base_engine import BaseEngine
from .regex_engine import RegexEngine
import random


class LLMEngine(BaseEngine):
    """Mock LLM engine — demonstrates swapping engine while remaining testable offline.
    It delegates to the RegexEngine and re-scores/normalizes output.
    """

    def __init__(self, seed: int = 42):
        self._regex = RegexEngine()
        random.seed(seed)

    def extract_entities(self, text: str, entity_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        ents = self._regex.extract_entities(text, entity_defs)
        # Simulate LLM: adjust confidences slightly, and add method "llm"
        for e in ents:
            e["confidence"] = min(0.99, e.get("confidence", 0.8) + random.uniform(0.02, 0.08))
            e["method"] = "llm"
        return ents

    def extract_relations(self, text: str, entities: List[Dict[str, Any]], relation_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        rels = self._regex.extract_relations(text, entities, relation_defs)
        # rescore
        for r in rels:
            r["confidence"] = min(0.99, r.get("confidence", 0.75) + random.uniform(0.01, 0.12))
            r["method"] = "llm"
        return rels
