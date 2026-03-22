#!/bin/bash

# Setup script for AI-Powered Website Audit Tool
# For Windows users: Run this in Git Bash or WSL

echo "=========================================="
echo "🔍 Website Audit Tool - Setup Script"
echo "=========================================="

# Check Python version
echo ""
echo "📋 Checking Python version..."
python --version

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo ""
echo "✅ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install requirements
echo ""
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
echo ""
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your GOOGLE_API_KEY"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your Google API key"
echo "2. Test the setup: python test_setup.py"
echo "3. Run the app: streamlit run app.py"
echo ""
