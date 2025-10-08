#!/bin/bash

echo "🚀 Starting AI English Coach Application"
echo "========================================"
echo ""

# Check if we're in the correct directory
if [ ! -f "model_service.py" ]; then
    echo "❌ Error: Please run this script from the KPPP directory"
    exit 1
fi

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# Install backend dependencies if needed
if [ ! -d "backend/__pycache__" ]; then
    echo "📦 Installing backend dependencies..."
    pip install -r backend/requirements.txt
fi

# Start backend
echo ""
echo "🔧 Starting Backend (FastAPI)..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo ""
echo "🎨 Starting Frontend (React)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Application Started!"
echo "========================================"
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "========================================"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
