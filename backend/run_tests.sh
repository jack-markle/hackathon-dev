#!/bin/bash
# Run test scenarios

echo "Running Test Scenarios for AI Pricing Monitor & Advisor"
echo "========================================================"

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found. Install dependencies first."
    exit 1
fi

# Run the test scenarios
python test_scenarios.py

echo ""
echo "========================================================"
echo "Test run complete!"

