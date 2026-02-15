# Design Document

## Overview

This document describes the design for integrating the LangChain-based AI backend with the Next.js frontend using LangServe. The integration enables real-time AI assistance for students through a chatbot interface on the Learn page, with support for five AI capabilities: Q&A chatbot, code explanation, hint generation, quiz feedback, and personalized greetings.

The design follows a client-server architecture where:
- **Backend**: Python FastAPI server using LangServe to expose LangChain chains as streaming REST APIs
- **Frontend**: Next.js React application with TypeScript, consuming the APIs through a custom client library
- **Communication**: HTTP/REST with Server-Sent Events (SSE) for streaming responses
- **UI Pattern**: Floating Action Button (FAB) that opens a Sheet component for chat interaction

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Maguru Learning Platform                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐         ┌──────────────────────────┐ │
│  │  Next.js Frontend    │         │  Python Backend          │ │
│  │  (Port 3000)         │         │  (Port 8000)             │ │
│  │                      │         │                          │ │
│  │  ┌────────────────┐  │         │  ┌────────────────────┐ │ │
│  │  │ Learn Page     │  │         │  │ LangServe Server   │ │ │
│  │  │                │  │         │  │                    │ │ │
│  │  │ ┌────────────┐ │  │         │  │ ┌──────────────┐  │ │ │
│  │  │ │ Chatbot UI │ │  │  HTTP   │  │ │ FastAPI App  │  │ │ │
│  │  │ │   (FAB +   │ │──┼────────►│  │ │   + CORS     │  │ │ │
│  │  │ │   Sheet)   │ │  │  SSE    │  │ └──────────────┘  │ │ │
│  │  │ └────────────┘ │  │         │  │         │         │ │ │
│  │  │                │  │         │  │         ▼         │ │ │
│  │  │ ┌────────────┐ │  │         │  │ ┌──────────────┐  │ │ │
│  │  │ │ API Client │ │  │         │  │ │ AI Chains    │  │ │ │
│  │  │ │ (ai-api.ts)│ │  │         │  │ │ - qa_chatbot │  │ │ │
│  │  │ └────────────┘ │  │         │  │ │ - explain    │  │ │ │
│  │  └────────────────┘  │         │  │ │ - hint       │  │ │ │
│  │                      │         │  │ │ - quiz       │  │ │ │
│  │                      │         │  │ │ - greeting   │  │ │ │
│  └──────────────────────┘         │  │ └──────────────┘  │ │ │
│                                   │  │         │         │ │ │
│                                   │  │         ▼         │ │ │
│                                   │  │ ┌──────────────┐  │ │ │
│                                   │  │ │ LLM Provider │  │ │ │
│                                   │  │ │ OpenRouter/  │  │ │ │
│                                   │  │ │ Z.AI         │  │ │ │
│                                   │  │ └──────────────┘  │ │ │
│                                   │  └────────────────────┘ │ │
│                                   └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Python 3.8+
- FastAPI (web framework)
- LangServe (chain deployment)
- LangChain (AI orchestration)
- Uvicorn (ASGI server)
- Pydantic (data validation)

**Frontend:**
- Next.js 15.5.3 (App Router)
- React 19
- TypeScript 5.9+
- shadcn/ui (UI components)
- TailwindCSS (styling)
- react-markdown (markdown rendering)

**Communication:**
- REST API (HTTP/HTTPS)
- Server-Sent Events (SSE) for streaming
- JSON for data serialization

## Components and Interfaces

### Backend Components

#### 1. LangServe Server (`server.py`)

The main FastAPI application that exposes AI chains as REST endpoints.

**Responsibilities:**
- Initialize FastAPI application
- Configure CORS middleware
- Register AI chain routes using `add_routes()`
- Start Uvicorn server on port 8000

**Key Functions:**
```python
def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Maguru AI API",
        description="LangServe API for Maguru Learning Platform",
        version="1.0.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

def register_chains(app: FastAPI) -> None:
    """Register all AI chains as LangServe routes."""
    # Each chain gets /invoke and /stream endpoints automatically
    add_routes(app, qa_chatbot_chain, path="/chatbot")
    add_routes(app, explain_code_chain, path="/explain-code")
    add_routes(app, hint_generator_chain, path="/hint")
    add_routes(app, quiz_feedback_chain, path="/quiz-feedback")
    add_routes(app, greeting_chain, path="/greeting")
```

**Endpoints Generated:**
- `/chatbot/invoke` - POST (non-streaming)
- `/chatbot/stream` - POST (streaming SSE)
- `/explain-code/invoke` - POST
- `/explain-code/stream` - POST
- `/hint/invoke` - POST
- `/hint/stream` - POST
- `/quiz-feedback/invoke` - POST
- `/quiz-feedback/stream` - POST
- `/greeting/invoke` - POST
- `/greeting/stream` - POST
- `/docs` - GET (automatic API documentation)

#### 2. AI Chain Adapters

Wrapper functions to make existing chains compatible with LangServe.

**Q&A Chatbot Adapter:**
```python
from langchain_core.runnables import RunnableLambda
from ai_chains.chains.qa_chatbot import answer_question

def create_qa_chatbot_chain():
    """Create LangServe-compatible Q&A chain."""
    def invoke(input_dict: dict) -> str:
        return answer_question(
            question=input_dict["question"],
            session_title=input_dict["session_title"],
            session_content=input_dict["session_content"],
            chat_history=input_dict.get("chat_history", [])
        )
    
    return RunnableLambda(invoke)
```

**Similar adapters for:**
- `create_explain_code_chain()`
- `create_hint_generator_chain()`
- `create_quiz_feedback_chain()`
- `create_greeting_chain()`

### Frontend Components

#### 1. API Client Library (`lib/ai-api.ts`)

TypeScript module providing typed functions for all LangServe endpoints.

**Core Functions:**
```typescript
// Base configuration
const LANGSERVE_BASE_URL = process.env.NEXT_PUBLIC_LANGSERVE_URL || 'http://localhost:8000'

// Streaming helper
async function* streamResponse(url: string, body: any): AsyncGenerator<string> {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ input: body })
  })
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }
  
  const reader = response.body!.getReader()
  const decoder = new TextDecoder()
  
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    
    const chunk = decoder.decode(value)
    const lines = chunk.split('\n')
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6)
        if (data === '[DONE]') return
        yield data
      }
    }
  }
}

// Q&A Chatbot
export async function* streamChatbot(request: ChatbotRequest): AsyncGenerator<string> {
  yield* streamResponse(`${LANGSERVE_BASE_URL}/chatbot/stream`, request)
}

// Code Explanation
export async function* streamExplainCode(codeSnippet: string): AsyncGenerator<string> {
  yield* streamResponse(`${LANGSERVE_BASE_URL}/explain-code/stream`, { code_snippet: codeSnippet })
}

// Hint Generator
export async function* streamHint(task: string, attempt: string, level: 1 | 2 | 3): AsyncGenerator<string> {
  yield* streamResponse(`${LANGSERVE_BASE_URL}/hint/stream`, { task, student_attempt: attempt, level })
}

// Quiz Feedback
export async function* streamQuizFeedback(
  question: string,
  studentAnswer: string,
  correctAnswer: string,
  isCorrect: boolean
): AsyncGenerator<string> {
  yield* streamResponse(`${LANGSERVE_BASE_URL}/quiz-feedback/stream`, {
    question,
    student_answer: studentAnswer,
    correct_answer: correctAnswer,
    is_correct: isCorrect
  })
}

// Greeting
export async function* streamGreeting(studentName: string, courseMetadata: any): AsyncGenerator<string> {
  yield* streamResponse(`${LANGSERVE_BASE_URL}/greeting/stream`, {
    student_name: studentName,
    course_metadata: courseMetadata
  })
}
```

#### 2. Chatbot UI Component (`features/course/components/chatbot/ChatbotAssistant.tsx`)

Main React component for the chatbot interface.

**Component Structure:**
```typescript
interface ChatbotAssistantProps {
  courseId: string
  sectionId: string
  itemId: string
  itemTitle: string
  currentContent: string
  completedItems: string[]
  progressPercentage: number
}

export function ChatbotAssistant(props: ChatbotAssistantProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  
  const handleSendMessage = async () => {
    // Add user message
    const userMessage: ChatMessage = {
      id: generateId(),
      role: 'student',
      content: input,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsStreaming(true)
    
    // Stream AI response
    const aiMessage: ChatMessage = {
      id: generateId(),
      role: 'ai',
      content: '',
      timestamp: new Date()
    }
    setMessages(prev => [...prev, aiMessage])
    
    try {
      for await (const chunk of streamChatbot({
        question: input,
        session_title: props.itemTitle,
        session_content: props.currentContent,
        chat_history: messages.slice(-10)
      })) {
        setMessages(prev => {
          const updated = [...prev]
          updated[updated.length - 1].content += chunk
          return updated
        })
      }
    } catch (error) {
      // Handle error
    } finally {
      setIsStreaming(false)
    }
  }
  
  return (
    <>
      {/* Floating Action Button */}
      <Button
        className="fixed bottom-6 right-6 rounded-full w-14 h-14"
        onClick={() => setIsOpen(true)}
      >
        <MessageCircle />
      </Button>
      
      {/* Sheet Component */}
      <Sheet open={isOpen} onOpenChange={setIsOpen}>
        <SheetContent side="right" className="w-full sm:w-[400px]">
          <SheetHeader>
            <SheetTitle>AI Assistant</SheetTitle>
          </SheetHeader>
          
          {/* Message List */}
          <ScrollArea className="flex-1 p-4">
            {messages.map(msg => (
              <ChatMessage key={msg.id} message={msg} />
            ))}
            {isStreaming && <TypingIndicator />}
          </ScrollArea>
          
          {/* Input Area */}
          <div className="p-4 border-t">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask a question..."
              disabled={isStreaming}
            />
            <Button onClick={handleSendMessage} disabled={isStreaming}>
              Send
            </Button>
          </div>
        </SheetContent>
      </Sheet>
    </>
  )
}
```

#### 3. Chat Message Component (`features/course/components/chatbot/ChatMessage.tsx`)

Component for rendering individual chat messages.

**Component Structure:**
```typescript
interface ChatMessageProps {
  message: ChatMessage
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isAI = message.role === 'ai'
  
  return (
    <div className={cn(
      "flex gap-3 mb-4",
      isAI ? "justify-start" : "justify-end"
    )}>
      {isAI && (
        <Avatar className="w-8 h-8">
          <Bot className="w-4 h-4" />
        </Avatar>
      )}
      
      <div className={cn(
        "rounded-lg p-3 max-w-[80%]",
        isAI ? "bg-beige-100" : "bg-kuning-100"
      )}>
        {isAI ? (
          <ReactMarkdown>{message.content}</ReactMarkdown>
        ) : (
          <p>{message.content}</p>
        )}
        <span className="text-xs text-beige-600 mt-1">
          {formatTime(message.timestamp)}
        </span>
      </div>
      
      {!isAI && (
        <Avatar className="w-8 h-8">
          <User className="w-4 h-4" />
        </Avatar>
      )}
    </div>
  )
}
```

## Data Models

### Backend Data Models

#### LangServe Input/Output Models

LangServe automatically generates Pydantic models from function signatures. For explicit typing:

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ChatMessage(BaseModel):
    """Chat message model."""
    role: str = Field(..., description="Message role: 'student' or 'ai'")
    content: str = Field(..., description="Message content")

class ChatbotInput(BaseModel):
    """Input for Q&A chatbot."""
    question: str = Field(..., description="Student's question")
    session_title: str = Field(..., description="Current lesson title")
    session_content: str = Field(..., description="Lesson markdown content")
    chat_history: List[ChatMessage] = Field(default_factory=list, description="Recent chat messages")

class ExplainCodeInput(BaseModel):
    """Input for code explanation."""
    code_snippet: str = Field(..., description="Code to explain")

class HintInput(BaseModel):
    """Input for hint generator."""
    task: str = Field(..., description="Exercise task description")
    student_attempt: str = Field(..., description="Student's current attempt")
    level: int = Field(..., ge=1, le=3, description="Hint level (1-3)")

class QuizFeedbackInput(BaseModel):
    """Input for quiz feedback."""
    question: str = Field(..., description="Quiz question")
    student_answer: str = Field(..., description="Student's answer")
    correct_answer: str = Field(..., description="Correct answer")
    is_correct: bool = Field(..., description="Whether answer is correct")

class GreetingInput(BaseModel):
    """Input for greeting generator."""
    student_name: str = Field(..., description="Student's name")
    course_metadata: Dict[str, Any] = Field(..., description="Course metadata")
```

### Frontend Data Models

#### TypeScript Interfaces

```typescript
// Chat message
export interface ChatMessage {
  id: string
  role: 'student' | 'ai'
  content: string
  timestamp: Date
}

// Chatbot context
export interface ChatbotContext {
  courseId: string
  sectionId: string
  itemId: string
  itemTitle: string
  currentContent: string
  completedItems: string[]
  progressPercentage: number
}

// API request types
export interface ChatbotRequest {
  question: string
  session_title: string
  session_content: string
  chat_history: Array<{
    role: string
    content: string
  }>
}

export interface ExplainCodeRequest {
  code_snippet: string
}

export interface HintRequest {
  task: string
  student_attempt: string
  level: 1 | 2 | 3
}

export interface QuizFeedbackRequest {
  question: string
  student_answer: string
  correct_answer: string
  is_correct: boolean
}

export interface GreetingRequest {
  student_name: string
  course_metadata: {
    title: string
    learning_objectives?: string[]
  }
}

// API response types
export interface StreamChunk {
  data: string
  done: boolean
}

export interface APIError {
  message: string
  status: number
  details?: any
}
```

### Environment Configuration

**Backend (`.env`):**
```bash
# LLM Provider Configuration
OPENROUTER_API_KEY=sk-...
OPENROUTER_MODEL=google/gemma-7b-it
ZAI_API_KEY=sk-...
ZAI_MODEL=glm-4.7

# Server Configuration
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000
```

**Frontend (`.env.local`):**
```bash
# LangServe API Configuration
NEXT_PUBLIC_LANGSERVE_URL=http://localhost:8000
```


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property Reflection

After analyzing all acceptance criteria, I identified several areas where properties can be consolidated:

**Consolidations Made:**
1. **Endpoint Generation**: Properties 1.1 and 1.4 both test that chains are exposed as endpoints. Combined into Property 1.
2. **Input Validation**: Multiple criteria (2.2, 3.2, 4.2, 5.2, 6.2) test input validation. Combined into Property 2.
3. **Streaming Format**: Criteria 2.3, 3.3, 9.1, 9.2, 13.1, 13.2 all test SSE streaming. Combined into Property 3.
4. **Error Responses**: Criteria 2.5, 11.3, 13.4 test error handling. Combined into Property 4.
5. **Context Passing**: Criteria 10.2, 10.3, 10.4 test context data passing. Combined into Property 5.
6. **Chat History**: Criteria 14.2, 14.3, 14.4 test history management. Combined into Property 6.

### Backend Properties

#### Property 1: All Chains Exposed as Endpoints

*For any* AI chain registered with LangServe, both `/invoke` and `/stream` endpoints should be automatically generated and accessible via HTTP POST requests.

**Validates: Requirements 1.1, 1.4**

#### Property 2: Input Validation Consistency

*For any* endpoint, when a request is sent with all required fields, it should be accepted (200/streaming response), and when required fields are missing, it should return a 422 validation error with details about the missing fields.

**Validates: Requirements 2.2, 2.5, 3.2, 4.2, 5.2, 6.2**

#### Property 3: Streaming Response Format

*For any* streaming endpoint (`/stream`), the response should use Server-Sent Events format with `data:` prefixed lines, proper `Content-Type: text/event-stream` header, and a completion event at the end.

**Validates: Requirements 2.3, 3.3, 9.1, 9.2, 13.1, 13.2, 13.5**

#### Property 4: Error Event Transmission

*For any* streaming request that encounters an error during processing, the server should send an error event in SSE format before closing the stream, rather than abruptly terminating the connection.

**Validates: Requirements 2.5, 11.3, 13.4**

#### Property 5: Context-Aware Responses

*For any* chatbot request with session_content containing specific keywords or concepts, the AI response should reference or relate to those concepts, demonstrating context awareness.

**Validates: Requirements 2.1, 2.4, 6.3**

#### Property 6: Hint Level Progression

*For any* task and student attempt, when requesting hints at levels 1, 2, and 3, the length and specificity of hints should increase monotonically (level 3 hint should be longer and more specific than level 1).

**Validates: Requirements 4.1, 4.3**

#### Property 7: Multi-Language Code Support

*For any* code snippet in a supported programming language (Python, JavaScript, Java, etc.), the explain-code endpoint should return a non-empty explanation without errors.

**Validates: Requirements 3.1, 3.5**

#### Property 8: Feedback Generation Consistency

*For any* quiz question with student answer and correct answer, feedback should be generated regardless of the is_correct flag value (both true and false should produce feedback).

**Validates: Requirements 5.1, 5.3**

#### Property 9: Greeting Variation

*For any* student name and course metadata, when requesting greetings multiple times (at least 3 times), at least 2 of the greetings should be different, demonstrating variety.

**Validates: Requirements 6.1, 6.5**

#### Property 10: CORS Header Presence

*For any* endpoint request from origin `http://localhost:3000`, the response should include `Access-Control-Allow-Origin` header with the correct origin value.

**Validates: Requirements 1.3**

#### Property 11: Provider Failover

*For any* chain invocation, if the primary LLM provider (OpenRouter) fails or is unavailable, the system should attempt to use the fallback provider (Z.AI) and return a response rather than failing completely.

**Validates: Requirements 11.4**

### Frontend Properties

#### Property 12: API Client Streaming

*For any* API client streaming function (streamChatbot, streamExplainCode, etc.), when called with valid input, it should yield string chunks incrementally via AsyncGenerator rather than returning all content at once.

**Validates: Requirements 7.2, 9.1**

#### Property 13: Network Error Handling

*For any* API client function, when the network request fails (server unreachable, timeout, etc.), it should throw an Error object with a descriptive message rather than silently failing or returning undefined.

**Validates: Requirements 7.4, 11.1, 11.2**

#### Property 14: Message Styling Distinction

*For any* chat message rendered in the UI, student messages and AI messages should have different CSS classes or styling attributes, making them visually distinguishable.

**Validates: Requirements 8.3**

#### Property 15: Markdown Rendering

*For any* AI message containing markdown syntax (bold, italic, code blocks, lists), the rendered output should display the formatted content rather than raw markdown syntax.

**Validates: Requirements 8.5**

#### Property 16: Chat History Persistence

*For any* sequence of messages sent during a session, all messages should remain in the UI state even after the Sheet component is closed and reopened, until the page is refreshed.

**Validates: Requirements 8.6, 14.5**

#### Property 17: Context Data Inclusion

*For any* chatbot API request sent from the UI, the request payload should include courseId, sectionId, itemId, session_title (lesson title), and session_content (markdown content) fields.

**Validates: Requirements 10.2, 10.3, 10.4**

#### Property 18: Chat History Truncation

*For any* chat history with more than 10 messages, when sending a new question, only the most recent 10 messages should be included in the chat_history field of the API request.

**Validates: Requirements 14.2, 14.4**

#### Property 19: Chat History Format

*For any* chat history sent to the API, each message should be formatted as an object with `role` (string) and `content` (string) properties, where role is either "student" or "ai".

**Validates: Requirements 14.3**

#### Property 20: Error Message Display

*For any* API error (validation error, network error, timeout), the Chatbot UI should display an error message to the user rather than silently failing or showing a blank state.

**Validates: Requirements 11.1, 11.2, 11.3**

#### Property 21: Console Error Logging

*For any* error that occurs in the Chatbot UI (API errors, rendering errors, etc.), an error message should be logged to the browser console with sufficient detail for debugging.

**Validates: Requirements 11.5**

#### Property 22: ARIA Label Presence

*For any* interactive element in the Chatbot UI (buttons, inputs, etc.), the element should have an `aria-label` or `aria-labelledby` attribute for screen reader accessibility.

**Validates: Requirements 15.3**

### Integration Properties

#### Property 23: End-to-End Streaming

*For any* question sent from the Chatbot UI, the response should appear incrementally in the UI as the backend streams it, rather than appearing all at once after the stream completes.

**Validates: Requirements 2.3, 9.1, 9.2**

#### Property 24: Context Update on Navigation

*For any* lesson navigation event (user moves to a different lesson), the Chatbot UI should update its internal context (itemId, itemTitle, currentContent) to reflect the new lesson before the next API request.

**Validates: Requirements 10.5**

### Edge Cases

The following edge cases should be handled by the property tests' input generators:

- **Empty Code Snippet** (3.4): Generator should include empty strings to verify error handling
- **Stream Interruption** (9.3): Test should simulate network interruption during streaming
- **Missing Environment Variables** (12.3): Test should verify error messages when env vars are missing
- **Empty Chat History** (2.4): Generator should include empty chat_history arrays

## Error Handling

### Backend Error Handling

**LLM Provider Errors:**
- Primary provider (OpenRouter) failure → Automatic fallback to Z.AI
- Both providers fail → Return user-friendly error message
- Timeout → Return partial response if available, otherwise error

**Input Validation Errors:**
- Missing required fields → 422 Unprocessable Entity with Pydantic validation details
- Invalid field types → 422 with type error details
- Out-of-range values (e.g., hint level > 3) → 422 with range error

**Streaming Errors:**
- Error during stream → Send error event in SSE format
- Connection lost → Log error, clean up resources
- Token limit exceeded → Truncate input, continue processing

**CORS Errors:**
- Request from unauthorized origin → 403 Forbidden
- Missing CORS headers → Automatic rejection by browser

### Frontend Error Handling

**Network Errors:**
- Server unreachable → Display "Cannot connect to AI server" message
- Timeout (>30s) → Display "Request timed out" with retry button
- 5xx errors → Display "Server error, please try again"

**API Errors:**
- 422 Validation → Display specific validation message
- 429 Rate Limit → Display "Too many requests, please wait"
- 401/403 Auth → Display "Authentication required"

**Streaming Errors:**
- Stream interrupted → Display partial response + "Connection lost" indicator
- Malformed SSE → Log error, display last valid chunk
- Empty stream → Display "No response received"

**UI Errors:**
- Component render error → Error boundary catches, displays fallback UI
- State update error → Log to console, attempt recovery
- Markdown parsing error → Display raw text as fallback

### Error Recovery Strategies

**Retry Logic:**
- Network errors: Exponential backoff (1s, 2s, 4s)
- Rate limits: Wait for specified duration
- Transient errors: Up to 3 retries

**Graceful Degradation:**
- LLM unavailable → Display cached responses or fallback messages
- Streaming fails → Fall back to non-streaming `/invoke` endpoint
- Markdown rendering fails → Display plain text

**User Communication:**
- All errors display user-friendly messages (no technical jargon)
- Provide actionable next steps (retry, refresh, contact support)
- Log technical details to console for developer debugging

## Testing Strategy

### Dual Testing Approach

This feature requires both unit tests and property-based tests:

**Unit Tests:**
- Specific examples demonstrating correct behavior
- Edge cases (empty inputs, boundary values)
- Error conditions (network failures, invalid inputs)
- Integration points between components
- UI interactions (button clicks, keyboard events)

**Property-Based Tests:**
- Universal properties across all inputs
- Comprehensive input coverage through randomization
- Invariants that must hold for all valid executions
- Minimum 100 iterations per property test

### Backend Testing

**Framework:** pytest + Hypothesis (property-based testing)

**Test Structure:**
```python
# Unit test example
def test_chatbot_endpoint_returns_200():
    """Test chatbot endpoint with valid input."""
    response = client.post("/chatbot/invoke", json={
        "input": {
            "question": "What is Python?",
            "session_title": "Introduction to Python",
            "session_content": "Python is a programming language...",
            "chat_history": []
        }
    })
    assert response.status_code == 200
    assert "output" in response.json()

# Property test example
@given(
    question=st.text(min_size=1),
    session_title=st.text(min_size=1),
    session_content=st.text(min_size=1),
    chat_history=st.lists(st.fixed_dictionaries({
        "role": st.sampled_from(["student", "ai"]),
        "content": st.text(min_size=1)
    }), max_size=10)
)
@settings(max_examples=100)
def test_property_chatbot_accepts_valid_input(question, session_title, session_content, chat_history):
    """Property: For any valid input, chatbot endpoint should return 200.
    
    Feature: langserve-integration, Property 2: Input Validation Consistency
    """
    response = client.post("/chatbot/invoke", json={
        "input": {
            "question": question,
            "session_title": session_title,
            "session_content": session_content,
            "chat_history": chat_history
        }
    })
    assert response.status_code == 200
```

**Test Coverage:**
- All 5 chain endpoints (invoke + stream)
- Input validation for each endpoint
- Streaming response format
- CORS headers
- Error handling
- Provider failover

### Frontend Testing

**Framework:** Jest + React Testing Library + fast-check (property-based testing)

**Test Structure:**
```typescript
// Unit test example
describe('ChatbotAssistant', () => {
  it('should open Sheet when FAB is clicked', () => {
    render(<ChatbotAssistant {...mockProps} />)
    const fab = screen.getByRole('button', { name: /open chat/i })
    fireEvent.click(fab)
    expect(screen.getByRole('dialog')).toBeInTheDocument()
  })
})

// Property test example
import fc from 'fast-check'

describe('Property: Message Styling Distinction', () => {
  it('should apply different styles to student and AI messages', () => {
    fc.assert(
      fc.property(
        fc.array(fc.record({
          id: fc.uuid(),
          role: fc.constantFrom('student', 'ai'),
          content: fc.string({ minLength: 1 }),
          timestamp: fc.date()
        }), { minLength: 1, maxLength: 20 }),
        (messages) => {
          const { container } = render(<MessageList messages={messages} />)
          
          const studentMessages = messages.filter(m => m.role === 'student')
          const aiMessages = messages.filter(m => m.role === 'ai')
          
          // Verify different styling
          const studentElements = container.querySelectorAll('[data-role="student"]')
          const aiElements = container.querySelectorAll('[data-role="ai"]')
          
          expect(studentElements.length).toBe(studentMessages.length)
          expect(aiElements.length).toBe(aiMessages.length)
          
          // Verify distinct CSS classes
          if (studentElements.length > 0 && aiElements.length > 0) {
            const studentClass = studentElements[0].className
            const aiClass = aiElements[0].className
            expect(studentClass).not.toBe(aiClass)
          }
        }
      ),
      { numRuns: 100 }
    )
  })
})
```

**Test Coverage:**
- API client functions (all 5 chains)
- Streaming response handling
- Error handling and display
- Chat message rendering
- Chat history management
- Context data passing
- UI interactions (FAB, Sheet, input)
- Accessibility (ARIA labels, keyboard navigation)

### Integration Testing

**End-to-End Flow:**
1. Start backend server
2. Start frontend dev server
3. Navigate to Learn page
4. Open chatbot
5. Send question
6. Verify streaming response appears
7. Verify chat history maintained
8. Test error scenarios

**Tools:**
- Backend: pytest with TestClient
- Frontend: Jest + Testing Library
- E2E: Manual testing (automated E2E out of scope for MVP)

### Test Execution

**Backend:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_chains --cov-report=html

# Run property tests only
pytest -m property

# Run specific test file
pytest tests/test_langserve_server.py
```

**Frontend:**
```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run property tests only
npm test -- --testNamePattern="Property:"

# Run specific test file
npm test -- ChatbotAssistant.test.tsx
```

### Property Test Configuration

All property tests must:
- Run minimum 100 iterations (configured in test settings)
- Include a comment tag referencing the design property
- Use smart generators that constrain to valid input space
- Test the property, not the implementation

**Tag Format:**
```python
# Python
"""Feature: langserve-integration, Property 1: All Chains Exposed as Endpoints"""

# TypeScript
// Feature: langserve-integration, Property 12: API Client Streaming
```
