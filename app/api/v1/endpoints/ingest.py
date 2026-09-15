from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Query
from typing import Optional
from app.schemas.ingest import (
    IngestResponseSchema,
    IngestTextRequestSchema,
    BulkIngestRequestSchema,
    BulkIngestResponseSchema,
    DeleteIngestRequestSchema,
    DeleteIngestResponseSchema,
    KnowledgeStatusResponseSchema
)
from app.services.rag_service import (
    ingest_document,
    ingest_text_content,
    bulk_ingest_course_lessons,
    delete_lesson_chunks,
    get_course_knowledge_status
)

router = APIRouter()

@router.post("/admin/ingest", response_model=IngestResponseSchema)
async def upload_knowledge_document(
    file: UploadFile = File(..., description="PDF or Markdown course document"),
    course_id: str = Form(..., description="Target Course Identifier")
):
    """Admin endpoint to ingest PDF/Markdown document into RAG vector store."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a filename.")

    ext = file.filename.split(".")[-1].lower()
    if ext not in ("pdf", "md", "txt", "markdown"):
        raise HTTPException(status_code=400, detail="Unsupported file extension. Allowed: .pdf, .md, .txt")

    try:
        content = await file.read()
        chunks = ingest_document(file_bytes=content, filename=file.filename, course_id=course_id)
        return IngestResponseSchema(
            status="success",
            filename=file.filename,
            course_id=course_id,
            chunks_processed=chunks,
            message="Dokumen berhasil di-ingest ke Vector Store RAG"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest document: {str(e)}")

@router.post("/ingest", response_model=IngestResponseSchema)
async def ingest_text_lesson_content(payload: IngestTextRequestSchema = Body(...)):
    """Auto-ingestion endpoint for Creator lesson content text into RAG vector store."""
    if not payload.course_id or not payload.content:
        raise HTTPException(status_code=400, detail="course_id and content are required")

    try:
        chunks = ingest_text_content(
            content=payload.content,
            course_id=payload.course_id,
            section_id=payload.section_id,
            lesson_id=payload.lesson_id,
            title=payload.title,
            course_slug=payload.course_slug
        )
        return IngestResponseSchema(
            status="success",
            filename="creator_lesson_content",
            course_id=payload.course_id,
            chunks_processed=chunks,
            message="Materi berhasil disinkronkan ke AI Vector Store"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest text content: {str(e)}")

@router.post("/ingest/bulk", response_model=BulkIngestResponseSchema)
async def bulk_ingest_lessons(payload: BulkIngestRequestSchema = Body(...)):
    """Bulk sync all lessons for a course into RAG vector store with clean replacement."""
    if not payload.course_id:
        raise HTTPException(status_code=400, detail="course_id is required")

    try:
        lessons_data = [lesson.model_dump() for lesson in payload.lessons]
        result = bulk_ingest_course_lessons(
            course_id=payload.course_id,
            lessons=lessons_data,
            course_slug=payload.course_slug
        )
        return BulkIngestResponseSchema(
            status="success",
            course_id=payload.course_id,
            total_lessons=result["total_lessons"],
            total_chunks=result["total_chunks"],
            message=f"{result['total_lessons']} materi ({result['total_chunks']} chunks) berhasil disinkronkan ke AI Knowledge Base"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to bulk ingest lessons: {str(e)}")

@router.delete("/ingest", response_model=DeleteIngestResponseSchema)
async def delete_ingest_chunks(payload: DeleteIngestRequestSchema = Body(...)):
    """Delete chunks for a specific lesson or entire course from vector store."""
    if not payload.course_id:
        raise HTTPException(status_code=400, detail="course_id is required")

    try:
        success = delete_lesson_chunks(course_id=payload.course_id, lesson_id=payload.lesson_id)
        return DeleteIngestResponseSchema(
            status="success" if success else "warning",
            course_id=payload.course_id,
            lesson_id=payload.lesson_id,
            message="Chunk materi berhasil dihapus dari AI Vector Store"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete ingest chunks: {str(e)}")

@router.get("/ingest/status", response_model=KnowledgeStatusResponseSchema)
async def get_knowledge_status(course_id: str = Query(..., description="Target course ID")):
    """Get current knowledge base indexing status and chunk count for a course."""
    if not course_id:
        raise HTTPException(status_code=400, detail="course_id is required")

    try:
        status_data = get_course_knowledge_status(course_id=course_id)
        return KnowledgeStatusResponseSchema(**status_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get knowledge status: {str(e)}")
