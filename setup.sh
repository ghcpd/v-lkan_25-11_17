#!/bin/bash

# Zodiac Explorer - Setup Script
# This script sets up the development environment for both backend and frontend

set -e

echo "================================================"
echo "Zodiac Explorer - Setup Script"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
echo -e "${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 is not installed. Please install Python 3.7 or higher.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python3 found: $(python3 --version)${NC}"
echo ""

# Check if Node.js is installed
echo -e "${YELLOW}Checking Node.js installation...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install Node.js 14 or higher.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"
echo ""

# Setup Backend
echo -e "${YELLOW}Setting up Backend...${NC}"
cd backend

# Create Python virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✓ Backend setup completed${NC}"
echo ""

# Setup Frontend
cd ../frontend

echo -e "${YELLOW}Setting up Frontend...${NC}"

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo -e "${GREEN}✓ Frontend setup completed${NC}"
echo ""

# Return to root directory
cd ..

echo "================================================"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo "================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. To start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate (on Linux/Mac) or venv\\Scripts\\activate (on Windows)"
echo "   python app.py"
echo ""
echo "2. In a new terminal, to start the frontend:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Open your browser and go to http://localhost:3000"
echo ""
echo "The API will be running on http://localhost:5000"
echo "================================================"
