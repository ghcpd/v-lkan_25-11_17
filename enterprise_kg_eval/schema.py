"""Output schema definitions for JSON validation."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

import jsonschema

OUTPUT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "component": {"type": "string", "enum": ["entities", "relations"]},
        "metadata": {
            "type": "object",
            "properties": {
                "engine": {"type": "string"},
                "component": {"type": "string"},
                "source_documents": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "generated_at": {"type": "string", "format": "date-time"},
                "document_count": {"type": "integer"},
            },
            "required": ["engine", "generated_at", "document_count"],
        },
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "attributes": {"type": ["object", "null"]},
                    "source_sentence": {"type": ["string", "null"]},
                    "metadata": {"type": "object"},
                    "subject_id": {"type": ["string", "null"]},
                    "object_id": {"type": ["string", "null"]},
                },
                "required": ["id", "type"],
            },
        },
    },
    "required": ["component", "metadata", "results"],
}


def validate_output(payload: Dict[str, Any]) -> None:
    """Raise if the payload does not match the schema."""

    jsonschema.validate(payload, OUTPUT_SCHEMA)
    generated_at = payload["metadata"].get("generated_at")
    if generated_at:
        datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
