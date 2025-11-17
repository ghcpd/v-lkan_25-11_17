#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

python -m pytest

python run_pipeline.py \
  --project-name "Enterprise-KG-Eval" \
  --documents documents.txt \
  --entities entities.json \
  --relations relations.json \
  --engine regex \
  --output output

echo "Pipeline execution and test suite completed."
