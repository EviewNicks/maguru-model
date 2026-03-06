# Design Document

## Overview

The Maguru MVP Foundation is a Python-based learning platform built with Streamlit for the UI, LangChain for AI orchestration, and OpenAI's GPT-3.5-turbo for language model capabilities. The system provides an interactive learning experience where students can learn Python programming through structured content, receive AI-powered assistance, take quizzes, and track their progress.

The foundation consists of four main layers:
1. **UI Layer** - Streamlit-based multi-page interface
2. **Session State Layer** - In-memory state management
3. **AI Layer** - LangChain chains for intelligent tutoring
4. **Data Layer** - YAML/Markdown content files

## Architecture

### File Organization Structure

```
maguru-mvp/
├── app.py                          # Main Streamlit entry point
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (API keys)
│
├── data/                           # Course content files
│   └── courses/
│       └── python_basics/
│           ├── course.yaml         # Course metadata
│           └── modules/
│               └── module_1/
│                   ├── module.yaml # Module metadata
│                   ├── sessions/
│                   │   ├── session_1_1.md
│                   │   └── session_1_2.md
│                   └── quiz.yaml   # Quiz definition
│
├── langchain/                      # AI chains and prompts
│   ├── __init__.py
│   ├── chains/
│   │   ├── __init__.py
│   │   ├── explain_code.py        # Code explanation chain
│   │   ├── hint_generator.py      # 3-level hint chain
│   │   ├── quiz_feedback.py       # Quiz feedback chain
│   │   ├── qa_chatbot.py          # Q&A chatbot chain
│   │   └── ai_greeting.py         # Greeting chain
│   └── prompts/
│       ├── explain_code.yaml      # Prompt template
│       ├── hint_generator.yaml
│       ├── quiz_feedback.yaml
│       ├── qa_chatbot.yaml
│       └── ai_greeting.yaml
│
├── ui/                             # Streamlit UI components
│   ├── __init__.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home.py                # Course selection page
│   │   ├── learn.py               # Learning page (content + chatbot)
│   │   ├── quiz.py                # Quiz taking page
│   │   └── progress.py            # Progress tracking page
│   └── components/
│       ├── __init__.py
│       ├── chatbot.py             # Chatbot UI component
│       └── progress_bar.py        # Progress indicator
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── session_manager.py         # Session state management
│   ├── content_loader.py          # Content loading/parsing
│   └── quiz_validator.py          # Quiz validation/scoring
│
└── tests/                          # Unit tests (optional for MVP)
    ├── test_session_manager.py
    ├── test_content_loader.py
    └── test_quiz_validator.py
```

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit UI Layer                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Home   │  │  Learn   │  │   Quiz   │  │ Progress │   │
│  │   Page   │  │   Page   │  │   Page   │  │   Page   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│         │              │              │              │       │
│         └──────────────┴──────────────┴──────────────┘       │
│                            │                                  │
├────────────────────────────┼──────────────────────────────────┤
│                  Session State Manager                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Progress | Quiz Scores | Chat History | Current     │   │
│  │  Tracking | Timestamps  | (10 msgs)    | Session     │   │
│  └──────────────────────────────────────────────────────┘   │
├───────────────────────────────────────────────────────────────┤
│                     AI Layer (LangChain)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Code Explain │  │ Hint Generator│  │ Quiz Feedback│      │
│  │    Chain     │  │    Chain      │  │    Chain     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │  Q&A Chatbot │  │  AI Greeting │                         │
│  │    Chain     │  │    Chain     │                         │
│  └──────────────┘  └──────────────┘                         │
├───────────────────────────────────────────────────────────────┤
│                      Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Content      │  │ Quiz         │  │ Session      │      │
│  │ Loader       │  │ Validator    │  │ Manager      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  YAML Files (course.yaml, module.yaml, quiz.yaml)   │    │
│  │  Markdown Files (session_1_1.md, session_1_2.md)    │    │
│  └─────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────┘
```

### Component Sequence Diagrams

#### Sequence 1: Course Selection and AI Greeting

```
Student          Home Page       Session Manager    AI Greeting Chain    Learn Page
   │                 │                  │                   │                │
   │──Select Course──>│                 │                   │                │
   │                 │                  │                   │                │
   │                 │──Check if first──>│                  │                │
   │                 │    time          │                   │                │
   │                 │<─Yes, first time─│                   │                │
   │                 │                  │                   │                │
   │                 │──Generate greeting────────────────────>│                │
   │                 │  (student_name,  │                   │                │
   │                 │   course_title)  │                   │                │
   │                 │                  │                   │                │
   │                 │<─────────────────────AI greeting msg─│                │
   │                 │                  │                   │                │
   │                 │──Update state────>│                  │                │
   │                 │  (current_course)│                   │                │
   │                 │                  │                   │                │
   │                 │──Navigate to Learn Page──────────────────────────────>│
   │                 │                  │                   │                │
   │<────Display greeting + session content────────────────────────────────│
   │                 │                  │                   │                │
```

#### Sequence 2: Learning Session with Chatbot

```
Student      Learn Page    Chatbot Component   QA Chain    Session Manager
   │             │                │               │              │
   │──View content>│               │               │              │
   │             │                │               │              │
   │──Ask question────────────────>│               │              │
   │             │                │               │              │
   │             │                │──Get context──────────────────>│
   │             │                │  (session,   │              │
   │             │                │   chat_history)              │
   │             │                │<─Context data─────────────────│
   │             │                │               │              │
   │             │                │──Generate answer──>│          │
   │             │                │  (question,  │              │
   │             │                │   context)   │              │
   │             │                │<─AI response─│              │
   │             │                │               │              │
   │             │                │──Save to history──────────────>│
   │             │                │  (student msg,│              │
   │             │                │   AI response)│              │
   │             │                │               │              │
   │<────────────────Display AI response          │              │
   │             │                │               │              │
```

#### Sequence 3: Quiz Taking and Scoring

```
Student      Quiz Page    Quiz Validator    Feedback Chain    Session Manager
   │             │              │                 │                 │
   │──Start quiz─>│             │                 │                 │
   │             │              │                 │                 │
   │──Submit answers──────────────>│              │                 │
   │             │              │                 │                 │
   │             │              │──Validate each──│                 │
   │             │              │  answer         │                 │
   │             │              │                 │                 │
   │             │              │──Calculate score│                 │
   │             │              │  (sum correct)  │                 │
   │             │              │                 │                 │
   │             │              │──Check pass/fail│                 │
   │             │              │  (>= 70%)       │                 │
   │             │              │                 │                 │
   │             │              │──Generate feedback───────>│       │
   │             │              │  for each question        │       │
   │             │              │<─Feedback messages────────│       │
   │             │              │                 │                 │
   │             │<─Score + feedback              │                 │
   │             │  + pass/fail │                 │                 │
   │             │              │                 │                 │
   │             │──Save score──────────────────────────────────────>│
   │             │  (quiz_id,   │                 │                 │
   │             │   score, timestamp)            │                 │
   │             │              │                 │                 │
   │<────Display results         │                 │                 │
   │             │              │                 │                 │
```

### API Interface Specifications

#### Session Manager API

```python
# Initialize session state
def init_session() -> None:
    """Initialize session state with default values.
    
    Creates session state keys:
    - current_course: str = ""
    - current_module: str = ""
    - current_session: str = ""
    - completed_sessions: List[str] = []
    - quiz_scores: Dict[str, Dict] = {}
    - chat_history: List[Dict] = []
    - student_name: str = ""
    """

# Update progress
def update_progress(course_id: str, module_id: str, session_id: str) -> None:
    """Mark a session as completed.
    
    Args:
        course_id: Course identifier
        module_id: Module identifier
        session_id: Session identifier
    
    Side effects:
        Adds session_id to completed_sessions list
    """

# Get current session
def get_current_session() -> Dict[str, str]:
    """Retrieve current learning session.
    
    Returns:
        Dict with keys: course, module, session
    """

# Save quiz score
def save_quiz_score(quiz_id: str, score: int, total: int, passed: bool) -> None:
    """Store quiz results.
    
    Args:
        quiz_id: Quiz identifier
        score: Points earned
        total: Total possible points
        passed: Whether score >= 70%
    
    Side effects:
        Adds entry to quiz_scores dict with timestamp
    """

# Chat history management
def get_chat_history() -> List[Dict[str, str]]:
    """Get recent chat messages (max 10).
    
    Returns:
        List of dicts with keys: role, content, timestamp
    """

def add_chat_message(role: str, content: str) -> None:
    """Add message to chat history.
    
    Args:
        role: "student" or "ai"
        content: Message text
    
    Side effects:
        Appends to chat_history, maintains max 10 messages
    """

# Session completion check
def is_session_completed(session_id: str) -> bool:
    """Check if session is completed.
    
    Args:
        session_id: Session identifier
    
    Returns:
        True if session_id in completed_sessions
    """
```

#### Content Loader API

```python
# Load course metadata
def load_course_metadata(course_id: str) -> Optional[Dict]:
    """Load course YAML file.
    
    Args:
        course_id: Course identifier
    
    Returns:
        Dict with keys: id, title, description, difficulty, modules, learning_objectives
        None if file not found or malformed
    """

# Load module list
def load_module_list(course_id: str) -> List[str]:
    """Get all modules for a course.
    
    Args:
        course_id: Course identifier
    
    Returns:
        List of module IDs from course metadata
    """

# Load session content
def load_session_content(course_id: str, module_id: str, session_id: str) -> Optional[str]:
    """Load session Markdown file.
    
    Args:
        course_id: Course identifier
        module_id: Module identifier
        session_id: Session identifier
    
    Returns:
        Markdown content as string
        None if file not found
    """

# Load quiz definition
def load_quiz_definition(course_id: str, module_id: str, quiz_id: str) -> Optional[Dict]:
    """Load quiz YAML file.
    
    Args:
        course_id: Course identifier
        module_id: Module identifier
        quiz_id: Quiz identifier
    
    Returns:
        Dict with keys: id, title, passing_score, questions
        None if file not found or malformed
    """

# Get next session
def get_next_session(course_id: str, module_id: str, current_session_id: str) -> Optional[str]:
    """Determine next session in learning path.
    
    Args:
        course_id: Course identifier
        module_id: Module identifier
        current_session_id: Current session identifier
    
    Returns:
        Next session ID in module's session list
        None if current session is last
    """
```

#### Quiz Validator API

```python
# Validate answer
def validate_answer(question: Dict, student_answer: Any) -> bool:
    """Check if answer is correct.
    
    Args:
        question: Question dict with type, correct answer
        student_answer: Student's answer (int for MC, str for code)
    
    Returns:
        True if answer matches correct answer
    """

# Calculate score
def calculate_score(quiz_definition: Dict, student_answers: Dict[str, Any]) -> int:
    """Calculate total quiz score.
    
    Args:
        quiz_definition: Quiz dict with questions
        student_answers: Dict mapping question_id to answer
    
    Returns:
        Total points earned
    """

# Get pass/fail status
def get_passed_status(score: int, total_points: int) -> bool:
    """Check if quiz passed.
    
    Args:
        score: Points earned
        total_points: Total possible points
    
    Returns:
        True if (score / total_points) >= 0.7
    """

# Identify weak areas
def identify_weak_areas(quiz_definition: Dict, incorrect_answers: List[str]) -> List[str]:
    """Map incorrect answers to topics.
    
    Args:
        quiz_definition: Quiz dict with questions
        incorrect_answers: List of incorrect question IDs
    
    Returns:
        List of topic names to review
    """
```

#### AI Chain APIs

```python
# Code explanation
def explain_code(code_snippet: str) -> str:
    """Generate code explanation in Indonesian.
    
    Args:
        code_snippet: Python code to explain
    
    Returns:
        Explanation text in Indonesian
    """

# Hint generation
def generate_hint(task: str, student_attempt: str, level: int) -> str:
    """Generate progressive hint.
    
    Args:
        task: Practice task description
        student_attempt: Student's current attempt
        level: Hint level (1=gentle, 2=conceptual, 3=direct)
    
    Returns:
        Hint text in Indonesian
    """

# Quiz feedback
def generate_feedback(question: str, student_answer: str, 
                     correct_answer: str, is_correct: bool) -> str:
    """Generate quiz feedback.
    
    Args:
        question: Question text
        student_answer: Student's answer
        correct_answer: Correct answer
        is_correct: Whether answer was correct
    
    Returns:
        Feedback text in Indonesian
    """

# Q&A chatbot
def answer_question(question: str, session_context: Dict, 
                   chat_history: List[Dict]) -> str:
    """Answer student question with context.
    
    Args:
        question: Student's question
        session_context: Current session data (title, content)
        chat_history: Recent chat messages (max 10)
    
    Returns:
        Answer text in Indonesian
    """

# AI greeting
def generate_greeting(student_name: str, course_metadata: Dict) -> str:
    """Generate personalized course greeting.
    
    Args:
        student_name: Student's name
        course_metadata: Course data (title, objectives)
    
    Returns:
        Greeting text in Indonesian
    """
```

### Data Flow

**Learning Flow:**
```
Student selects course → AI greeting → Load session content → 
Display theory + chatbot → Student asks questions → 
AI responds with context → Student takes quiz → 
Validate answers → Calculate score → Pass/Fail decision →
Update progress → Show next steps
```

**AI Interaction Flow:**
```
User input → Session context + Chat history → 
LangChain prompt template → GPT-3.5-turbo → 
Response processing → Display to user → 
Update chat history (maintain 10 messages)
```

## Components and Interfaces

### 1. Session Manager (`utils/session_manager.py`)

**Purpose:** Manage user session state throughout the learning experience.

**Key Functions:**
- `init_session()` - Initialize session state with default values
- `update_progress(course_id, module_id, session_id)` - Mark session as completed
- `get_current_session()` - Retrieve active learning session
- `save_quiz_score(quiz_id, score, timestamp)` - Store quiz results
- `get_chat_history()` - Retrieve recent chat messages (max 10)
- `add_chat_message(role, content)` - Append message to history
- `is_session_completed(session_id)` - Check completion status

**State Structure:**
```python
{
    "current_course": str,
    "current_module": str,
    "current_session": str,
    "completed_sessions": List[str],
    "quiz_scores": Dict[str, {"score": int, "timestamp": str}],
    "chat_history": List[{"role": str, "content": str}],  # max 10
    "student_name": str
}
```

### 2. Content Loader (`utils/content_loader.py`)

**Purpose:** Load and parse course content from YAML and Markdown files.

**Key Functions:**
- `load_course_metadata(course_id)` - Parse course.yaml
- `load_module_list(course_id)` - Get all modules for a course
- `load_session_content(course_id, module_id, session_id)` - Parse session markdown
- `load_quiz_definition(course_id, module_id, quiz_id)` - Parse quiz.yaml
- `get_next_session(course_id, module_id, current_session_id)` - Determine next session
- `get_prerequisites(session_id)` - Get prerequisite sessions

**Error Handling:**
- Return `None` for missing files
- Return error dict for malformed YAML/Markdown
- Log errors for debugging
- Provide user-friendly error messages

### 3. Quiz Validator (`utils/quiz_validator.py`)

**Purpose:** Validate quiz answers and calculate scores.

**Key Functions:**
- `validate_answer(question, student_answer)` - Check if answer is correct
- `calculate_score(quiz_definition, student_answers)` - Sum points from correct answers
- `get_passed_status(score, total_points)` - Check if score >= 70%
- `identify_weak_areas(quiz_definition, incorrect_answers)` - Map errors to topics
- `generate_feedback(question, student_answer, is_correct)` - Create feedback message

**Validation Logic:**
- Multiple choice: Compare index with correct answer
- Code completion: Normalize whitespace and compare strings
- Partial credit: Not supported in MVP (binary correct/incorrect)

### 4. AI Chains (LangChain LCEL)

#### Code Explanation Chain (`langchain/chains/explain_code.py`)

**Purpose:** Explain Python code in Indonesian with clear, student-friendly language.

**Chain Structure:**
```python
prompt_template = PromptTemplate(
    template="""You are a friendly coding tutor for Indonesian students.
    
    Explain this code clearly in Indonesian:
    ```python
    {code}
    ```
    
    Focus on:
    1. What each line does
    2. Why it works that way
    3. Common mistakes to avoid
    
    Keep it simple and encouraging!""",
    input_variables=["code"]
)

chain = prompt_template | llm | StrOutputParser()
```

**Functions:**
- `create_explain_chain()` - Build LCEL chain
- `explain_code(code_snippet)` - Execute explanation
- `explain_with_level(code_snippet, level)` - Adjust complexity (simple/detailed)

#### Hint Generator Chain (`langchain/chains/hint_generator.py`)

**Purpose:** Generate progressive hints (3 levels) for practice tasks.

**Chain Structure:**
```python
hint_prompt = PromptTemplate(
    template="""You are helping an Indonesian student with a coding task.
    
    Task: {task}
    Current attempt: {student_attempt}
    Hint level: {level}
    
    Level 1 (Gentle): Subtle guidance, point to right direction
    Level 2 (Conceptual): Explain concept with similar example
    Level 3 (Direct): Show approach with missing pieces
    
    Provide a {level} hint in Indonesian.""",
    input_variables=["task", "student_attempt", "level"]
)

chain = hint_prompt | llm | StrOutputParser()
```

**Functions:**
- `create_hint_chain()` - Build LCEL chain
- `generate_hint(task, student_attempt, level)` - Generate specific level hint
- `get_all_hints(task, student_attempt)` - Generate all 3 levels at once

#### Quiz Feedback Chain (`langchain/chains/quiz_feedback.py`)

**Purpose:** Generate encouraging feedback for quiz answers.

**Chain Structure:**
```python
feedback_prompt = PromptTemplate(
    template="""You are a supportive coding tutor for Indonesian students.
    
    Question: {question}
    Student answer: {student_answer}
    Correct answer: {correct_answer}
    Is correct: {is_correct}
    
    If correct: Celebrate and explain why it's right
    If incorrect: Gently correct and explain the misconception
    
    Use encouraging language in Indonesian.""",
    input_variables=["question", "student_answer", "correct_answer", "is_correct"]
)

chain = feedback_prompt | llm | StrOutputParser()
```

**Functions:**
- `create_feedback_chain()` - Build LCEL chain
- `generate_feedback(question, student_answer, correct_answer, is_correct)` - Generate feedback
- `generate_correct_feedback(question, answer)` - Positive reinforcement
- `generate_incorrect_feedback(question, student_answer, correct_answer)` - Gentle correction

#### Q&A Chatbot Chain (`langchain/chains/qa_chatbot.py`)

**Purpose:** Answer student questions with session context awareness.

**Chain Structure:**
```python
qa_prompt = PromptTemplate(
    template="""You are a friendly AI tutor helping Indonesian students learn Python.
    
    Current session: {session_title}
    Session content: {session_content}
    Chat history: {chat_history}
    
    Student question: {question}
    
    Answer in Indonesian with:
    - Reference to session material when relevant
    - Clear explanations with examples
    - Encouraging and patient tone
    """,
    input_variables=["session_title", "session_content", "chat_history", "question"]
)

chain = qa_prompt | llm | StrOutputParser()
```

**Functions:**
- `create_qa_chain()` - Build LCEL chain
- `answer_question(question, session_context, chat_history)` - Generate answer
- `format_chat_history(messages)` - Format last 10 messages for context

#### AI Greeting Chain (`langchain/chains/ai_greeting.py`)

**Purpose:** Generate personalized greeting when student starts a course.

**Chain Structure:**
```python
greeting_prompt = PromptTemplate(
    template="""You are a friendly AI tutor welcoming an Indonesian student.
    
    Student name: {student_name}
    Course: {course_title}
    Learning objectives: {learning_objectives}
    
    Create a warm greeting that:
    1. Uses the student's name
    2. Explains what they'll learn
    3. Asks if they're ready to begin
    
    Use friendly Indonesian language.""",
    input_variables=["student_name", "course_title", "learning_objectives"]
)

chain = greeting_prompt | llm | StrOutputParser()
```

**Functions:**
- `create_greeting_chain()` - Build LCEL chain
- `generate_greeting(student_name, course_metadata)` - Generate personalized greeting

### 5. UI Components

#### Home Page (`ui/pages/home.py`)

**Purpose:** Course selection and landing page.

**Components:**
- `render_course_list()` - Display available courses as cards
- `render_course_card(course_metadata)` - Show title, description, difficulty
- `handle_course_selection(course_id)` - Process selection and navigate

**Layout:**
```
┌─────────────────────────────────────┐
│         Welcome to Maguru!          │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │  Python Basics                │  │
│  │  Difficulty: Beginner         │  │
│  │  Duration: 10 hours           │  │
│  │  [Start Learning]             │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

#### Learn Page (`ui/pages/learn.py`)

**Purpose:** Main learning interface with theory and chatbot.

**Components:**
- `render_session_content(session_data)` - Display theory, examples, practice
- `render_practice_task(task)` - Show practice exercise
- `render_navigation()` - Previous/Next/Take Quiz buttons
- `integrate_chatbot()` - Embed chatbot component

**Layout:**
```
┌─────────────────────────────────────┐
│    Progress: ████░░░░░░ 40%        │
├─────────────────┬───────────────────┤
│                 │                   │
│  Session 1.1    │   Ask AI Tutor    │
│                 │                   │
│  # Variables    │  [Chat messages]  │
│  Concept...     │                   │
│  Example...     │  [Input field]    │
│  Practice...    │  [Send] [Hint]    │
│                 │                   │
├─────────────────┴───────────────────┤
│  [← Previous]  [Take Quiz →]        │
└─────────────────────────────────────┘
```

#### Quiz Page (`ui/pages/quiz.py`)

**Purpose:** Quiz taking interface with immediate feedback.

**Components:**
- `render_quiz_intro(quiz_metadata)` - Instructions, time limit, passing score
- `render_question(question, index)` - Display question with options/input
- `handle_answer(question_id, answer)` - Process submission
- `render_results(score, feedback)` - Show score, pass/fail, detailed feedback
- `handle_retry()` - Allow quiz retry

**Flow:**
```
Intro → Q1 → Q2 → ... → Submit → Results → Pass/Fail → Next Steps
```

#### Progress Page (`ui/pages/progress.py`)

**Purpose:** Track and display learning progress.

**Components:**
- `render_overall_progress(completed, total)` - Course completion percentage
- `render_module_progress(modules)` - Module-by-module status
- `render_quiz_history(scores)` - Past quiz attempts with timestamps
- `render_recommendations(next_session)` - What to study next

**Layout:**
```
┌─────────────────────────────────────┐
│  Overall Progress: 40%              │
│  ████████░░░░░░░░░░░░░░░░░░░░       │
├─────────────────────────────────────┤
│  Module 1: Variables & Data Types   │
│  ✓ Session 1.1 - Completed          │
│  ✓ Session 1.2 - Completed          │
│  ✓ Quiz - Passed (85%)              │
├─────────────────────────────────────┤
│  Next: Module 2 - Control Flow      │
└─────────────────────────────────────┘
```

#### Chatbot Component (`ui/components/chatbot.py`)

**Purpose:** Interactive Q&A interface.

**Components:**
- `render_chat_interface()` - Display chat UI
- `handle_user_message(message)` - Process input and get AI response
- `display_ai_response(response)` - Show AI message
- `maintain_history()` - Keep last 10 messages

**Features:**
- Message history with role distinction (student/AI)
- Text input field with send button
- Hint button for 3-level hints
- Loading indicator during AI processing

## Data Models

### Course Metadata (YAML)

```yaml
id: python_basics
title: "Python Basics for Beginners"
description: "Learn fundamental Python programming concepts"
difficulty: beginner
duration_hours: 10
prerequisites: []
modules:
  - module_1
learning_objectives:
  - "Understand Python variables and data types"
  - "Master basic control flow"
  - "Write simple Python programs"
```

### Module Metadata (YAML)

```yaml
id: module_1
title: "Variables & Data Types"
description: "Learn about variables and basic data types in Python"
sessions:
  - session_1_1
  - session_1_2
quiz: quiz_module_1
estimated_duration_minutes: 30
```

### Session Content (Markdown)

```markdown
# Session 1.1: Introduction to Variables

## Learning Objectives
- Understand what variables are
- Learn how to create variables in Python
- Practice variable naming

## Concept
Variables are containers for storing data values...

## Example
```python
name = "Maguru"
age = 25
```

## Practice Task
Create a variable called `student_name` with your name.

## Discussion Questions
- Why do we need variables?
- What happens if we use a variable before creating it?
```

### Quiz Definition (YAML)

```yaml
id: quiz_module_1
title: "Variables & Data Types Quiz"
passing_score: 70
time_limit_minutes: 10
questions:
  - id: q1
    type: multiple_choice
    question: "How do you create a variable in Python?"
    options:
      - "var name = 'value'"
      - "name = 'value'"
      - "let name = 'value'"
    correct: 1
    points: 10
    explanation: "Python uses direct assignment without keywords like 'var' or 'let'."
    
  - id: q2
    type: code_completion
    question: "Complete the code to create a variable called 'city':"
    template: "___ = 'Jakarta'"
    answer: "city"
    points: 15
    explanation: "Variable names go on the left side of the assignment operator."
```

### Session State Schema

```python
{
    "initialized": bool,
    "student_name": str,
    "current_course": str,
    "current_module": str,
    "current_session": str,
    "completed_sessions": List[str],
    "quiz_scores": {
        "quiz_id": {
            "score": int,
            "total": int,
            "passed": bool,
            "timestamp": str,
            "attempt": int
        }
    },
    "chat_history": [
        {
            "role": str,  # "student" or "ai"
            "content": str,
            "timestamp": str
        }
    ],  # max 10 messages
    "current_page": str
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

**Note:** For MVP, we focus on 8 critical properties that ensure core functionality. Additional properties can be added post-MVP.

### Property 1: Session Initialization Completeness

*For any* application start, initializing the session state should result in a state dict that contains all required keys (current_course, current_module, current_session, completed_sessions, quiz_scores, chat_history, student_name) with appropriate default values.

**Validates: Requirements 1.1**

### Property 2: Quiz Score Calculation Accuracy

*For any* set of quiz questions and student answers, the calculated score should equal the sum of points for all questions where the student answer is correct.

**Validates: Requirements 3.3**

### Property 3: Pass/Fail Threshold Enforcement (70%)

*For any* quiz score and total points, get_passed_status should return True if and only if (score / total_points) >= 0.7.

**Validates: Requirements 3.4, 15.1, 15.2**

### Property 4: Chat History 10-Message Limit

*For any* sequence of messages added to chat history, the chat_history list should contain all messages if total is ≤ 10, or only the most recent 10 messages if total exceeds 10.

**Validates: Requirements 1.4, 7.2, 7.6**

### Property 5: Content Hierarchy Integrity

*For any* course, all referenced modules should exist, all referenced sessions within modules should exist, and all referenced quizzes should exist, maintaining the Course → Module → Session → Quiz hierarchy.

**Validates: Requirements 8.5**

### Property 6: Navigation State Preservation

*For any* sequence of page navigations (home → learn → quiz → progress), all session state values (completed_sessions, quiz_scores, chat_history) should remain unchanged after navigation.

**Validates: Requirements 9.6**

### Property 7: Quiz Unlock After Passing

*For any* quiz that is passed (score >= 70%), the next module or session in the learning path should become accessible.

**Validates: Requirements 15.3**

### Property 8: AI Greeting Trigger on First Course Selection

*For any* student selecting a course for the first time (course not in completed_sessions), the system should generate an AI greeting message.

**Validates: Requirements 16.1**

## Error Handling

**Philosophy for MVP:** Keep error handling simple and fail-fast. Focus on preventing crashes rather than comprehensive error recovery.

### Content Loading Errors

**Missing Files:**
```python
try:
    with open(filepath, 'r') as f:
        content = f.read()
except FileNotFoundError:
    return None  # Caller handles None
```

**Malformed YAML:**
```python
try:
    data = yaml.safe_load(file_content)
except yaml.YAMLError:
    return None  # Caller handles None
```

### AI Chain Errors

**API Failures:**
```python
try:
    response = chain.invoke(input_data)
except Exception as e:
    return "AI tutor sedang tidak tersedia. Silakan coba lagi."
```

**Empty Responses:**
```python
if not response or response.strip() == "":
    return "Maaf, saya tidak mengerti. Bisa diulang pertanyaannya?"
```

### Quiz Validation Errors

**Invalid Answer Format:**
```python
# Multiple choice: ensure integer
if not isinstance(answer, int) or answer < 0:
    return False

# Code completion: normalize whitespace
student_code = answer.strip().lower()
expected_code = correct_answer.strip().lower()
return student_code == expected_code
```

### Session State Errors

**State Corruption:**
```python
# Reinitialize if state is missing required keys
required_keys = ['current_course', 'completed_sessions', 'quiz_scores']
if not all(key in st.session_state for key in required_keys):
    init_session()  # Reset to defaults
```

## Testing Strategy

**MVP Testing Philosophy:** Focus on manual testing and basic unit tests for critical functions. Avoid over-engineering test infrastructure.

### Testing Approach

**Manual Testing (Primary):**
- Test all E2E user flows manually during development
- Quick feedback loop for UI/UX issues
- No test automation overhead

**Basic Unit Tests (Secondary):**
- Test critical business logic only
- Focus on functions with complex logic (quiz scoring, validation)
- Use Python's built-in `unittest` or `pytest`

### Manual Testing Scenarios

**Scenario 1: Complete Learning Flow**
```
1. Open app → Select Python Basics course
2. View Session 1.1 content
3. Chat with AI tutor (ask 2-3 questions)
4. Navigate to Session 1.2
5. Take Module 1 Quiz
6. Pass with score >= 70%
7. View progress page
✓ Verify: Progress updated, quiz score saved, next module unlocked
```

**Scenario 2: Failed Quiz Flow**
```
1. Take Module 1 Quiz
2. Answer incorrectly to get score < 70%
3. View results page
4. Check recommendations displayed
5. Click retry button
6. Retake quiz and pass
✓ Verify: Retry works, new score saved, can proceed
```

**Scenario 3: Chat Context Flow**
```
1. Start learning session
2. Ask AI tutor a question
3. Ask follow-up question
4. Send 10+ messages total
5. Check chat history
✓ Verify: Only last 10 messages kept, context maintained
```

**Scenario 4: Navigation Flow**
```
1. Home → Learn → Progress → Quiz → Home
2. Check session state after each navigation
✓ Verify: State preserved (completed sessions, scores, chat history)
```

**Scenario 5: AI Greeting Flow**
```
1. Enter student name
2. Select course for first time
3. View AI greeting message
✓ Verify: Greeting includes student name, explains course content
```

### Unit Testing Focus

**Critical Functions to Test:**

**Session Manager (`utils/session_manager.py`):**
```python
def test_init_session():
    """Test session initialization with all required keys"""
    
def test_save_quiz_score():
    """Test quiz score storage with timestamp"""
    
def test_chat_history_limit():
    """Test chat history maintains max 10 messages"""
```

**Quiz Validator (`utils/quiz_validator.py`):**
```python
def test_calculate_score():
    """Test score calculation accuracy"""
    
def test_pass_fail_threshold():
    """Test 70% threshold enforcement"""
    
def test_validate_multiple_choice():
    """Test multiple choice answer validation"""
    
def test_validate_code_completion():
    """Test code completion with whitespace normalization"""
```

**Content Loader (`utils/content_loader.py`):**
```python
def test_load_course_metadata():
    """Test loading valid course YAML"""
    
def test_load_missing_file():
    """Test graceful handling of missing files"""
    
def test_content_hierarchy():
    """Test course → module → session → quiz references"""
```

### Test Execution

**During Development:**
- Run unit tests after implementing each utility module
- Manual test after completing each UI page
- Quick smoke test before committing code

**Before Deployment:**
- Run all 5 manual E2E scenarios
- Run all unit tests
- Fix any critical bugs found

### Test Coverage Goals

**Realistic MVP Targets:**
- Manual testing: 100% of user flows (5 scenarios)
- Unit testing: Critical functions only (~15-20 tests)
- No automated integration tests
- No CI/CD pipeline

**Time Estimate:**
- Unit test writing: 2-3 days
- Manual testing: Ongoing during development (~30 min/day)
- Total testing time: ~3-4 days (vs 16-22 days with property-based testing)

---

**Document Version**: 1.0
**Last Updated**: 2025-02-10
**Status**: Ready for Review
