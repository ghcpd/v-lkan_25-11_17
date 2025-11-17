from typing import List, Dict, Any
from ..data_loader import DataLoader
from ..config_loader import ConfigLoader
from ..pipelines.engine_factory import get_engine
from ..output_writer import OutputWriter
from pathlib import Path


class RelationExtractorPipeline:
    def __init__(self, relations_config_path: str, documents_path: str, entities: List[Dict[str, Any]], output_path: str, engine: str = "regex"):
        self.loader = DataLoader(documents_path)
        self.config = ConfigLoader('', relations_config_path)
        self.engine = get_engine(engine)
        self.output_path = Path(output_path)
        self.entities = entities

    def run(self) -> List[Dict[str, Any]]:
        docs = self.loader.load()
        relation_defs = self.config.load_relations()
        all_relations = []
        for doc_id, doc in enumerate(docs):
            rels = self.engine.extract_relations(doc, self.entities, relation_defs)
            for r in rels:
                r.setdefault("source_context", {})
                r["source_context"]["doc_id"] = doc_id
                r["source_context"]["text"] = doc
            all_relations.extend(rels)

        # deduplicate
        seen = {}
        deduped = []
        for r in all_relations:
            if r["id"] not in seen:
                seen[r["id"]] = r
                deduped.append(r)
        OutputWriter.write_json(deduped, self.output_path)
        return deduped
