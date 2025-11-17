"""Writes schema-validated JSON outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .models import EntityRecord, RelationRecord
from .schema import OUTPUT_SCHEMA, validate_output


ResultRecord = EntityRecord | RelationRecord


class UnifiedWriter:
    """Write entities or relations with a shared schema."""

    def __init__(self, schema: Dict[str, Any] = OUTPUT_SCHEMA):
        self.schema = schema

    def _build_payload(
        self,
        component: str,
        results: Iterable[ResultRecord],
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "component": component,
            "metadata": metadata,
            "results": [record.to_dict() for record in results],
        }

    def write(
        self,
        component: str,
        results: Iterable[ResultRecord],
        metadata: Dict[str, Any],
        destination: Path,
    ) -> Dict[str, Any]:
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = self._build_payload(component, results, metadata)
        validate_output(payload)
        with destination.open("w", encoding="utf-8") as target:
            json.dump(payload, target, indent=2)
        return payload
