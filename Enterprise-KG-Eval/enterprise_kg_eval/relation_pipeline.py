from typing import List, Dict, Any


class RelationPipeline:
    def __init__(self, engine):
        self.engine = engine

    def run(self, texts: List[str], rel_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for i, t in enumerate(texts):
            rels = self.engine.extract_relations(t, rel_defs)
            results.append({'doc_id': i, 'text': t, 'relations': rels})
        return results
