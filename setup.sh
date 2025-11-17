@echo off
REM Top-level setup
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist output mkdir output
python -m pytest -q

echo Setup completed
