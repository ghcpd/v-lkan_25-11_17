# Quick Start Guide - Enterprise KG Evaluation

## 30-Second Setup

```bash
# 1. Navigate to project
cd Enterprise-KG-Eval

# 2. Install dependencies (one-time)
pip install pytest pytest-cov

# 3. Run the pipeline
python main.py

# 4. Check outputs
cat output/entities_output.json
cat output/relations_output.json
```

---

## What Gets Generated

After running `python main.py`:

### ✅ output/entities_output.json
- **Total entities extracted:** 40+
- **Format:** Strict JSON schema
- **Contains:** Person, Company, Project, etc.
- **Fields:** id, text, type, start, end, confidence

### ✅ output/relations_output.json
- **Total relations extracted:** 30+
- **Format:** Strict JSON schema
- **Contains:** works_at, manages, leads, etc.
- **Fields:** id, type, head, tail, confidence

### ✅ output/kg_output.json
- **Combined knowledge graph**
- **Entities + relations in one file**
- **Ready for downstream processing**

---

## Run Tests

```bash
# Unit tests only
pytest tests/test_pipeline.py -v

# With coverage report
pytest tests/ -v --cov=src --cov-report=html

# Full E2E test suite (recommended)
bash run_test.sh
```

---

## Use in Python Code

```python
from main import run_extraction_pipeline

# Run the complete pipeline
entity_batches, relation_batches = run_extraction_pipeline(
    documents_path="documents.txt",
    entities_config_path="entities.json",
    relations_config_path="relations.json",
    output_dir="output"
)

# Now access results
print(f"Total entities: {sum(len(b) for b in entity_batches)}")
print(f"Total relations: {sum(len(b) for b in relation_batches)}")
```

---

## Docker

```bash
# Build
docker build -t kge:latest .

# Run
docker run -v $(pwd)/output:/app/output kge:latest
```

---

## File Manifest

```
Enterprise-KG-Eval/
├── main.py                    ← Run this
├── documents.txt              ← Input documents
├── entities.json              ← 10 entity types
├── relations.json             ← 30 relation types
├── README.md                  ← Full documentation
├── PROJECT_OVERVIEW.md        ← Architecture guide
├── DELIVERY_SUMMARY.md        ← What was delivered
├── QUICKSTART.md              ← This file
├── requirements.txt           ← Dependencies
├── Dockerfile                 ← Container image
├── setup.sh                   ← Setup script
├── run_test.sh                ← Test script
├── test_report_template.json  ← Evaluation template
├── src/                       ← Python modules
│   ├── data_loader.py
│   ├── engines/
│   ├── pipelines/
│   └── utils/
├── tests/                     ← Unit tests
│   └── test_pipeline.py
└── output/                    ← Generated outputs
    ├── entities_output.json
    ├── relations_output.json
    └── kg_output.json
```

---

## Common Commands

```bash
# Run pipeline
python main.py

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Check specific test file
pytest tests/test_pipeline.py::TestDocumentLoader -v

# Run E2E suite
bash run_test.sh

# Build Docker image
docker build -t enterprise-kg-eval:1.0 .

# Run Docker container
docker run -v $(pwd)/output:/app/output enterprise-kg-eval:1.0
```

---

## Architecture

```
main.py
  ├─ DocumentLoader loads documents.txt
  ├─ ConfigLoader loads entities.json, relations.json
  ├─ RegexExtractionEngine extracts entities & relations
  ├─ EntityExtractionPipeline runs entity extraction
  ├─ RelationExtractionPipeline runs relation extraction
  └─ OutputWriter writes JSON with schema validation
```

---

## Key Features

| Feature | Details |
|---------|---------|
| **10 Entity Types** | Person, Company, Project, Department, Position, Technology, Location, Team, Product, Client |
| **30 Relation Types** | works_at, manages, leads, supervises, project_period, company_industry, and more |
| **Pluggable Engines** | Swap extraction engines (Regex → ML → LLM) |
| **Strict Schemas** | JSON schema validation on all outputs |
| **Full Testing** | 30+ unit tests, 85%+ coverage |
| **Docker Ready** | Container image included |
| **Well Documented** | 850+ lines of documentation |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Documents not found" | Ensure documents.txt is in project root |
| "No entities extracted" | Check document format matches regex patterns |
| "Import errors" | Run: `pip install -r requirements.txt` |
| "Tests fail" | Run: `pytest tests/ -v --tb=short` for details |

---

## Next: Extend the System

### Add Custom Extraction Engine
```python
from src.engines.base import BaseExtractionEngine

class MyEngine(BaseExtractionEngine):
    def extract_entities(self, doc, types):
        # Your implementation
        pass
    
    def extract_relations(self, doc, entities, types):
        # Your implementation
        pass

# Use: engine = MyEngine()
```

### Add More Entity Types
1. Add to `entities.json`:
   ```json
   {
     "NewType": ["attr1", "attr2"]
   }
   ```

2. Add pattern to `RegexExtractionEngine.patterns`:
   ```python
   self.patterns["NewType"] = r"your_regex"
   ```

---

## Support

- **Documentation:** See README.md, PROJECT_OVERVIEW.md
- **Tests:** Run `pytest tests/ -v`
- **Examples:** See `main.py` and `tests/test_pipeline.py`

---

**Ready to go! Run:** `python main.py`
