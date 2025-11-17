"""Data loading module for documents and configurations."""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DocumentLoader:
    """Load and parse document text files."""

    def __init__(self, file_path: str):
        """Initialize document loader.
        
        Args:
            file_path: Path to the documents.txt file
        """
        self.file_path = Path(file_path)
        self.documents: List[str] = []

    def load(self) -> List[str]:
        """Load documents from file.
        
        Returns:
            List of document strings
            
        Raises:
            FileNotFoundError: If document file not found
            IOError: If unable to read file
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Document file not found: {self.file_path}")
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Split by blank lines to handle document boundaries
                self.documents = [doc.strip() for doc in content.split('\n\n') if doc.strip()]
            logger.info(f"Loaded {len(self.documents)} documents from {self.file_path}")
            return self.documents
        except IOError as e:
            logger.error(f"Error reading document file: {e}")
            raise

    def get_documents(self) -> List[str]:
        """Get loaded documents."""
        return self.documents


class ConfigLoader:
    """Load entity and relation type configurations."""

    def __init__(self, entities_path: str, relations_path: str):
        """Initialize config loader.
        
        Args:
            entities_path: Path to entities.json
            relations_path: Path to relations.json
        """
        self.entities_path = Path(entities_path)
        self.relations_path = Path(relations_path)
        self.entities: Dict[str, List[str]] = {}
        self.relations: Dict[str, List[str]] = {}

    def load_entities(self) -> Dict[str, List[str]]:
        """Load entity type definitions.
        
        Returns:
            Dictionary mapping entity type to attributes
            
        Raises:
            FileNotFoundError: If entities.json not found
            json.JSONDecodeError: If invalid JSON
        """
        if not self.entities_path.exists():
            raise FileNotFoundError(f"Entities config not found: {self.entities_path}")
        
        try:
            with open(self.entities_path, 'r', encoding='utf-8') as f:
                self.entities = json.load(f)
            logger.info(f"Loaded {len(self.entities)} entity types")
            return self.entities
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in entities file: {e}")
            raise

    def load_relations(self) -> Dict[str, List[str]]:
        """Load relation type definitions.
        
        Returns:
            Dictionary mapping relation type to entity types
            
        Raises:
            FileNotFoundError: If relations.json not found
            json.JSONDecodeError: If invalid JSON
        """
        if not self.relations_path.exists():
            raise FileNotFoundError(f"Relations config not found: {self.relations_path}")
        
        try:
            with open(self.relations_path, 'r', encoding='utf-8') as f:
                self.relations = json.load(f)
            logger.info(f"Loaded {len(self.relations)} relation types")
            return self.relations
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in relations file: {e}")
            raise

    def load_all(self) -> tuple:
        """Load both entity and relation configs.
        
        Returns:
            Tuple of (entities dict, relations dict)
        """
        entities = self.load_entities()
        relations = self.load_relations()
        return entities, relations

    def get_entity_types(self) -> List[str]:
        """Get list of all entity types."""
        return list(self.entities.keys())

    def get_relation_types(self) -> List[str]:
        """Get list of all relation types."""
        return list(self.relations.keys())
