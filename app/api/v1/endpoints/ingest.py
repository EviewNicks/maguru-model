from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.ingest import IngestResponseSchema
from app.services.rag_service import ingest_document

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
