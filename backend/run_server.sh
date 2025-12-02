#!/bin/bash
# Quick start script for the backend server

echo "Starting AI Pricing Monitor & Advisor Backend..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo ""
echo "Server will be available at:"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="
echo ""

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

