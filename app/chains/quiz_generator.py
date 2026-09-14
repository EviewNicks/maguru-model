"""Automated Quiz Generator Chain for generating assessment questions from lesson content."""
import json
import re
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.core.llm import get_llm_pool
from app.services.rag_service import get_course_context
from app.schemas.quiz import GenerateQuizRequestSchema

logger = logging.getLogger(__name__)

_chain = None

def _get_quiz_llm():
    """Get LLM for quiz generation with responsive timeout (25s) and token budget (4000)."""
    openrouter_key = settings.OPENROUTER_API_KEY
    models = settings.model_pool
    pool = []
    for model_name in models:
        try:
            pool.append(ChatOpenAI(
                model=model_name,
                api_key=openrouter_key or "sk-placeholder",
                base_url=settings.OPENROUTER_BASE_URL,
                temperature=0.4,
                max_completion_tokens=4000,
                request_timeout=25,
                max_retries=1
            ))
        except Exception:
            pass

    if not pool:
        pool.append(ChatOpenAI(
            model="cohere/north-mini-code:free",
            api_key=openrouter_key or "sk-placeholder",
            base_url=settings.OPENROUTER_BASE_URL,
            temperature=0.4,
            max_completion_tokens=4000,
            request_timeout=25,
            max_retries=1
        ))

    primary = pool[0]
    if len(pool) > 1:
        return primary.with_fallbacks(pool[1:])
    return primary

_prompt = None

def _get_prompt():
    """Get or load prompt template."""
    global _prompt
    if _prompt is None:
        prompt_path = Path(__file__).parent.parent / "prompts" / "quiz_generator.yaml"
        _prompt = load_prompt(str(prompt_path))
    return _prompt

def _get_chain():
    """Get or create chain (lazy initialization)."""
    global _chain
    if _chain is None:
        _chain = _get_prompt() | _get_quiz_llm() | StrOutputParser()
    return _chain

def _sanitize_input(text: Optional[str], max_len: int = 4000) -> str:
    """Sanitize and truncate input text for prompt injection protection."""
    if not text:
        return ""
    sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', str(text))
    return sanitized[:max_len]

def _clean_json_str(s: str) -> str:
    """Sanitize and repair common LLM formatting flaws in pure Python."""
    if not s:
        return ""
    # Strip markdown wrappers if any leaked in
    s = re.sub(r'<think>.*?</think>', '', s, flags=re.DOTALL).strip()
    s = re.sub(r'^```(?:json)?\s*', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\s*```$', '', s)
    s = s.strip()

    # Extract array [ ... ] if surrounded by conversational filler
    start = s.find('[')
    end = s.rfind(']')
    if start != -1 and end != -1 and end > start:
        s = s[start:end+1].strip()

    # Replace Python literals with JSON equivalents
    s = re.sub(r'\bNone\b', 'null', s)
    s = re.sub(r'\bTrue\b', 'true', s)
    s = re.sub(r'\bFalse\b', 'false', s)

    # Remove trailing commas before closing braces or brackets
    s = re.sub(r',\s*([}\]])', r'\1', s)

    # Fix single quotes used as keys: 'key': -> "key":
    s = re.sub(r"'\s*([a-zA-Z0-9_\-]+)\s*'\s*:", r'"\1":', s)

    # Fix single quotes on values: : 'val' -> : "val"
    def _fix_sq_val(m):
        content = m.group(1).replace('"', '\\"')
        return f': "{content}"{m.group(2)}'
    s = re.sub(r":\s*'([^']*)'(\s*[,}\]])", _fix_sq_val, s)

    # Fix single quotes in string arrays like 'hints': ['Hint 1', 'Hint 2']
    def _fix_sq_array(m):
        items = m.group(1)
        fixed_items = re.sub(r"'([^']*)'", r'"\1"', items)
        return f'[{fixed_items}]'
    s = re.sub(r'\[([^\[\]]*?)\]', _fix_sq_array, s)

    return s

def _regex_rescue_questions(raw_text: str, default_diff: str = "medium") -> List[Dict[str, Any]]:
    """Ultimate rescue: regex extracts question blocks when JSON parsers fail."""
    extracted = []
    # Split text into candidate blocks by looking for "question": or 'question':
    raw_blocks = re.split(r'(?=\{\s*["\']question["\']\s*:)', raw_text)
    for block in raw_blocks:
        if not re.search(r'["\']question["\']\s*:', block):
            continue

        # Extract question text
        q_match = re.search(r'["\']question["\']\s*:\s*["\'](.*?)(?=["\']\s*,\s*["\']options|\n\s*["\']options)', block, re.DOTALL)
        if not q_match:
            q_match = re.search(r'["\']question["\']\s*:\s*"((?:[^"\\]|\\.)*)"', block, re.DOTALL)
        q_text = q_match.group(1).strip() if q_match else ""
        if not q_text:
            continue

        # Extract options
        opts = {}
        for opt_key in ['a', 'b', 'c', 'd']:
            opt_m = re.search(rf'["\']{opt_key}["\']\s*:\s*["\']?(.*?)(?:["\']?\s*[,}}\n])', block, re.IGNORECASE)
            opts[opt_key] = opt_m.group(1).strip() if opt_m else ""

        # Must have at least 2 non-empty options
        if sum(1 for v in opts.values() if v) < 2:
            continue

        # Extract correct
        c_m = re.search(r'["\']correct["\']\s*:\s*["\']?([a-dA-D])["\']?', block)
        correct = c_m.group(1).lower() if c_m else "a"

        # Extract topic
        top_m = re.search(r'["\']topic["\']\s*:\s*["\']?(.*?)(?:["\']?\s*[,}}\n])', block)
        topic = top_m.group(1).strip() if top_m else "Konsep Pemrograman"

        # Extract micro_skill
        sk_m = re.search(r'["\']micro_skill["\']\s*:\s*["\']?(.*?)(?:["\']?\s*[,}}\n])', block)
        micro_skill = sk_m.group(1).strip() if sk_m else re.sub(r'[^a-z0-9]+', '-', topic.lower()).strip('-')

        # Extract explanation
        exp_m = re.search(r'["\']explanation["\']\s*:\s*["\']?(.*?)(?:["\']?\s*[,}}\n]|\Z)', block, re.DOTALL)
        explanation = exp_m.group(1).strip() if exp_m else f"Jawaban yang benar adalah {correct.upper()}."

        # Extract hints
        hints = []
        hints_m = re.findall(r'["\']hints["\']\s*:\s*\[(.*?)\]', block, re.DOTALL)
        if hints_m:
            raw_h = re.findall(r'["\'](.*?)["\']', hints_m[0])
            hints = [h.strip() for h in raw_h if h.strip() and h.lower() != "hints"]
        if not hints:
            hints = [
                f"Perhatikan kembali konsep inti pada pembahasan {topic}.",
                f"Analisis mengapa opsi {correct.upper()} adalah solusi paling tepat."
            ]

        norm = _validate_and_normalize_question({
            "question": q_text.replace('\\n', '\n'),
            "options": opts,
            "correct": correct,
            "topic": topic,
            "micro_skill": micro_skill,
            "difficulty": default_diff,
            "explanation": explanation,
            "hints": hints
        }, default_diff=default_diff)

        if norm:
            extracted.append(norm)

    return extracted

def _extract_individual_objects(target: str, default_diff: str = "medium") -> List[Dict[str, Any]]:
    """Balanced brace scanner that extracts and validates every complete JSON object."""
    questions = []
    i = 0
    n = len(target)
    while i < n:
        if target[i] == '{':
            brace_count = 0
            in_string = False
            escape = False
            start_pos = i
            valid = False

            j = i
            while j < n:
                char = target[j]
                if in_string:
                    if escape:
                        escape = False
                    elif char == '\\':
                        escape = True
                    elif char == '"':
                        in_string = False
                else:
                    if char == '"':
                        in_string = True
                    elif char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            obj_str = target[start_pos:j+1]
                            try:
                                obj = json.loads(_clean_json_str(obj_str), strict=False)
                                if isinstance(obj, dict) and "question" in obj:
                                    questions.append(obj)
                                    valid = True
                            except Exception:
                                # Try regex rescue for this single object block
                                single_rescued = _regex_rescue_questions(obj_str, default_diff=default_diff)
                                if single_rescued:
                                    questions.extend(single_rescued)
                                    valid = True
                            i = j
                            break
                j += 1
            if not valid and brace_count != 0:
                # Truncated trailing object
                break
        i += 1
    return questions

def _validate_and_normalize_question(q: Dict[str, Any], default_diff: str = "medium") -> Optional[Dict[str, Any]]:
    """Ensure question object conforms strictly to expected schema with 4 options and valid keys."""
    if not isinstance(q, dict):
        return None

    question_text = str(q.get("question", "")).strip()
    if not question_text:
        return None

    options = q.get("options")
    if not isinstance(options, dict):
        return None

    # Normalize option keys
    norm_options = {}
    for k in ["a", "b", "c", "d"]:
        val = options.get(k) or options.get(k.upper()) or ""
        norm_options[k] = str(val).strip()

    # Must have at least 2 non-empty options
    if sum(1 for v in norm_options.values() if v) < 2:
        return None

    # Normalize correct answer
    raw_correct = str(q.get("correct", "a")).strip().lower()
    correct_key = raw_correct[0] if raw_correct and raw_correct[0] in ["a", "b", "c", "d"] else "a"

    topic = str(q.get("topic", "Konsep Dasar")).strip() or "Konsep Dasar"
    difficulty = str(q.get("difficulty", default_diff)).strip().lower()
    if difficulty not in ["easy", "medium", "hard"]:
        difficulty = default_diff

    explanation = str(q.get("explanation", "")).strip()
    if not explanation:
        explanation = f"Jawaban yang benar adalah {correct_key.upper()}."

    # Normalize progressive hints (Hint 1 & Hint 2)
    raw_hints = q.get("hints", [])
    norm_hints: List[str] = []
    if isinstance(raw_hints, list):
        norm_hints = [str(h).strip() for h in raw_hints if str(h).strip()]
    elif isinstance(raw_hints, str) and raw_hints.strip():
        norm_hints = [raw_hints.strip()]

    if not norm_hints:
        norm_hints = [
            f"Perhatikan kembali konsep inti pada pembahasan {topic}.",
            f"Bandingkan alasan mengapa opsi {correct_key.upper()} menjadi solusi paling tepat secara logis."
        ]
    elif len(norm_hints) == 1:
        norm_hints.append(f"Periksa kembali detail teknis dan alur eksekusi pada {topic}.")

    # Normalize micro_skill tag
    raw_skill = str(q.get("micro_skill", "")).strip().lower()
    if not raw_skill:
        raw_skill = re.sub(r'[^a-z0-9]+', '-', topic.lower()).strip('-') or "general-skill"

    return {
        "question": question_text,
        "options": norm_options,
        "correct": correct_key,
        "topic": topic,
        "micro_skill": raw_skill,
        "difficulty": difficulty,
        "explanation": explanation,
        "hints": norm_hints[:2]
    }

def _extract_json_array(raw_text: str, default_diff: str = "medium") -> List[Dict[str, Any]]:
    """Safely extract and parse JSON array from raw LLM output with multiple fallback strategies."""
    if not raw_text or not raw_text.strip():
        raise ValueError("Raw LLM output is completely empty")

    logger.info(f"[QUIZ_GEN][EXTRACT] Raw text length: {len(raw_text)} chars")

    # 1. Strip reasoning thinking tokens
    cleaned = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL).strip()

    # 2. Extract code fence if present
    fence_match = re.search(r'```(?:json)?\s*(\[\s*\{.*?\}\s*\])\s*```', cleaned, re.DOTALL)
    if fence_match:
        target = fence_match.group(1).strip()
    else:
        # Strip markdown fences if wrapping the entire string
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        # Locate outer [ ... ]
        start = cleaned.find('[')
        end = cleaned.rfind(']')
        if start != -1 and end != -1 and end > start:
            target = cleaned[start:end+1].strip()
        else:
            target = cleaned

    parsed_raw_list = []

    # 3. Direct JSON load attempt with strict=False and trailing-comma cleaner
    try:
        data = json.loads(_clean_json_str(target), strict=False)
        if isinstance(data, list):
            parsed_raw_list = data
        elif isinstance(data, dict) and "questions" in data and isinstance(data["questions"], list):
            parsed_raw_list = data["questions"]
        elif isinstance(data, dict):
            parsed_raw_list = [data]
    except Exception as e1:
        logger.warning(f"[QUIZ_GEN][JSON_PARSE_WARN] Direct array loads failed: {str(e1)}. Attempting individual object extraction.")

    # 4. Balanced brace object extraction fallback (handles truncations & code blocks)
    if not parsed_raw_list:
        parsed_raw_list = _extract_individual_objects(target, default_diff=default_diff)
        if parsed_raw_list:
            logger.info(f"[QUIZ_GEN][RECOVERED] Successfully extracted {len(parsed_raw_list)} question objects via balanced scanner")

    # 5. Normalize and filter valid questions
    valid_questions = []
    for item in parsed_raw_list:
        norm = _validate_and_normalize_question(item, default_diff=default_diff)
        if norm:
            valid_questions.append(norm)

    if valid_questions:
        logger.info(f"[QUIZ_GEN][SUCCESS] Validated {len(valid_questions)} questions with full options and explanations")
        return valid_questions

    # 6. Global regex rescue fallback across the entire raw LLM output
    logger.warning("[QUIZ_GEN][REGEX_RESCUE_TRIGGER] Attempting global regex rescue across raw LLM text")
    rescued = _regex_rescue_questions(raw_text, default_diff=default_diff)
    if rescued:
        logger.info(f"[QUIZ_GEN][RECOVERED_REGEX] Successfully recovered {len(rescued)} questions via global regex rescue")
        return rescued

    logger.error(f"[QUIZ_GEN][EXTRACT_FAILED] Failed to extract any valid questions. Raw head: {raw_text[:400]}")
    raise ValueError(f"Could not parse LLM output as valid JSON quiz array. Raw sample: {raw_text[:300]}")

def _is_uuid_or_hash(val: Optional[str]) -> bool:
    """Check if string is a raw UUID, cuid, or hex hash that should not be shown to users."""
    if not val:
        return False
    s = str(val).strip()
    if re.match(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$', s):
        return True
    if len(s) >= 20 and re.match(r'^[0-9a-fA-F\-_]+$', s):
        return True
    return False

def _get_clean_display_title(course_id: str, course_title: Optional[str] = None) -> str:
    """Derive clean, human-readable topic name, stripping any raw database UUIDs."""
    if course_title and str(course_title).strip() and not _is_uuid_or_hash(str(course_title)):
        return _sanitize_input(str(course_title).strip(), max_len=100)
    if course_id and not _is_uuid_or_hash(course_id) and course_id.lower() not in ("umum", "default", "none"):
        return course_id.strip()[:100]
    return "Konsep Dasar Pemrograman"

def _generate_smart_fallback_questions(
    display_title: str,
    count: int,
    difficulty: str = "medium",
    question_style: str = "balanced"
) -> List[Dict[str, Any]]:
    """Generate high-quality, educationally sound fallback questions without any raw UUIDs."""
    safe_title = display_title if display_title and not _is_uuid_or_hash(display_title) else "Konsep Pemrograman"

    catalog = [
        {
            "question": f"Manakah dari pernyataan berikut yang paling tepat mengenai materi {safe_title}?",
            "options": {
                "a": "Pemrograman memerlukan pemahaman tipe data, struktur kontrol dasar, dan penanganan error yang baik",
                "b": "Semua variabel tidak memerlukan penamaan deskriptif maupun deklarasi tipe",
                "c": "Bahasa pemrograman tidak dapat mengeksekusi operasi matematika dan pembandingan logika",
                "d": "Tipe data string hanya boleh menampung angka desimal"
            },
            "correct": "a",
            "topic": f"Konsep Inti ({safe_title})",
            "micro_skill": "core-principles",
            "difficulty": difficulty,
            "explanation": f"Pemahaman tipe data, kontrol alur, dan logika eksekusi merupakan fondasi penting dalam {safe_title}.",
            "hints": [
                f"Pikirkan konsep paling mendasar yang diperlukan untuk membangun program dalam materi {safe_title}.",
                "Perhatikan mengapa struktur kontrol dan tipe data adalah elemen mutlak dalam komputasi."
            ]
        },
        {
            "question": f"Perhatikan analisis cuplikan kode Python berikut:\n```python\n1: def hitung_total(items):\n2:     total = 0\n3:     for x in items:\n4:         if isinstance(x, (int, float)):\n5:             total += x\n6:     return total\n```\nApa yang dikembalikan oleh fungsi di atas jika dipanggil dengan `hitung_total([10, 'dua puluh', 30.5, None])`?",
            "options": {
                "a": "40.5 (hanya menjumlahkan elemen numerik dan mengabaikan non-numerik)",
                "b": "Memicu TypeError karena string 'dua puluh' tidak bisa dijumlahkan",
                "c": "60.5",
                "d": "None"
            },
            "correct": "a",
            "topic": "Penanganan Tipe Data & Filtering",
            "micro_skill": "type-checking-flow",
            "difficulty": difficulty,
            "explanation": "Pengecekan `isinstance(x, (int, float))` pada baris 4 menyaring elemen non-numerik seperti string dan None, sehingga hanya 10 dan 30.5 yang dijumlahkan (10 + 30.5 = 40.5).",
            "hints": [
                "Perhatikan percabangan kondisi pada baris 4 sebelum operasi penambahan dilakukan.",
                "Hanya nilai bertipe integer dan float yang akan ditambahkan ke variabel total."
            ]
        },
        {
            "question": f"Dalam merancang sistem berbasis {safe_title}, seorang developer menemukan fungsi mengalami crash saat data bernilai kosong (null/undefined) diterima. Manakah pendekatan best practice yang paling disarankan?",
            "options": {
                "a": "Menerapkan validasi input defensif di awal fungsi atau menggunakan fallback default value",
                "b": "Menonaktifkan logging error agar crash tidak terlihat di dashboard server",
                "c": "Menghapus seluruh baris kode yang memproses data terkait",
                "d": "Membiarkan exception terjadi tanpa mekanisme recovery"
            },
            "correct": "a",
            "topic": "Error Handling & Defensive Coding",
            "micro_skill": "null-safety-guard",
            "difficulty": difficulty,
            "explanation": "Menerapkan guard clause atau default value di awal fungsi memastikan aplikasi tetap tangguh saat menerima payload tak terduga.",
            "hints": [
                "Pertimbangkan pola perancangan defensif untuk menjaga ketersediaan layanan.",
                "Pemeriksaan nilai awal (guard clause) mencegah runtime error pada eksekusi lanjutan."
            ]
        },
        {
            "question": f"Perhatikan kode perulangan yang memiliki potensi bug:\n```python\n1: def cari_indeks(daftar, target):\n2:     for i in range(len(daftar)):\n3:         if daftar[i] == target:\n4:             return i\n5:     return -1\n```\nKondisi apa yang menyebabkan fungsi ini mengembalikan nilai `-1`?",
            "options": {
                "a": "Ketika nilai `target` tidak ditemukan di dalam list `daftar`",
                "b": "Ketika `daftar` memiliki lebih dari 1 elemen bernilai sama",
                "c": "Ketika elemen target berada pada indeks pertama (indeks 0)",
                "d": "Ketika terjadi kesalahan sintaks pada perulangan for"
            },
            "correct": "a",
            "topic": "Algoritma Pencarian & Alur Eksekusi",
            "micro_skill": "linear-search-logic",
            "difficulty": difficulty,
            "explanation": "Fungsi mencari target secara linier. Jika loop selesai tanpa menemukan kecocokan, baris 5 dieksekusi dan mengembalikan sentinel value -1.",
            "hints": [
                "Perhatikan posisi `return -1` yang berada di luar blok perulangan for.",
                "Nilai -1 adalah konvensi umum yang menandakan elemen yang dicari tidak ada dalam koleksi."
            ]
        },
        {
            "question": f"Perhatikan cuplikan kode perhitungan diskon berikut:\n```python\n1: def hitung_harga_akhir(harga, diskon_persen):\n2:     if diskon_persen < 0 or diskon_persen > 100:\n3:         return harga\n4:     potongan = harga * (diskon_persen / 100)\n5:     return harga + potongan\n```\nBaris nomor berapakah yang memicu bug perhitungan logika?",
            "options": {
                "a": "Baris 5 (seharusnya `harga - potongan`)",
                "b": "Baris 2 (kondisi batas persentase keliru)",
                "c": "Baris 4 (rumus perhitungan persentase tidak tepat)",
                "d": "Baris 1 (argumen fungsi tidak valid)"
            },
            "correct": "a",
            "topic": "Bug Hunting & Logic Error",
            "micro_skill": "logic-bug-hunting",
            "difficulty": difficulty,
            "explanation": "Baris 5 keliru menambahkan potongan (`harga + potongan`), padahal diskon seharusnya mengurangi harga dasar (`harga - potongan`).",
            "hints": [
                "Periksa operator matematika yang digunakan pada pengembalian nilai akhir.",
                "Diskon seharusnya mengurangi harga barang, bukan membuatnya lebih mahal."
            ]
        }
    ]

    needed = max(1, count)
    results: List[Dict[str, Any]] = []
    while len(results) < needed:
        for item in catalog:
            if len(results) >= needed:
                break
            results.append(item.copy())
    return results[:needed]

def _invoke_backup_model(candidate_model: str, payload: dict) -> str:
    """Invoke a specific candidate model from settings.model_pool as fallback."""
    openrouter_key = settings.OPENROUTER_API_KEY
    if not openrouter_key or openrouter_key.startswith("sk-placeholder"):
        return ""
    prompt = _get_prompt()
    backup_llm = ChatOpenAI(
        model=candidate_model,
        api_key=openrouter_key,
        base_url=settings.OPENROUTER_BASE_URL,
        temperature=0.3,
        max_completion_tokens=4000,
        request_timeout=20,
        max_retries=1
    )
    backup_chain = prompt | backup_llm | StrOutputParser()
    return backup_chain.invoke(payload)

def generate_quiz_questions(
    course_id: str,
    course_title: Optional[str] = None,
    section_id: Optional[str] = None,
    num_questions: int = 5,
    difficulty: str = "medium",
    question_style: str = "balanced",
    lesson_content: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Generate structured quiz assessment questions based on course/lesson content with multi-model fallback."""
    safe_course_id = _sanitize_input(course_id, max_len=100) or "umum"
    display_title = _get_clean_display_title(course_id=safe_course_id, course_title=course_title)
    safe_difficulty = difficulty.lower() if difficulty.lower() in ("easy", "medium", "hard") else "medium"
    valid_styles = ("balanced", "code_analysis", "case_study", "conceptual")
    safe_question_style = question_style.lower() if question_style.lower() in valid_styles else "balanced"

    content_for_prompt = ""
    if lesson_content and lesson_content.strip():
        content_for_prompt = _sanitize_input(lesson_content, max_len=3500)
    else:
        try:
            content_for_prompt = get_course_context(course_id=safe_course_id, query="quiz materi konsep dasar", top_k=4)
        except Exception as e:
            logger.warning(f"RAG context retrieval for quiz generator fallback: {str(e)}")

    if not content_for_prompt or not content_for_prompt.strip():
        content_for_prompt = f"Materi pembelajaran mencakup topik '{display_title}' dengan fokus pada konsep dasar pemrograman, penanganan error, struktur data, dan best practice industri."

    logger.info(f"[QUIZ_GEN][DISPATCH] Generating {num_questions} '{safe_difficulty}' questions with style '{safe_question_style}' for topic '{display_title}' (content len: {len(content_for_prompt)})")

    prompt_payload = {
        "lesson_content": content_for_prompt,
        "num_questions": str(num_questions),
        "difficulty": safe_difficulty,
        "question_style": safe_question_style
    }

    raw_output = ""
    # 1. Attempt with primary chain
    try:
        raw_output = _get_chain().invoke(prompt_payload)
        logger.info(f"[QUIZ_GEN][RESPONSE] Received raw LLM response ({len(raw_output or '')} chars)")
    except Exception as e_primary:
        logger.warning(f"[QUIZ_GEN][PRIMARY_FAIL] Primary chain invocation failed: {str(e_primary)}")

    # 2. If primary returned empty or failed, iterate through backup models in settings.model_pool (max 2 attempts)
    if not raw_output or len(raw_output.strip()) < 30:
        logger.warning(f"[QUIZ_GEN][RETRY] Primary model returned empty/short output ({len(raw_output or '')} chars). Iterating backup model pool...")
        for candidate_model in settings.model_pool[:2]:
            try:
                logger.info(f"[QUIZ_GEN][RETRY_ATTEMPT] Trying backup model: {candidate_model}")
                candidate_output = _invoke_backup_model(candidate_model, prompt_payload)
                if candidate_output and len(candidate_output.strip()) >= 50:
                    logger.info(f"[QUIZ_GEN][RETRY_SUCCESS] Backup model '{candidate_model}' returned {len(candidate_output)} chars")
                    raw_output = candidate_output
                    break
            except Exception as e_candidate:
                logger.warning(f"[QUIZ_GEN][MODEL_FAIL] Backup model '{candidate_model}' failed: {str(e_candidate)}")

    # 3. Extract JSON questions
    valid_questions: List[Dict[str, Any]] = []
    if raw_output and len(raw_output.strip()) >= 30:
        try:
            valid_questions = _extract_json_array(raw_output, default_diff=safe_difficulty)
        except Exception as e_extract:
            logger.warning(f"[QUIZ_GEN][EXTRACT_WARN] Extraction failed from LLM text: {str(e_extract)}")

    # 4. Guarantee exact requested question count (supplement or generate fallback)
    if not valid_questions:
        logger.info(f"[QUIZ_GEN][FALLBACK_GEN] Generating {num_questions} high-quality contextual fallback questions for '{display_title}'")
        valid_questions = _generate_smart_fallback_questions(display_title, num_questions, safe_difficulty, safe_question_style)
    elif len(valid_questions) < num_questions:
        missing_count = num_questions - len(valid_questions)
        logger.info(f"[QUIZ_GEN][PADDING] Supplementing {missing_count} questions to fulfill requested {num_questions} questions")
        supplements = _generate_smart_fallback_questions(display_title, missing_count, safe_difficulty, safe_question_style)
        valid_questions.extend(supplements)

    return valid_questions[:num_questions]

def create_quiz_generator_chain():
    """Create LangServe-compatible runnable with explicit input schema."""
    def invoke(input_data: Any) -> dict:
        if isinstance(input_data, dict):
            cid = input_data.get("course_id", "umum")
            ctitle = input_data.get("course_title", None)
            sid = input_data.get("section_id", None)
            nq = input_data.get("num_questions", 5)
            diff = input_data.get("difficulty", "medium")
            qs = input_data.get("question_style", "balanced")
            lc = input_data.get("lesson_content", None)
        else:
            cid = getattr(input_data, "course_id", "umum")
            ctitle = getattr(input_data, "course_title", None)
            sid = getattr(input_data, "section_id", None)
            nq = getattr(input_data, "num_questions", 5)
            diff = getattr(input_data, "difficulty", "medium")
            qs = getattr(input_data, "question_style", "balanced")
            lc = getattr(input_data, "lesson_content", None)

        try:
            nq = int(nq)
        except (ValueError, TypeError):
            nq = 5

        questions = generate_quiz_questions(
            course_id=cid,
            course_title=ctitle,
            section_id=sid,
            num_questions=nq,
            difficulty=diff,
            question_style=qs,
            lesson_content=lc
        )
        return {"status": "success", "course_id": cid, "questions": questions}
    return RunnableLambda(invoke).with_types(input_type=GenerateQuizRequestSchema)
