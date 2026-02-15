# Frontend Project Analysis - Maguru Learning Platform

## Executive Summary

**Project**: Maguru E-Learning Platform Frontend
**Framework**: Next.js 15.5.3 (App Router) + React 19
**Target Pages**: Course & Learn (Learning Mode) for Chatbot Integration
**Analysis Date**: 2026-02-15

---

## 1. Project Architecture Overview

### 1.1 Tech Stack
| Component | Technology | Version | Purpose |
|-----------|------------|----------|---------|
| **Framework** | Next.js | 15.5.3 | React framework with App Router |
| **UI Library** | React | 19.1.1 | Core UI rendering |
| **Styling** | TailwindCSS | 4.1.13 | Utility-first CSS |
| **Components** | shadcn/ui | @radix-ui | UI component library |
| **Icons** | lucide-react | ^0.554.0 | Icon set |
| **Markdown** | react-markdown | ^10.1.0 | Content rendering |
| **State** | React Hooks | - | Client-side state |
| **TypeScript** | TypeScript | ^5.9.2 | Type safety |

### 1.2 Project Structure
```
maguru/
├── app/                          # Next.js App Router
│   ├── api/                     # API Routes
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
```

---

## 2. Target Page Analysis: Learn Mode (`app/course/[slug]/learn/page.tsx`)

### 2.1 Page Structure
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
│  │          │  │                                     │  │
│  │          │  ├─────────────────────────────────────┤  │
│  │          │  │      Navigation Controls           │  │
│  └──────────┘  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Core Components Used

| Component | Purpose | Integration Point for Chatbot |
|-----------|---------|------------------------------|
| `CourseSidebar` | Course timeline navigation | **Potential chatbot-trigger location** |
| `ContentRenderer` | Markdown content display | **Primary chatbot context area** |
| `Progress` | Progress indicator | Can show chatbot-assisted progress |
| `Button` | Navigation controls | **Chatbot toggle button** |

### 2.3 State Management

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

### 2.4 Content Loading Flow

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
```

---

## 3. Key Data Structures

### 3.1 Course Types (`features/course/types/course.types.ts`)

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

### 3.2 API Endpoints

| Endpoint | Method | Purpose |
|-----------|---------|---------|
| `/api/courses` | GET | List all courses |
| `/api/courses/[slug]` | GET | Get course details + progress |
| `/api/courses/[slug]/content` | POST | Get markdown content by path |

---

## 4. Integration Points for Chatbot

### 4.1 Optimal Integration Locations

#### Location A: Content Area (Primary)
**Position**: Right side or bottom of content area
**Rationale**: Direct context awareness of current lesson content
**Implementation**:
```tsx
<div className="lg:col-span-3 relative">
  {/* Existing Content */}
  <ContentRenderer content={content} />

  {/* Chatbot Integration Point */}
  <ChatbotAssistant
    courseId={slug}
    currentSectionId={currentSectionId}
    currentItemId={currentItemId}
    content={content}
  />
</div>
```

#### Location B: Floating Action Button
**Position**: Fixed position (bottom-right)
**Rationale**: Always accessible without cluttering content
**Implementation**:
```tsx
<ChatbotFab
  onClick={toggleChatbot}
  context={{ slug, sectionId: currentSectionId, itemId: currentItemId }}
/>
```

#### Location C: Sidebar Enhancement
**Position**: Within CourseSidebar as expandable section
**Rationale**: Natural course navigation flow integration
**Implementation**:
```tsx
<Sidebar>
  {/* Existing timeline */}
  <ChatbotSection
    active={chatbotOpen}
    onToggle={toggleChatbot}
  />
</Sidebar>
```

### 4.2 Context Data Available for Chatbot

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

## 5. API Integration Strategy for Chatbot

### 5.1 Recommended API Structure

```typescript
// Chatbot API Endpoints to create:
POST /api/chatbot/query
{
  "courseSlug": "python-basics",
  "sectionId": "section-01",
  "itemId": "01-introduction",
  "content": "...markdown content...",
  "query": "What is Python?"
  "history": [...]
}
→ Response: { "answer": "...", "context": {...} }

POST /api/chatbot/stream
{
  "sessionId": "...",
  "query": "..."
}
→ Response: Server-Sent Events (SSE) stream
```

### 5.2 Integration with Existing API Pattern

The existing API follows Next.js App Router conventions:
- Route handlers in `app/api/`
- JSON responses with `NextResponse.json()`
- Error handling with status codes

Chatbot API should follow the same pattern for consistency.

---

## 6. UI/UX Design Considerations

### 6.1 Current Theme: Ancient Fantasy Asia

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

### 6.2 Chatbot UI Recommendations

1. **Match Theme**: Use consistent colors and styling
2. **Glass Effect**: Implement frosted glass chat interface
3. **Smooth Animations**: Use existing animation patterns
4. **Responsive**: Collapsible on mobile, persistent on desktop

---

## 7. Technical Constraints & Considerations

### 7.1 Client-Side Only
The learn page is a client component (`'use client'`), meaning:
- ✅ Can use browser APIs (localStorage, IndexedDB)
- ✅ Real-time interactions possible
- ⚠️ API calls from client only (no server actions directly)

### 7.2 Content Security
- Path validation prevents directory traversal
- Content is markdown-based (safe rendering)
- No user-generated content injection currently

### 7.3 Progress Tracking
- Stored in localStorage: `maguru_course_progress`
- Can be enhanced with chatbot interaction tracking

### 7.4 Performance Considerations
- Content is loaded on-demand per item
- Markdown parsing happens client-side
- Progressive loading with skeleton states

---

## 8. Recommendations for Chatbot Implementation

### 8.1 Immediate Integration Steps

1. **Create Chatbot Component**
   - Location: `features/course/components/ChatbotAssistant.tsx`
   - Use existing UI components (Button, Dialog, Sheet)

2. **Add Chatbot Context Provider**
   - Wrap the learning mode content
   - Provide course context to chatbot

3. **Implement Chatbot Toggle**
   - Floating action button (FAB) with icon
   - Slide-in panel using Sheet component

4. **API Integration**
   - Create `/api/chatbot/query` endpoint
   - Connect chatbot component to backend

### 8.2 Feature Enhancements

| Priority | Feature | Description |
|----------|----------|-------------|
| **P0** | Context-aware Q&A | Chatbot answers based on current lesson |
| **P0** | Progress tracking | Track chatbot-assisted learning |
| **P1** | Hint system | Contextual hints for exercises |
| **P1** | Code explanation | Python code explanations in chatbot |
| **P2** | Quiz assistance | Help with quiz questions |
| **P2** | Learning recommendations | Suggest next topics |

### 8.3 Code Integration Example

```tsx
// features/course/components/ChatbotAssistant.tsx
'use client'

import { useState } from 'react'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { MessageCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { ChatbotContext } from './ChatbotContext'

export function ChatbotAssistant({
  courseId,
  sectionId,
  itemId,
  content
}: ChatbotContext) {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([])

  const handleQuery = async (query: string) => {
    // API call to chatbot backend
    const response = await fetch('/api/chatbot/query', {
      method: 'POST',
      body: JSON.stringify({
        courseId, sectionId, itemId, content, query
      })
    })
    // Handle response...
  }

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button className="fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg">
          <MessageCircle className="h-6 w-6" />
        </Button>
      </SheetTrigger>
      <SheetContent className="w-full sm:w-[500px]">
        <ChatInterface messages={messages} onSend={handleQuery} />
      </SheetContent>
    </Sheet>
  )
}
```

---

## 9. Testing Considerations

### 9.1 Unit Tests
- Chatbot component rendering
- Context passing correctness
- API integration mocking

### 9.2 Integration Tests
- End-to-end chatbot flow
- Context accuracy across course navigation
- Progress tracking with chatbot

### 9.3 E2E Tests (Playwright)
- User opens chatbot → asks question → receives answer
- Chatbot context updates on navigation
- Chatbot persists across item changes

---

## 10. Summary

### Key Takeaways

1. **Architecture**: Clean feature-based architecture with clear separation
2. **Target Page**: `app/course/[slug]/learn/page.tsx` is ideal for chatbot integration
3. **Context Available**: Full course, section, item, and content data accessible
4. **Integration Points**: Multiple viable locations (content area, FAB, sidebar)
5. **API Pattern**: Consistent with existing Next.js API routes
6. **Design System**: Ancient Fantasy Asia theme to maintain consistency

### Next Steps

1. Design chatbot UI matching the theme
2. Create chatbot API endpoint
3. Implement chatbot component
4. Integrate with learn page
5. Test context accuracy and responsiveness
6. Deploy and monitor usage

---

**Analysis Completed**: 2026-02-15
**Project**: Maguru Learning Platform
**Target**: Course & Learn Mode for AI Chatbot Integration
