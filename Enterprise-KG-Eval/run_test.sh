#!/bin/bash
set -e

echo "=========================================="
echo "Enterprise KG Evaluation - Test Suite"
echo "=========================================="

# Setup
echo "Setting up environment..."
mkdir -p output
mkdir -p config

# Copy config files
echo "Preparing configuration files..."
if [ -f "../entities.json" ]; then
    cp ../entities.json config/ || true
fi

if [ -f "../relations.json" ]; then
    cp ../relations.json config/ || true
fi

if [ -f "../documents.txt" ]; then
    cp ../documents.txt . || true
fi

# Run unit tests
echo ""
echo "=========================================="
echo "Running Unit Tests"
echo "=========================================="
pytest tests/test_pipeline.py -v --cov=src --cov-report=html --cov-report=term-missing

# Run E2E pipeline
echo ""
echo "=========================================="
echo "Running End-to-End Pipeline"
echo "=========================================="
python main.py

# Check outputs
echo ""
echo "=========================================="
echo "Verifying Output Files"
echo "=========================================="
if [ -f "output/entities_output.json" ]; then
    echo "✓ Entities output found"
    echo "  $(wc -l < output/entities_output.json) lines"
else
    echo "✗ Entities output NOT found"
fi

if [ -f "output/relations_output.json" ]; then
    echo "✓ Relations output found"
    echo "  $(wc -l < output/relations_output.json) lines"
else
    echo "✗ Relations output NOT found"
fi

if [ -f "output/kg_output.json" ]; then
    echo "✓ Combined KG output found"
    echo "  $(wc -l < output/kg_output.json) lines"
else
    echo "✗ Combined KG output NOT found"
fi

echo ""
echo "=========================================="
echo "Test Suite Complete!"
echo "=========================================="
echo "Coverage report generated in htmlcov/"
echo "=========================================="
