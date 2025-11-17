"""Entrypoint exposing the evaluation pipeline via CLI."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict

from .config_loader import ConfigLoader
from .data_loader import load_documents
from .engines import LLMStubEngine, MLEngine, RegexExtractionEngine
from .pipeline import EntityExtractionPipeline, RelationExtractionPipeline
from .writer import UnifiedWriter

ENGINE_REGISTRY: Dict[str, type] = {
    "regex": RegexExtractionEngine,
    "ml": MLEngine,
    "llm": LLMStubEngine,
}


def _build_metadata(engine_name: str, component: str, document_count: int, document_path: Path) -> dict:
    return {
        "engine": engine_name,
        "component": component,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_documents": [str(document_path.resolve())],
        "document_count": document_count,
    }


def _make_engine(name: str, entity_defs: dict, relation_defs: dict):
    engine_cls = ENGINE_REGISTRY.get(name.lower())
    if not engine_cls:
        raise ValueError(f"Unknown engine {name}, choose from {list(ENGINE_REGISTRY)}")
    return engine_cls(entity_defs, relation_defs)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Enterprise KG evaluation runner.")
    parser.add_argument("--documents", default="documents.txt", help="Path to the documents text file.")
    parser.add_argument("--entities", default="entities.json", help="Path to the entity definitions.")
    parser.add_argument("--relations", default="relations.json", help="Path to the relation definitions.")
    parser.add_argument("--engine", default="regex", choices=list(ENGINE_REGISTRY), help="Extraction engine to use.")
    parser.add_argument("--output-dir", default="output", help="Directory to store JSON outputs.")
    parser.add_argument("--entities-output", default=None, help="Explicit path for entity output.")
    parser.add_argument("--relations-output", default=None, help="Explicit path for relation output.")
    args = parser.parse_args(argv)

    base_path = Path.cwd()
    loader = ConfigLoader(base_path)
    entity_defs = loader.load_entity_definitions(Path(args.entities))
    relation_defs = loader.load_relation_definitions(Path(args.relations))

    engine = _make_engine(args.engine, entity_defs, relation_defs)
    documents = load_documents(Path(args.documents))

    entity_pipeline = EntityExtractionPipeline(engine)
    relation_pipeline = RelationExtractionPipeline(engine)

    entity_records = entity_pipeline.run(documents)
    relation_records = relation_pipeline.run(entity_records)

    output_path = Path(args.output_dir)
    writer = UnifiedWriter()

    entity_dest = (
        Path(args.entities_output)
        if args.entities_output
        else output_path / "entities_output.json"
    )
    relation_dest = (
        Path(args.relations_output)
        if args.relations_output
        else output_path / "relations_output.json"
    )

    entity_metadata = _build_metadata(args.engine, "entities", len(documents), Path(args.documents))
    writer.write("entities", entity_records, entity_metadata, entity_dest)

    relation_metadata = _build_metadata(args.engine, "relations", len(documents), Path(args.documents))
    writer.write("relations", relation_records, relation_metadata, relation_dest)


if __name__ == "__main__":
    main()
