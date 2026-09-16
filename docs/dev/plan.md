# Rencana Implementasi: Integrasi LangServe Backend + Next.js Frontend

## Ringkasan

**Tujuan**: Menghubungkan LangChain AI chains (backend) dengan Next.js frontend menggunakan LangServe

**Pendekatan**: LangServe (tool resmi LangChain untuk men-deploy chains sebagai REST API)

**Target**: Chatbot assistance di halaman Learn Mode Maguru Platform

**Timeline**: ~2-3 hari untuk implementasi lengkap

---

## 1. Prasyarat (Prerequisites)

### 1.1 Backend Requirements

| Tool | Version | Status |
|------|---------|--------|
| Python | 3.8+ | ✅ Required |
| FastAPI | latest | ✅ Required |
| LangServe | latest | ✅ Required |
| LangChain | latest | ✅ Ready |
| uvicorn | latest | ✅ Required |

### 1.2 Frontend Requirements

| Tool | Version | Status |
|------|---------|--------|
| Node.js | 18+ | ✅ Ready |
| Next.js | 15.5.3 | ✅ Ready |
| TypeScript | 5.9+ | ✅ Ready |

### 1.3 API Keys

Diperlukan environment variables untuk LLM providers:

```bash
# OpenRouter (Primary)
OPENROUTER_API_KEY=sk-...
OPENROUTER_MODEL=google/gemma-7b-it

# Z.AI (Fallback)
ZAI_API_KEY=sk-...
ZAI_MODEL=glm-4.7
```

---

## 2. Arsitektur Target

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Maguru Learning Platform                  │
├─────────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────┐      ┌─────────────────────────┐ │
│  │   Next.js Frontend    │      │   Python Backend       │ │
│  │   Port: 3000          │      │   Port: 8000           │ │
│  │                        │      │                        │ │
│  │  Components:          │      │  Components:          │ │
│  │  - Learn Page         │      │  - LangServe Server    │ │
│  │  - Chatbot UI         │      │  - AI Chains          │ │
│  │  - API Client         │      │  - LLM Integration     │ │
│  └─────────────────────────┘      └─────────────────────────┘ │
│              ▲                            ▲              │
│              │                            │              │
│              │ HTTP / REST API             │              │
│              └────────────────────────────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Rencana Implementasi

### Fase 1: Backend Setup (LangServe Server)

**Estimasi Waktu**: 1-2 jam

#### Langkah 1.1: Install Dependencies

```bash
cd maguru-model
pip install langserve fastapi uvicorn[standard] pydantic
```

#### Langkah 1.2: Buat File Server

**File**: `maguru-model/server.py`

**Struktur**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from ai_chains.chains import qa_chatbot, explain_code, hint_generator
from ai_chains.chains.quiz_feedback import generate_feedback
from ai_chains.chains.ai_greeting import generate_greeting

app = FastAPI(title="Maguru AI API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add LangServe routes for each chain
add_routes(app, qa_chatbot.answer_question, path="/chatbot")
add_routes(app, explain_code.explain_code, path="/explain-code")
add_routes(app, hint_generator.generate_hint, path="/hint")
add_routes(app, generate_feedback, path="/quiz-feedback")
add_routes(app, generate_greeting, path="/greeting")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Langkah 1.3: Test Server

```bash
python server.py
# Should show: INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test endpoints**:
```bash
# Test chatbot endpoint
curl -X POST http://localhost:8000/chatbot/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": {"question": "Halo", "session_title": "Test", "session_content": "...", "chat_history": []}}'
```

#### Checklist Backend:
- [ ] Install langserve
- [ ] Buat server.py
- [ ] Import semua chains
- [ ] Configure CORS
- [ ] Test endpoint lokal
- [ ] Update requirements.txt

---

### Fase 2: Frontend API Client

**Estimasi Waktu**: 1-2 jam

#### Langkah 2.1: Buat Directory lib (jika belum ada)

```bash
cd maguru
mkdir -p lib
```

#### Langkah 2.2: Buat File API Client

**File**: `maguru/lib/ai-api.ts`

**Struktur**:
```typescript
// LangServe API Base URL
const LANGSERVE_BASE_URL = process.env.NEXT_PUBLIC_LANGSERVE_URL || 'http://localhost:8000'

// Types
export interface ChatMessage {
  role: 'student' | 'ai'
  content: string
}

export interface ChatbotRequest {
  question: string
  session_title: string
  session_content: string
  chat_history: ChatMessage[]
}

export interface ChatbotResponse {
  output: string
}

// Q&A Chatbot Function
export async function queryChatbot(request: ChatbotRequest): Promise<ChatbotResponse> {
  try {
    const response = await fetch(`${LANGSERVE_BASE_URL}/chatbot/invoke`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: request })
    })

    if (!response.ok) {
      throw new Error(`Chatbot API error: ${response.status}`)
    }

    return response.json()
  } catch (error) {
    console.error('Error calling chatbot:', error)
    throw error
  }
}

// Code Explanation Function
export async function explainCode(codeSnippet: string): Promise<{output: string}> {
  try {
    const response = await fetch(`${LANGSERVE_BASE_URL}/explain-code/invoke`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: { code_snippet: codeSnippet } })
    })

    if (!response.ok) {
      throw new Error(`Explain code API error: ${response.status}`)
    }

    return response.json()
  } catch (error) {
    console.error('Error explaining code:', error)
    throw error
  }
}

// Hint Generator Function
export async function getHint(
  task: string,
  studentAttempt: string,
  level: 1 | 2 | 3
): Promise<{output: string}> {
  try {
    const response = await fetch(`${LANGSERVE_BASE_URL}/hint/invoke`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        input: { task, student_attempt: studentAttempt, level }
      })
    })

    if (!response.ok) {
      throw new Error(`Hint API error: ${response.status}`)
    }

    return response.json()
  } catch (error) {
    console.error('Error getting hint:', error)
    throw error
  }
}
```

#### Langkah 2.3: Configure Environment Variable

**File**: `maguru/.env.local`

```bash
NEXT_PUBLIC_LANGSERVE_URL=http://localhost:8000
```

#### Checklist Frontend API:
- [ ] Buat directory lib/
- [ ] Buat file ai-api.ts
- [ ] Implement queryChatbot function
- [ ] Implement explainCode function
- [ ] Implement getHint function
- [ ] Add error handling
- [ ] Configure .env.local

---

### Fase 3: Chatbot UI Component

**Estimasi Waktu**: 2-3 jam

#### Langkah 3.1: Buat Directory Chatbot (jika belum ada)

```bash
cd maguru
mkdir -p features/course/components/chatbot
```

#### Langkah 3.2: Buat File Context Types

**File**: `maguru/features/course/components/chatbot/types.ts`

```typescript
export interface ChatbotContextProps {
  courseId: string
  sectionId: string
  itemId: string
  itemTitle: string
  currentContent: string
  completedItems: string[]
  progressPercentage: number
}

export interface ChatMessage {
  id: string
  role: 'student' | 'ai'
  content: string
  timestamp: Date
}
```

#### Langkah 3.3: Buat Chatbot Component Utama

**File**: `maguru/features/course/components/chatbot/ChatbotAssistant.tsx`

**Fitur**:
- Floating action button (FAB)
- Sheet panel untuk chat
- Message list dengan scroll
- Input field
- Loading state
- Error handling

#### Langkah 3.4: Buat Chat Message Component

**File**: `maguru/features/course/components/chatbot/ChatMessage.tsx`

**Fitur**:
- Style berbeda untuk student vs AI
- Avatar/ikon
- Timestamp
- Markdown rendering untuk AI response

#### Checklist UI Component:
- [ ] Buat directory chatbot/
- [ ] Buat types.ts
- [ ] Buat ChatbotAssistant.tsx
- [ ] Buat ChatMessage.tsx
- [ ] Implement floating button
- [ ] Implement Sheet panel
- [ ] Implement message list
- [ ] Implement input field
- [ ] Add loading states
- [ ] Add error handling
- [ ] Match theme (Ancient Fantasy Asia)

---

### Fase 4: Integrasi ke Learn Page

**Estimasi Waktu**: 1 jam

#### Langkah 4.1: Buka Learn Page

**File**: `maguru/app/course/[slug]/learn/page.tsx`

#### Langkah 4.2: Import Chatbot Component

```tsx
import { ChatbotAssistant } from '@/features/course/components/chatbot/ChatbotAssistant'
```

#### Langkah 4.3: Tambah Chatbot ke Layout

Tambahkan komponen ChatbotAssistant di dalam LearningModeContent return:

```tsx
// Sebelum </div> terakhir
<ChatbotAssistant
  courseId={slug}
  sectionId={currentSectionId}
  itemId={currentItemId}
  itemTitle={currentItem?.title || ''}
  currentContent={content}
  completedItems={progress?.completedItems || []}
  progressPercentage={navigationInfo.progressPercentage}
/>
```

#### Checklist Integrasi:
- [ ] Import ChatbotAssistant
- [ ] Tambah ke layout Learn page
- [ ] Pass semua context yang diperlukan
- [ ] Test rendering di browser
- [ ] Test responsive di mobile

---

### Fase 5: Testing & Debugging

**Estimasi Waktu**: 1-2 jam

#### Langkah 5.1: Unit Testing

Test komponen secara terpisah:

```bash
# Test component rendering
npm test ChatbotAssistant

# Test API client
npm test ai-api
```

#### Langkah 5.2: Integration Testing

Test flow end-to-end:

1. **Backend Test**:
   ```bash
   # Start backend
   python server.py

   # Test endpoint
   curl -X POST http://localhost:8000/chatbot/invoke \
     -H "Content-Type: application/json" \
     -d '{"input": {"question": "Apa itu Python?", ...}}'
   ```

2. **Frontend Test**:
   - Buka http://localhost:3000/course/python-basics/learn
   - Klik tombol chatbot
   - Kirim pertanyaan
   - Verifikasi jawaban muncul

3. **CORS Test**:
   - Pastikan frontend bisa panggil backend
   - Cek browser console untuk CORS errors

#### Checklist Testing:
- [ ] Backend endpoint respond dengan benar
- [ ] Frontend bisa panggil backend
- [ ] CORS tidak ada masalah
- [ ] Error handling berfungsi
- [ ] Loading states berfungsi
- [ ] Responsive design benar

---

### Fase 6: Deployment Preparation

**Estimasi Waktu**: 1-2 jam

#### Langkah 6.1: Environment Configuration

Production environment variables:

```bash
# .env.production
NEXT_PUBLIC_LANGSERVE_URL=https://maguru-ai.your-domain.com
```

#### Langkah 6.2: Update requirements.txt

```txt
# Add to maguru-model/requirements.txt
langserve>=0.0.1
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
```

#### Checklist Deployment:
- [ ] Update .env untuk production
- [ ] Update requirements.txt
- [ ] Test di production environment
- [ ] Configure CORS untuk production domain

---

## 4. File yang Akan Dibuat/Diubah

### 4.1 File Baru (Backend)

| File | Path | Description |
|------|-------|-------------|
| `server.py` | `maguru-model/server.py` | LangServe server |

### 4.2 File Baru (Frontend)

| File | Path | Description |
|------|-------|-------------|
| `ai-api.ts` | `maguru/lib/ai-api.ts` | API client functions |
| `types.ts` | `maguru/features/course/components/chatbot/types.ts` | TypeScript types |
| `ChatbotAssistant.tsx` | `maguru/features/course/components/chatbot/ChatbotAssistant.tsx` | Main chatbot component |
| `ChatMessage.tsx` | `maguru/features/course/components/chatbot/ChatMessage.tsx` | Message component |

### 4.3 File yang Akan Dimodifikasi

| File | Path | Changes |
|------|-------|---------|
| `page.tsx` | `maguru/app/course/[slug]/learn/page.tsx` | Add ChatbotAssistant |
| `requirements.txt` | `maguru-model/requirements.txt` | Add langserve dependencies |
| `.env.local` | `maguru/.env.local` | Add NEXT_PUBLIC_LANGSERVE_URL |

---

## 5. Urutan Implementasi (Step-by-Step)

### Hari 1: Backend & API Client

1. Install dependencies: `pip install langserve`
2. Buat `maguru-model/server.py`
3. Test backend endpoint
4. Buat `maguru/lib/ai-api.ts`
5. Configure `.env.local`

**Output Akhir Hari 1**: Backend berjalan, frontend bisa panggil API

### Hari 2: UI Components & Integrasi

6. Buat `maguru/features/course/components/chatbot/` directory
7. Buat `types.ts`
8. Buat `ChatbotAssistant.tsx`
9. Buat `ChatMessage.tsx`
10. Integrasikan ke Learn page

**Output Akhir Hari 2**: Chatbot UI muncul di Learn page

### Hari 3: Testing & Deployment

11. Unit testing komponen
12. Integration testing
13. Debug dan fix
14. Test responsive
15. Prepare deployment

**Output Akhir Hari 3**: Siap untuk production

---

## 6. Troubleshooting Common Issues

### 6.1 CORS Errors

**Masalah**: Browser menolak request ke backend

**Solusi**:
1. Pastikan CORS middleware ada di server.py
2. Tambah domain production ke allow_origins
3. Cek browser console untuk detail error

### 6.2 Connection Refused

**Masalah**: Tidak bisa connect ke localhost:8000

**Solusi**:
1. Pastikan backend server berjalan
2. Cek port 8000 tidak dipakai program lain
3. Verifikasi NEXT_PUBLIC_LANGSERVE_URL benar

### 6.3 Type Errors

**Masalah**: TypeScript compilation error

**Solusi**:
1. Pastikan types.ts diimport dengan benar
2. Cek interface names sesuai
3. Run `npm run type-check` untuk detail error

### 6.4 LangServe Import Errors

**Masalah**: Cannot import chain modules

**Solusi**:
1. Pastikan working directory benar
2. Cek __init__.py ada di ai_chains/
3. Install ulang langchain jika perlu

---

## 7. Success Criteria

### 7.1 Backend Success

- [ ] Server berjalan tanpa error
- [ ] Semua endpoints respond dengan benar
- [ ] CORS configured dengan benar
- [ ] LLM providers connected

### 7.2 Frontend Success

- [ ] Chatbot UI muncul di Learn page
- [ ] Bisa kirim pertanyaan
- [ ] Jawaban AI muncul
- [ ] Chat history maintained
- [ ] Error handling berfungsi
- [ ] Responsive di mobile

### 7.3 Integration Success

- [ ] Frontend bisa panggil backend
- [ ] Context passed dengan benar
- [ ] Loading states berfungsi
- [ ] User experience smooth

---

## 8. Next Steps Setelah Implementasi

### 8.1 Features Enhancement

| Priority | Feature | Description |
|----------|----------|-------------|
| P1 | Streaming responses | Real-time typing effect |
| P1 | Quiz assistance | Help with quiz questions |
| P2 | Code block explanation | Better code explanation UI |
| P2 | Learning analytics | Track chatbot usage |

### 8.2 Performance Optimization

- Implement response caching
- Add rate limiting
- Optimize prompt size
- Monitor API latency

### 8.3 Monitoring

- Add error tracking (Sentry)
- Add analytics (user actions)
- Log chatbot interactions
- Monitor LLM API costs

---

## 9. Resources & References

### 9.1 Documentation

- [LangServe Documentation](https://python.langchain.com/docs/langserve)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js App Router](https://nextjs.org/docs/app)

### 9.2 Examples

- LangServe examples: https://github.com/langchain-ai/langserve
- Next.js + FastAPI: https://github.com/tiangolo/fastapi/discussions/9205

---

**Plan Created**: 2026-02-15
**Author**: Claude Code
**Project**: Maguru Learning Platform
**Integration**: LangServe Backend + Next.js Frontend
