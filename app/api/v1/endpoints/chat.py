import json
import uuid
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatInputSchema, ChatResponseSchema
from app.chains.qa_chatbot import answer_question
from app.graphs.qa_graph import astream_qa_graph

router = APIRouter()

@router.post("/chat/invoke", response_model=ChatResponseSchema)
async def chat_invoke(payload: ChatInputSchema):
    """Invoke AI Co-Teacher chatbot response synchronously with state persistence."""
    thread_id = payload.thread_id or f"session-{payload.course_id or 'global'}-{uuid.uuid4()}"
    answer = answer_question(
        question=payload.question,
        session_title=payload.session_title,
        session_content=payload.session_content,
        chat_history=payload.chat_history,
        course_id=payload.course_id,
        thread_id=thread_id
    )
    return ChatResponseSchema(answer=answer, thread_id=thread_id)

@router.post("/chat/stream")
@router.post("/chatbot/stream")
async def chat_stream(payload: ChatInputSchema):
    """Stream AI Co-Teacher response token-by-token using Server-Sent Events (SSE)."""
    thread_id = payload.thread_id or f"session-{payload.course_id or 'global'}-{uuid.uuid4()}"

    async def event_generator():
        yield f"event: thread_id\ndata: {json.dumps({'thread_id': thread_id})}\n\n"
        async for token in astream_qa_graph(
            question=payload.question,
            course_id=payload.course_id,
            session_title=payload.session_title,
            session_content=payload.session_content,
            thread_id=thread_id
        ):
            payload_data = json.dumps({"token": token, "content": token})
            yield f"event: data\ndata: {payload_data}\n\n"
        yield "event: end\ndata: {}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
