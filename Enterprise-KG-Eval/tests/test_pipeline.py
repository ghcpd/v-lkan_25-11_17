"""Unit tests for the Enterprise KG Evaluation pipeline."""

import pytest
import json
import tempfile
from pathlib import Path
from typing import List, Dict, Any

from src.data_loader import DocumentLoader, ConfigLoader
from src.engines import RegexExtractionEngine
from src.pipelines import EntityExtractionPipeline, RelationExtractionPipeline
from src.utils import OutputWriter, Config


# Fixtures
@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_document():
    """Sample document for testing."""
    return "John Doe, age 32, works at OpenAI as a Researcher. Jane Smith manages 2 projects: Delta, Epsilon."


@pytest.fixture
def sample_entities_config(temp_dir):
    """Create sample entities config."""
    entities = {
        "Person": ["name", "age", "position"],
        "Company": ["name", "industry"],
        "Project": ["name", "status"],
    }
    config_path = temp_dir / "entities.json"
    with open(config_path, 'w') as f:
        json.dump(entities, f)
    return str(config_path)


@pytest.fixture
def sample_relations_config(temp_dir):
    """Create sample relations config."""
    relations = {
        "works_at": ["Person", "Company"],
        "manages": ["Person", "Project"],
        "leads": ["Person", "Team"],
    }
    config_path = temp_dir / "relations.json"
    with open(config_path, 'w') as f:
        json.dump(relations, f)
    return str(config_path)


@pytest.fixture
def sample_documents_file(temp_dir, sample_document):
    """Create sample documents file."""
    doc_path = temp_dir / "documents.txt"
    with open(doc_path, 'w') as f:
        f.write(sample_document)
    return str(doc_path)


@pytest.fixture
def extraction_engine():
    """Create extraction engine."""
    return RegexExtractionEngine()


# Tests for DocumentLoader
class TestDocumentLoader:
    """Test document loading functionality."""

    def test_load_documents(self, sample_documents_file):
        """Test loading documents from file."""
        loader = DocumentLoader(sample_documents_file)
        docs = loader.load()
        assert len(docs) > 0
        assert isinstance(docs, list)

    def test_load_nonexistent_file(self):
        """Test loading nonexistent file."""
        loader = DocumentLoader("nonexistent.txt")
        with pytest.raises(FileNotFoundError):
            loader.load()

    def test_get_documents(self, sample_documents_file):
        """Test retrieving loaded documents."""
        loader = DocumentLoader(sample_documents_file)
        loader.load()
        docs = loader.get_documents()
        assert len(docs) > 0


# Tests for ConfigLoader
class TestConfigLoader:
    """Test configuration loading."""

    def test_load_entities(self, sample_entities_config):
        """Test loading entity configuration."""
        loader = ConfigLoader(sample_entities_config, "dummy.json")
        entities = loader.load_entities()
        assert isinstance(entities, dict)
        assert "Person" in entities

    def test_load_relations(self, sample_relations_config):
        """Test loading relation configuration."""
        loader = ConfigLoader("dummy.json", sample_relations_config)
        relations = loader.load_relations()
        assert isinstance(relations, dict)
        assert "works_at" in relations

    def test_load_all(self, sample_entities_config, sample_relations_config):
        """Test loading both configs."""
        loader = ConfigLoader(sample_entities_config, sample_relations_config)
        entities, relations = loader.load_all()
        assert len(entities) > 0
        assert len(relations) > 0

    def test_get_entity_types(self, sample_entities_config, sample_relations_config):
        """Test getting entity types."""
        loader = ConfigLoader(sample_entities_config, sample_relations_config)
        loader.load_entities()
        types = loader.get_entity_types()
        assert "Person" in types

    def test_get_relation_types(self, sample_entities_config, sample_relations_config):
        """Test getting relation types."""
        loader = ConfigLoader(sample_entities_config, sample_relations_config)
        loader.load_relations()
        types = loader.get_relation_types()
        assert "works_at" in types


# Tests for RegexExtractionEngine
class TestRegexExtractionEngine:
    """Test regex extraction engine."""

    def test_engine_initialization(self, extraction_engine):
        """Test engine initialization."""
        assert extraction_engine.engine_name == "Regex"

    def test_extract_entities(self, extraction_engine, sample_document):
        """Test entity extraction."""
        entity_types = ["Person", "Company", "Project"]
        entities = extraction_engine.extract_entities(sample_document, entity_types)
        assert isinstance(entities, list)
        assert len(entities) > 0

    def test_extract_relations(self, extraction_engine, sample_document):
        """Test relation extraction."""
        # First extract entities
        entity_types = ["Person", "Company"]
        entities = extraction_engine.extract_entities(sample_document, entity_types)
        
        # Then extract relations
        relation_types = ["works_at", "manages"]
        relations = extraction_engine.extract_relations(sample_document, entities, relation_types)
        assert isinstance(relations, list)

    def test_validate_extraction(self, extraction_engine):
        """Test extraction validation."""
        valid_entity = {
            "text": "John Doe",
            "type": "Person",
            "start": 0,
            "end": 8,
            "confidence": 0.9
        }
        assert extraction_engine.validate_extraction(valid_entity, "entity")

        invalid_entity = {
            "text": "John Doe",
            "type": "Person"
        }
        assert not extraction_engine.validate_extraction(invalid_entity, "entity")


# Tests for EntityExtractionPipeline
class TestEntityExtractionPipeline:
    """Test entity extraction pipeline."""

    def test_pipeline_initialization(self, extraction_engine):
        """Test pipeline initialization."""
        entity_types = ["Person", "Company"]
        pipeline = EntityExtractionPipeline(extraction_engine, entity_types)
        assert pipeline.engine is not None
        assert len(pipeline.entity_types) == 2

    def test_process_document(self, extraction_engine, sample_document):
        """Test processing single document."""
        entity_types = ["Person", "Company"]
        pipeline = EntityExtractionPipeline(extraction_engine, entity_types)
        entities = pipeline.process(sample_document)
        assert isinstance(entities, list)

    def test_process_batch(self, extraction_engine):
        """Test processing batch of documents."""
        docs = ["John Doe works at OpenAI.", "Jane Smith works at Google."]
        entity_types = ["Person", "Company"]
        pipeline = EntityExtractionPipeline(extraction_engine, entity_types)
        batches = pipeline.process_batch(docs)
        assert len(batches) == 2

    def test_get_statistics(self, extraction_engine, sample_document):
        """Test getting pipeline statistics."""
        entity_types = ["Person", "Company"]
        pipeline = EntityExtractionPipeline(extraction_engine, entity_types)
        pipeline.process(sample_document)
        stats = pipeline.get_statistics()
        assert "total_entities" in stats
        assert "entity_types" in stats
        assert "avg_confidence" in stats


# Tests for RelationExtractionPipeline
class TestRelationExtractionPipeline:
    """Test relation extraction pipeline."""

    def test_pipeline_initialization(self, extraction_engine):
        """Test pipeline initialization."""
        relation_types = ["works_at", "manages"]
        pipeline = RelationExtractionPipeline(extraction_engine, relation_types)
        assert pipeline.engine is not None
        assert len(pipeline.relation_types) == 2

    def test_process_document(self, extraction_engine, sample_document):
        """Test processing single document."""
        # Get entities first
        entity_types = ["Person", "Company", "Project"]
        entity_pipeline = EntityExtractionPipeline(extraction_engine, entity_types)
        entities = entity_pipeline.process(sample_document)
        
        # Extract relations
        relation_types = ["works_at", "manages"]
        relation_pipeline = RelationExtractionPipeline(extraction_engine, relation_types)
        relations = relation_pipeline.process(sample_document, entities)
        assert isinstance(relations, list)

    def test_get_statistics(self, extraction_engine, sample_document):
        """Test getting pipeline statistics."""
        entity_types = ["Person", "Company"]
        entity_pipeline = EntityExtractionPipeline(extraction_engine, entity_types)
        entities = entity_pipeline.process(sample_document)
        
        relation_types = ["works_at"]
        relation_pipeline = RelationExtractionPipeline(extraction_engine, relation_types)
        relation_pipeline.process(sample_document, entities)
        
        stats = relation_pipeline.get_statistics()
        assert "total_relations" in stats
        assert "relation_types" in stats


# Tests for OutputWriter
class TestOutputWriter:
    """Test output writing functionality."""

    def test_writer_initialization(self, temp_dir):
        """Test writer initialization."""
        writer = OutputWriter(str(temp_dir))
        assert writer.output_dir.exists()

    def test_write_entities(self, temp_dir):
        """Test writing entities."""
        entities = [
            {
                "id": "e_1",
                "text": "John Doe",
                "type": "Person",
                "start": 0,
                "end": 8,
                "confidence": 0.9
            }
        ]
        writer = OutputWriter(str(temp_dir))
        output_file = writer.write_entities(entities)
        assert Path(output_file).exists()

    def test_write_relations(self, temp_dir):
        """Test writing relations."""
        relations = [
            {
                "id": "r_1",
                "type": "works_at",
                "head": "e_1",
                "head_text": "John Doe",
                "tail": "e_2",
                "tail_text": "OpenAI",
                "confidence": 0.85
            }
        ]
        writer = OutputWriter(str(temp_dir))
        output_file = writer.write_relations(relations)
        assert Path(output_file).exists()

    def test_write_combined(self, temp_dir):
        """Test writing combined output."""
        entities = [
            {
                "id": "e_1",
                "text": "John Doe",
                "type": "Person",
                "start": 0,
                "end": 8,
                "confidence": 0.9
            }
        ]
        relations = [
            {
                "id": "r_1",
                "type": "works_at",
                "head": "e_1",
                "head_text": "John Doe",
                "tail": "e_2",
                "tail_text": "OpenAI",
                "confidence": 0.85
            }
        ]
        writer = OutputWriter(str(temp_dir))
        output_file = writer.write_combined(entities, relations)
        assert Path(output_file).exists()


# Tests for Config
class TestConfig:
    """Test configuration manager."""

    def test_config_initialization(self):
        """Test config initialization."""
        config = Config()
        assert isinstance(config.settings, dict)

    def test_load_and_get(self):
        """Test loading and getting config values."""
        config = Config()
        config.load("test_key", "test_value")
        assert config.get("test_key") == "test_value"

    def test_get_with_default(self):
        """Test getting config with default."""
        config = Config()
        assert config.get("nonexistent", "default") == "default"

    def test_set_batch_mode(self):
        """Test setting batch mode."""
        config = Config()
        config.set_batch_mode(batch_size=20)
        assert config.get("batch_size") == 20

    def test_as_dict(self):
        """Test getting config as dictionary."""
        config = Config()
        config.load("key1", "value1")
        config.load("key2", "value2")
        config_dict = config.as_dict()
        assert len(config_dict) >= 2


# Integration tests
class TestIntegration:
    """Integration tests for complete pipeline."""

    def test_end_to_end_pipeline(self, sample_documents_file, sample_entities_config, sample_relations_config, temp_dir):
        """Test complete end-to-end pipeline."""
        from main import run_extraction_pipeline
        
        entity_batches, relation_batches = run_extraction_pipeline(
            documents_path=sample_documents_file,
            entities_config_path=sample_entities_config,
            relations_config_path=sample_relations_config,
            output_dir=str(temp_dir)
        )
        
        assert len(entity_batches) > 0
        assert len(relation_batches) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
