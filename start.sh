#!/bin/bash
# ============================================
#  Soil Texture AI — One-Click Start Script
# ============================================
# Usage:  ./start.sh
# This starts both the backend (FastAPI) and frontend (Next.js).
# Press Ctrl+C to stop both servers.

cd "$(dirname "$0")"
PROJECT_DIR="$(pwd)"

echo "🌱 Starting Soil Texture AI..."
echo ""

# --- Kill any old processes on our ports ---
echo "🧹 Clearing ports 8000 & 3000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null
sleep 1

# --- Backend (FastAPI on port 8000) ---
echo "🔧 Starting Backend (http://localhost:8000)..."
cd "$PROJECT_DIR"
source venv/bin/activate
cd backend
python main.py &
BACKEND_PID=$!

# --- Frontend (Next.js on port 3000) ---
echo "🎨 Starting Frontend (http://localhost:3000)..."
cd "$PROJECT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "============================================"
echo "  ✅ Both servers are running!"
echo ""
echo "  🌐 Frontend:  http://localhost:3000"
echo "  🔗 Backend:   http://localhost:8000"
echo "  📡 API Docs:  http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop both servers."
echo "============================================"
echo ""

# Cleanup on Ctrl+C
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID 2>/dev/null
    wait $FRONTEND_PID 2>/dev/null
    echo "✅ Done. Goodbye!"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for both
wait
