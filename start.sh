#!/bin/bash

set -e
echo "🚀 Starting Resume Tailor Application..."
echo ""

# Start backend
echo "🐍 Starting backend server on http://localhost:8000..."
cd backend
PYTHONPATH=$(pwd) python3 -m uvicorn main:app --reload --port 8000 --log-level critical > /dev/null 2>&1 &
BACKEND_PID=$!

cd ..
# Wait for backend to start
sleep 2

# Start frontend
echo "⚛️ Starting frontend on http://localhost:5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "========================================"
echo "✨ Resume Tailor is running!"
echo "Frontend: http://localhost:5173"
echo "Backend: http://localhost:8000"
echo "========================================"
echo ""

# Open browser (works on macOS, adjust for other OS)
sleep 3
open http://localhost:5173 2>/dev/null || echo "Please open http://localhost:5173 in your browser"

# Keep servers running
wait
echo "========================================"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Trap Ctrl+C and cleanup
trap "echo '\n🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

wait
