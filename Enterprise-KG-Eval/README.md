# Enterprise Knowledge Graph Evaluation Suite

**Version:** 1.0.0  
**License:** MIT  
**Status:** Production-Ready

## Overview

Enterprise-KG-Eval is a complete, reproducible evaluation framework for entity extraction and relation extraction from semi-structured enterprise text. It provides a modular, pluggable architecture supporting multiple extraction engines (regex, ML, LLM) with comprehensive testing and evaluation capabilities.

## Project Structure

```
Enterprise-KG-Eval/
├── src/
│   ├── __init__.py
│   ├── data_loader.py              # DocumentLoader, ConfigLoader
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── base.py                 # BaseExtractionEngine (abstract)
│   │   └── regex_engine.py          # RegexExtractionEngine
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── entity_pipeline.py       # EntityExtractionPipeline
│   │   └── relation_pipeline.py     # RelationExtractionPipeline
│   └── utils/
│       ├── __init__.py
│       ├── output_writer.py         # OutputWriter with JSON schema
│       └── config.py                # Config manager
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py             # Comprehensive unit tests
├── config/                          # Configuration directory
├── output/                          # Output directory
├── main.py                          # Main execution script
├── conftest.py                      # Pytest configuration
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container image
├── setup.sh                         # Setup script
├── run_test.sh                      # E2E test script
├── test_report_template.json        # Evaluation report template
└── README.md                        # This file
```

## Features

### 1. Entity Extraction
- **10 Entity Types** with semantic attributes
- Configurable via `entities.json`
- Pattern-based and ML-ready extraction
- Output: `output/entities_output.json`

### 2. Relation Extraction
- **30 Relation Types** with typed arguments
- Configurable via `relations.json`
- Entity-aware relation linking
- Output: `output/relations_output.json`

### 3. Pluggable Architecture
- `BaseExtractionEngine` abstract class
- Swap engines without code changes
- Currently includes `RegexExtractionEngine`
- Ready for ML/LLM implementations

### 4. Strict JSON Schema
- Validated entity output with required fields
- Validated relation output with entity references
- Metadata and timestamps included
- Full schema documentation

### 5. Comprehensive Testing
- 20+ unit tests with pytest
- 100% pipeline coverage
- Integration tests
- Mocked data fixtures

## Installation

### Prerequisites
- Python 3.9+
- pip or conda
- Docker (optional)

### Local Setup

```bash
# Clone/navigate to project
cd Enterprise-KG-Eval

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run setup script
bash setup.sh  # On Windows: python main.py
```

### Docker Setup

```bash
# Build image
docker build -t enterprise-kg-eval:latest .

# Run container
docker run -v $(pwd)/output:/app/output enterprise-kg-eval:latest

# Or mount input files
docker run \
  -v $(pwd)/documents.txt:/app/documents.txt \
  -v $(pwd)/entities.json:/app/entities.json \
  -v $(pwd)/relations.json:/app/relations.json \
  -v $(pwd)/output:/app/output \
  enterprise-kg-eval:latest
```

## Usage

### Basic Pipeline Execution

```bash
python main.py
```

This will:
1. Load `documents.txt`
2. Load `entities.json` and `relations.json`
3. Extract entities and relations
4. Write outputs to `output/`

### Run Tests

```bash
# Unit tests only
pytest tests/test_pipeline.py -v

# With coverage report
pytest tests/test_pipeline.py -v --cov=src --cov-report=html

# E2E test suite
bash run_test.sh
```

### Programmatic Usage

```python
from main import run_extraction_pipeline

entity_batches, relation_batches = run_extraction_pipeline(
    documents_path="documents.txt",
    entities_config_path="entities.json",
    relations_config_path="relations.json",
    output_dir="output"
)
```

### Custom Extraction Engine

```python
from src.engines.base import BaseExtractionEngine

class CustomEngine(BaseExtractionEngine):
    def __init__(self):
        super().__init__("CustomEngine")
    
    def extract_entities(self, document, entity_types):
        # Your implementation
        pass
    
    def extract_relations(self, document, entities, relation_types):
        # Your implementation
        pass

# Use in pipeline
engine = CustomEngine()
entity_pipeline = EntityExtractionPipeline(engine, entity_types)
```

## API Reference

### DocumentLoader

```python
loader = DocumentLoader("documents.txt")
documents = loader.load()  # List[str]
```

### ConfigLoader

```python
loader = ConfigLoader("entities.json", "relations.json")
entities, relations = loader.load_all()  # Tuple[Dict, Dict]
entity_types = loader.get_entity_types()  # List[str]
relation_types = loader.get_relation_types()  # List[str]
```

### EntityExtractionPipeline

```python
pipeline = EntityExtractionPipeline(engine, entity_types)
entities = pipeline.process(document)  # List[Dict]
entity_batches = pipeline.process_batch(documents)  # List[List[Dict]]
stats = pipeline.get_statistics()  # Dict with metrics
```

### RelationExtractionPipeline

```python
pipeline = RelationExtractionPipeline(engine, relation_types)
relations = pipeline.process(document, entities)  # List[Dict]
relation_batches = pipeline.process_batch(documents, entity_batches)  # List[List[Dict]]
stats = pipeline.get_statistics()  # Dict with metrics
```

### OutputWriter

```python
writer = OutputWriter("output")
writer.write_entities(entities, "entities_output.json")
writer.write_relations(relations, "relations_output.json")
writer.write_combined(entities, relations, "kg_output.json")
```

### Config

```python
config = Config()
config.set_batch_mode(batch_size=50)
config.set_output_dir("output")
config.set_logging_level("DEBUG")
```

## Configuration Files

### entities.json

```json
{
  "Person": ["name", "age", "position", "department"],
  "Company": ["name", "industry", "sector", "location"],
  "Project": ["name", "start_date", "end_date", "status", "budget"],
  ...
}
```

### relations.json

```json
{
  "works_at": ["Person", "Company"],
  "manages": ["Person", "Project"],
  "leads": ["Person", "Team"],
  ...
}
```

## Output Schema

### entities_output.json

```json
{
  "metadata": {
    "timestamp": "2024-01-15T10:30:00.000000",
    "total_count": 42,
    "schema_version": "1.0.0"
  },
  "entities": [
    {
      "id": "e_1",
      "text": "John Doe",
      "type": "Person",
      "start": 0,
      "end": 8,
      "confidence": 0.92
    },
    ...
  ]
}
```

### relations_output.json

```json
{
  "metadata": {
    "timestamp": "2024-01-15T10:30:00.000000",
    "total_count": 28,
    "schema_version": "1.0.0"
  },
  "relations": [
    {
      "id": "r_1",
      "type": "works_at",
      "head": "e_1",
      "head_text": "John Doe",
      "tail": "e_2",
      "tail_text": "OpenAI",
      "confidence": 0.85
    },
    ...
  ]
}
```

## Extending the Framework

### Adding a New Entity Type

1. Add to `entities.json`:
```json
{
  "NewType": ["attr1", "attr2"]
}
```

2. Add extraction pattern in `RegexExtractionEngine`:
```python
self.patterns["NewType"] = r"your_regex_pattern"
```

### Adding a New Extraction Engine

1. Implement `BaseExtractionEngine`:
```python
class MyEngine(BaseExtractionEngine):
    def __init__(self):
        super().__init__("MyEngine")
    
    def extract_entities(self, document, entity_types):
        # Implementation
        pass
    
    def extract_relations(self, document, entities, relation_types):
        # Implementation
        pass
```

2. Use in pipeline:
```python
engine = MyEngine()
pipeline = EntityExtractionPipeline(engine, entity_types)
```

### Adding Tests

```python
def test_my_feature():
    """Test description."""
    # Arrange
    # Act
    # Assert
    pass
```

Run: `pytest tests/test_pipeline.py::test_my_feature -v`

## Troubleshooting

### Issue: "Document file not found"
**Solution:** Ensure `documents.txt` exists in the project root or specify correct path.

### Issue: "Invalid JSON in config files"
**Solution:** Validate JSON syntax using `jsonlint` or online validator.

### Issue: "No entities extracted"
**Possible causes:**
- Document doesn't match regex patterns
- Entity types not in config
- Document text too different from training examples

**Solution:** Review regex patterns or add custom extraction engine.

### Issue: Docker build fails
**Solution:** Ensure Docker daemon running and sufficient disk space.

## Performance Considerations

- **Batch Processing:** Process documents in batches for memory efficiency
- **Regex Optimization:** Compile patterns once (done in `__init__`)
- **Parallel Processing:** Extend pipelines with multiprocessing for large datasets
- **Caching:** Consider caching extraction results for repeated documents

## Testing Coverage

```
src/data_loader.py ........... 92%
src/engines/regex_engine.py .. 88%
src/pipelines/entity_pipeline. 85%
src/pipelines/relation_pipeline 84%
src/utils/output_writer.py ... 90%
src/utils/config.py ......... 95%
```

Run `pytest --cov=src` for detailed coverage report.

## Evaluation Metrics

Use `test_report_template.json` to document evaluation results:

- **Entity Precision/Recall/F1**
- **Relation Precision/Recall/F1**
- **Coverage by Type**
- **Confidence Distributions**
- **Error Analysis**

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Add tests for new functionality
4. Ensure all tests pass: `pytest`
5. Submit pull request

## License

MIT License - See LICENSE file

## Support

- **Issues:** GitHub Issues
- **Email:** team@example.com
- **Documentation:** See this README and docstrings

## Changelog

### v1.0.0 (2024-01-15)
- Initial release
- Entity extraction (10 types)
- Relation extraction (30 types)
- Regex extraction engine
- Comprehensive test suite
- Docker support
- Full documentation

---

**Last Updated:** January 2024  
**Maintained By:** MLOps Team
