#!/bin/bash

set -e

echo "🚀 Starting Resume Tailor Application..."
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

echo ""
echo "🐍 Starting backend server on http://localhost:8000..."
PYTHONPATH=$(pwd)/backend python3 -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

cd ..

echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "Node modules already installed, skipping..."
fi

echo ""
echo "⚛️  Starting frontend on http://localhost:5173..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "✨ Resume Tailor is running!"
echo "Frontend: http://localhost:5173"
echo "Backend: http://localhost:8000"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Trap Ctrl+C and cleanup
trap "echo '\n🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

wait
