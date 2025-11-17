from typing import List, Dict, Any


class EntityPipeline:
    def __init__(self, engine):
        self.engine = engine

    def run(self, texts: List[str], entity_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for i, t in enumerate(texts):
            ents = self.engine.extract_entities(t, entity_defs)
            results.append({'doc_id': i, 'text': t, 'entities': ents})
        return results
