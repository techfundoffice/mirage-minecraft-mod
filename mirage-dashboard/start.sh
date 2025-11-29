#!/bin/bash

# Start Mirage Dashboard - Backend and Frontend

echo "🚀 Starting Mirage Workflow Dashboard..."
echo ""

# Kill any existing processes on ports 5000 and 5173
echo "🧹 Cleaning up existing processes..."
lsof -ti:5000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

# Start Flask API server in background
echo "🔧 Starting API server on port 5000..."
cd "$(dirname "$0")"
python3 server/api_server.py > logs/api.log 2>&1 &
API_PID=$!
echo "   API PID: $API_PID"

# Wait for API to start
sleep 3

# Check if API is running
if curl -s http://localhost:5000/api/health > /dev/null; then
    echo "   ✅ API server running"
else
    echo "   ❌ API server failed to start"
    exit 1
fi

# Start React dev server
echo "🎨 Starting React frontend on port 5173..."
npm run dev &
REACT_PID=$!
echo "   React PID: $REACT_PID"

# Wait for React to start
sleep 5

echo ""
echo "🎉 Dashboard is ready!"
echo ""
echo "📝 Access points:"
echo "   Frontend: http://localhost:5173"
echo "   API:      http://localhost:5000/api"
echo ""
echo "💡 Tip: Press Ctrl+C to stop both servers"
echo ""

# Keep script running
wait
