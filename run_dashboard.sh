#!/bin/bash

# Call Report Dashboard - Setup and Run Script
# This script installs dependencies and launches the dashboard

echo "================================================"
echo "Call Report Dashboard - Setup & Launch"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null
then
    echo "❌ Error: Python is not installed"
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null
then
    PYTHON_CMD=python3
    PIP_CMD=pip3
else
    PYTHON_CMD=python
    PIP_CMD=pip
fi

echo "✅ Found Python: $($PYTHON_CMD --version)"
echo ""

# Check if requirements are already installed
echo "📦 Checking dependencies..."
if $PIP_CMD show streamlit &> /dev/null
then
    echo "✅ Dependencies already installed"
else
    echo "📥 Installing dependencies..."
    $PIP_CMD install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies installed successfully"
    else
        echo "❌ Error installing dependencies"
        exit 1
    fi
fi

echo ""
echo "🚀 Launching Call Report Dashboard..."
echo ""
echo "The dashboard will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the dashboard"
echo ""
echo "================================================"
echo ""

# Launch the dashboard
streamlit run dashboard.py
