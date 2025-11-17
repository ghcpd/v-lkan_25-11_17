#!/bin/bash

# Zodiac Explorer - Test Script
# This script runs tests and validation checks

set -e

echo "================================================"
echo "Zodiac Explorer - Test Suite"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test Backend API
echo -e "${BLUE}Testing Backend API...${NC}"
echo ""

# Start backend in background
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
sleep 3

# Test health check
echo -e "${YELLOW}Test 1: Health Check${NC}"
response=$(curl -s http://localhost:5000/api/health)
if echo "$response" | grep -q "ok"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
    kill $BACKEND_PID
    exit 1
fi
echo ""

# Test get all zodiacs
echo -e "${YELLOW}Test 2: Get All Zodiacs${NC}"
response=$(curl -s http://localhost:5000/api/zodiacs)
if echo "$response" | grep -q "Aries"; then
    echo -e "${GREEN}✓ Successfully retrieved all zodiacs${NC}"
else
    echo -e "${RED}✗ Failed to retrieve zodiacs${NC}"
    kill $BACKEND_PID
    exit 1
fi
echo ""

# Test get specific zodiac
echo -e "${YELLOW}Test 3: Get Specific Zodiac (Aries)${NC}"
response=$(curl -s http://localhost:5000/api/zodiacs/Aries)
if echo "$response" | grep -q "Aries"; then
    echo -e "${GREEN}✓ Successfully retrieved Aries zodiac${NC}"
else
    echo -e "${RED}✗ Failed to retrieve Aries zodiac${NC}"
    kill $BACKEND_PID
    exit 1
fi
echo ""

# Test get random zodiac
echo -e "${YELLOW}Test 4: Get Random Zodiac${NC}"
response=$(curl -s http://localhost:5000/api/zodiacs/random)
if echo "$response" | grep -q "success"; then
    echo -e "${GREEN}✓ Successfully retrieved random zodiac${NC}"
else
    echo -e "${RED}✗ Failed to retrieve random zodiac${NC}"
    kill $BACKEND_PID
    exit 1
fi
echo ""

# Test get elements
echo -e "${YELLOW}Test 5: Get Elements${NC}"
response=$(curl -s http://localhost:5000/api/elements)
if echo "$response" | grep -q "Fire\|Earth\|Air\|Water"; then
    echo -e "${GREEN}✓ Successfully retrieved elements${NC}"
else
    echo -e "${RED}✗ Failed to retrieve elements${NC}"
    kill $BACKEND_PID
    exit 1
fi
echo ""

# Test search
echo -e "${YELLOW}Test 6: Search Zodiacs${NC}"
response=$(curl -s "http://localhost:5000/api/zodiacs/search?q=leo")
if echo "$response" | grep -q "Leo"; then
    echo -e "${GREEN}✓ Successfully searched zodiacs${NC}"
else
    echo -e "${RED}✗ Failed to search zodiacs${NC}"
    kill $BACKEND_PID
    exit 1
fi
echo ""

# Test element filter
echo -e "${YELLOW}Test 7: Filter by Element${NC}"
response=$(curl -s "http://localhost:5000/api/zodiacs/search?element=Fire")
if echo "$response" | grep -q "Aries\|Leo\|Sagittarius"; then
    echo -e "${GREEN}✓ Successfully filtered by element${NC}"
else
    echo -e "${RED}✗ Failed to filter by element${NC}"
    kill $BACKEND_PID
    exit 1
fi
echo ""

# Test error handling
echo -e "${YELLOW}Test 8: Error Handling (Invalid Zodiac)${NC}"
response=$(curl -s http://localhost:5000/api/zodiacs/InvalidSign)
if echo "$response" | grep -q "not found"; then
    echo -e "${GREEN}✓ Error handling works correctly${NC}"
else
    echo -e "${RED}✗ Error handling failed${NC}"
    kill $BACKEND_PID
    exit 1
fi
echo ""

# Stop backend
kill $BACKEND_PID
wait $BACKEND_PID 2>/dev/null || true

cd ..

echo "================================================"
echo -e "${GREEN}All tests passed! ✓${NC}"
echo "================================================"
echo ""
echo "Summary:"
echo "✓ Health Check"
echo "✓ Get All Zodiacs"
echo "✓ Get Specific Zodiac"
echo "✓ Get Random Zodiac"
echo "✓ Get Elements"
echo "✓ Search Zodiacs"
echo "✓ Filter by Element"
echo "✓ Error Handling"
echo ""
echo "================================================"
