# Requirements Document

## Introduction

Dokumen ini mendefinisikan requirements untuk integrasi LangServe Backend dengan Next.js Frontend pada Maguru Learning Platform. Sistem ini akan menghubungkan AI chains yang sudah ada (berbasis LangChain) dengan antarmuka pengguna frontend melalui REST API menggunakan LangServe, dengan fokus pada chatbot assistance di halaman Learn Mode.

## Glossary

- **LangServe_Server**: FastAPI server yang mengekspos LangChain chains sebagai REST API endpoints
- **AI_Chain**: LangChain Expression Language (LCEL) chain yang memproses input dan menghasilkan AI response
- **Chatbot_UI**: React component yang menampilkan interface chat untuk interaksi user dengan AI
- **Learn_Page**: Halaman Next.js di `/course/[slug]/learn` tempat user belajar course content
- **Streaming_Response**: Server-Sent Events (SSE) yang mengirim AI response secara incremental
- **FAB**: Floating Action Button, tombol yang melayang di posisi fixed untuk membuka chatbot
- **Sheet_Component**: Sliding panel component dari shadcn/ui untuk menampilkan chat interface
- **Course_Context**: Data course yang sedang dipelajari (slug, section, item, content)
- **CORS**: Cross-Origin Resource Sharing, mekanisme untuk mengizinkan request dari domain berbeda

## Requirements

### Requirement 1: LangServe Server Setup

**User Story:** As a backend developer, I want to deploy AI chains as REST API endpoints, so that the frontend can consume AI services via HTTP requests.

#### Acceptance Criteria

1. THE LangServe_Server SHALL expose all five AI chains as REST API endpoints
2. WHEN the server starts, THE LangServe_Server SHALL listen on port 8000
3. THE LangServe_Server SHALL configure CORS to allow requests from localhost:3000
4. WHEN a chain is added, THE LangServe_Server SHALL automatically generate `/invoke` and `/stream` endpoints
5. THE LangServe_Server SHALL serve automatic API documentation at `/docs` endpoint

### Requirement 2: Q&A Chatbot API

**User Story:** As a student, I want to ask questions about the current lesson, so that I can get contextual help while learning.

#### Acceptance Criteria

1. WHEN a POST request is sent to `/chatbot/stream`, THE LangServe_Server SHALL process the question with course context
2. THE LangServe_Server SHALL accept input containing question, session_title, session_content, and chat_history
3. WHEN processing a question, THE LangServe_Server SHALL stream the AI response using Server-Sent Events
4. THE LangServe_Server SHALL maintain chat history context across multiple questions
5. IF the request is malformed, THEN THE LangServe_Server SHALL return a 422 error with validation details

### Requirement 3: Code Explanation API

**User Story:** As a student, I want to get explanations for code snippets in the lesson, so that I can understand programming concepts better.

#### Acceptance Criteria

1. WHEN a POST request is sent to `/explain-code/stream`, THE LangServe_Server SHALL analyze the provided code snippet
2. THE LangServe_Server SHALL accept input containing code_snippet as a string
3. THE LangServe_Server SHALL stream the code explanation response
4. WHEN the code snippet is empty, THE LangServe_Server SHALL return an error response
5. THE LangServe_Server SHALL handle code snippets in multiple programming languages

### Requirement 4: Hint Generator API

**User Story:** As a student, I want to receive progressive hints for exercises, so that I can solve problems independently without getting direct answers.

#### Acceptance Criteria

1. WHEN a POST request is sent to `/hint/stream`, THE LangServe_Server SHALL generate a hint based on the difficulty level
2. THE LangServe_Server SHALL accept input containing task, student_attempt, and level (1, 2, or 3)
3. THE LangServe_Server SHALL stream hints with increasing specificity based on level
4. WHEN level is 1, THE LangServe_Server SHALL provide subtle guidance
5. WHEN level is 3, THE LangServe_Server SHALL provide more direct hints

### Requirement 5: Quiz Feedback API

**User Story:** As a student, I want to receive personalized feedback on my quiz answers, so that I can learn from my mistakes.

#### Acceptance Criteria

1. WHEN a POST request is sent to `/quiz-feedback/stream`, THE LangServe_Server SHALL generate feedback for the student's answer
2. THE LangServe_Server SHALL accept input containing question, student_answer, correct_answer, and is_correct flag
3. THE LangServe_Server SHALL stream constructive feedback regardless of correctness
4. WHEN the answer is incorrect, THE LangServe_Server SHALL explain why and guide toward the correct answer
5. WHEN the answer is correct, THE LangServe_Server SHALL provide positive reinforcement

### Requirement 6: AI Greeting API

**User Story:** As a student, I want to receive a personalized greeting when I start learning, so that I feel welcomed and motivated.

#### Acceptance Criteria

1. WHEN a POST request is sent to `/greeting/stream`, THE LangServe_Server SHALL generate a personalized greeting
2. THE LangServe_Server SHALL accept input containing student_name and course_metadata
3. THE LangServe_Server SHALL stream a greeting that references the course context
4. THE LangServe_Server SHALL generate culturally appropriate greetings
5. THE LangServe_Server SHALL vary greeting messages to avoid repetition

### Requirement 7: Frontend API Client

**User Story:** As a frontend developer, I want a typed API client for LangServe endpoints, so that I can safely consume AI services with proper error handling.

#### Acceptance Criteria

1. THE API_Client SHALL provide TypeScript functions for all five AI chain endpoints
2. WHEN calling an API function, THE API_Client SHALL handle streaming responses using ReadableStream
3. THE API_Client SHALL use the NEXT_PUBLIC_LANGSERVE_URL environment variable for base URL
4. IF a network error occurs, THEN THE API_Client SHALL throw a descriptive error
5. THE API_Client SHALL include proper TypeScript types for all request and response payloads

### Requirement 8: Chatbot UI Component

**User Story:** As a student, I want an accessible chat interface on the Learn page, so that I can interact with the AI assistant while studying.

#### Acceptance Criteria

1. THE Chatbot_UI SHALL display as a Floating Action Button in the bottom-right corner
2. WHEN the FAB is clicked, THE Chatbot_UI SHALL open a Sheet_Component with chat interface
3. THE Chatbot_UI SHALL display chat messages with distinct styling for student and AI messages
4. WHEN the AI is responding, THE Chatbot_UI SHALL show a typing indicator
5. THE Chatbot_UI SHALL render AI responses with markdown formatting support
6. THE Chatbot_UI SHALL maintain chat history during the session
7. THE Chatbot_UI SHALL be responsive and work on mobile devices
8. THE Chatbot_UI SHALL match the Ancient Fantasy Asia theme of the platform

### Requirement 9: Streaming Response Handling

**User Story:** As a student, I want to see AI responses appear in real-time, so that I get immediate feedback without waiting for the complete response.

#### Acceptance Criteria

1. WHEN the AI generates a response, THE Chatbot_UI SHALL display text incrementally as it streams
2. THE Chatbot_UI SHALL handle Server-Sent Events from the LangServe streaming endpoints
3. IF the stream is interrupted, THEN THE Chatbot_UI SHALL display the partial response received
4. THE Chatbot_UI SHALL show a visual indicator while streaming is in progress
5. WHEN streaming completes, THE Chatbot_UI SHALL mark the message as complete

### Requirement 10: Course Context Integration

**User Story:** As a student, I want the chatbot to understand what lesson I'm currently studying, so that it provides relevant and contextual answers.

#### Acceptance Criteria

1. WHEN the chatbot is opened, THE Chatbot_UI SHALL capture the current Course_Context
2. THE Chatbot_UI SHALL pass courseId, sectionId, itemId, and currentContent to the API
3. WHEN sending a question, THE Chatbot_UI SHALL include the lesson title as session_title
4. THE Chatbot_UI SHALL include the markdown content as session_content
5. THE Chatbot_UI SHALL update context when the user navigates to a different lesson

### Requirement 11: Error Handling and Resilience

**User Story:** As a student, I want clear error messages when something goes wrong, so that I understand what happened and can try again.

#### Acceptance Criteria

1. IF the LangServe_Server is unreachable, THEN THE Chatbot_UI SHALL display a connection error message
2. IF an API request times out, THEN THE Chatbot_UI SHALL allow the user to retry
3. WHEN a validation error occurs, THE Chatbot_UI SHALL display the specific validation issue
4. IF the LLM provider fails, THEN THE LangServe_Server SHALL attempt to use the fallback provider
5. THE Chatbot_UI SHALL log errors to the browser console for debugging

### Requirement 12: Development Environment Configuration

**User Story:** As a developer, I want clear environment configuration, so that I can run the integrated system locally.

#### Acceptance Criteria

1. THE LangServe_Server SHALL read LLM API keys from environment variables
2. THE Frontend SHALL read the LangServe URL from NEXT_PUBLIC_LANGSERVE_URL
3. WHEN environment variables are missing, THE System SHALL display clear error messages
4. THE System SHALL provide example environment files (.env.example)
5. THE System SHALL document all required environment variables in README

### Requirement 13: API Response Format

**User Story:** As a frontend developer, I want consistent API response formats, so that I can reliably parse and display AI responses.

#### Acceptance Criteria

1. THE LangServe_Server SHALL return streaming responses in Server-Sent Events format
2. WHEN streaming, THE LangServe_Server SHALL send events with `data:` prefix
3. THE LangServe_Server SHALL send a final event to indicate stream completion
4. IF an error occurs during streaming, THEN THE LangServe_Server SHALL send an error event
5. THE LangServe_Server SHALL include proper Content-Type headers for streaming responses

### Requirement 14: Chat History Management

**User Story:** As a student, I want my conversation history preserved during a session, so that the AI can reference previous questions and answers.

#### Acceptance Criteria

1. THE Chatbot_UI SHALL store chat messages in component state
2. WHEN sending a new question, THE Chatbot_UI SHALL include previous messages as chat_history
3. THE Chatbot_UI SHALL format chat_history as an array of {role, content} objects
4. THE Chatbot_UI SHALL limit chat_history to the most recent 10 messages to avoid token limits
5. WHEN the Sheet_Component is closed, THE Chatbot_UI SHALL preserve chat history

### Requirement 15: UI Accessibility

**User Story:** As a student with accessibility needs, I want the chatbot interface to be keyboard navigable and screen reader friendly, so that I can use it effectively.

#### Acceptance Criteria

1. THE FAB SHALL be keyboard accessible with proper focus indicators
2. THE Sheet_Component SHALL trap focus when open
3. THE Chatbot_UI SHALL provide ARIA labels for all interactive elements
4. WHEN the Sheet opens, THE Chatbot_UI SHALL announce the change to screen readers
5. THE Chatbot_UI SHALL support keyboard shortcuts for common actions (Escape to close, Enter to send)
