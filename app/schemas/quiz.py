from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class QuizOptionsSchema(BaseModel):
    a: str = Field(..., description="Pilihan A")
    b: str = Field(..., description="Pilihan B")
    c: str = Field(..., description="Pilihan C")
    d: str = Field(..., description="Pilihan D")

class QuizQuestionSchema(BaseModel):
    question: str = Field(..., description="Teks pertanyaan kuis")
    options: QuizOptionsSchema = Field(..., description="Pilihan jawaban a, b, c, d")
    correct: str = Field(..., description="Kunci jawaban: a, b, c, atau d")
    topic: str = Field(..., description="Topik/subtopik materi")
    difficulty: str = Field("medium", description="Tingkat kesulitan: easy, medium, hard")

class GenerateQuizRequestSchema(BaseModel):
    course_id: str = Field("umum", description="CUID atau ID unik kursus")
    section_id: str = Field("", description="CUID section (opsional)")
    num_questions: int = Field(5, description="Jumlah soal kuis yang diminta")
    difficulty: str = Field("medium", description="Tingkat kesulitan kuis: easy, medium, hard")
    lesson_content: str = Field("", description="Teks materi langsung dari lesson jika tidak dari vectorstore")

class GenerateQuizResponseSchema(BaseModel):
    status: str = Field("success", description="Status operasi pengerjaan kuis")
    course_id: str = Field(..., description="Target course ID")
    section_id: Optional[str] = Field(None, description="Target section ID")
    questions: List[QuizQuestionSchema] = Field(..., description="Daftar soal kuis berformat JSON")
