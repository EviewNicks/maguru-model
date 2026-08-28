from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from app.schemas.ingest import IngestResponseSchema, IngestTextRequestSchema
from app.services.rag_service import ingest_document, ingest_text_content

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
            lesson_id=payload.lesson_id
        )
        return IngestResponseSchema(
            status="success",
            filename="creator_lesson_content",
            course_id=payload.course_id,
            chunks_processed=chunks,
            message="Content materi berhasil di-ingest ke Vector Store RAG"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest text content: {str(e)}")
