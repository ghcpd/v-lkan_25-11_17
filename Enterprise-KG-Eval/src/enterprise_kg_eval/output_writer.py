"""Utilities to serialize pipeline outputs to disk."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Iterable, List, Sequence

from .entity_pipeline import EntityExtractionResult
from .relation_pipeline import RelationExtractionResult


class UnifiedOutputWriter:
    """Writes entity and relation predictions following a strict schema."""

    def __init__(self, entity_output_path: Path | str, relation_output_path: Path | str) -> None:
        self.entity_output_path = Path(entity_output_path)
        self.relation_output_path = Path(relation_output_path)
        self.entity_output_path.parent.mkdir(parents=True, exist_ok=True)
        self.relation_output_path.parent.mkdir(parents=True, exist_ok=True)

    def write_entities(
        self, project_name: str, results: Sequence[EntityExtractionResult] | Iterable[EntityExtractionResult]
    ) -> Path:
        payload = {
            "project": project_name,
            "generated_at": self._timestamp(),
            "documents": [
                {
                    "document_id": result.document.document_id,
                    "text_checksum": self._checksum(result.document.text),
                    "entities": [
                        {
                            "type": entity.entity_type,
                            "text": entity.text,
                            "start": entity.start,
                            "end": entity.end,
                            "confidence": round(entity.confidence, 3),
                            "attributes": entity.attributes,
                        }
                        for entity in result.predictions
                    ],
                }
                for result in results
            ],
        }
        self._write_json(self.entity_output_path, payload)
        return self.entity_output_path

    def write_relations(
        self, project_name: str, results: Sequence[RelationExtractionResult] | Iterable[RelationExtractionResult]
    ) -> Path:
        payload = {
            "project": project_name,
            "generated_at": self._timestamp(),
            "documents": [
                {
                    "document_id": result.document_id,
                    "relations": [
                        {
                            "type": relation.relation_type,
                            "source": relation.source,
                            "target": relation.target,
                            "confidence": round(relation.confidence, 3),
                            "evidence": relation.evidence,
                            "attributes": relation.attributes,
                        }
                        for relation in result.relations
                    ],
                }
                for result in results
            ],
        }
        self._write_json(self.relation_output_path, payload)
        return self.relation_output_path

    def _write_json(self, path: Path, payload: dict) -> None:
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)

    def _checksum(self, text: str) -> str:
        return sha256(text.encode("utf-8")).hexdigest()

    def _timestamp(self) -> str:
        return datetime.now(tz=timezone.utc).isoformat()

