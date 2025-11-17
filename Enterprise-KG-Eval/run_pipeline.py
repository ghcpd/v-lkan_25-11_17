#!/usr/bin/env python3
"""Command-line runner for Enterprise-KG-Eval."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.enterprise_kg_eval.pipeline_runner import PipelineRunner


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Enterprise-KG-Eval extraction pipelines."
    )
    parser.add_argument("--project-name", default="Enterprise-KG-Eval", help="Project label.")
    parser.add_argument(
        "--documents",
        default="documents.txt",
        help="Path to the enterprise documents text file.",
    )
    parser.add_argument(
        "--entities",
        default="entities.json",
        help="Entity schema definition file.",
    )
    parser.add_argument(
        "--relations",
        default="relations.json",
        help="Relation schema definition file.",
    )
    parser.add_argument(
        "--engine",
        default="regex",
        help="Extraction engine key (regex, llm, ml).",
    )
    parser.add_argument(
        "--output",
        default="output",
        help="Directory for pipeline outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    runner = PipelineRunner(
        project_name=args.project_name,
        documents_path=args.documents,
        entity_config_path=args.entities,
        relation_config_path=args.relations,
        output_dir=Path(args.output),
        engine_name=args.engine,
    )
    entity_path, relation_path = runner.run()
    print(f"Entity output written to: {entity_path}")
    print(f"Relation output written to: {relation_path}")


if __name__ == "__main__":
    main()

