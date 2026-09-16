# -*- coding: utf-8 -*-
"""Verification tests for the refactored app architecture."""

import sys
sys.path.insert(0, '.')

def test_app_imports():
    """Verify that core app packages and routes import without errors."""
    from app.core.config import settings
    from app.core.llm import get_llm
    from app.services.rag_service import get_course_context
    from app.chains import (
        answer_question,
        explain_code,
        generate_hint,
        generate_feedback,
        generate_greeting
    )
    from app.main import app

    assert settings.PROJECT_NAME == "Maguru AI API"
    assert app is not None
    print("✅ All app package imports verified successfully!")

if __name__ == "__main__":
    test_app_imports()
