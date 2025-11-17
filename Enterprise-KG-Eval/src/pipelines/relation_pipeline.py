"""Relation extraction pipeline."""

from typing import List, Dict, Any
import logging

from ..engines.base import BaseExtractionEngine

logger = logging.getLogger(__name__)


class RelationExtractionPipeline:
    """End-to-end relation extraction pipeline."""

    def __init__(self, engine: BaseExtractionEngine, relation_types: List[str]):
        """Initialize relation extraction pipeline.
        
        Args:
            engine: Extraction engine instance
            relation_types: List of relation types to extract
        """
        self.engine = engine
        self.relation_types = relation_types
        self.extracted_relations: List[Dict[str, Any]] = []

    def process(
        self,
        document: str,
        entities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process document and extract relations.
        
        Args:
            document: Input text document
            entities: Previously extracted entities
            
        Returns:
            List of extracted relations
        """
        try:
            logger.info(f"Processing relations with {len(self.relation_types)} relation types")
            relations = self.engine.extract_relations(document, entities, self.relation_types)
            self.extracted_relations = relations
            logger.info(f"Pipeline extracted {len(relations)} relations")
            return relations
        except Exception as e:
            logger.error(f"Error in relation extraction pipeline: {e}")
            raise

    def process_batch(
        self,
        documents: List[str],
        entity_batches: List[List[Dict[str, Any]]]
    ) -> List[List[Dict[str, Any]]]:
        """Process multiple documents for relations.
        
        Args:
            documents: List of documents
            entity_batches: List of entity batches (one per document)
            
        Returns:
            List of relation lists (one per document)
        """
        batch_results = []
        for i, (doc, entities) in enumerate(zip(documents, entity_batches)):
            try:
                relations = self.process(doc, entities)
                batch_results.append(relations)
                logger.info(f"Processed relations for document {i+1}/{len(documents)}")
            except Exception as e:
                logger.error(f"Failed to process relations for document {i+1}: {e}")
                batch_results.append([])
        return batch_results

    def get_statistics(self) -> Dict[str, Any]:
        """Get relation extraction statistics.
        
        Returns:
            Dictionary with statistics
        """
        type_counts = {}
        confidence_scores = []
        
        for relation in self.extracted_relations:
            rtype = relation.get("type", "unknown")
            type_counts[rtype] = type_counts.get(rtype, 0) + 1
            confidence_scores.append(relation.get("confidence", 0))
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        return {
            "total_relations": len(self.extracted_relations),
            "relation_types": type_counts,
            "avg_confidence": round(avg_confidence, 3),
            "min_confidence": min(confidence_scores) if confidence_scores else 0,
            "max_confidence": max(confidence_scores) if confidence_scores else 0,
        }
