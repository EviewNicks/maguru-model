from fastapi import APIRouter
from app.schemas.chat import ChatInputSchema, ChatResponseSchema
from app.chains.qa_chatbot import answer_question

router = APIRouter()

@router.post("/chat/invoke", response_model=ChatResponseSchema)
async def chat_invoke(payload: ChatInputSchema):
    """Invoke AI Co-Teacher chatbot response synchronously."""
    answer = answer_question(
        question=payload.question,
        session_title=payload.session_title,
        session_content=payload.session_content,
        chat_history=payload.chat_history,
        course_id=payload.course_id
    )
    return ChatResponseSchema(answer=answer)
