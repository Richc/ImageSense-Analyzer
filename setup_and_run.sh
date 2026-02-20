#!/bin/bash
# Quick Setup Script for ImageSense Analyzer
# Run this to install and run the application

echo "=========================================="
echo "ImageSense Analyzer - Quick Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.9 or higher from python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Check for API key
echo "Checking for OpenAI API key..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set!"
    echo ""
    echo "Please set your API key:"
    echo "  export OPENAI_API_KEY='your-key-here'"
    echo ""
    echo "Or add it to your shell profile (~/.zshrc or ~/.bashrc):"
    echo "  echo 'export OPENAI_API_KEY=\"your-key-here\"' >> ~/.zshrc"
    echo "  source ~/.zshrc"
    echo ""
    read -p "Do you want to set it now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your OpenAI API key: " API_KEY
        export OPENAI_API_KEY="$API_KEY"
        echo "✓ API key set for this session"
        echo "⚠️  Note: This is temporary. Add it to your shell profile for permanent use."
    else
        echo "❌ Cannot proceed without API key"
        exit 1
    fi
else
    echo "✓ API key found"
fi
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Run the application
echo "=========================================="
echo "Starting ImageSense Analyzer..."
echo "=========================================="
echo ""

python3 image_analyzer_app.py
