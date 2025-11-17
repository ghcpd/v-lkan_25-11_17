"""Load entity and relation configuration files."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


EntitySchema = Dict[str, List[str]]
RelationSchema = Dict[str, List[str]]


@dataclass(frozen=True)
class ExtractionConfig:
    """Unified configuration container."""

    entities: EntitySchema
    relations: RelationSchema


def _load_json_file(file_path: Path | str) -> dict:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_entity_schema(file_path: Path | str) -> EntitySchema:
    """Load entity-type definitions."""
    data = _load_json_file(file_path)
    if not isinstance(data, dict):
        raise ValueError("Entity schema must be a JSON object.")
    return {str(key): list(value) for key, value in data.items()}


def load_relation_schema(file_path: Path | str) -> RelationSchema:
    """Load relation-type definitions."""
    data = _load_json_file(file_path)
    if not isinstance(data, dict):
        raise ValueError("Relation schema must be a JSON object.")
    return {str(key): list(value) for key, value in data.items()}


def load_config(entity_path: Path | str, relation_path: Path | str) -> ExtractionConfig:
    """Load both entity and relation configuration files."""
    return ExtractionConfig(
        entities=load_entity_schema(entity_path),
        relations=load_relation_schema(relation_path),
    )

