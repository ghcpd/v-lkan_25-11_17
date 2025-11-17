#!/bin/bash
set -e

echo "=========================================="
echo "Enterprise KG Evaluation - Setup Script"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python --version || { echo "Python not found"; exit 1; }

# Create directories
echo "Creating directories..."
mkdir -p output
mkdir -p config

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "Running unit tests..."
pytest tests/test_pipeline.py -v --cov=src --cov-report=term-missing

# Copy config files if they exist in parent directory
if [ -f "../entities.json" ]; then
    echo "Copying entities.json..."
    cp ../entities.json config/ || true
fi

if [ -f "../relations.json" ]; then
    echo "Copying relations.json..."
    cp ../relations.json config/ || true
fi

if [ -f "../documents.txt" ]; then
    echo "Copying documents.txt..."
    cp ../documents.txt . || true
fi

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo "To run the pipeline, execute:"
echo "  python main.py"
echo "=========================================="
