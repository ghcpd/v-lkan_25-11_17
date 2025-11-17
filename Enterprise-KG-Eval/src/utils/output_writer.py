"""Unified output writer with strict JSON schema."""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class OutputWriter:
    """Write extraction results to JSON with strict schema validation."""

    # Strict JSON schemas
    ENTITY_SCHEMA = {
        "type": "object",
        "required": ["id", "text", "type", "start", "end", "confidence"],
        "properties": {
            "id": {"type": "string"},
            "text": {"type": "string"},
            "type": {"type": "string"},
            "start": {"type": "integer"},
            "end": {"type": "integer"},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        }
    }

    RELATION_SCHEMA = {
        "type": "object",
        "required": ["id", "type", "head", "tail", "confidence"],
        "properties": {
            "id": {"type": "string"},
            "type": {"type": "string"},
            "head": {"type": "string"},
            "head_text": {"type": "string"},
            "tail": {"type": "string"},
            "tail_text": {"type": "string"},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        }
    }

    def __init__(self, output_dir: str = "output"):
        """Initialize output writer.
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory: {self.output_dir}")

    def write_entities(
        self,
        entities: List[Dict[str, Any]],
        output_file: str = "entities_output.json"
    ) -> str:
        """Write entities to JSON file with schema validation.
        
        Args:
            entities: List of extracted entities
            output_file: Output filename
            
        Returns:
            Path to output file
            
        Raises:
            ValueError: If schema validation fails
        """
        # Validate entities against schema
        for entity in entities:
            if not self._validate_against_schema(entity, self.ENTITY_SCHEMA):
                logger.warning(f"Entity validation failed: {entity}")

        output_path = self.output_dir / output_file
        
        output_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_count": len(entities),
                "schema_version": "1.0.0",
            },
            "entities": entities,
        }

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Wrote {len(entities)} entities to {output_path}")
            return str(output_path)
        except IOError as e:
            logger.error(f"Error writing entities file: {e}")
            raise

    def write_relations(
        self,
        relations: List[Dict[str, Any]],
        output_file: str = "relations_output.json"
    ) -> str:
        """Write relations to JSON file with schema validation.
        
        Args:
            relations: List of extracted relations
            output_file: Output filename
            
        Returns:
            Path to output file
            
        Raises:
            ValueError: If schema validation fails
        """
        # Validate relations against schema
        for relation in relations:
            if not self._validate_against_schema(relation, self.RELATION_SCHEMA):
                logger.warning(f"Relation validation failed: {relation}")

        output_path = self.output_dir / output_file
        
        output_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_count": len(relations),
                "schema_version": "1.0.0",
            },
            "relations": relations,
        }

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Wrote {len(relations)} relations to {output_path}")
            return str(output_path)
        except IOError as e:
            logger.error(f"Error writing relations file: {e}")
            raise

    def write_combined(
        self,
        entities: List[Dict[str, Any]],
        relations: List[Dict[str, Any]],
        output_file: str = "kg_output.json"
    ) -> str:
        """Write combined knowledge graph output.
        
        Args:
            entities: List of extracted entities
            relations: List of extracted relations
            output_file: Output filename
            
        Returns:
            Path to output file
        """
        output_path = self.output_dir / output_file
        
        output_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "entity_count": len(entities),
                "relation_count": len(relations),
                "schema_version": "1.0.0",
            },
            "entities": entities,
            "relations": relations,
        }

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Wrote combined KG output to {output_path}")
            return str(output_path)
        except IOError as e:
            logger.error(f"Error writing combined output: {e}")
            raise

    @staticmethod
    def _validate_against_schema(item: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """Validate item against JSON schema.
        
        Args:
            item: Item to validate
            schema: Schema to validate against
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in item:
                return False
        return True
