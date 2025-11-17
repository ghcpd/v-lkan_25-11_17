@echo off
REM Run the full E2E pipeline then run pytest tests
python -c "from enterprise_kg_eval.main import run; run(entity_engine='regex', relation_engine='regex')"
python -m pytest -q
