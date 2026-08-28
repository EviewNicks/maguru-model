# -*- coding: utf-8 -*-
"""Verification tests for automated quiz generator chain & schemas."""

import sys
sys.path.insert(0, '.')

def test_quiz_schema_and_prompt():
    """Verify that quiz schemas and prompt template load cleanly."""
    from app.schemas.quiz import QuizQuestionSchema, GenerateQuizRequestSchema, GenerateQuizResponseSchema
    from app.chains.quiz_generator import create_quiz_generator_chain

    # Verify DTO creation
    req = GenerateQuizRequestSchema(course_id="test-course-123", num_questions=3)
    assert req.course_id == "test-course-123"
    assert req.num_questions == 3
    assert req.difficulty == "medium"

    # Verify chain creation
    chain = create_quiz_generator_chain()
    assert chain is not None
    print("✅ Quiz generator schemas and chain initialization verified successfully!")

if __name__ == "__main__":
    test_quiz_schema_and_prompt()
