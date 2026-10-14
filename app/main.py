import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve.server import add_routes

from app.core.config import settings
from app.api.router import api_router
from app.api.v1.endpoints import ingest
from app.agents import (
    create_co_teacher_chain,
    create_greeting_chain,
    create_code_explainer_chain,
    create_hint_generator_chain,
    create_quiz_feedback_chain,
    create_quiz_engine_chain,
)

from contextlib import asynccontextmanager
from app.db.checkpointer import close_checkpointer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to handle startup and graceful shutdown."""
    logger.info("Starting up Maguru AI Backend...")
    yield
    logger.info("Shutting down Maguru AI Backend...")
    close_checkpointer()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="LangServe API & RAG Backend for Maguru Learning Platform",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS Middleware Setup
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global Exception Handlers for Security & Clean Error Handling
    @application.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Exception on {request.url}: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Terjadi kesalahan pada server AI. Silakan coba beberapa saat lagi.",
                "detail": str(exc) if settings.PROJECT_NAME != "Production" else "Internal server error"
            }
        )

    # Register API V1 Routers
    application.include_router(api_router, prefix="/api")

    # Direct route for admin ingest for convenience (/admin/ingest)
    application.include_router(ingest.router)

    # Register LangServe Routes
    _register_langserve_routes(application)

    return application


def _register_langserve_routes(app: FastAPI) -> None:
    """Register all AI agents as LangServe SSE endpoints (routes unchanged)."""
    add_routes(app, create_co_teacher_chain(), path="/chatbot")
    add_routes(app, create_code_explainer_chain(), path="/explain-code")
    add_routes(app, create_hint_generator_chain(), path="/hint")
    add_routes(app, create_quiz_feedback_chain(), path="/quiz-feedback")
    add_routes(app, create_greeting_chain(), path="/greeting")
    add_routes(app, create_quiz_engine_chain(), path="/generate-quiz")


app = create_app()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": "LangServe API & RAG Backend for Maguru Learning Platform",
        "endpoints": {
            "chatbot": {"invoke": "/chatbot/invoke", "stream": "/chatbot/stream"},
            "explain-code": {"invoke": "/explain-code/invoke", "stream": "/explain-code/stream"},
            "hint": {"invoke": "/hint/invoke", "stream": "/hint/stream"},
            "quiz-feedback": {"invoke": "/quiz-feedback/invoke", "stream": "/quiz-feedback/stream"},
            "greeting": {"invoke": "/greeting/invoke", "stream": "/greeting/stream"},
            "generate-quiz": {"invoke": "/generate-quiz/invoke", "api_v1": "/api/v1/generate-quiz"},
            "admin-ingest": "/admin/ingest",
            "ingest-text": "/api/v1/ingest",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Root health check endpoint."""
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }
