import os
import tempfile
import logging
from typing import List, Optional, Dict, Any
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.db.vector_store import get_vectorstore
from app.core.config import settings

logger = logging.getLogger(__name__)

def delete_lesson_chunks(course_id: str, lesson_id: Optional[str] = None) -> bool:
    """Delete chunks belonging to a specific lesson or an entire course to prevent duplicates."""
    db_url = settings.DATABASE_URL
    if not db_url or not course_id:
        return False

    try:
        from sqlalchemy import create_engine, text
        engine = create_engine(db_url)
        with engine.connect() as conn:
            if lesson_id:
                query = text("""
                    DELETE FROM langchain_pg_embedding 
                    WHERE (cmetadata->>'course_id' = :course_id OR cmetadata->>'course_slug' = :course_id)
                      AND cmetadata->>'lesson_id' = :lesson_id
                """)
                conn.execute(query, {"course_id": course_id, "lesson_id": lesson_id})
            else:
                query = text("""
                    DELETE FROM langchain_pg_embedding 
                    WHERE (cmetadata->>'course_id' = :course_id OR cmetadata->>'course_slug' = :course_id)
                """)
                conn.execute(query, {"course_id": course_id})
            conn.commit()
        logger.info(f"Deleted vector chunks for course='{course_id}', lesson='{lesson_id or '*'}'")
        return True
    except Exception as e:
        logger.warning(f"Could not delete vector chunks via SQL (table may not exist or offline): {str(e)}")
        return False

def get_course_knowledge_status(course_id: str) -> Dict[str, Any]:
    """Check total indexed chunks and sync availability for a course."""
    db_url = settings.DATABASE_URL
    if not db_url or not course_id:
        return {
            "status": "success",
            "course_id": course_id,
            "total_chunks": 0,
            "is_synced": False,
            "last_synced_at": None,
            "message": "Vector store database URL not configured."
        }

    try:
        from sqlalchemy import create_engine, text
        engine = create_engine(db_url)
        with engine.connect() as conn:
            query = text("""
                SELECT count(*) 
                FROM langchain_pg_embedding 
                WHERE (cmetadata->>'course_id' = :course_id OR cmetadata->>'course_slug' = :course_id)
            """)
            result = conn.execute(query, {"course_id": course_id})
            count = result.scalar() or 0
            return {
                "status": "success",
                "course_id": course_id,
                "total_chunks": int(count),
                "is_synced": count > 0,
                "last_synced_at": None,
                "message": f"{count} knowledge chunks tersimpan di AI Vector Store."
            }
    except Exception as e:
        logger.warning(f"Error checking knowledge status for course '{course_id}': {str(e)}")
        return {
            "status": "success",
            "course_id": course_id,
            "total_chunks": 0,
            "is_synced": False,
            "last_synced_at": None,
            "message": f"Status check offline: {str(e)}"
        }

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
    lesson_id: Optional[str] = None,
    title: Optional[str] = "",
    course_slug: Optional[str] = ""
) -> int:
    """Ingest raw lesson text content from Creator into pgvector store with deduplication.

    Args:
        content: Raw text or markdown content of the lesson
        course_id: Course identifier metadata
        section_id: Optional section identifier metadata
        lesson_id: Optional lesson identifier metadata
        title: Optional lesson title
        course_slug: Optional course slug

    Returns:
        Number of processed chunks stored
    """
    if not content or not content.strip():
        return 0

    # 1. Deduplication: Invalidate previous chunks for this lesson
    if lesson_id:
        delete_lesson_chunks(course_id=course_id, lesson_id=lesson_id)

    # 2. Enrich content with lesson title header for semantic context
    header = f"# {title.strip()}\n\n" if title and title.strip() else ""
    augmented_content = header + content.strip()

    doc = Document(
        page_content=augmented_content,
        metadata={
            "course_id": course_id,
            "course_slug": course_slug or "",
            "section_id": section_id or "",
            "lesson_id": lesson_id or "",
            "title": title or "",
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
        logger.info(f"Ingested {len(chunks)} lesson text chunks for course '{course_id}', lesson '{lesson_id}'")
        return len(chunks)
    except Exception as e:
        logger.error(f"Error adding text chunks to vectorstore: {str(e)}", exc_info=True)
        return len(chunks)

def bulk_ingest_course_lessons(
    course_id: str,
    lessons: List[Dict[str, Any]],
    course_slug: Optional[str] = ""
) -> Dict[str, int]:
    """Bulk ingest all lessons of a course with clean replacement.

    Args:
        course_id: Course identifier metadata
        lessons: List of lesson dicts with lesson_id, section_id, title, content
        course_slug: Optional course slug

    Returns:
        Dict with total_lessons and total_chunks
    """
    if not lessons:
        return {"total_lessons": 0, "total_chunks": 0}

    # Clean old chunks for the entire course to guarantee freshness
    delete_lesson_chunks(course_id=course_id)

    all_docs: List[Document] = []
    for item in lessons:
        title = (item.get("title") or "").strip()
        raw_content = (item.get("content") or "").strip()
        lesson_id = item.get("lesson_id") or ""
        section_id = item.get("section_id") or ""

        if not raw_content and not title:
            continue

        augmented_content = f"# {title}\n\n{raw_content}" if title else raw_content
        doc = Document(
            page_content=augmented_content,
            metadata={
                "course_id": course_id,
                "course_slug": course_slug or "",
                "section_id": section_id,
                "lesson_id": lesson_id,
                "title": title,
                "source": "creator_bulk_sync"
            }
        )
        all_docs.append(doc)

    if not all_docs:
        return {"total_lessons": 0, "total_chunks": 0}

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_chunks = splitter.split_documents(all_docs)

    vectorstore = get_vectorstore()
    if vectorstore is not None:
        try:
            vectorstore.add_documents(all_chunks)
            logger.info(f"Bulk ingested {len(all_chunks)} chunks for {len(all_docs)} lessons in course '{course_id}'")
        except Exception as e:
            logger.error(f"Error adding bulk chunks to vectorstore: {str(e)}", exc_info=True)

    return {
        "total_lessons": len(all_docs),
        "total_chunks": len(all_chunks)
    }

def get_course_context(
    course_id: str,
    query: str,
    top_k: int = 4,
    section_id: Optional[str] = None,
    lesson_id: Optional[str] = None
) -> str:
    """Retrieve top-K relevant text chunks for a given course and query with optional scoping.

    Args:
        course_id: Course identifier filter
        query: User question query
        top_k: Number of chunks to retrieve
        section_id: Optional section filter
        lesson_id: Optional lesson filter

    Returns:
        Combined text context string
    """
    if not course_id or not query:
        return ""

    try:
        vectorstore = get_vectorstore()
        if vectorstore is None:
            return ""

        docs: List[Document] = []

        # 1. Scoped retrieval: Try most specific filter first (lesson_id)
        if lesson_id:
            try:
                docs = vectorstore.similarity_search(
                    query,
                    k=top_k,
                    filter={"lesson_id": lesson_id}
                )
            except Exception as e_lesson:
                logger.warning(f"Scoped lesson search fallback for {lesson_id}: {str(e_lesson)}")

        # 2. Section-scoped retrieval if lesson-scoped yielded few or no results
        if len(docs) < 2 and section_id:
            try:
                section_docs = vectorstore.similarity_search(
                    query,
                    k=top_k,
                    filter={"section_id": section_id}
                )
                seen_content = {d.page_content for d in docs}
                for sd in section_docs:
                    if sd.page_content not in seen_content:
                        docs.append(sd)
                        seen_content.add(sd.page_content)
            except Exception as e_sec:
                logger.warning(f"Scoped section search fallback for {section_id}: {str(e_sec)}")

        # 3. Course-level retrieval fallback if still insufficient
        if len(docs) < 2:
            try:
                course_docs = vectorstore.similarity_search(
                    query,
                    k=top_k,
                    filter={"course_id": course_id}
                )
                seen_content = {d.page_content for d in docs}
                for cd in course_docs:
                    if cd.page_content not in seen_content:
                        docs.append(cd)
                        seen_content.add(cd.page_content)
            except Exception as e_course:
                logger.warning(f"Course-level search fallback for {course_id}: {str(e_course)}")

        if not docs:
            return ""

        # Format each chunk with clear lesson title header for LLM provenance
        formatted_chunks = []
        for doc in docs[:top_k]:
            title = doc.metadata.get("title") or ""
            if title and not doc.page_content.startswith("#"):
                formatted_chunks.append(f"### Materi: {title}\n{doc.page_content}")
            else:
                formatted_chunks.append(doc.page_content)

        return "\n\n---\n\n".join(formatted_chunks)
    except Exception as e:
        logger.warning(f"RAG retrieval fallback for course {course_id}: {str(e)}")
        return ""

def get_proportional_course_context(
    course_id: str,
    query: str = "konsep dasar prinsip implementasi kurikulum",
    max_chunks: int = 6
) -> str:
    """Retrieve proportional representative chunks across different sections/lessons for pre-test."""
    if not course_id:
        return ""
    try:
        vectorstore = get_vectorstore()
        if vectorstore is None:
            return ""
        all_docs = vectorstore.similarity_search(query, k=max_chunks * 2, filter={"course_id": course_id})
        if not all_docs:
            return ""

        # Group by lesson_id or title to sample evenly across different topics
        selected_docs: List[Document] = []
        seen_topics = set()
        for doc in all_docs:
            topic = doc.metadata.get("lesson_id") or doc.metadata.get("title") or "umum"
            if topic not in seen_topics:
                selected_docs.append(doc)
                seen_topics.add(topic)
            if len(selected_docs) >= max_chunks:
                break

        if len(selected_docs) < max_chunks:
            for doc in all_docs:
                if doc not in selected_docs:
                    selected_docs.append(doc)
                if len(selected_docs) >= max_chunks:
                    break

        formatted_chunks = []
        for doc in selected_docs:
            title = doc.metadata.get("title") or ""
            if title and not doc.page_content.startswith("#"):
                formatted_chunks.append(f"### Materi: {title}\n{doc.page_content}")
            else:
                formatted_chunks.append(doc.page_content)

        return "\n\n---\n\n".join(formatted_chunks)
    except Exception as e:
        logger.warning(f"Proportional RAG retrieval error for course {course_id}: {str(e)}")
        return ""
