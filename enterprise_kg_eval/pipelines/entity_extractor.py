from typing import List, Dict, Any
from ..data_loader import DataLoader
from ..config_loader import ConfigLoader
from ..pipelines.engine_factory import get_engine
from ..output_writer import OutputWriter
from pathlib import Path


class EntityExtractorPipeline:
    def __init__(self, entities_config_path: str, documents_path: str, output_path: str, engine: str = "regex"):
        self.loader = DataLoader(documents_path)
        self.config = ConfigLoader(entities_config_path, '')
        self.engine = get_engine(engine)
        self.output_path = Path(output_path)

    def run(self) -> List[Dict[str, Any]]:
        docs = self.loader.load()
        entity_defs = self.config.load_entities()
        all_entities = []
        for doc_id, doc in enumerate(docs):
            ents = self.engine.extract_entities(doc, entity_defs)
            # Add source context
            for e in ents:
                e.setdefault("source", {})
                e["source"]["doc_id"] = doc_id
                e["source"]["text"] = doc
            all_entities.extend(ents)

        # deduplicate by (type, text)
        key_map = {}
        deduped = []
        for e in all_entities:
            key = (e["type"], e["text"])
            if key not in key_map:
                key_map[key] = e
                deduped.append(e)
            else:
                # merge attributes
                key_map[key]["attributes"].update(e.get("attributes", {}))
        # write output
        OutputWriter.write_json(list(deduped), self.output_path)
        return deduped
