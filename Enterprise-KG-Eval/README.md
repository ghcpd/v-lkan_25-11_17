# Enterprise-KG-Eval

Evaluation project for entity and relation extraction on semi-structured enterprise text.

## Overview

This repository provides a reproducible evaluation pipeline for extracting entities and relations from text documents. It supports modular extraction engines (regex, stub LLM), uses config JSON files for entity and relation definitions, and writes structured output.

## Structure

- `enterprise_kg_eval/` : package
- `output/` : generated outputs
- `tests/` : pytest tests
- `v-lkan_25-11_17/` : source documents and config (expected to exist in parent workspace)

## Quickstart

1. Create a virtual environment and install deps:

   setup.sh

2. Run the pipeline on the provided sample files:

   run_test.sh

3. View outputs in `output/entities_output.json` and `output/relations_output.json`.

## Design

- `engines.py` implements a `BaseEngine` with two implementations: `RegexEngine` and `StubLLMEngine`.
- `entity_pipeline` and `relation_pipeline` are simple wrappers to run extraction over documents.
- `writer.py` creates JSON outputs.
- Tests validate loader, pipelines and writer.

## Troubleshooting

- Ensure `v-lkan_25-11_17/documents.txt`, `entities.json`, and `relations.json` exist.
- Use `--engine llm` to use the stub LLM engine for example-driven extraction.
