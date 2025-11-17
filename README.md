# Enterprise-KG-Eval

Enterprise-KG-Eval is a reproducible evaluation harness for semi-structured enterprise text. It loads a corpus of documents, applies interchangeable entity/relation extraction engines, and writes schema-validated outputs so downstream verification and metrics tooling can consume the results predictably.

## Getting started
1. Ensure you are in the repository root (`Enterprise-KG-Eval`).
2. Run `./setup.sh` to install the minimal dependencies, prepare the `output` directory, and execute the unit tests.
3. Run `./run_test.sh` to execute the full E2E pipeline and rerun the Pytest suite (this is the canonical end-to-end smoke test).

## Project layout
The repository tree mirrors the evaluation flow:

```
.
├── Dockerfile
├── README.md
├── documents.txt
├── entities.json
├── relations.json
├── requirements.txt
├── run_test.sh
├── setup.sh
├── test_report_template.json
├── project_structure.txt
├── output/
│   └── .gitkeep
├── enterprise_kg_eval/
│   ├── __init__.py
│   ├── cli.py
│   ├── config_loader.py
│   ├── data_loader.py
│   ├── pipeline.py
│   ├── schema.py
│   ├── writer.py
│   ├── models.py
│   └── engines/
│       ├── __init__.py
│       ├── base.py
│       ├── llm_stub_engine.py
│       ├── ml_engine.py
│       └── regex_engine.py
├── tests/
│   ├── __init__.py
│   ├── test_pipeline.py
│   └── test_writer.py
```

For the live tree output, consult `project_structure.txt`.

## Usage
The main driver is exposed via `python -m enterprise_kg_eval.cli`. By default it:

- loads `documents.txt`, `entities.json`, and `relations.json` from the repo root,
- runs the regex-based extraction engine,
- writes schema-validated JSON files to `output/entities_output.json` and `output/relations_output.json`.

You can override the defaults:

```
python -m enterprise_kg_eval.cli \
  --documents documents.txt \
  --entities entities.json \
  --relations relations.json \
  --output-dir output \
  --engine ml
```

Use `--engine` to swap between `regex`, `ml`, and `llm`.

## Testing

- `pytest` exercises the pipelines and writer against the supplied documents.
- `run_test.sh` runs the CLI and then `pytest` for a full regression check.

## Docker

Build the container with:

```
docker build -t enterprise-kg-eval .
```

The default container command runs `python -m enterprise_kg_eval.cli --engine regex`.

## Troubleshooting

- If a schema validation error surfaces, inspect `output/*.json` and compare against `enterprise_kg_eval/schema.py`.
- Missing data? The project derives fallback departments/teams/products if the input does not spell them out, so rerun the pipeline if you change the document set to regenerate those heuristics.
