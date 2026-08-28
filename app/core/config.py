import os
from typing import List

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    USE_PYDANTIC_SETTINGS = True
except ImportError:
    try:
        from pydantic.v1 import BaseSettings
    except ImportError:
        from pydantic import BaseSettings
    USE_PYDANTIC_SETTINGS = False
    SettingsConfigDict = None

class Settings(BaseSettings):
    """Application Settings loaded from environment variables."""
    if USE_PYDANTIC_SETTINGS and SettingsConfigDict:
        model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    else:
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            extra = "ignore"

    # Application Configuration
    PROJECT_NAME: str = "Maguru AI API"
    VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    # AI & LLM Providers (OpenRouter Model Pool & Fallbacks)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = ""
    OPENROUTER_MODEL_1: str = ""
    OPENROUTER_MODEL_2: str = ""
    OPENROUTER_MODEL_3: str = ""
    OPENROUTER_MODELS: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_TEMPERATURE: float = 0.7
    OPENROUTER_MAX_TOKENS: int = 2000

    # Embedding Model
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Supabase PostgreSQL Database (pgvector)
    DATABASE_URL: str = ""

    @property
    def cors_origins(self) -> List[str]:
        raw = self.ALLOWED_ORIGINS or "http://localhost:3000"
        return [origin.strip() for origin in raw.split(",") if origin.strip()]

    @property
    def model_pool(self) -> List[str]:
        """Collect all configured models in priority order with clean trimming."""
        candidates = []
        
        # 1. Check comma-separated models list
        if self.OPENROUTER_MODELS:
            candidates.extend([m.strip() for m in self.OPENROUTER_MODELS.split(",") if m.strip()])
            
        # 2. Check numbered priority models
        for m in [self.OPENROUTER_MODEL_1, self.OPENROUTER_MODEL_2, self.OPENROUTER_MODEL_3, self.OPENROUTER_MODEL]:
            if m and m.strip():
                cleaned = m.strip()
                if cleaned not in candidates:
                    candidates.append(cleaned)
                    
        # 3. Default fallback if empty
        if not candidates:
            candidates = [
                "nvidia/nemotron-3.5-lightning:free",
                "openai/gpt-oss-20b:free",
                "google/gemma-4-31b-it:free",
                "liquid/lfm-2.5-2.6b:free"
            ]
            
        return candidates

settings = Settings()
