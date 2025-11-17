@echo off
REM Setup script for Enterprise-KG-Eval
python -m pip install --upgrade pip
pip install -r ../requirements.txt
REM Prepare output directory at repository root
if not exist ..\output mkdir ..\output
python -m pytest -q
echo Setup complete
