# Frontend Project Analysis - Maguru Learning Platform

## Executive Summary

**Project**: Maguru E-Learning Platform Frontend
**Framework**: Next.js 15.5.3 (App Router) + React 19
**Backend**: LangChain LCEL with LangServe API
**Target Pages**: Course & Learn (Learning Mode) for Chatbot Integration
**Analysis Date**: 2026-02-15

---

## 1. Project Architecture Overview

### 1.1 Tech Stack
| Component | Technology | Version | Purpose |
|-----------|------------|----------|---------|
| **Frontend Framework** | Next.js | 15.5.3 | React framework with App Router |
| **UI Library** | React | 19.1.1 | Core UI rendering |
| **Styling** | TailwindCSS | 4.1.13 | Utility-first CSS |
| **Components** | shadcn/ui | @radix-ui | UI component library |
| **Icons** | lucide-react | ^0.554.0 | Icon set |
| **Markdown** | react-markdown | ^10.1.0 | Content rendering |
| **State** | React Hooks | - | Client-side state |
| **TypeScript** | TypeScript | ^5.9.2 | Type safety |
| **Backend Framework** | Python | 3.x+ | AI Chain implementation |
| **AI Framework** | LangChain | LCEL | LangChain Expression Language |
| **AI API** | LangServe | latest | REST API for chains |
| **LLM Provider** | OpenRouter/Z.AI | - | AI Model provider |

### 1.2 Project Structure
```
maguru/                              # Next.js Frontend
├── app/                          # Next.js App Router
│   ├── api/                     # API Routes (courses only)
│   │   └── courses/
│   │       ├── route.ts          # GET /api/courses (list)
│   │       └── [slug]/
│   │           ├── route.ts      # GET /api/courses/:slug (detail)
│   │           └── content/
│   │               └── route.ts # POST /api/courses/:slug/content
│   └── course/
│       ├── page.tsx             # Course listing page
│       └── [slug]/
│           ├── page.tsx         # Course detail (Overview + Timeline)
│           └── learn/
│               └── page.tsx     # Learning mode (TARGET FOR CHATBOT)
│
├── features/                     # Feature-based modules
│   └── course/
│       ├── components/          # UI Components
│       │   ├── ContentRenderer.tsx
│       │   ├── CourseHeader.tsx
│       │   ├── CourseSidebar.tsx
│       │   └── Sidebar/       # Sidebar sub-components
│       ├── hooks/              # Custom React Hooks
│       │   ├── useCourse.ts
│       │   └── useCopyCode.ts
│       ├── lib/                # Utilities
│       │   └── courseUtils.ts
│       ├── types/              # TypeScript Definitions
│       │   └── course.types.ts
│       └── api.ts              # Client-side API functions
│
├── components/                  # Shared UI Components
│   └── ui/                   # shadcn/ui components
│       ├── button.tsx
│       ├── sidebar.tsx
│       ├── progress.tsx
│       ├── dialog.tsx
│       └── ...
│
└── docs/                       # Course content storage
    └── course/                # Markdown course files


maguru-model/                         # Backend (Python)
├── ai_chains/                   # AI Chain Implementations
│   ├── chains/
│   │   ├── qa_chatbot.py       # Q&A Chain
│   │   ├── explain_code.py     # Code Explanation Chain
│   │   ├── hint_generator.py   # Hint Generator Chain
│   │   ├── quiz_feedback.py    # Quiz Feedback Chain
│   │   └── ai_greeting.py      # Greeting Chain
│   ├── prompts/                 # Prompt Templates (YAML)
│   └── __init__.py              # LLM Configuration
│
├── app.py                       # Streamlit UI (legacy)
├── server.py                    # LangServe Server (TO CREATE)
├── requirements.txt              # Python Dependencies
└── docs/
    ├── frontend.md               # This file
    └── plan.md                 # Implementation Plan
```

---

## 2. Backend: LangServe Integration

### 2.1 LangServe Overview

**LangServe** adalah tool resmi LangChain untuk men-deploy chain sebagai REST API.

**Kelebihan LangServe**:
- ✅ **Otomatis**: Tidak perlu tulis endpoint manual
- ✅ **Type-Safe**: Input/output types otomatis dari signature fungsi
- ✅ **Streaming Support**: Bisa stream response untuk UX yang lebih baik
- ✅ **Documentation**: API docs otomatis di `/docs`
- ✅ **Batch Support**: Bisa proses banyak request sekaligus

### 2.2 AI Chains Available

| Chain | File | Purpose | Input | Output |
|--------|-------|---------|--------|--------|
| **qa_chatbot** | `qa_chatbot.py` | Q&A with context | question, session_title, session_content, chat_history | str (jawaban) |
| **explain_code** | `explain_code.py` | Code explanation | code_snippet | str (penjelasan) |
| **hint_generator** | `hint_generator.py` | Progressive hints | task, attempt, level | str (hint) |
| **quiz_feedback** | `quiz_feedback.py` | Quiz feedback | question, student_answer, correct_answer, is_correct | str (feedback) |
| **ai_greeting** | `ai_greeting.py` | Personalized greeting | student_name, course_metadata | str (greeting) |

### 2.3 LangServe Endpoint Structure

Setelah LangServe berjalan, endpoints akan otomatis dibuat:

| Chain | Endpoint URL | Method | Input Format | Output Format |
|--------|--------------|---------|--------------|---------------|
| qa_chatbot | `/chatbot/invoke` | POST | `{ "input": {...} }` | `{ "output": "..." }` |
| qa_chatbot | `/chatbot/stream` | POST | `{ "input": {...} }` | SSE stream |
| explain_code | `/explain-code/invoke` | POST | `{ "input": {...} }` | `{ "output": "..." }` |
| hint_generator | `/hint/invoke` | POST | `{ "input": {...} }` | `{ "output": "..." }` |
| quiz_feedback | `/quiz-feedback/invoke` | POST | `{ "input": {...} }` | `{ "output": "..." }` |

---

## 3. Target Page Analysis: Learn Mode (`app/course/[slug]/learn/page.tsx`)

### 3.1 Page Structure

The Learning Mode page is a client-side component (`'use client'`) designed for immersive learning experience.

**Key Layout**:
```
┌─────────────────────────────────────────────────────────────┐
│                     Learning Mode                         │
│  ┌──────────┐  ┌─────────────────────────────────────┐  │
│  │          │  │      Mobile Navigation Bar          │  │
│  │  Sidebar │  ├─────────────────────────────────────┤  │
│  │ (Desktop)│  │      Content Header              │  │
│  │          │  ├─────────────────────────────────────┤  │
│  │          │  │                                     │  │
│  │  Course  │  │      Content Renderer               │  │
│  │ Timeline │  │      (Markdown Content)            │  │
│  │          │  │                                     │  │
│  │          │  │      [CHATBOT FAB]               │  │
│  │          │  ├─────────────────────────────────────┤  │
│  │          │  │      Navigation Controls           │  │
│  └──────────┘  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Core Components Used

| Component | Purpose | Integration Point for Chatbot |
|-----------|---------|------------------------------|
| `CourseSidebar` | Course timeline navigation | **Potential chatbot-trigger location** |
| `ContentRenderer` | Markdown content display | **Primary chatbot context area** |
| `Progress` | Progress indicator | Can show chatbot-assisted progress |
| `Button` | Navigation controls | **Chatbot toggle button** |

### 3.3 State Management

The page uses `useCourse` hook which provides:

```typescript
interface UseCourseReturn {
  // Data
  course: Course | null
  progress: CourseProgress | undefined
  loading: boolean
  error: string | null

  // Current State
  currentSectionId: string
  currentItemId: string
  currentContentPath: string

  // Navigation Actions
  navigateToItem: (sectionId, itemId) => void
  navigateToNextItem: () => void
  navigateToPreviousItem: () => void
  markCurrentItemCompleted: () => void

  // Helpers
  getNavigationInfo: () => NavigationInfo
  isCompleted: boolean
  completionPercentage: number
}
```

### 3.4 Content Loading Flow

```
User visits /course/[slug]/learn
  ↓
useCourse hook loads course data via getCourse(slug)
  ↓
Current item selected (from progress or default)
  ↓
useEffect triggers on item change
  ↓
getCourseContent(slug, currentContentPath) loads markdown
  ↓
ContentRenderer displays markdown content
  ↓
[USER CLICKS CHATBOT]
  ↓
Chatbot sends request to LangServe API
  ↓
AI processes with LangChain
  ↓
Response displayed in chatbot UI
```

---

## 4. Key Data Structures

### 4.1 Course Types (`features/course/types/course.types.ts`)

```typescript
interface Course {
  slug: string
  metadata: CourseMetadata
  sections: CourseSection[]
  totalItems: number
  estimatedDuration: string
  overviewContent?: string
}

interface CourseSection {
  id: string
  title: string
  description?: string
  order: number
  items: CourseItem[]
}

interface CourseItem {
  id: string
  title: string
  description?: string
  contentPath: string        // Path to markdown file
  contentType: 'markdown' | 'video' | 'quiz' | 'exercise'
  order: number
  duration?: string
  isOptional?: boolean
}

interface CourseProgress {
  courseId: string
  completedItems: string[]
  currentSectionId?: string
  currentItemId?: string
  lastAccessedAt: string
  completionPercentage: number
  isCompleted: boolean
  completedAt?: string
}
```

### 4.2 Existing Frontend API Endpoints

| Endpoint | Method | Purpose |
|-----------|---------|---------|
| `/api/courses` | GET | List all courses |
| `/api/courses/[slug]` | GET | Get course details + progress |
| `/api/courses/[slug]/content` | POST | Get markdown content by path |

### 4.3 LangServe API Endpoints (to create)

| Endpoint | Method | Purpose |
|-----------|---------|---------|
| `/chatbot/invoke` | POST | Q&A with context |
| `/chatbot/stream` | POST | Streaming Q&A |
| `/explain-code/invoke` | POST | Code explanation |
| `/hint/invoke` | POST | Progressive hints |
| `/quiz-feedback/invoke` | POST | Quiz feedback |

---

## 5. Integration Points for Chatbot

### 5.1 Optimal Integration Locations

#### Location A: Floating Action Button (Recommended) ⭐

**Position**: Fixed position (bottom-right)
**Rationale**: Always accessible without cluttering content
**Implementation**:
```tsx
<ChatbotFab
  onClick={toggleChatbot}
  context={{ slug, sectionId: currentSectionId, itemId: currentItemId }}
/>
```

#### Location B: Content Area (Alternative)

**Position**: Right side or bottom of content area
**Rationale**: Direct context awareness of current lesson content

#### Location C: Sidebar Enhancement (Alternative)

**Position**: Within CourseSidebar as expandable section
**Rationale**: Natural course navigation flow integration

### 5.2 Context Data Available for Chatbot

```typescript
interface ChatbotContext {
  // Course Information
  courseId: string              // course slug
  courseMetadata: CourseMetadata  // title, level, tags

  // Current Position
  sectionId: string
  itemId: string
  itemTitle: string

  // Content
  currentContent: string        // Full markdown content

  // Progress
  completedItems: string[]
  progressPercentage: number
  isCompleted: boolean
}
```

---

## 6. Frontend-Backend Connection Strategy

### 6.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Maguru Platform                           │
├─────────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────┐      ┌─────────────────────────┐ │
│  │   Next.js Frontend    │      │   Python Backend       │ │
│  │   (port 3000)         │      │   (port 8000)         │ │
│  │                        │      │                        │ │
│  │  ┌─────────────────┐   │      │  ┌─────────────────┐   │ │
│  │  │  Learn Page    │   │      │  │  LangServe      │   │ │
│  │  │  + Chatbot UI  │   │      │  │  Server         │   │ │
│  │  │                │   │      │  │                │   │ │
│  │  │  fetch() ──────┼───┼─────►│  /chatbot/invoke│   │ │
│  │  │                │   │      │  │                │   │ │
│  │  │  LangChain Client│  │      │  │  ┌───────────┐  │   │ │
│  │  └─────────────────┘   │      │  │  │AI Chains │  │   │ │
│  │                        │      │  │  │           │  │   │ │
│  └─────────────────────────┘      │  │  │ qa_chatbot│  │   │ │
│                                  │  │  │ explain   │  │   │ │
│                                  │  │  │ _code     │  │   │ │
│                                  │  │  │ hint_     │  │   │ │
│                                  │  │  │ generator │  │   │ │
│                                  │  │  └───────────┘  │   │ │
│                                  │  └─────────────────┘   │ │
│                                  └─────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Frontend API Client

**Location**: `maguru/lib/ai-api.ts`

```typescript
// LangServe API Configuration
const LANGSERVE_BASE_URL = process.env.NEXT_PUBLIC_LANGSERVE_URL || 'http://localhost:8000'

// Q&A Chatbot
export interface ChatbotRequest {
  question: string
  session_title: string
  session_content: string
  chat_history: Array<{role: string, content: string}>
}

export interface ChatbotResponse {
  output: string
}

export async function queryChatbot(request: ChatbotRequest): Promise<ChatbotResponse> {
  const response = await fetch(`${LANGSERVE_BASE_URL}/chatbot/invoke`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ input: request })
  })

  if (!response.ok) {
    throw new Error('Chatbot API error')
  }

  return response.json()
}

// Streaming version (optional)
export async function streamChatbot(request: ChatbotRequest): Promise<ReadableStream> {
  const response = await fetch(`${LANGSERVE_BASE_URL}/chatbot/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ input: request })
  })

  if (!response.ok) {
    throw new Error('Chatbot streaming error')
  }

  return response.body!
}
```

---

## 7. UI/UX Design Considerations

### 7.1 Current Theme: Ancient Fantasy Asia

**Color Palette**:
- Primary: `beige-50` to `beige-900` (backgrounds, text)
- Accent: `kuning` (yellow), `hijau` (green), `merah` (red)
- Secondary: Various gradient overlays

**Typography**:
- Primary: Poppins (body text)
- Accent: Playfair Display (headings)

**Design Elements**:
- Glass panels with shadows
- Whimsical animations (bounce, scale)
- Nature motifs (emoji: 📚, 🎓)

### 7.2 Chatbot UI Recommendations

1. **Match Theme**: Use consistent colors and styling
2. **Glass Effect**: Implement frosted glass chat interface
3. **Smooth Animations**: Use existing animation patterns
4. **Responsive**: Collapsible on mobile, persistent on desktop
5. **Streaming UI**: Show typing indicator during AI response

---

## 8. Technical Constraints & Considerations

### 8.1 CORS Configuration

**LangServe perlu CORS enabled untuk Next.js**:

```python
# Di maguru-model/server.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://maguru.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 8.2 Environment Variables

**Required Variables**:

```bash
# Backend (maguru-model/.env)
OPENROUTER_API_KEY=sk-...
OPENROUTER_MODEL=google/gemma-7b-it
ZAI_API_KEY=sk-...
ZAI_MODEL=glm-4.7

# Frontend (maguru/.env.local)
NEXT_PUBLIC_LANGSERVE_URL=http://localhost:8000
```

### 8.3 Error Handling

**Frontend Error Handling**:
- Network errors: Retry with exponential backoff
- API errors: Show user-friendly message
- Timeout: Fallback to cached responses

**Backend Error Handling**:
- LLM API errors: Fallback to secondary provider
- Invalid input: Return specific error messages
- Rate limiting: Implement request throttling

---

## 9. Recommendations for Chatbot Implementation

### 9.1 Immediate Integration Steps

1. **Create LangServe Server** (`maguru-model/server.py`)
   - Install langserve
   - Import chains
   - Use `add_routes()` to expose chains

2. **Create Frontend API Client** (`maguru/lib/ai-api.ts`)
   - Implement queryChatbot function
   - Implement streaming version (optional)
   - Add error handling

3. **Create Chatbot Component** (`maguru/features/course/components/ChatbotAssistant.tsx`)
   - Use shadcn/ui Sheet component
   - Add floating action button
   - Implement chat interface

4. **Integrate to Learn Page**
   - Add ChatbotAssistant to learn page
   - Pass context (course, section, item, content)
   - Test integration

### 9.2 Feature Enhancements

| Priority | Feature | Description |
|----------|----------|-------------|
| **P0** | Context-aware Q&A | Chatbot answers based on current lesson |
| **P0** | Progress tracking | Track chatbot-assisted learning |
| **P1** | Hint system | Contextual hints for exercises |
| **P1** | Code explanation | Python code explanations in chatbot |
| **P1** | Streaming responses | Real-time typing effect |
| **P2** | Quiz assistance | Help with quiz questions |
| **P2** | Learning recommendations | Suggest next topics |

---

## 10. Deployment Strategy

### 10.1 Development Environment

```
Terminal 1 (Backend):
cd maguru-model
pip install -r requirements.txt langserve
python server.py
# Running on http://localhost:8000

Terminal 2 (Frontend):
cd ../maguru
npm run dev
# Running on http://localhost:3000
```

### 10.2 Production Deployment

| Component | Platform | URL | Notes |
|------------|----------|-----|-------|
| Frontend | Vercel | https://maguru.com | Add NEXT_PUBLIC_LANGSERVE_URL |
| Backend | Railway/Render | https://maguru-ai.railway.app | Configure CORS |

---

## 11. Summary

### Key Takeaways

1. **Architecture**: LangServe + Next.js is a clean, production-ready combination
2. **Backend**: AI chains are ready and functional
3. **Frontend**: Learn page is ideal for chatbot integration
4. **Integration**: LangServe provides automatic API generation
5. **Context Available**: Full course data can be passed to chatbot
6. **Design**: Ancient Fantasy Asia theme to maintain consistency

### Next Steps

See `docs/plan.md` for detailed implementation plan.

---

**Analysis Completed**: 2026-02-15
**Project**: Maguru Learning Platform
**Integration**: LangServe Backend + Next.js Frontend
