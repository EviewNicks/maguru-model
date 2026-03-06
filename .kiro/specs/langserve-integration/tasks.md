# Implementation Plan: LangServe Integration

## Overview

This implementation plan breaks down the integration of LangServe Backend with Next.js Frontend into discrete, executable tasks. Each task builds on previous work and includes specific requirements references. The plan follows a logical progression: backend setup → API client → UI components → integration → testing.

## Tasks

- [x] 1. Setup Backend Infrastructure
  - Create LangServe server with FastAPI
  - Configure CORS and environment
  - _Requirements: 1.1, 1.2, 1.3, 1.5, 12.1_

- [x] 1.1 Install Backend Dependencies
  - Add langserve, fastapi, uvicorn to requirements.txt
  - Install dependencies with pip
  - _Requirements: 1.1_

- [x] 1.2 Create LangServe Server File
  - Create `server.py` in project root
  - Initialize FastAPI application with title and description
  - Configure CORS middleware for localhost:3000
  - _Requirements: 1.2, 1.3_

- [x] 1.3 Create AI Chain Adapters
  - Create adapter functions for all 5 chains (qa_chatbot, explain_code, hint_generator, quiz_feedback, ai_greeting)
  - Wrap existing chain functions with RunnableLambda for LangServe compatibility
  - Handle input dictionary unpacking
  - _Requirements: 1.1, 1.4_

- [x] 1.4 Register Chain Routes
  - Use `add_routes()` to register all 5 chains
  - Verify `/invoke` and `/stream` endpoints are generated
  - Configure paths: /chatbot, /explain-code, /hint, /quiz-feedback, /greeting
  - _Requirements: 1.1, 1.4, 1.5_

- [x]* 1.5 Write Property Test for Endpoint Generation
  - **Property 1: All Chains Exposed as Endpoints**
  - **Validates: Requirements 1.1, 1.4**
  - Test that all 5 chains have both /invoke and /stream endpoints
  - Verify endpoints respond to POST requests

- [x] 1.6 Add Server Startup Script
  - Add `if __name__ == "__main__"` block
  - Configure uvicorn to run on 0.0.0.0:8000
  - Add reload option for development
  - _Requirements: 1.2_

- [x]* 1.7 Write Unit Tests for Server Configuration
  - Test CORS headers are present
  - Test server starts on correct port
  - Test /docs endpoint is accessible
  - _Requirements: 1.2, 1.3, 1.5_

- [x] 2. Implement Backend Input Validation and Error Handling
  - Add Pydantic models for input validation
  - Implement error handling for all chains
  - _Requirements: 2.2, 2.5, 3.2, 3.4, 4.2, 5.2, 6.2, 11.4_

- [x] 2.1 Create Pydantic Input Models
  - Define ChatbotInput, ExplainCodeInput, HintInput, QuizFeedbackInput, GreetingInput
  - Add field validation with Field() descriptors
  - Add constraints (e.g., hint level 1-3)
  - _Requirements: 2.2, 3.2, 4.2, 5.2, 6.2_

- [x]* 2.2 Write Property Test for Input Validation
  - **Property 2: Input Validation Consistency**
  - **Validates: Requirements 2.2, 2.5, 3.2, 4.2, 5.2, 6.2**
  - Test that valid inputs are accepted (200 response)
  - Test that missing required fields return 422 with details

- [x] 2.3 Implement LLM Provider Failover
  - Modify chain adapters to catch LLM provider errors
  - Add try-except blocks with fallback to secondary provider
  - Log provider failures
  - _Requirements: 11.4_

- [x]* 2.4 Write Unit Test for Provider Failover
  - Mock primary provider failure
  - Verify fallback provider is used
  - Verify response is still returned
  - _Requirements: 11.4_

- [x] 2.5 Add Error Event Handling for Streaming
  - Wrap streaming logic in try-except
  - Send error events in SSE format when errors occur
  - Ensure proper stream cleanup
  - _Requirements: 2.5, 13.4_

- [x]* 2.6 Write Property Test for Error Events
  - **Property 4: Error Event Transmission**
  - **Validates: Requirements 2.5, 11.3, 13.4**
  - Test that errors during streaming send error events
  - Verify SSE format is maintained

- [x] 3. Verify Backend Streaming Implementation
  - Test SSE format and streaming behavior
  - _Requirements: 2.3, 3.3, 9.1, 13.1, 13.2, 13.3, 13.5_

- [x]* 3.1 Write Property Test for Streaming Format
  - **Property 3: Streaming Response Format**
  - **Validates: Requirements 2.3, 3.3, 9.1, 9.2, 13.1, 13.2, 13.5**
  - Test that streaming endpoints return SSE format
  - Verify `data:` prefix on events
  - Verify Content-Type header is text/event-stream
  - Verify completion event is sent

- [x]* 3.2 Write Property Test for Context-Aware Responses
  - **Property 5: Context-Aware Responses**
  - **Validates: Requirements 2.1, 2.4, 6.3**
  - Test that responses reference session_content keywords
  - Test that chat_history context is maintained

- [x]* 3.3 Write Property Test for Hint Level Progression
  - **Property 6: Hint Level Progression**
  - **Validates: Requirements 4.1, 4.3**
  - Test that level 3 hints are longer than level 1
  - Test that specificity increases with level

- [x]* 3.4 Write Property Test for Multi-Language Code Support
  - **Property 7: Multi-Language Code Support**
  - **Validates: Requirements 3.1, 3.5**
  - Test code explanation for Python, JavaScript, Java
  - Verify non-empty explanations for all languages

- [x]* 3.5 Write Property Test for Feedback Generation
  - **Property 8: Feedback Generation Consistency**
  - **Validates: Requirements 5.1, 5.3**
  - Test feedback is generated for both correct and incorrect answers
  - Verify non-empty feedback in both cases

- [x]* 3.6 Write Property Test for Greeting Variation
  - **Property 9: Greeting Variation**
  - **Validates: Requirements 6.1, 6.5**
  - Test that multiple greeting requests produce different results
  - Verify at least 2 out of 3 greetings are unique

- [x] 4. Create Frontend API Client Library
  - Build TypeScript API client with streaming support
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 12.2_

- [x] 4.1 Create API Client File Structure
  - Create `lib/ai-api.ts` file
  - Define TypeScript interfaces for all request/response types
  - Add base URL configuration from environment variable
  - _Requirements: 7.1, 7.3, 12.2_

- [x] 4.2 Implement Streaming Helper Function
  - Create `streamResponse()` async generator function
  - Parse SSE format (data: prefix)
  - Handle stream completion ([DONE] event)
  - Decode chunks with TextDecoder
  - _Requirements: 7.2, 9.2_

- [x] 4.3 Implement Chatbot API Function
  - Create `streamChatbot()` async generator
  - Accept ChatbotRequest interface
  - Call /chatbot/stream endpoint
  - Yield response chunks
  - _Requirements: 2.1, 7.1, 7.2_

- [x] 4.4 Implement Other Chain API Functions
  - Create `streamExplainCode()` for code explanation
  - Create `streamHint()` for hint generation
  - Create `streamQuizFeedback()` for quiz feedback
  - Create `streamGreeting()` for greetings
  - _Requirements: 3.1, 4.1, 5.1, 6.1, 7.1, 7.2_

- [x] 4.5 Add Error Handling to API Client
  - Wrap fetch calls in try-catch
  - Throw descriptive errors for network failures
  - Handle HTTP error status codes
  - _Requirements: 7.4, 11.1, 11.2_

- [x]* 4.6 Write Property Test for API Client Streaming
  - **Property 12: API Client Streaming**
  - **Validates: Requirements 7.2, 9.1**
  - Test that API functions yield chunks incrementally
  - Verify AsyncGenerator behavior

- [x]* 4.7 Write Property Test for Network Error Handling
  - **Property 13: Network Error Handling**
  - **Validates: Requirements 7.4, 11.1, 11.2**
  - Test that network failures throw descriptive errors
  - Mock server unreachable, timeout scenarios

- [x] 5. Create Chatbot UI Components
  - Build React components for chatbot interface
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 9.1, 9.3, 9.4, 9.5_

- [x] 5.1 Create Chatbot Types File
  - Create `features/course/components/chatbot/types.ts`
  - Define ChatMessage, ChatbotContext interfaces
  - Export all types
  - _Requirements: 8.1_

- [x] 5.2 Create ChatMessage Component
  - Create `features/course/components/chatbot/ChatMessage.tsx`
  - Implement distinct styling for student vs AI messages
  - Add avatar/icons for each role
  - Add timestamp display
  - Integrate react-markdown for AI messages
  - _Requirements: 8.3, 8.5_

- [x]* 5.3 Write Property Test for Message Styling
  - **Property 14: Message Styling Distinction**
  - **Validates: Requirements 8.3**
  - Test that student and AI messages have different CSS classes
  - Verify visual distinction

- [x]* 5.4 Write Property Test for Markdown Rendering
  - **Property 15: Markdown Rendering**
  - **Validates: Requirements 8.5**
  - Test that markdown syntax is rendered as formatted content
  - Test bold, italic, code blocks, lists

- [x] 5.5 Create ChatbotAssistant Component
  - Create `features/course/components/chatbot/ChatbotAssistant.tsx`
  - Add component props interface (ChatbotContext)
  - Initialize state (isOpen, messages, input, isStreaming)
  - _Requirements: 8.1, 8.6_

- [x] 5.6 Implement Floating Action Button
  - Add FAB with fixed positioning (bottom-right)
  - Use shadcn/ui Button component
  - Add MessageCircle icon from lucide-react
  - Handle click to open Sheet
  - _Requirements: 8.1, 8.2_

- [x] 5.7 Implement Sheet Component
  - Use shadcn/ui Sheet component
  - Configure side="right" with appropriate width
  - Add SheetHeader with title
  - Add SheetContent with chat interface
  - _Requirements: 8.2_

- [x] 5.8 Implement Message List with ScrollArea
  - Use shadcn/ui ScrollArea component
  - Map over messages array
  - Render ChatMessage for each message
  - Add TypingIndicator when isStreaming
  - Auto-scroll to bottom on new messages
  - _Requirements: 8.3, 8.4, 9.4_

- [x] 5.9 Implement Input Area
  - Add Input component for message text
  - Add Send Button
  - Handle Enter key to send
  - Disable input while streaming
  - _Requirements: 8.2_

- [x] 5.10 Implement Message Sending Logic
  - Create handleSendMessage function
  - Add user message to state
  - Clear input field
  - Call streamChatbot API
  - Stream AI response incrementally
  - Update AI message content as chunks arrive
  - Handle streaming completion
  - _Requirements: 9.1, 9.5_

- [x]* 5.11 Write Property Test for Chat History Persistence
  - **Property 16: Chat History Persistence**
  - **Validates: Requirements 8.6, 14.5**
  - Test that messages persist after Sheet close/reopen
  - Verify state is maintained

- [x]* 5.12 Write Unit Tests for UI Interactions
  - Test FAB click opens Sheet
  - Test Sheet close button works
  - Test Enter key sends message
  - Test typing indicator appears during streaming
  - _Requirements: 8.2, 8.4, 9.4_

- [x] 5.13 Add Responsive Styling
  - Add mobile-specific styles
  - Make Sheet full-width on mobile
  - Adjust FAB size for mobile
  - Test at different viewport sizes
  - _Requirements: 8.7_

- [x] 5.14 Apply Ancient Fantasy Asia Theme
  - Use beige color palette
  - Add glass effect to Sheet
  - Use Poppins font
  - Add subtle animations
  - _Requirements: 8.8_

- [x] 6. Implement Course Context Integration
  - Pass course context to chatbot
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 6.1 Capture Course Context in ChatbotAssistant
  - Accept context props (courseId, sectionId, itemId, itemTitle, currentContent)
  - Store context in component state or ref
  - _Requirements: 10.1_

- [x] 6.2 Pass Context to API Requests
  - Include session_title (itemTitle) in chatbot requests
  - Include session_content (currentContent) in chatbot requests
  - Truncate session_content if too long (>1000 chars)
  - _Requirements: 10.2, 10.3, 10.4_

- [x]* 6.3 Write Property Test for Context Data Inclusion
  - **Property 17: Context Data Inclusion**
  - **Validates: Requirements 10.2, 10.3, 10.4**
  - Test that API requests include all context fields
  - Verify field values match props

- [x] 6.4 Implement Context Update on Navigation
  - Use useEffect to watch for prop changes
  - Update internal context when props change
  - Clear chat history on lesson change (optional)
  - _Requirements: 10.5_

- [x]* 6.5 Write Unit Test for Context Updates
  - Test that context updates when props change
  - Verify new context is used in next API request
  - _Requirements: 10.5_

- [x] 7. Implement Chat History Management
  - Manage chat history state and API passing
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [x] 7.1 Store Messages in Component State
  - Use useState for messages array
  - Add messages when user sends or AI responds
  - _Requirements: 14.1_

- [x] 7.2 Format Chat History for API
  - Create formatChatHistory helper function
  - Convert ChatMessage[] to {role, content}[] format
  - Limit to most recent 10 messages
  - _Requirements: 14.2, 14.3, 14.4_

- [x]* 7.3 Write Property Test for Chat History Truncation
  - **Property 18: Chat History Truncation**
  - **Validates: Requirements 14.2, 14.4**
  - Test that only last 10 messages are sent
  - Verify truncation with >10 messages

- [x]* 7.4 Write Property Test for Chat History Format
  - **Property 19: Chat History Format**
  - **Validates: Requirements 14.3**
  - Test that each message has role and content
  - Verify role is "student" or "ai"

- [x] 8. Implement Error Handling and Display
  - Add error states and user-friendly messages
  - _Requirements: 11.1, 11.2, 11.3, 11.5_

- [x] 8.1 Add Error State to ChatbotAssistant
  - Add error state variable
  - Create error display component
  - Show error messages in chat area
  - _Requirements: 11.1, 11.2, 11.3_

- [x] 8.2 Handle API Errors in Message Sending
  - Wrap API calls in try-catch
  - Set error state on failures
  - Display specific error messages (connection, timeout, validation)
  - Add retry button for recoverable errors
  - _Requirements: 11.1, 11.2, 11.3_

- [x] 8.3 Add Console Error Logging
  - Log all errors to console with context
  - Include error type, message, and stack trace
  - _Requirements: 11.5_

- [x]* 8.4 Write Property Test for Error Display
  - **Property 20: Error Message Display**
  - **Validates: Requirements 11.1, 11.2, 11.3**
  - Test that errors are displayed to user
  - Verify error messages are user-friendly

- [x]* 8.5 Write Property Test for Console Logging
  - **Property 21: Console Error Logging**
  - **Validates: Requirements 11.5**
  - Test that errors are logged to console
  - Verify log includes sufficient detail

- [x] 8.6 Handle Stream Interruption
  - Detect stream interruption (connection lost)
  - Display partial response received
  - Add "Connection lost" indicator
  - _Requirements: 9.3_

- [x]* 8.7 Write Unit Test for Stream Interruption
  - Mock stream interruption
  - Verify partial response is displayed
  - Verify error indicator appears
  - _Requirements: 9.3_

- [x] 9. Implement Accessibility Features
  - Add ARIA labels and keyboard support
  - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_

- [x] 9.1 Add Keyboard Accessibility to FAB
  - Ensure FAB is focusable
  - Add visible focus indicator
  - Support Enter/Space to activate
  - _Requirements: 15.1_

- [x] 9.2 Implement Focus Trap in Sheet
  -Use shadcn/ui Sheet's built-in focus trap
  - Verify focus stays within Sheet when open
  - _Requirements: 15.2_

- [x] 9.3 Add ARIA Labels to Interactive Elements
  - Add aria-label to FAB
  - Add aria-label to Send button
  - Add aria-label to Input field
  - Add aria-label to Close button
  - _Requirements: 15.3_

- [x]* 9.4 Write Property Test for ARIA Labels
  - **Property 22: ARIA Label Presence**
  - **Validates: Requirements 15.3**
  - Test that all interactive elements have ARIA labels
  - Verify accessibility attributes

- [x] 9.5 Add Screen Reader Announcements
  - Add aria-live region for new messages
  - Announce when Sheet opens
  - Announce when AI responds
  - _Requirements: 15.4_

- [x] 9.6 Implement Keyboard Shortcuts
  - Add Escape key to close Sheet
  - Add Enter key to send message
  - Document shortcuts in UI
  - _Requirements: 15.5_

- [x]* 9.7 Write Unit Tests for Keyboard Shortcuts
  -Test Escape closes Sheet
  - Test Enter sends message
  - Test Tab navigation
  - _Requirements: 15.5_

- [x] 10. Integrate Chatbot into Learn Page
  - Add ChatbotAssistant to Learn page
  - _Requirements: 8.1, 10.1, 10.2_

- [x] 10.1 Import ChatbotAssistant in Learn Page
  - Open `app/course/[slug]/learn/page.tsx`
  - Add import for ChatbotAssistant
  - _Requirements: 8.1_

- [x] 10.2 Add ChatbotAssistant to Page Layout
  - Place ChatbotAssistant component before closing div
  - Pass all required props from useCourse hook
  - Map course data to ChatbotContext props
  - _Requirements: 10.1, 10.2_

- [x] 10.3 Test Integration in Browser
  - Start backend server
  - Start frontend dev server
  - Navigate to Learn page
  - Verify FAB appears
  - Test opening chatbot
  - Test sending messages
  - _Requirements: 8.1, 8.2_

- [x] 11. Environment Configuration and Documentation
  - Setup environment variables and documentation
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [x] 11.1 Create Backend .env.example
  - Add OPENROUTER_API_KEY
  - Add OPENROUTER_MODEL
  - Add ZAI_API_KEY
  - Add ZAI_MODEL
  - Add HOST and PORT
  - Add ALLOWED_ORIGINS
  - _Requirements: 12.4_

- [x] 11.2 Create Frontend .env.local.example
  - Add NEXT_PUBLIC_LANGSERVE_URL
  - Document default value (http://localhost:8000)
  - _Requirements: 12.4_

- [x] 11.3 Add Environment Variable Validation
  - Check for required env vars on server startup
  - Display clear error messages if missing
  - Exit gracefully with instructions
  - _Requirements: 12.3_

- [x]* 11.4 Write Unit Test for Environment Validation
  - Test error messages when env vars missing
  - Verify clear instructions are provided
  - _Requirements: 12.3_

- [x] 11.5 Update README with Setup Instructions
  - Document all required environment variables
  - Add setup steps for backend
  - Add setup steps for frontend
  - Add troubleshooting section
  - _Requirements: 12.5_

- [] 12. Checkpoint - Integration Testing
  - Ensure all components work together end-to-end
  - _Requirements: All_

- [ ] 12.1 Test Complete User Flow
  - Start both servers
  - Navigate to Learn page
  - Open chatbot
  - Send question about current lesson
  - Verify streaming response
  - Send follow-up question
  - Verify chat history maintained
  - Navigate to different lesson
  - Verify context updates

- [ ] 12.2 Test All AI Chain Endpoints
  - Test Q&A chatbot with various questions
  - Test code explanation with code snippets
  - Test hint generator with different levels
  - Test quiz feedback with correct/incorrect answers
  - Test greeting generation

- [ ] 12.3 Test Error Scenarios
  - Test with backend server stopped
  - Test with invalid API key
  - Test with malformed requests
  - Test with network interruption
  - Verify error messages are user-friendly

- [ ] 12.4 Test Accessibility
  - Test keyboard navigation
  - Test with screen reader
  - Verify ARIA labels
  - Test focus management

- [ ] 12.5 Test Responsive Design
  - Test on desktop (1920x1080)
  - Test on tablet (768x1024)
  - Test on mobile (375x667)
  - Verify FAB and Sheet work on all sizes

- [ ] 13. Final Checkpoint - Code Review and Cleanup
  - Review all code for quality and consistency
  - _Requirements: All_

- [ ] 13.1 Review Backend Code
  - Check code style and formatting
  - Verify error handling is comprehensive
  - Ensure logging is appropriate
  - Remove debug code

- [ ] 13.2 Review Frontend Code
  - Check TypeScript types are correct
  - Verify component structure is clean
  - Ensure styling is consistent
  - Remove console.logs (except error logging)

- [ ] 13.3 Run All Tests
  - Run backend tests: `pytest`
  - Run frontend tests: `npm test`
  - Verify all tests pass
  - Check test coverage

- [ ] 13.4 Update Documentation
  - Ensure README is complete
  - Add inline code comments where needed
  - Document any known limitations
  - Add deployment notes (if applicable)

## Notes

- Tasks marked with `*` are optional test tasks that can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints (12, 13) ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The implementation follows a logical order: backend → API client → UI → integration
- All streaming functionality uses Server-Sent Events (SSE)
- All UI components use shadcn/ui for consistency
- Testing uses Jest + fast-check (frontend) and pytest + Hypothesis (backend)
