import os
import tempfile
import logging
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.db.vector_store import get_vectorstore

logger = logging.getLogger(__name__)

def ingest_document(file_bytes: bytes, filename: str, course_id: str) -> int:
    """Load, chunk, embed, and store document into pgvector store.

    Args:
        file_bytes: Document file content
        filename: Name of the uploaded file
        course_id: Course identifier metadata

    Returns:
        Number of processed chunks stored
    """
    ext = os.path.splitext(filename)[1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        if ext == ".pdf":
            loader = PyPDFLoader(tmp_path)
        else:
            loader = TextLoader(tmp_path, encoding="utf-8")
        
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        for chunk in chunks:
            chunk.metadata["course_id"] = course_id
            chunk.metadata["source"] = filename

        vectorstore = get_vectorstore()
        if vectorstore is None:
            raise RuntimeError("VectorStore is unavailable. Check DATABASE_URL configuration.")

        vectorstore.add_documents(chunks)
        logger.info(f"Successfully ingested {len(chunks)} chunks for course '{course_id}'")
        return len(chunks)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def ingest_text_content(
    content: str,
    course_id: str,
    section_id: Optional[str] = None,
    lesson_id: Optional[str] = None
) -> int:
    """Ingest raw lesson text content from Creator into pgvector store.

    Args:
        content: Raw text or markdown content of the lesson
        course_id: Course identifier metadata
        section_id: Optional section identifier metadata
        lesson_id: Optional lesson identifier metadata

    Returns:
        Number of processed chunks stored
    """
    if not content or not content.strip():
        return 0

    doc = Document(
        page_content=content,
        metadata={
            "course_id": course_id,
            "section_id": section_id or "",
            "lesson_id": lesson_id or "",
            "source": "creator_lesson_content"
        }
    )

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents([doc])

    vectorstore = get_vectorstore()
    if vectorstore is None:
        logger.warning(f"VectorStore unavailable, fallback indexing for course {course_id}")
        return len(chunks)

    try:
        vectorstore.add_documents(chunks)
        logger.info(f"Ingested {len(chunks)} lesson text chunks for course '{course_id}'")
        return len(chunks)
    except Exception as e:
        logger.error(f"Error adding text chunks to vectorstore: {str(e)}", exc_info=True)
        return len(chunks)

def get_course_context(course_id: str, query: str, top_k: int = 4) -> str:
    """Retrieve top-K relevant text chunks for a given course and query.

    Args:
        course_id: Course identifier filter
        query: User question query
        top_k: Number of chunks to retrieve

    Returns:
        Combined text context string
    """
    if not course_id or not query:
        return ""

    try:
        vectorstore = get_vectorstore()
        if vectorstore is None:
            return ""

        docs = vectorstore.similarity_search(
            query,
            k=top_k,
            filter={"course_id": course_id}
        )
        if not docs:
            return ""
        return "\n\n---\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        logger.warning(f"RAG retrieval fallback for course {course_id}: {str(e)}")
        return ""
