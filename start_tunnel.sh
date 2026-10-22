#!/usr/bin/env bash
# ==============================================================================
# NeuronForce - 1-Click Live Public Demo Launcher (via Cloudflare Tunnel)
# ==============================================================================

set -e
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"
CLOUDFLARED="/opt/homebrew/bin/cloudflared"

echo "🚀 Starting NeuronForce Live Demo..."

# 1. Start FastAPI backend if not already running on port 8000
if ! lsof -i :8000 > /dev/null 2>&1; then
    echo "⚡ Starting FastAPI backend on http://127.0.0.1:8000..."
    (cd "$BACKEND_DIR" && "$VENV_PYTHON" -m uvicorn app.main:app --host 0.0.0.0 --port 8000) &
    BACKEND_PID=$!
    sleep 2
else
    echo "✅ FastAPI backend is already running on port 8000."
fi

# 2. Start Next.js frontend if not already running on port 3000
if ! lsof -i :3000 > /dev/null 2>&1; then
    echo "⚛️ Building and starting Next.js frontend on http://127.0.0.1:3000..."
    (cd "$FRONTEND_DIR" && npm run build && npm run start) &
    FRONTEND_PID=$!
    sleep 4
else
    echo "✅ Next.js frontend is already running on port 3000."
fi

# 3. Launch Cloudflare Tunnel
echo "🌐 Opening Cloudflare public HTTPS tunnel..."
echo "--------------------------------------------------------"
"$CLOUDFLARED" tunnel --protocol http2 --url http://localhost:3000
