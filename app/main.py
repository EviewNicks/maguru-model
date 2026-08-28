import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve.server import add_routes

from app.core.config import settings
from app.api.router import api_router
from app.api.v1.endpoints import ingest
from app.chains import (
    create_qa_chatbot_chain,
    create_explain_code_chain,
    create_hint_generator_chain,
    create_quiz_feedback_chain,
    create_greeting_chain,
    create_quiz_generator_chain
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="LangServe API & RAG Backend for Maguru Learning Platform",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
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
    """Register all AI chains as LangServe SSE endpoints."""
    qa_chain = create_qa_chatbot_chain()
    explain_chain = create_explain_code_chain()
    hint_chain = create_hint_generator_chain()
    quiz_chain = create_quiz_feedback_chain()
    greeting_chain = create_greeting_chain()
    quiz_gen_chain = create_quiz_generator_chain()

    add_routes(app, qa_chain, path="/chatbot")
    add_routes(app, explain_chain, path="/explain-code")
    add_routes(app, hint_chain, path="/hint")
    add_routes(app, quiz_chain, path="/quiz-feedback")
    add_routes(app, greeting_chain, path="/greeting")
    add_routes(app, quiz_gen_chain, path="/generate-quiz")

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
