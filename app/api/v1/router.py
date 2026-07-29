from fastapi import APIRouter
from app.api.v1.endpoints import health, ingest, chat

api_v1_router = APIRouter()

api_v1_router.include_router(health.router, tags=["Health"])
api_v1_router.include_router(ingest.router, tags=["Ingestion"])
api_v1_router.include_router(chat.router, tags=["Chat"])
