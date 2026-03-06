# API Testing - Maguru LangServe

## 📋 Prerequisites

1. **Server running:**
   ```bash
   cd D:\.maguru\maguru-model
   python server.py
   ```
   Server runs on `http://localhost:8000`

2. **Postman installed:** [Download Postman](https://www.postman.com/downloads/)

3. **Environment variables set:** `.env` file with `OPENROUTER_API_KEY`

---

## 🚀 Quick Start

### Import Collection

1. Open Postman
2. Click **Import** (top-left)
3. Select `api_test/maguru-api.postman_collection.json`
4. Click **Import**

### Test Health Check

```
GET http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "service": "Maguru AI API",
  "version": "1.0.0"
}
```

---

## ⚠️ CRITICAL: Request Format

**All POST requests must wrap input in `input` key:**

```json
{
  "input": {
    "actual_fields_here": "..."
  }
}
```

❌ **WRONG:**
```json
{
  "question": "Apa itu Python?"
}
```

✅ **CORRECT:**
```json
{
  "input": {
    "question": "Apa itu Python?",
    "session_title": "Python Basics",
    "session_content": "...",
    "chat_history": []
  }
}
```

---

## 🧪 Test Endpoints

### 1. Health Check (GET)
```
GET /health
```

### 2. Chatbot (POST)

**Invoke (non-streaming):**
```json
POST /chatbot/invoke
{
  "input": {
    "question": "Apa itu variabel?",
    "session_title": "Python Basics",
    "session_content": "Variabel adalah...",
    "chat_history": []
  }
}
```

**Stream (SSE):**
```json
POST /chatbot/stream
{
  "input": {
    "question": "Apa itu variabel?",
    "session_title": "Python Basics",
    "session_content": "Variabel adalah...",
    "chat_history": []
  }
}
```

### 3. Explain Code (POST)
```json
POST /explain-code/stream
{
  "input": {
    "code": "x = 5\nprint(x)"
  }
}
```

### 4. Hint Generator (POST)
```json
POST /hint/stream
{
  "input": {
    "task": "Buat function luas segitiga",
    "attempt": "def hitung(): return 0",
    "level": 1
  }
}
```

**Level options:**
- `1` - Halus (gentle)
- `2` - Konseptual (conceptual)
- `3` - Langsung (direct)

### 5. Quiz Feedback (POST)
```json
POST /quiz-feedback/stream
{
  "input": {
    "question": "Output dari print(2+2)?",
    "student_answer": "5",
    "correct_answer": "4",
    "is_correct": false
  }
}
```

**Note:** `is_correct` is **boolean**, not string!

### 6. Greeting (POST)
```json
POST /greeting/stream
{
  "input": {
    "student_name": "Budi",
    "course_metadata": {
      "title": "Python Basics for Beginners"
    }
  }
}
```

---

## 📊 Expected Responses

### Invoke (non-streaming)
```json
{
  "output": "Jawaban AI di sini..."
}
```

### Stream (SSE format)
```
data: {"output": "Jawaban"}
data: {"output": "AI"}
data: {"output": "di sini..."}
data: [DONE]
```

---

## 🐛 Common Issues

| Error | Cause | Fix |
|-------|--------|-----|
| **422 Unprocessable Entity** | Missing `input` wrapper | Wrap request body in `{"input": {...}}` |
| **Connection refused** | Server not running | Run `python server.py` |
| **API key error** | Missing OPENROUTER_API_KEY | Add to `.env` file |
| **Wrong field name** | Type mismatch | Check field names below |

---

## 📝 Field Reference

### Chatbot
| Field | Type | Required |
|-------|------|----------|
| `question` | string | ✅ |
| `session_title` | string | ❌ |
| `session_content` | string | ❌ |
| `chat_history` | array | ❌ |

### Hint
| Field | Type | Required |
|-------|------|----------|
| `task` | string | ✅ |
| `attempt` | string | ✅ |
| `level` | number (1-3) | ✅ |

### Quiz Feedback
| Field | Type | Required |
|-------|------|----------|
| `question` | string | ✅ |
| `student_answer` | string | ✅ |
| `correct_answer` | string | ❌ |
| `is_correct` | boolean | ✅ |

### Greeting
| Field | Type | Required |
|-------|------|----------|
| `student_name` | string | ❌ |
| `course_metadata` | object | ❌ |

---

## 📚 Next Steps

After confirming API works in Postman:
1. Fix frontend `api.ts` to wrap requests in `{"input": ...}`
2. Update TypeScript interfaces in `types/index.ts`
3. Test frontend integration

---

**Created:** 2025-03-06
**Version:** 1.0
