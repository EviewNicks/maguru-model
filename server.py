# ========================================
# Maguru - LangServe API Server
# ========================================
#
# Exposes AI chains as REST API endpoints
# using FastAPI + LangServe
#
# Usage: python server.py
# Default: http://localhost:8000
#

import os
import logging
import asyncio
from typing import Optional, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

from langserve.server import add_routes
from langchain_core.runnables import RunnableLambda

from ai_chains.chains.qa_chatbot import answer_question
from ai_chains.chains.explain_code import explain_code
from ai_chains.chains.hint_generator import generate_hint
from ai_chains.chains.quiz_feedback import generate_feedback
from ai_chains.chains.ai_greeting import generate_greeting

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Validate required environment variables
required_vars = ['OPENROUTER_API_KEY']
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    raise RuntimeError(
        f"❌ Missing required environment variables: {', '.join(missing)}\n"
        f"Please create a .env file with these variables.\n"
        f"Copy .env.example to .env and add your API keys."
    )

# ========================================
# Chain Adapters (LangServe compatibility)
# ========================================

def _with_fallback(func, fallback_msg: str, **kwargs):
    """Execute function with fallback on error."""
    try:
        return func(**kwargs)
    except Exception as e:
        logger.error(f"Chain error: {str(e)}", exc_info=True)
        return fallback_msg


def create_qa_chatbot_chain():
    """Create LangServe-compatible Q&A chatbot chain."""
    def invoke(input_dict: dict) -> str:
        return _with_fallback(
            answer_question,
            "Maaf, saya tidak bisa menjawab pertanyaan ini sekarang. Silakan coba lagi.",
            question=input_dict.get("question", ""),
            session_title=input_dict.get("session_title", ""),
            session_content=input_dict.get("session_content", ""),
            chat_history=input_dict.get("chat_history", [])
        )
    return RunnableLambda(invoke)


def create_explain_code_chain():
    """Create LangServe-compatible code explanation chain."""
    def invoke(input_dict: dict) -> str:
        return _with_fallback(
            explain_code,
            "Maaf, saya tidak bisa menjelaskan kode ini sekarang. Silakan coba lagi.",
            code_snippet=input_dict.get("code", "")
        )
    return RunnableLambda(invoke)


def create_hint_generator_chain():
    """Create LangServe-compatible hint generator chain."""
    def invoke(input_dict: dict) -> str:
        level = input_dict.get("level", 1)
        if not isinstance(level, int):
            try:
                level = int(level)
            except (ValueError, TypeError):
                level = 1
        level = max(1, min(3, level))
        return _with_fallback(
            generate_hint,
            "Hint tidak tersedia sekarang. Silakan coba lagi.",
            task=input_dict.get("task", ""),
            student_attempt=input_dict.get("attempt", ""),
            level=level
        )
    return RunnableLambda(invoke)


def create_quiz_feedback_chain():
    """Create LangServe-compatible quiz feedback chain."""
    def invoke(input_dict: dict) -> str:
        is_correct = input_dict.get("is_correct", False)
        if isinstance(is_correct, str):
            is_correct = is_correct.lower() in ("true", "1", "yes", "benar")
        return _with_fallback(
            generate_feedback,
            "Feedback tidak tersedia sekarang.",
            question=input_dict.get("question", ""),
            student_answer=input_dict.get("student_answer", ""),
            correct_answer=input_dict.get("correct_answer", ""),
            is_correct=is_correct
        )
    return RunnableLambda(invoke)


def create_greeting_chain():
    """Create LangServe-compatible greeting chain."""
    def invoke(input_dict: dict) -> str:
        course_metadata = input_dict.get("course_metadata", {})
        if isinstance(course_metadata, str):
            course_metadata = {"title": course_metadata}
        return _with_fallback(
            generate_greeting,
            f"Halo {input_dict.get('student_name', 'Siswa')}! Selamat datang!",
            student_name=input_dict.get("student_name", "Siswa"),
            course_metadata=course_metadata
        )
    return RunnableLambda(invoke)


# ========================================
# FastAPI Application
# ========================================

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Maguru AI API",
        description="LangServe API for Maguru Learning Platform",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    allowed_origins = [origin.strip() for origin in allowed_origins]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def register_chains(app: FastAPI) -> None:
    """Register all AI chains as LangServe routes."""
    qa_chain = create_qa_chatbot_chain()
    explain_chain = create_explain_code_chain()
    hint_chain = create_hint_generator_chain()
    quiz_chain = create_quiz_feedback_chain()
    greeting_chain = create_greeting_chain()

    add_routes(app, qa_chain, path="/chatbot")
    add_routes(app, explain_chain, path="/explain-code")
    add_routes(app, hint_chain, path="/hint")
    add_routes(app, quiz_chain, path="/quiz-feedback")
    add_routes(app, greeting_chain, path="/greeting")


# ========================================
# Application Factory
# ========================================

app = create_app()
register_chains(app)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Maguru AI API",
        "version": "1.0.0",
        "description": "LangServe API for Maguru Learning Platform",
        "endpoints": {
            "chatbot": {
                "invoke": "/chatbot/invoke",
                "stream": "/chatbot/stream"
            },
            "explain-code": {
                "invoke": "/explain-code/invoke",
                "stream": "/explain-code/stream"
            },
            "hint": {
                "invoke": "/hint/invoke",
                "stream": "/hint/stream"
            },
            "quiz-feedback": {
                "invoke": "/quiz-feedback/invoke",
                "stream": "/quiz-feedback/stream"
            },
            "greeting": {
                "invoke": "/greeting/invoke",
                "stream": "/greeting/stream"
            },
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        },
        "streaming": {
            "format": "Server-Sent Events (SSE)",
            "content_type": "text/event-stream",
            "completion_event": "[DONE]"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Maguru AI API",
        "version": "1.0.0"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for all unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return {
        "error": "Internal server error",
        "message": str(exc),
        "type": type(exc).__name__
    }


# ========================================
# Server Startup
# ========================================

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
