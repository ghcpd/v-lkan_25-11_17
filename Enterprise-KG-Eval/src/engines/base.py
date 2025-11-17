"""Base class for pluggable extraction engines."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class BaseExtractionEngine(ABC):
    """Abstract base class for extraction engines.
    
    Supports pluggable extraction strategies:
    - Regex-based extraction
    - ML model-based extraction
    - LLM-based extraction
    """

    def __init__(self, engine_name: str):
        """Initialize extraction engine.
        
        Args:
            engine_name: Name of the engine for logging
        """
        self.engine_name = engine_name
        logger.info(f"Initialized {engine_name} extraction engine")

    @abstractmethod
    def extract_entities(
        self, 
        document: str, 
        entity_types: List[str]
    ) -> List[Dict[str, Any]]:
        """Extract entities from document.
        
        Args:
            document: Input text document
            entity_types: List of entity types to extract
            
        Returns:
            List of extracted entities with metadata
        """
        pass

    @abstractmethod
    def extract_relations(
        self,
        document: str,
        entities: List[Dict[str, Any]],
        relation_types: List[str]
    ) -> List[Dict[str, Any]]:
        """Extract relations from document.
        
        Args:
            document: Input text document
            entities: List of previously extracted entities
            relation_types: List of relation types to extract
            
        Returns:
            List of extracted relations with metadata
        """
        pass

    def validate_extraction(self, item: Dict[str, Any], item_type: str) -> bool:
        """Validate extracted item format.
        
        Args:
            item: Extracted item to validate
            item_type: Either 'entity' or 'relation'
            
        Returns:
            True if valid, False otherwise
        """
        if item_type == "entity":
            required = {"text", "type", "start", "end", "confidence"}
            return all(k in item for k in required)
        elif item_type == "relation":
            required = {"type", "head", "tail", "confidence"}
            return all(k in item for k in required)
        return False
