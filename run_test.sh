@echo off
REM Top-level run tests
python -c "from enterprise_kg_eval.main import run; run()"
python -m pytest -q
