# Requirements Document

## Introduction

This document specifies the requirements for the Maguru MVP Foundation - a complete foundational system for an AI-powered coding learning platform. The foundation includes core utilities for session management and content loading, AI capabilities for code explanation and student assistance, course content structure, and a multi-page Streamlit user interface with an interactive chatbot.

## Glossary

- **System**: The Maguru MVP Foundation application
- **Session_Manager**: Component responsible for managing user session state in Streamlit
- **Content_Loader**: Component responsible for loading course content from YAML and Markdown files
- **Quiz_Validator**: Component responsible for validating quiz answers and calculating scores
- **AI_Chain**: LangChain LCEL chain that processes AI requests
- **Chatbot**: Interactive Q&A component that assists students during learning
- **Course**: Top-level learning container with modules and sessions
- **Module**: Grouping of related learning sessions within a course
- **Session**: Individual learning unit with theory content and practice tasks
- **Quiz**: Assessment with multiple choice and code completion questions
- **Hint**: Progressive guidance provided to students (3 levels: gentle, conceptual, direct)

## Requirements

### Requirement 1: Session State Management

**User Story:** As a student, I want my learning progress to be tracked during my session, so that I can continue where I left off and see my quiz scores.

#### Acceptance Criteria

1. WHEN the application starts, THE System SHALL initialize session state with default values
2. WHEN a student completes a session, THE Session_Manager SHALL update the progress tracking
3. WHEN a student submits a quiz, THE Session_Manager SHALL save the quiz score with timestamp
4. WHEN a student sends a chat message, THE Session_Manager SHALL add the message to chat history
5. WHEN retrieving current session data, THE Session_Manager SHALL return the active course, module, and session information

### Requirement 2: Content Loading and Parsing

**User Story:** As a student, I want to access course materials and quizzes, so that I can learn Python programming concepts.

#### Acceptance Criteria

1. WHEN loading course metadata, THE Content_Loader SHALL parse the course YAML file and return structured data
2. WHEN loading module information, THE Content_Loader SHALL retrieve all modules for a given course
3. WHEN loading session content, THE Content_Loader SHALL parse Markdown files and return formatted content
4. WHEN loading quiz definitions, THE Content_Loader SHALL parse quiz YAML files with questions and answers
5. IF a content file is missing or malformed, THEN THE Content_Loader SHALL handle the error gracefully and return an appropriate error message
6. WHEN determining the next session, THE Content_Loader SHALL identify the subsequent session in the learning path

### Requirement 3: Quiz Validation and Scoring

**User Story:** As a student, I want my quiz answers to be validated accurately, so that I receive fair assessment and helpful feedback.

#### Acceptance Criteria

1. WHEN validating a multiple choice answer, THE Quiz_Validator SHALL compare the student's selection with the correct answer index
2. WHEN validating a code completion answer, THE Quiz_Validator SHALL check if the student's code matches the expected answer
3. WHEN calculating total score, THE Quiz_Validator SHALL sum the points from all correct answers
4. WHEN determining pass/fail status, THE Quiz_Validator SHALL check if the score is greater than or equal to 70%
5. WHEN identifying weak areas, THE Quiz_Validator SHALL analyze incorrect answers and map them to specific topics
6. WHEN generating feedback, THE Quiz_Validator SHALL provide detailed explanations for each question

### Requirement 4: AI Code Explanation

**User Story:** As a student, I want the AI to explain Python code to me in Indonesian, so that I can understand how the code works.

#### Acceptance Criteria

1. WHEN a student requests code explanation, THE AI_Chain SHALL generate a clear explanation in Indonesian language
2. WHEN explaining code, THE System SHALL describe what each line or block does
3. WHEN explaining code, THE System SHALL include common mistakes related to the concept
4. IF the code contains syntax errors, THEN THE System SHALL handle the error gracefully and provide guidance
5. WHEN generating explanations, THE System SHALL use analogies relevant to Indonesian students

### Requirement 5: Progressive Hint Generation

**User Story:** As a student, I want to receive progressive hints when I'm stuck, so that I can learn to solve problems without getting the direct answer immediately.

#### Acceptance Criteria

1. WHEN a student requests a Level 1 hint, THE System SHALL provide subtle guidance pointing toward the solution
2. WHEN a student requests a Level 2 hint, THE System SHALL explain the relevant concept with a similar example
3. WHEN a student requests a Level 3 hint, THE System SHALL show the approach with some missing pieces
4. WHEN generating hints, THE System SHALL maintain context from the current session
5. WHEN a student has already received a hint level, THE System SHALL remember this within the session

### Requirement 6: Quiz Feedback Generation

**User Story:** As a student, I want to receive detailed feedback on my quiz answers, so that I can learn from my mistakes and understand why answers are correct or incorrect.

#### Acceptance Criteria

1. WHEN a student answers correctly, THE System SHALL provide positive reinforcement and explain why the answer is correct
2. WHEN a student answers incorrectly, THE System SHALL gently correct the mistake and explain the misconception
3. WHEN providing feedback, THE System SHALL suggest related topics for review if needed
4. WHEN generating feedback, THE System SHALL use encouraging and supportive language in Indonesian
5. WHEN explaining incorrect answers, THE System SHALL show the correct answer with step-by-step explanation

### Requirement 7: Interactive Chatbot

**User Story:** As a student, I want to chat with an AI tutor during my learning session, so that I can ask questions and get immediate help.

#### Acceptance Criteria

1. WHEN a student sends a message, THE Chatbot SHALL generate a context-aware response based on the current session
2. WHEN maintaining conversation, THE Chatbot SHALL preserve chat history for natural dialogue flow
3. WHEN answering questions, THE Chatbot SHALL reference specific examples or explanations from the current session material
4. WHEN a student asks a follow-up question, THE Chatbot SHALL use previous conversation context to provide relevant answers
5. WHEN responding, THE Chatbot SHALL use friendly, encouraging, and patient tone in Indonesian language
6. WHEN chat history exceeds 10 messages, THE Chatbot SHALL maintain only the most recent 10 messages for context

### Requirement 8: Course Content Structure

**User Story:** As a content creator, I want course materials to be organized in a structured format, so that the system can load and display them correctly.

#### Acceptance Criteria

1. THE System SHALL support course metadata in YAML format with id, title, description, difficulty, and modules list
2. THE System SHALL support module metadata in YAML format with id, title, description, sessions list, and quiz reference
3. THE System SHALL support session content in Markdown format with learning objectives, concepts, examples, and practice tasks
4. THE System SHALL support quiz definitions in YAML format with questions, options, correct answers, points, and explanations
5. WHEN organizing content, THE System SHALL maintain a hierarchy of Course → Module → Session → Quiz

### Requirement 9: Multi-Page User Interface

**User Story:** As a student, I want to navigate between different pages of the application, so that I can select courses, learn content, take quizzes, and view my progress.

#### Acceptance Criteria

1. WHEN accessing the home page, THE System SHALL display available courses with title, description, and difficulty level
2. WHEN selecting a course, THE System SHALL navigate to the learning page for that course
3. WHEN on the learning page, THE System SHALL display session content and provide access to the chatbot
4. WHEN ready to take a quiz, THE System SHALL navigate to the quiz page
5. WHEN viewing progress, THE System SHALL display completed sessions, quiz scores, and next recommended session
6. WHEN navigating between pages, THE System SHALL preserve session state

### Requirement 10: Chatbot User Interface Component

**User Story:** As a student, I want a user-friendly chat interface, so that I can easily interact with the AI tutor.

#### Acceptance Criteria

1. WHEN the chatbot is displayed, THE System SHALL show message history with clear distinction between student and AI messages
2. WHEN a student types a message, THE System SHALL provide a text input field and send button
3. WHEN a message is sent, THE System SHALL display a loading indicator while waiting for AI response
4. WHEN displaying AI responses, THE System SHALL format them clearly and readably
5. WHEN the hint button is clicked, THE System SHALL provide access to the 3-level hint system

### Requirement 11: Course Content Data

**User Story:** As a student, I want to learn about Python variables and data types, so that I can understand fundamental programming concepts.

#### Acceptance Criteria

1. THE System SHALL include a Python Basics course with metadata defining learning objectives
2. THE System SHALL include at least 1 complete module (Module 1: Variables & Data Types) with at least 2 sessions
3. WHEN accessing Session 1.1, THE System SHALL provide content about introduction to variables
4. WHEN accessing Session 1.2, THE System SHALL provide content about data types in Python
5. THE System SHALL include a quiz for Module 1 with multiple choice and code completion questions

### Requirement 12: Learning Page Interface

**User Story:** As a student, I want to view session content and interact with the chatbot on the same page, so that I can learn and ask questions simultaneously.

#### Acceptance Criteria

1. WHEN viewing a learning session, THE System SHALL display theory content with concepts and examples
2. WHEN viewing a learning session, THE System SHALL display practice tasks for the student to attempt
3. WHEN on the learning page, THE System SHALL provide navigation buttons to move between sessions
4. WHEN on the learning page, THE System SHALL integrate the chatbot component for Q&A
5. WHEN displaying content, THE System SHALL show a progress indicator at the top of the page

### Requirement 13: Quiz Taking Interface

**User Story:** As a student, I want to take quizzes with a clear interface, so that I can test my understanding of the material.

#### Acceptance Criteria

1. WHEN starting a quiz, THE System SHALL display quiz instructions and time limit
2. WHEN taking a quiz, THE System SHALL display one question at a time with clear formatting
3. WHEN answering a question, THE System SHALL allow the student to select an option or enter code
4. WHEN submitting the quiz, THE System SHALL calculate the score and display results
5. WHEN viewing results, THE System SHALL show pass/fail status, score breakdown, and feedback for each question
6. IF the student fails, THEN THE System SHALL provide option to retry the quiz

### Requirement 14: Progress Tracking Interface

**User Story:** As a student, I want to see my learning progress, so that I can track my achievements and know what to study next.

#### Acceptance Criteria

1. WHEN viewing progress, THE System SHALL display overall course completion percentage
2. WHEN viewing progress, THE System SHALL show module-by-module completion status
3. WHEN viewing progress, THE System SHALL display quiz score history with timestamps
4. WHEN viewing progress, THE System SHALL recommend the next session to study
5. WHEN displaying progress, THE System SHALL use visual indicators like progress bars and checklists

### Requirement 15: Quiz Pass/Fail Decision Flow

**User Story:** As a student, I want the system to guide me based on my quiz performance, so that I can improve my understanding before moving forward.

#### Acceptance Criteria

1. WHEN a quiz score is greater than or equal to 70%, THE System SHALL mark the quiz as passed
2. WHEN a quiz score is less than 70%, THE System SHALL mark the quiz as failed
3. WHEN a student passes a quiz, THE System SHALL unlock the next module or session
4. WHEN a student fails a quiz, THE System SHALL display recommendations for topics to review
5. WHEN a student fails a quiz, THE System SHALL allow unlimited retry attempts

### Requirement 16: AI Greeting and Orientation

**User Story:** As a student, I want to be greeted by the AI when I start a course, so that I feel welcomed and understand what I will learn.

#### Acceptance Criteria

1. WHEN a student selects a course for the first time, THE System SHALL trigger an AI greeting message
2. WHEN greeting the student, THE AI SHALL use the student's name if provided
3. WHEN greeting the student, THE AI SHALL explain what will be learned in the course using simple language
4. WHEN greeting the student, THE AI SHALL ask if the student is ready to begin
5. WHEN greeting the student, THE AI SHALL use friendly and encouraging tone in Indonesian language

---

**Document Version**: 1.0
**Last Updated**: 2025-02-10
**Status**: Ready for Review
