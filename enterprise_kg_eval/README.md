# Enterprise-KG-Eval

## Overview
Enterprise-KG-Eval is a minimal, reproducible project to evaluate entity extraction and relation extraction pipelines against semi-structured enterprise text.

Features:
- 10 predefined entity types and 30 relation types (from `entities.json` and `relations.json`).
- Three engine types: `regex`, `llm` (mocked), and `ml` (placeholder).
- Unified JSON output with schema validation via `pydantic`.
- Unit tests implemented with `pytest`.
- Dockerfile and scripts for reproducible runs.

## Installation
1. Python 3.9+ recommended.
2. Install dependencies:

Windows (cmd.exe):

python -m pip install --upgrade pip
pip install -r requirements.txt

## Usage
Run the extraction pipeline (default uses regex engine):

python -c "from enterprise_kg_eval.main import run; run()"

To specify engines:

python -c "from enterprise_kg_eval.main import run; run(entity_engine='llm', relation_engine='regex')"

Outputs will be written to `enterprise_kg_eval/output/entities_output.json` and `enterprise_kg_eval/output/relations_output.json`.

## Running Tests
Windows (cmd.exe):

@echo off
python -m pytest -q

## Docker
Build:

docker build -t enterprise-kg-eval .

Run:

docker run --rm enterprise-kg-eval

## Troubleshooting
- Ensure `entities.json`, `relations.json`, and `documents.txt` exist at repository root.
- For large data, replace the regex engine with a proper model in `engines/ml_engine.py`.

