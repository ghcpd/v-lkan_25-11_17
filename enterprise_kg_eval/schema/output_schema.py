from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class EntityModel(BaseModel):
    id: str
    type: str
    text: str
    attributes: Dict[str, Any] = Field(default_factory=dict)
    confidence: float
    method: str
    source: Dict[str, Any]


class RelationModel(BaseModel):
    id: str
    type: str
    source: Optional[str]
    target: Optional[str]
    attributes: Dict[str, Any] = Field(default_factory=dict)
    confidence: float
    method: str
    source_context: Dict[str, Any]
