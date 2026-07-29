from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the sender: 'student' or 'ai'")
    content: str = Field(..., description="Message content")

class ChatInputSchema(BaseModel):
    question: str = Field(..., description="Student question")
    session_title: Optional[str] = Field("", description="Current session title")
    session_content: Optional[str] = Field("", description="Current session content")
    chat_history: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Recent conversation history")
    course_id: Optional[str] = Field(None, description="Optional Course ID for RAG context retrieval")

class ChatResponseSchema(BaseModel):
    answer: str = Field(..., description="AI response answer in Indonesian")
