#!/bin/bash

set -e

echo "🚀 Setting up Resume Tailor Application..."
echo ""

# Check for LaTeX
echo "🔍 Checking for LaTeX installation..."
if ! command -v pdflatex &> /dev/null; then
    echo "⚠️  LaTeX not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            echo "❌ Homebrew not found. Please install Homebrew first: https://brew.sh"
            exit 1
        fi
        brew install --cask mactex-no-gui
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update
        sudo apt-get install -y texlive-latex-base texlive-latex-extra
    else
        echo "⚠️  Unsupported OS. Please install LaTeX manually."
    fi
else
    echo "✅ LaTeX is installed"
fi

echo ""

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "⚠️  Warning: backend/.env file not found!"
    echo "Please create backend/.env with your GEMINI_API_KEY"
    echo "Example: GEMINI_API_KEY=your_key_here"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📦 Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt

cd ..

echo "📦 Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "Node modules already installed, skipping..."
fi

cd ..

echo ""
echo "========================================"
echo "✅ Setup complete!"
echo "You can now run: ./start.sh"
echo "========================================"
