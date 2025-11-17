#!/bin/bash

# Portfolio Website - Python Flask Version
# Quick start script

echo "========================================="
echo "  Portfolio Website - Python Version"
echo "========================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing/updating dependencies..."
pip install -q -r requirements.txt

echo ""
echo "========================================="
echo "  Starting Flask Server"
echo "========================================="
echo ""
echo "Server will be available at:"
echo "  http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python app.py
