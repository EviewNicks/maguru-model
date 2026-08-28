from typing import Optional
from pydantic import BaseModel, Field

class IngestResponseSchema(BaseModel):
    status: str = Field("success", description="Status of the ingestion operation")
    filename: str = Field(..., description="Uploaded document filename")
    course_id: str = Field(..., description="Target course ID")
    chunks_processed: int = Field(..., description="Number of text chunks embedded and stored")
    message: str = Field("Dokumen berhasil di-ingest ke Vector Store RAG", description="Human-readable result message")

class IngestTextRequestSchema(BaseModel):
    course_id: str = Field(..., description="Target course CUID/ID")
    section_id: Optional[str] = Field(None, description="Optional section CUID/ID")
    lesson_id: Optional[str] = Field(None, description="Optional lesson CUID/ID")
    content: str = Field(..., description="Raw text content of the lesson")
