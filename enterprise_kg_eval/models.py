"""Shared dataclasses for entity and relation outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EntityRecord:
    id: str
    type: str
    attributes: Dict[str, Any]
    source_sentence: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "attributes": self.attributes,
            "source_sentence": self.source_sentence,
            "metadata": self.metadata,
        }


@dataclass
class RelationRecord:
    id: str
    type: str
    subject_id: str
    object_id: Optional[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "subject_id": self.subject_id,
            "object_id": self.object_id,
            "metadata": self.metadata,
        }
