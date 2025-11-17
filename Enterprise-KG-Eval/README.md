# Enterprise-KG-Eval

Enterprise-KG-Eval is a production-ready evaluation harness for entity and relation extraction on semi-structured enterprise text. The project offers deterministic pipelines, pluggable extraction engines, reproducible outputs, and end-to-end automation via shell scripts, Docker, and pytest-based validation.

## Features
- **Entity extraction** for 10 predefined entity types backed by JSON configuration.
- **Relation extraction** for 30 predefined relation types sourced from a dedicated schema.
- **Module-swappable engine** architecture (regex engine provided, LLM/ML ready).
- **Unified JSON outputs** for entities and relations with checksums and metadata.
- **Dockerized workflow** with `setup.sh` and `run_test.sh` automation.

## Project Structure
```
Enterprise-KG-Eval/
├── Dockerfile
├── README.md
├── documents.txt
├── entities.json
├── relations.json
├── requirements.txt
├── run_pipeline.py
├── run_test.sh
├── setup.sh
├── test_report_template.json
├── output/
│   └── .gitkeep
├── src/
│   └── enterprise_kg_eval/
│       ├── __init__.py
│       ├── config_loader.py
│       ├── data_loader.py
│       ├── engine_factory.py
│       ├── entity_pipeline.py
│       ├── models.py
│       ├── output_writer.py
│       ├── pipeline_runner.py
│       ├── relation_pipeline.py
│       └── engines/
│           ├── __init__.py
│           ├── base.py
│           └── regex_engine.py
└── tests/
    ├── __init__.py
    ├── data/
    ├── test_config_loader.py
    ├── test_data_loader.py
    ├── test_entity_pipeline.py
    └── test_relation_pipeline.py
```

## Installation
```bash
./setup.sh
```
The script upgrades `pip`, installs `requirements.txt`, prepares the `output/` folder, and runs `pytest` to validate the environment.

## Usage
Run the full evaluation pipeline plus tests:
```bash
./run_test.sh
```

Standalone pipeline run:
```bash
python run_pipeline.py \
  --project-name Enterprise-KG-Eval \
  --documents documents.txt \
  --entities entities.json \
  --relations relations.json \
  --engine regex \
  --output output
```

Outputs are written to:
- `output/entities_output.json`
- `output/relations_output.json`

## Configuration
- **entities.json** – Defines the 10 entity types and their attributes.
- **relations.json** – Defines 30 relation types, their argument entity types, and optional attribute targets.
Modify these files to introduce new types without touching pipeline code.

## Extending Extraction Engines
`src/enterprise_kg_eval/engine_factory.py` maintains an engine registry. Add a new engine class (LLM, ML, etc.) implementing `ExtractionEngine` and register it with a key (e.g., `llm`). Invoke via `--engine llm`.

## API Highlights
- `DocumentLoader` – Normalizes raw documents into `Document` objects.
- `EntityExtractionPipeline` – Applies the configured engine to produce entity predictions.
- `RelationExtractionPipeline` – Consumes entity predictions to detect relations.
- `UnifiedOutputWriter` – Emits strict JSON schemas with metadata for scoring or integration.

## Testing
All unit tests live under `tests/` and can be run via `python -m pytest`. Add regression tests for new extraction rules to keep coverage current.

## Docker
```
docker build -t enterprise-kg-eval .
docker run --rm enterprise-kg-eval
```
The container executes `run_test.sh` ensuring parity with local runs.

## Troubleshooting
- **No entities extracted**: Confirm delimiter assumptions in `documents.txt` (default double newline). Adjust `DocumentLoader`.
- **Missing relation detections**: Update `RELATION_KEYWORDS` in `regex_engine.py` or implement a richer engine.
- **Permission issues**: Ensure scripts are executable (`chmod +x setup.sh run_test.sh`) in UNIX-like environments.

For additional customization or questions, refer to inline module docstrings.
