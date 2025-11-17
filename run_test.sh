#!/usr/bin/env bash
set -euo pipefail

mkdir -p output

python -m enterprise_kg_eval.cli --engine regex

python -m pytest tests
