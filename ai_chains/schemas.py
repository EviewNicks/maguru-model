# ========================================
# Pydantic Input Models
# ========================================
#
# Input validation for LangServe endpoints
#

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any


class ChatbotInput(BaseModel):
    """Input model for Q&A chatbot."""
    question: str = Field(..., description="Student's question", min_length=1)
    session_title: str = Field(..., description="Current session/lesson title", min_length=1)
    session_content: str = Field(default="", description="Session markdown content")
    chat_history: List[Dict[str, str]] = Field(
        default_factory=list,
        description="List of recent chat messages"
    )

    @validator('chat_history')
    def validate_chat_history(cls, v):
        """Validate chat history format."""
        if not isinstance(v, list):
            return []
        valid_messages = []
        for msg in v[-10:]:  # Limit to last 10 messages
            if isinstance(msg, dict):
                valid_messages.append({
                    "role": str(msg.get("role", "student")),
                    "content": str(msg.get("content", ""))
                })
        return valid_messages

    @validator('session_content')
    def truncate_content(cls, v):
        """Truncate content if too long."""
        if len(v) > 1000:
            return v[:1000]
        return v


class ExplainCodeInput(BaseModel):
    """Input model for code explanation."""
    code: str = Field(..., description="Code snippet to explain", min_length=1)

    @validator('code')
    def validate_code(cls, v):
        """Ensure code is not empty."""
        if not v or v.isspace():
            raise ValueError("Code cannot be empty")
        return v.strip()


class HintInput(BaseModel):
    """Input model for hint generator."""
    task: str = Field(..., description="Practice task description", min_length=1)
    attempt: str = Field(default="", description="Student's current attempt")
    level: int = Field(
        default=1,
        ge=1,
        le=3,
        description="Hint level (1=gentle, 2=conceptual, 3=direct)"
    )

    @validator('task')
    def validate_task(cls, v):
        """Ensure task is not empty."""
        if not v or v.isspace():
            raise ValueError("Task cannot be empty")
        return v.strip()


class QuizFeedbackInput(BaseModel):
    """Input model for quiz feedback."""
    question: str = Field(..., description="Question text", min_length=1)
    student_answer: str = Field(default="", description="Student's answer")
    correct_answer: str = Field(..., description="Correct answer", min_length=1)
    is_correct: bool = Field(..., description="Whether answer was correct")

    @validator('student_answer', pre=True)
    def validate_student_answer(cls, v):
        """Handle string boolean for is_correct."""
        if v is None:
            return ""
        return str(v)

    @validator('question', 'correct_answer')
    def validate_not_empty(cls, v):
        """Ensure required fields are not empty."""
        if not v or v.isspace():
            raise ValueError("This field cannot be empty")
        return v.strip()


class GreetingInput(BaseModel):
    """Input model for AI greeting."""
    student_name: str = Field(default="Siswa", description="Student's name")
    course_metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Course metadata with title and learning_objectives"
    )

    @validator('student_name')
    def validate_name(cls, v):
        """Ensure name is reasonable."""
        if not v:
            return "Siswa"
        return str(v).strip()[:50]  # Limit to 50 characters

    @validator('course_metadata', pre=True)
    def validate_metadata(cls, v):
        """Handle course metadata."""
        if v is None:
            return {}
        if isinstance(v, str):
            return {"title": v}
        if isinstance(v, dict):
            return {
                "title": str(v.get("title", ""))[:100],
                "learning_objectives": v.get("learning_objectives", [])
            }
        return {}


# ========================================
# Response Models
# ========================================

class AIResponse(BaseModel):
    """Standard AI response model."""
    content: str = Field(..., description="AI-generated content")
    success: bool = Field(default=True, description="Whether request succeeded")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class StreamingChunk(BaseModel):
    """Streaming response chunk."""
    event: str = Field(..., description="Event type (data or error)")
    data: str = Field(default="", description="Chunk content")
