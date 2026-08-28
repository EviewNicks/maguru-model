from fastapi import APIRouter, HTTPException, Body
from app.schemas.quiz import GenerateQuizRequestSchema, GenerateQuizResponseSchema
from app.chains.quiz_generator import generate_quiz_questions

router = APIRouter()

@router.post("/generate-quiz", response_model=GenerateQuizResponseSchema)
async def generate_quiz_endpoint(payload: GenerateQuizRequestSchema = Body(...)):
    """API Endpoint to generate automated quiz assessment questions using AI & RAG."""
    if not payload.course_id:
        raise HTTPException(status_code=400, detail="course_id is required")

    try:
        questions = generate_quiz_questions(
            course_id=payload.course_id,
            section_id=payload.section_id,
            num_questions=payload.num_questions,
            difficulty=payload.difficulty,
            lesson_content=payload.lesson_content
        )
        return GenerateQuizResponseSchema(
            status="success",
            course_id=payload.course_id,
            section_id=payload.section_id,
            questions=questions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz questions: {str(e)}")
