from typing import Optional, List
from pydantic import BaseModel, Field

class IngestResponseSchema(BaseModel):
    status: str = Field("success", description="Status of the ingestion operation")
    filename: str = Field(..., description="Uploaded document filename or content source")
    course_id: str = Field(..., description="Target course ID")
    chunks_processed: int = Field(..., description="Number of text chunks embedded and stored")
    message: str = Field("Dokumen berhasil di-ingest ke Vector Store RAG", description="Human-readable result message")

class IngestTextRequestSchema(BaseModel):
    course_id: str = Field(..., description="Target course CUID/ID")
    section_id: Optional[str] = Field(None, description="Optional section CUID/ID")
    lesson_id: Optional[str] = Field(None, description="Optional lesson CUID/ID")
    title: Optional[str] = Field("", description="Optional lesson title")
    course_slug: Optional[str] = Field("", description="Optional course slug")
    content: str = Field(..., description="Raw text content of the lesson")

class BulkIngestLessonItemSchema(BaseModel):
    lesson_id: str = Field(..., description="Unique lesson identifier")
    section_id: Optional[str] = Field(None, description="Optional section identifier")
    title: str = Field(..., description="Lesson title")
    content: str = Field(..., description="Full text content of the lesson")

class BulkIngestRequestSchema(BaseModel):
    course_id: str = Field(..., description="Target course ID")
    course_slug: Optional[str] = Field("", description="Optional course slug")
    lessons: List[BulkIngestLessonItemSchema] = Field(default_factory=list, description="List of lessons to ingest")

class BulkIngestResponseSchema(BaseModel):
    status: str = Field("success", description="Status of bulk ingestion")
    course_id: str = Field(..., description="Target course ID")
    total_lessons: int = Field(..., description="Number of lessons processed")
    total_chunks: int = Field(..., description="Total text chunks embedded and stored")
    message: str = Field("Seluruh materi berhasil disinkronkan ke AI Knowledge Base", description="Result message")

class DeleteIngestRequestSchema(BaseModel):
    course_id: str = Field(..., description="Target course ID")
    lesson_id: Optional[str] = Field(None, description="Optional specific lesson ID to delete. If omitted, deletes all chunks for course.")

class DeleteIngestResponseSchema(BaseModel):
    status: str = Field("success", description="Status of deletion")
    course_id: str = Field(..., description="Target course ID")
    lesson_id: Optional[str] = Field(None, description="Deleted lesson ID if specific")
    message: str = Field("Chunk materi berhasil dihapus dari Vector Store", description="Result message")

class KnowledgeStatusResponseSchema(BaseModel):
    status: str = Field("success", description="Status check result")
    course_id: str = Field(..., description="Target course ID")
    total_chunks: int = Field(0, description="Number of active knowledge chunks in vector store")
    is_synced: bool = Field(False, description="Whether course has at least one chunk indexed")
    last_synced_at: Optional[str] = Field(None, description="ISO timestamp of last sync if available")
    message: str = Field("Knowledge base status retrieved", description="Status message")
