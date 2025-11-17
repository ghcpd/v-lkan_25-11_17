"""Entity extraction pipeline."""

from typing import List, Dict, Any
import logging

from ..engines.base import BaseExtractionEngine

logger = logging.getLogger(__name__)


class EntityExtractionPipeline:
    """End-to-end entity extraction pipeline."""

    def __init__(self, engine: BaseExtractionEngine, entity_types: List[str]):
        """Initialize entity extraction pipeline.
        
        Args:
            engine: Extraction engine instance
            entity_types: List of entity types to extract
        """
        self.engine = engine
        self.entity_types = entity_types
        self.extracted_entities: List[Dict[str, Any]] = []

    def process(self, document: str) -> List[Dict[str, Any]]:
        """Process document and extract entities.
        
        Args:
            document: Input text document
            
        Returns:
            List of extracted entities
        """
        try:
            logger.info(f"Processing document with {len(self.entity_types)} entity types")
            entities = self.engine.extract_entities(document, self.entity_types)
            self.extracted_entities = entities
            logger.info(f"Pipeline extracted {len(entities)} entities")
            return entities
        except Exception as e:
            logger.error(f"Error in entity extraction pipeline: {e}")
            raise

    def process_batch(self, documents: List[str]) -> List[List[Dict[str, Any]]]:
        """Process multiple documents.
        
        Args:
            documents: List of documents to process
            
        Returns:
            List of entity lists (one per document)
        """
        batch_results = []
        for i, doc in enumerate(documents):
            try:
                entities = self.process(doc)
                batch_results.append(entities)
                logger.info(f"Processed document {i+1}/{len(documents)}")
            except Exception as e:
                logger.error(f"Failed to process document {i+1}: {e}")
                batch_results.append([])
        return batch_results

    def get_statistics(self) -> Dict[str, Any]:
        """Get extraction statistics.
        
        Returns:
            Dictionary with statistics
        """
        type_counts = {}
        confidence_scores = []
        
        for entity in self.extracted_entities:
            etype = entity.get("type", "unknown")
            type_counts[etype] = type_counts.get(etype, 0) + 1
            confidence_scores.append(entity.get("confidence", 0))
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        return {
            "total_entities": len(self.extracted_entities),
            "entity_types": type_counts,
            "avg_confidence": round(avg_confidence, 3),
            "min_confidence": min(confidence_scores) if confidence_scores else 0,
            "max_confidence": max(confidence_scores) if confidence_scores else 0,
        }
