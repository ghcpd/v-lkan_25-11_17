@echo off
REM Run E2E pipeline and tests
python -m enterprise_kg_eval.run_pipeline
pytest -q
