from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role pengirim: 'student' atau 'ai'")
    content: str = Field(..., description="Isi teks pesan")

class ChatInputSchema(BaseModel):
    question: str = Field(..., description="Pertanyaan dari siswa / user")
    session_title: str = Field("", description="Judul sesi atau materi pembelajaran (opsional)")
    session_content: str = Field("", description="Potongan materi sesi pembelajaran (opsional)")
    course_id: str = Field("", description="ID Kursus untuk RAG knowledge base retrieval (opsional)")
    thread_id: str = Field("", description="Session / Thread ID untuk persistensi memori percakapan (opsional)")

class ChatResponseSchema(BaseModel):
    answer: str = Field(..., description="Jawaban AI Co-Teacher dalam Bahasa Indonesia")
    thread_id: Optional[str] = Field(None, description="Thread ID sesi memori percakapan")

class ExplainCodeInputSchema(BaseModel):
    code: str = Field(..., description="Potongan kode pemrograman yang ingin dijelaskan oleh AI")

class HintInputSchema(BaseModel):
    task: str = Field(..., description="Deskripsi soal atau tugas pemrograman yang sedang dikerjakan")
    student_attempt: str = Field("", description="Kode atau percobaan solusi yang ditulis siswa")
    level: int = Field(1, description="Tingkat petunjuk (1: Tip umum, 2: Clue logika, 3: Panduan detail)")

class QuizFeedbackInputSchema(BaseModel):
    question: str = Field(..., description="Pertanyaan kuis")
    student_answer: str = Field(..., description="Jawaban yang dipilih siswa")
    correct_answer: str = Field(..., description="Kunci jawaban yang benar")
    is_correct: bool = Field(False, description="Status apakah jawaban siswa benar (True/False)")

class GreetingInputSchema(BaseModel):
    user_name: str = Field("Siswa", description="Nama siswa / pengguna")
