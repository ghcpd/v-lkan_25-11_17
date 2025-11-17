"""Main execution module for the KG evaluation pipeline."""

import logging
from typing import Tuple, List, Dict, Any
from pathlib import Path

from src.data_loader import DocumentLoader, ConfigLoader
from src.engines import RegexExtractionEngine
from src.pipelines import EntityExtractionPipeline, RelationExtractionPipeline
from src.utils import OutputWriter, Config


def setup_logging(level: str = "INFO"):
    """Setup logging configuration.
    
    Args:
        level: Logging level
    """
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def run_extraction_pipeline(
    documents_path: str,
    entities_config_path: str,
    relations_config_path: str,
    output_dir: str = "output"
) -> Tuple[List[List[Dict[str, Any]]], List[List[Dict[str, Any]]]]:
    """Run complete extraction pipeline.
    
    Args:
        documents_path: Path to documents.txt
        entities_config_path: Path to entities.json
        relations_config_path: Path to relations.json
        output_dir: Output directory
        
    Returns:
        Tuple of (entity_batches, relation_batches)
    """
    setup_logging("INFO")
    logger = logging.getLogger(__name__)
    
    logger.info("=== Enterprise KG Evaluation Pipeline ===")
    
    # Load configurations
    logger.info("Loading configurations...")
    config_loader = ConfigLoader(entities_config_path, relations_config_path)
    entities_config, relations_config = config_loader.load_all()
    
    entity_types = list(entities_config.keys())
    relation_types = list(relations_config.keys())
    
    logger.info(f"Loaded {len(entity_types)} entity types")
    logger.info(f"Loaded {len(relation_types)} relation types")
    
    # Load documents
    logger.info("Loading documents...")
    doc_loader = DocumentLoader(documents_path)
    documents = doc_loader.load()
    logger.info(f"Loaded {len(documents)} documents")
    
    # Initialize extraction engine
    logger.info("Initializing extraction engine...")
    engine = RegexExtractionEngine()
    
    # Initialize pipelines
    entity_pipeline = EntityExtractionPipeline(engine, entity_types)
    relation_pipeline = RelationExtractionPipeline(engine, relation_types)
    
    # Process documents
    logger.info("Processing entities...")
    entity_batches = entity_pipeline.process_batch(documents)
    entity_stats = entity_pipeline.get_statistics()
    logger.info(f"Entity extraction stats: {entity_stats}")
    
    logger.info("Processing relations...")
    relation_batches = relation_pipeline.process_batch(documents, entity_batches)
    relation_stats = relation_pipeline.get_statistics()
    logger.info(f"Relation extraction stats: {relation_stats}")
    
    # Flatten and write outputs
    logger.info("Writing outputs...")
    writer = OutputWriter(output_dir)
    
    all_entities = [e for batch in entity_batches for e in batch]
    all_relations = [r for batch in relation_batches for r in batch]
    
    entities_path = writer.write_entities(all_entities)
    relations_path = writer.write_relations(all_relations)
    kg_path = writer.write_combined(all_entities, all_relations)
    
    logger.info(f"Entities written to: {entities_path}")
    logger.info(f"Relations written to: {relations_path}")
    logger.info(f"Combined KG written to: {kg_path}")
    
    logger.info("=== Pipeline Complete ===")
    
    return entity_batches, relation_batches


if __name__ == "__main__":
    # Default paths - override with command line arguments as needed
    entity_batches, relation_batches = run_extraction_pipeline(
        documents_path="documents.txt",
        entities_config_path="entities.json",
        relations_config_path="relations.json",
        output_dir="output"
    )
