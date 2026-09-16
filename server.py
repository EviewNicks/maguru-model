# ========================================
# Maguru - LangServe & RAG API Server
# ========================================
#
# Exposes AI chains & RAG service as REST API endpoints
# using FastAPI + LangServe
#
# Usage: python server.py
# Default: http://localhost:8000
#

import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    host = settings.HOST or os.getenv("HOST", "0.0.0.0")
    port = settings.PORT or int(os.getenv("PORT", "8000"))

    print(f"🚀 Starting Maguru AI Server on http://{host}:{port}")
    print(f"📚 OpenAPI Documentation available at http://localhost:{port}/docs")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
