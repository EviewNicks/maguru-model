# Maguru MVP Implementation Plan

> **Comprehensive sprint plan for building a fully functional MVP of the Maguru AI Coding Learning Platform**

**Document Version**: 1.0
**Created**: 2025-02-10
**Status**: Ready for Execution
**Sprint Duration**: 2-3 weeks

---

## Table of Contents

1. [MVP Scope Definition](#mvp-scope-definition)
2. [Complete File Structure](#complete-file-structure)
3. [Task Breakdown](#task-breakdown)
4. [Implementation Order](#implementation-order)
5. [Priority Levels](#priority-levels)
6. [Testing Checkpoints](#testing-checkpoints)
7. [Weekly Milestones](#weekly-milestones)

---

## MVP Scope Definition

### What IS MVP (Must Have)

| Feature                   | Description                                 | Acceptance Criteria                                 |
| ---------------------------| ---------------------------------------------| -----------------------------------------------------|
| **Course Selection**      | List available courses with metadata        | User can view and select a course                   |
| **AI Greeting**           | Personalized welcome after course selection | AI greets user by name, explains course content     |
| **Theory Display**        | Render structured learning content          | Content shows concept, examples, practice tasks     |
| **Q&A Chatbot**           | Context-aware AI chat during learning       | Chatbot responds to questions about current session |
| **Quiz System**           | Multiple choice + code completion questions | Immediate validation and scoring                    |
| **Progress Tracking**     | Visual progress indicators                  | Progress bar and completion status visible          |
| **70% Passing Threshold** | Pass/fail logic for progression             | Score >=70% unlocks next content                    |
| **Prerequisite Review**   | Triggered on failing quiz                   | Automatic recommendation when score <70%            |
| **Code Explanation**      | AI explains code snippets                   | User can paste code and get explanation             |
| **3-Level Hints**         | Progressive hint system                     | Gentle → Conceptual → Direct hints available        |

### What is NOT MVP (Post-MVP)

| Feature | Reason |
|---------|--------|
| User Authentication | Anonymous sessions sufficient for MVP |
| Database Persistence | Streamlit session state adequate |
| Multiple Languages | Python only for MVP |
| Live Code Execution | Static content + AI explanation sufficient |
| Gamification (Badges, Leaderboards) | Nice-to-have, not core learning |
| Video Content | Text-based content sufficient |
| Mobile Apps | Responsive web sufficient |
| Spaced Repetition | Advanced feature |

---

## Complete File Structure

```
maguru-model/
├── app.py                                    # ✓ Main entry point (EXISTS)
├── requirements.txt                          # ✓ Dependencies (EXISTS)
├── .env                                      # ✓ Environment config (EXISTS)
├── .env.example                              # ✓ Environment template (EXISTS)
├── .gitignore                                # ✓ Git ignore (EXISTS)
│
├── docs/
│   ├── project.md                           # ✓ Original concept (EXISTS)
│   ├── new-project.md                       # ✓ Detailed MVP spec (EXISTS)
│   ├── mvp-implementation-plan.md           # ↳ THIS FILE - Implementation plan
│   └── api-reference.md                     # ↳ API documentation (NEW)
│
├── data/                                     # ↳ Course content (NEW DIRECTORY)
│   └── courses/
│       ├── _metadata.yaml                    # ↳ Course catalog metadata
│       └── python_basics/                    # ↳ First course: Python Basics
│           ├── course.yaml                   # ↳ Course configuration
│           ├── cover.png                     # ↳ Course thumbnail
│           └── modules/
│               ├── 01_variables_and_types/
│               │   ├── module.yaml           # ↳ Module configuration
│               │   └── sessions/
│               │       ├── 01_introduction/
│               │       │   ├── session.yaml  # ↳ Session metadata
│               │       │   └── content.md    # ↳ Theory content
│               │       └── 02_strings/
│               │           ├── session.yaml
│               │           └── content.md
│               ├── 02_control_flow/
│               │   ├── module.yaml
│               │   └── sessions/
│               │       ├── 01_if_statements/
│               │       │   ├── session.yaml
│               │       │   └── content.md
│               │       └── 02_loops/
│               │           ├── session.yaml
│               │           └── content.md
│               └── 03_functions/
│                   ├── module.yaml
│                   └── sessions/
│                       ├── 01_defining_functions/
│                       │   ├── session.yaml
│                       │   └── content.md
│                       └── 02_parameters_return/
│                           ├── session.yaml
│                           └── content.md
│
├── langchain/                                # ↳ AI components (NEW DIRECTORY)
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── llm.py                           # ↳ LLM initialization & config
│   │
│   ├── chains/                               # ↳ LCEL chains (NEW DIRECTORY)
│   │   ├── __init__.py
│   │   ├── greeting_chain.py                # ↳ AI greeting generation
│   │   ├── code_explanation_chain.py        # ↳ Code explanation
│   │   ├── hint_chain.py                    # ↳ 3-level hint generation
│   │   ├── quiz_feedback_chain.py           # ↳ Quiz answer feedback
│   │   └── qa_chain.py                      # ↳ Q&A chatbot
│   │
│   ├── graphs/                               # ↳ LangGraph flows (NEW DIRECTORY)
│   │   ├── __init__.py
│   │   ├── adaptive_learning_graph.py       # ↳ Adaptive learning flow
│   │   └── prerequisite_review_graph.py     # ↳ Review recommendation logic
│   │
│   └── prompts/                              # ↳ Prompt templates (NEW DIRECTORY)
│       ├── __init__.py
│       ├── greeting_template.txt             # ↳ Greeting prompt
│       ├── code_explanation_template.txt     # ↳ Code explanation prompt
│       ├── hint_templates/                   # ↳ Hint level prompts
│       │   ├── gentle_template.txt
│       │   ├── conceptual_template.txt
│       │   └── direct_template.txt
│       ├── quiz_feedback_template.txt        # ↳ Quiz feedback prompt
│       └── qa_template.txt                   # ↳ Q&A prompt
│
├── ui/                                       # ↳ UI components (NEW DIRECTORY)
│   ├── __init__.py
│   ├── pages/                                # ↳ Multi-page components
│   │   ├── __init__.py
│   │   ├── home.py                          # ↳ Landing page
│   │   ├── course_selection.py              # ↳ Course listing & selection
│   │   ├── learning.py                      # ↳ Main learning interface
│   │   ├── quiz.py                          # ↳ Quiz interface
│   │   ├── review.py                        # ↳ Prerequisite review
│   │   └── progress.py                     # ↳ Progress dashboard
│   │
│   └── components/                           # ↳ Reusable UI components
│       ├── __init__.py
│       ├── chatbot.py                       # ↳ Chatbot UI component
│       ├── progress_bar.py                  # ↳ Progress visualization
│       ├── quiz_renderer.py                 # ↳ Quiz question renderer
│       ├── content_display.py               # ↳ Theory content display
│       └── navigation.py                    # ↳ Navigation helpers
│
├── utils/                                    # ↳ Utility modules (NEW DIRECTORY)
│   ├── __init__.py
│   ├── session_manager.py                   # ↳ Session state management
│   ├── content_loader.py                    # ↳ Content parsing & loading
│   ├── quiz_validator.py                    # ↳ Quiz validation logic
│   ├── progress_tracker.py                  # ↳ Progress calculation
│   ├── prerequisite_analyzer.py             # ↳ Review recommendation logic
│   └── config.py                            # ↳ Application configuration
│
├── styles/                                   # ↳ Styling (NEW DIRECTORY)
│   └── custom.css                           # ↳ Custom CSS for Streamlit
│
└── tests/                                    # ↳ Tests (NEW DIRECTORY)
    ├── __init__.py
    ├── test_chains.py                       # ↳ Chain tests
    ├── test_content_loader.py               # ↳ Content loading tests
    ├── test_quiz_validator.py               # ↳ Quiz validation tests
    └── test_session_manager.py              # ↳ Session state tests
```

---

## Task Breakdown

### Phase 1: Foundation Setup (Days 1-2)

#### 1.1 Project Structure & Configuration
- **File**: `utils/config.py`
- **Description**: Central configuration management for app settings, LLM parameters, paths
- **Dependencies**: None
- **Priority**: CRITICAL
- **Estimated Time**: 1 hour

```yaml
Purpose:
  - Centralize all configuration constants
  - Manage environment variable access
  - Define path constants for data directories

Key Components:
  - APP_CONFIG: App name, version, debug mode
  - LLM_CONFIG: Model name, temperature, max tokens
  - PATH_CONFIG: Data paths, content paths
  - QUIZ_CONFIG: Passing threshold, retry limits
```

#### 1.2 Content Loader
- **File**: `utils/content_loader.py`
- **Description**: Load and parse YAML/Markdown course content
- **Dependencies**: `utils/config.py`
- **Priority**: CRITICAL
- **Estimated Time**: 2 hours

```yaml
Purpose:
  - Parse course YAML metadata
  - Load session markdown content
  - Cache loaded content in session state
  - Handle missing or malformed content files

Key Functions:
  - load_course_catalog(): Return list of available courses
  - load_course(course_id): Load full course structure
  - load_session(course_id, module_id, session_id): Load specific session
  - load_quiz(course_id, module_id): Load quiz for module
```

#### 1.3 Session Manager
- **File**: `utils/session_manager.py`
- **Description**: Manage Streamlit session state for user progress
- **Dependencies**: `utils/config.py`
- **Priority**: CRITICAL
- **Estimated Time**: 2 hours

```yaml
Purpose:
  - Initialize session state on first load
  - Track current course, module, session
  - Store quiz scores and history
  - Manage chat history
  - Handle progress state

Key Functions:
  - initialize_session(): Set up all session state variables
  - get_current_position(): Return current course/module/session
  - update_position(): Move to next content
  - save_quiz_result(): Store quiz attempt
  - get_progress(): Calculate completion percentage
  - add_chat_message(): Store chat interaction
```

#### 1.4 Course Content Structure
- **Files**: Complete `data/courses/` directory structure
- **Description**: Create first course with sample content
- **Dependencies**: None
- **Priority**: CRITICAL
- **Estimated Time**: 3-4 hours

```yaml
Deliverables:
  - data/courses/_metadata.yaml: Course catalog
  - python_basics/course.yaml: Course configuration
  - Module 1: Variables & Data Types (2 sessions)
  - Module 2: Control Flow (2 sessions)
  - Each session includes:
    - session.yaml: Metadata, objectives, quiz link
    - content.md: Theory, examples, practice tasks
```

### Phase 2: AI Layer (Days 2-4)

#### 2.1 LLM Initialization
- **File**: `langchain/models/llm.py`
- **Description**: Initialize OpenAI LLM with configuration
- **Dependencies**: `utils/config.py`, `openai`, `langchain-openai`
- **Priority**: CRITICAL
- **Estimated Time**: 1 hour

```yaml
Purpose:
  - Create LLM instance with proper configuration
  - Handle API key from environment
  - Implement error handling for API failures
  - Support both GPT-3.5 and GPT-4 (configurable)

Key Functions:
  - get_llm(): Return configured LLM instance
  - test_connection(): Verify API access
```

#### 2.2 Greeting Chain
- **File**: `langchain/chains/greeting_chain.py`
- **Description**: Generate personalized AI greeting for course start
- **Dependencies**: `langchain/models/llm.py`
- **Priority**: HIGH
- **Estimated Time**: 1.5 hours

```yaml
Purpose:
  - Generate personalized welcome message
  - Include user name from input
  - Explain course objectives
  - Ask if student is ready to begin

Inputs:
  - user_name: Student's name
  - course_title: Course being taken
  - course_objectives: Learning objectives

Outputs:
  - greeting_text: Personalized welcome message
```

#### 2.3 Code Explanation Chain
- **File**: `langchain/chains/code_explanation_chain.py`
- **Description**: Explain code snippets in simple terms
- **Dependencies**: `langchain/models/llm.py`
- **Priority**: HIGH
- **Estimated Time**: 2 hours

```yaml
Purpose:
  - Analyze code snippet structure
  - Explain each line/block in simple language
  - Provide real-world analogies
  - Highlight common mistakes

Inputs:
  - code_snippet: Python code to explain
  - complexity_level: "beginner" | "intermediate" | "advanced"
  - focus_area: Optional specific section to explain

Outputs:
  - explanation: Structured code explanation
  - analogies: Real-world comparisons
  - common_mistakes: Pitfalls to avoid
```

#### 2.4 Hint Chain (3-Level)
- **File**: `langchain/chains/hint_chain.py`
- **Description**: Generate progressive hints for practice problems
- **Dependencies**: `langchain/models/llm.py`
- **Priority**: HIGH
- **Estimated Time**: 2.5 hours

```yaml
Purpose:
  - Generate hints at 3 progressive levels
  - Track which hints have been shown
  - Adapt hints based on context

Inputs:
  - problem_description: What the student is trying to solve
  - hint_level: 1 (gentle) | 2 (conceptual) | 3 (direct)
  - session_context: Current learning material

Outputs:
  - hint_text: Appropriate hint for level
  - next_action: Suggested next step
```

#### 2.5 Quiz Feedback Chain
- **File**: `langchain/chains/quiz_feedback_chain.py`
- **Description**: Generate detailed feedback for quiz answers
- **Dependencies**: `langchain/models/llm.py`
- **Priority**: HIGH
- **Estimated Time**: 2 hours

```yaml
Purpose:
  - Explain why answer is correct/incorrect
  - Provide positive reinforcement
  - Connect to related concepts
  - Offer review suggestions for wrong answers

Inputs:
  - question: Quiz question text
  - user_answer: Student's answer
  - correct_answer: Correct answer
  - is_correct: Boolean
  - session_context: Related learning material

Outputs:
  - feedback_text: Detailed explanation
  - reinforcement: Positive message
  - suggestions: What to review if wrong
```

#### 2.6 Q&A Chatbot Chain
- **File**: `langchain/chains/qa_chain.py`
- **Description**: Context-aware Q&A for learning sessions
- **Dependencies**: `langchain/models/llm.py`
- **Priority**: HIGH
- **Estimated Time**: 2.5 hours

```yaml
Purpose:
  - Answer student questions about current session
  - Maintain conversation context
  - Provide additional examples
  - Redirect out-of-scope questions politely

Inputs:
  - question: Student's question
  - session_content: Current session material
  - chat_history: Previous messages in session
  - course_context: Overall course context

Outputs:
  - answer: Response to question
  - follow_up_suggestions: Related topics to explore
```

### Phase 3: Adaptive Learning (Days 4-6)

#### 3.1 Adaptive Learning Graph
- **File**: `langchain/graphs/adaptive_learning_graph.py`
- **Description**: LangGraph for adaptive learning flow decisions
- **Dependencies**: All chains, `utils/session_manager.py`
- **Priority**: HIGH
- **Estimated Time**: 3 hours

```yaml
Purpose:
  - Orchestrate learning flow based on performance
  - Decide next action after quiz (pass/retry/review)
  - Trigger prerequisite review when needed
  - Track learning patterns

States:
  - start: Entry point
  - learning: Active learning session
  - quiz_assessment: Evaluating quiz results
  - pass_ready: Student passed, ready to continue
  - review_needed: Student needs prerequisite review
  - retry_allowed: Student can retry quiz

Transitions:
  - Based on quiz score (>=70% pass, <70% review)
  - Based on student choice (retry/review/continue)
```

#### 3.2 Prerequisite Analyzer
- **File**: `utils/prerequisite_analyzer.py`
- **Description**: Analyze quiz results to identify weak areas
- **Dependencies**: None
- **Priority**: MEDIUM
- **Estimated Time**: 2 hours

```yaml
Purpose:
  - Map incorrect answers to concepts
  - Identify prerequisite topics to review
  - Generate personalized review plan
  - Estimate review time

Key Functions:
  - analyze_quiz_results(quiz_attempt): Return weak areas
  - identify_prerequisites(weak_areas): Return review topics
  - create_review_plan(topics): Structured review sequence
  - estimate_review_time(topics): Time estimate
```

#### 3.3 Quiz Validator
- **File**: `utils/quiz_validator.py`
- **Description**: Validate quiz answers and calculate scores
- **Dependencies**: None
- **Priority**: CRITICAL
- **Estimated Time**: 1.5 hours

```yaml
Purpose:
  - Validate multiple choice answers
  - Validate code completion answers
  - Calculate score with topic breakdown
  - Handle multiple valid answers

Key Functions:
  - validate_multiple_choice(answer, correct): Boolean
  - validate_code_completion(answer, options): Accept flexible answers
  - calculate_score(attempt): Return score and topic breakdown
  - is_passing_score(score): Boolean (>=70%)
```

#### 3.4 Progress Tracker
- **File**: `utils/progress_tracker.py`
- **Description**: Calculate and track learning progress
- **Dependencies**: `utils/session_manager.py`
- **Priority**: MEDIUM
- **Estimated Time**: 1.5 hours

```yaml
Purpose:
  - Calculate overall course completion
  - Track module completion
  - Track session completion
  - Generate progress statistics

Key Functions:
  - get_course_progress(): Percentage complete
  - get_module_progress(): Module completion status
  - get_next_session(): Return next incomplete session
  - get_completion_summary(): Overall progress summary
```

### Phase 4: UI Components (Days 5-8)

#### 4.1 Home Page
- **File**: `ui/pages/home.py`
- **Description**: Landing page with course overview
- **Dependencies**: `utils/content_loader.py`
- **Priority**: CRITICAL
- **Estimated Time**: 2 hours

```yaml
Components:
  - Hero section with app description
  - Featured courses grid
  - How it works section
  - Call to action to start learning
```

#### 4.2 Course Selection Page
- **File**: `ui/pages/course_selection.py`
- **Description**: Display available courses and handle selection
- **Dependencies**: `utils/content_loader.py`, `utils/session_manager.py`
- **Priority**: CRITICAL
- **Estimated Time**: 2 hours

```yaml
Components:
  - Course catalog display
  - Course cards with metadata
  - Course detail modal
  - Selection confirmation
  - Name input for personalization
```

#### 4.3 Learning Page (Main)
- **File**: `ui/pages/learning.py`
- **Description**: Main learning interface with content and chatbot
- **Dependencies**: All chains, `ui/components/chatbot.py`, `ui/components/content_display.py`
- **Priority**: CRITICAL
- **Estimated Time**: 4 hours

```yaml
Components:
  - Session header with progress
  - Theory content display
  - Examples section
  - Practice tasks
  - Integrated chatbot
  - Navigation buttons (Next/Previous)
  - Code explanation input
  - Hint request button
```

#### 4.4 Quiz Page
- **File**: `ui/pages/quiz.py`
- **Description**: Quiz interface with validation and feedback
- **Dependencies**: `utils/quiz_validator.py`, `langchain/chains/quiz_feedback_chain.py`
- **Priority**: CRITICAL
- **Estimated Time**: 3 hours

```yaml
Components:
  - Quiz instructions
  - Question renderer (multiple choice + code completion)
  - Answer input
  - Submit button
  - Feedback display with AI explanation
  - Score summary
  - Retry/Continue options
```

#### 4.5 Review Page
- **File**: `ui/pages/review.py`
- **Description**: Prerequisite review interface
- **Dependencies**: `utils/prerequisite_analyzer.py`, `ui/pages/learning.py`
- **Priority**: MEDIUM
- **Estimated Time**: 2.5 hours

```yaml
Components:
  - Review recommendation display
  - Weak areas explanation
  - Review content display
  - Mini-quiz after review
  - Verification of understanding
```

#### 4.6 Progress Page
- **File**: `ui/pages/progress.py`
- **Description**: Progress dashboard and statistics
- **Dependencies**: `utils/progress_tracker.py`
- **Priority**: MEDIUM
- **Estimated Time**: 2 hours

```yaml
Components:
  - Overall progress bar
  - Module completion checklist
  - Quiz score history
  - Learning statistics
  - Achievement badges (if time permits)
```

#### 4.7 Chatbot Component
- **File**: `ui/components/chatbot.py`
- **Description**: Reusable chatbot UI component
- **Dependencies**: `langchain/chains/qa_chain.py`
- **Priority**: HIGH
- **Estimated Time**: 2.5 hours

```yaml
Components:
  - Chat message display
  - Input field
  - Send button
  - Message history
  - Loading indicator
  - Suggested questions
```

#### 4.8 Content Display Component
- **File**: `ui/components/content_display.py`
- **Description**: Render markdown learning content
- **Dependencies**: None
- **Priority**: HIGH
- **Estimated Time**: 1.5 hours

```yaml
Components:
  - Markdown renderer
  - Code syntax highlighting
  - Example boxes
  - Task checklist
  - Collapsible sections
```

#### 4.9 Progress Bar Component
- **File**: `ui/components/progress_bar.py`
- **Description**: Visual progress indicator
- **Dependencies**: None
- **Priority**: LOW
- **Estimated Time**: 1 hour

```yaml
Components:
  - Linear progress bar
  - Circular progress indicator
  - Milestone markers
  - Status labels
```

#### 4.10 Quiz Renderer Component
- **File**: `ui/components/quiz_renderer.py`
- **Description**: Render different quiz question types
- **Dependencies**: None
- **Priority**: HIGH
- **Estimated Time**: 2 hours

```yaml
Components:
  - Multiple choice renderer
  - Code completion renderer
  - Answer input handlers
  - Validation feedback display
```

### Phase 5: Integration & Polish (Days 8-10)

#### 5.1 Main App Integration
- **File**: `app.py` (Update existing)
- **Description**: Integrate all pages with navigation
- **Dependencies**: All UI pages
- **Priority**: CRITICAL
- **Estimated Time**: 2 hours

```yaml
Updates:
  - Add page navigation
  - Initialize session state
  - Route to appropriate page
  - Handle page transitions
  - Error handling
```

#### 5.2 Custom Styling
- **File**: `styles/custom.css`
- **Description**: Custom CSS for consistent branding
- **Dependencies**: None
- **Priority**: LOW
- **Estimated Time**: 1.5 hours

```yaml
Elements:
  - Color scheme definition
  - Typography
  - Component styling
  - Responsive adjustments
  - Accessibility enhancements
```

#### 5.3 Error Handling
- **File**: `utils/error_handler.py` (NEW)
- **Description**: Centralized error handling
- **Dependencies**: None
- **Priority**: MEDIUM
- **Estimated Time**: 2 hours

```yaml
Purpose:
  - Handle API failures gracefully
  - Display user-friendly error messages
  - Log errors for debugging
  - Implement retry logic
```

#### 5.4 Testing Suite
- **File**: `tests/` (multiple files)
- **Description**: Test coverage for critical components
- **Dependencies**: All modules
- **Priority**: MEDIUM
- **Estimated Time**: 4 hours

```yaml
Test Files:
  - test_chains.py: Test all LangChain chains
  - test_content_loader.py: Test content loading
  - test_quiz_validator.py: Test quiz logic
  - test_session_manager.py: Test session state
```

---

## Implementation Order

### Week 1: Foundation & Core AI

**Day 1 (Monday)**
1. Create directory structure
2. Implement `utils/config.py`
3. Implement `utils/session_manager.py`
4. Create course content skeleton (metadata.yaml)
5. Testing checkpoint: Verify session state initialization

**Day 2 (Tuesday)**
1. Implement `utils/content_loader.py`
2. Create first module content (2 sessions)
3. Implement `langchain/models/llm.py`
4. Test OpenAI API connection
5. Testing checkpoint: Load and display course content

**Day 3 (Wednesday)**
1. Implement greeting chain
2. Implement code explanation chain
3. Implement Q&A chatbot chain
4. Create chatbot UI component
5. Testing checkpoint: Test AI chains with sample inputs

**Day 4 (Thursday)**
1. Implement hint chain (3 levels)
2. Implement quiz validator
3. Create course selection page
4. Create learning page (basic version)
5. Testing checkpoint: End-to-end course selection to learning

**Day 5 (Friday)**
1. Implement quiz feedback chain
2. Create quiz page
3. Integrate chatbot in learning page
4. Testing checkpoint: Complete learning → quiz flow

### Week 2: Adaptive Learning & Polish

**Day 6 (Monday)**
1. Implement prerequisite analyzer
2. Implement adaptive learning graph
3. Create review page
4. Testing checkpoint: Test prerequisite review flow

**Day 7 (Tuesday)**
1. Implement progress tracker
2. Create progress page
3. Add progress visualization
4. Testing checkpoint: Progress tracking accuracy

**Day 8 (Wednesday)**
1. Create content display component
2. Create quiz renderer component
3. Create progress bar component
4. Refine UI/UX across all pages
5. Testing checkpoint: Visual consistency check

**Day 9 (Thursday)**
1. Implement error handling
2. Add loading states
3. Implement retry logic
4. Create additional course content (Module 2-3)
5. Testing checkpoint: Error scenario testing

**Day 10 (Friday)**
1. Write tests for critical components
2. Fix bugs from testing
3. Performance optimization
4. Documentation updates
5. Testing checkpoint: Full regression testing

### Week 3: Content & Final Polish (Optional)

**Day 11-13**
1. Complete course content (remaining modules)
2. Additional quiz questions
3. UI polish and refinement
4. Accessibility improvements

**Day 14-15**
1. Final testing
2. Bug fixes
3. Deployment preparation
4. User testing (if possible)

---

## Priority Levels

### CRITICAL (Must Have for MVP)
Blocks marked with 🔴 CRITICAL must be completed for MVP to function:

1. `utils/config.py` - Configuration management
2. `utils/session_manager.py` - Session state
3. `utils/content_loader.py` - Content loading
4. `utils/quiz_validator.py` - Quiz validation
5. `langchain/models/llm.py` - LLM initialization
6. `langchain/chains/greeting_chain.py` - AI greeting
7. `langchain/chains/qa_chain.py` - Q&A chatbot
8. `langchain/chains/quiz_feedback_chain.py` - Quiz feedback
9. `ui/pages/course_selection.py` - Course selection
10. `ui/pages/learning.py` - Main learning interface
11. `ui/pages/quiz.py` - Quiz interface
12. `ui/components/chatbot.py` - Chatbot UI
13. `ui/components/content_display.py` - Content rendering
14. `data/courses/` - At least 1 complete course (2 modules, 4 sessions)

### HIGH (Important for Good UX)
Blocks marked with 🟡 HIGH significantly improve user experience:

1. `langchain/chains/code_explanation_chain.py` - Code explanation
2. `langchain/chains/hint_chain.py` - Hint system
3. `langchain/graphs/adaptive_learning_graph.py` - Adaptive flow
4. `utils/prerequisite_analyzer.py` - Review recommendations
5. `utils/progress_tracker.py` - Progress calculation
6. `ui/pages/review.py` - Review interface
7. `ui/pages/progress.py` - Progress dashboard
8. `ui/components/quiz_renderer.py` - Quiz rendering

### MEDIUM (Nice to Have)
Blocks marked with 🟢 MEDIUM add polish but aren't essential:

1. `ui/pages/home.py` - Landing page (can start directly at course selection)
2. `ui/components/progress_bar.py` - Custom progress bars (use Streamlit default)
3. `utils/error_handler.py` - Centralized error handling
4. `tests/` - Test suite (manual testing OK for MVP)

### LOW (Can Skip)
Blocks marked with 🔵 LOW can be deferred to post-MVP:

1. `styles/custom.css` - Custom styling (use Streamlit defaults)
2. Gamification features (badges, achievements)
3. Advanced visualizations
4. Multiple courses (start with 1)

---

## Testing Checkpoints

### Checkpoint 1: Foundation (Day 1, End of Day)
**Goal**: Verify project structure and session state

```yaml
Tests:
  - [ ] All directories created successfully
  - [ ] Session state initializes without errors
  - [ ] Config loads from environment
  - [ ] App runs without crashes

Manual Test:
  - Run streamlit run app.py
  - Verify no import errors
  - Check session state variables in developer tools
```

### Checkpoint 2: Content Loading (Day 2, End of Day)
**Goal**: Verify content can be loaded and displayed

```yaml
Tests:
  - [ ] Course catalog loads successfully
  - [ ] Course metadata parses correctly
  - [ ] Session content loads from markdown
  - [ ] Missing files handled gracefully

Manual Test:
  - Browse to course selection page
  - Verify Python Basics course appears
  - Click course and see details
```

### Checkpoint 3: AI Chains (Day 3, End of Day)
**Goal**: Verify AI components work

```yaml
Tests:
  - [ ] LLM connects to OpenAI API
  - [ ] Greeting chain generates response
  - [ ] Code explanation chain works
  - [ ] Q&A chain responds to questions
  - [ ] API errors handled gracefully

Manual Test:
  - Enter name on course selection
  - Verify AI greeting appears
  - Ask chatbot a question
  - Paste code for explanation
```

### Checkpoint 4: Learning Flow (Day 4, End of Day)
**Goal**: Verify basic learning experience

```yaml
Tests:
  - [ ] Course selection starts learning session
  - [ ] Theory content displays correctly
  - [ ] Examples render with syntax highlighting
  - [ ] Chatbot integrates in learning page
  - [ ] Navigation between sessions works

Manual Test:
  - Select Python Basics course
  - Enter name
  - Complete first session
  - Navigate to next session
```

### Checkpoint 5: Quiz System (Day 5, End of Day)
**Goal**: Verify quiz functionality

```yaml
Tests:
  - [ ] Quiz questions render correctly
  - [ ] Multiple choice answers validate
  - [ ] Code completion answers validate
  - [ ] Feedback displays for correct answers
  - [ ] Feedback displays for incorrect answers
  - [ ] Score calculates correctly
  - [ ] Pass/fail threshold works (70%)

Manual Test:
  - Complete a session
  - Take the quiz
  - Answer some correctly, some incorrectly
  - Verify feedback is helpful
  - Check score calculation
```

### Checkpoint 6: Adaptive Flow (Day 6, End of Day)
**Goal**: Verify prerequisite review system

```yaml
Tests:
  - [ ] Score < 70% triggers review recommendation
  - [ ] Weak areas identified correctly
  - [ ] Review page displays appropriate content
  - [ ] Mini-quiz after review works
  - [ ] Passing mini-quiz allows retry

Manual Test:
  - Fail a quiz intentionally (score < 70%)
  - Verify review recommendation appears
  - Go through review flow
  - Pass mini-quiz
  - Retry original quiz
```

### Checkpoint 7: Progress Tracking (Day 7, End of Day)
**Goal**: Verify progress system

```yaml
Tests:
  - [ ] Progress bar updates correctly
  - [ ] Completed sessions marked
  - [ ] Overall progress calculates accurately
  - [ ] Progress persists in session

Manual Test:
  - Complete multiple sessions
  - Check progress page
  - Verify completion status
  - Navigate between sessions
```

### Checkpoint 8: UI Polish (Day 8, End of Day)
**Goal**: Verify UI consistency

```yaml
Tests:
  - [ ] All pages use consistent styling
  - [ ] Navigation works between all pages
  - [ ] Mobile responsive (basic)
  - [ ] Loading states display
  - [ ] Error messages are user-friendly

Manual Test:
  - Navigate through entire app
  - Test on different screen sizes
  - Trigger error scenarios
  - Check loading states
```

### Checkpoint 9: Full Integration (Day 9, End of Day)
**Goal**: End-to-end testing

```yaml
Tests:
  - [ ] Complete full learning journey
  - [ ] Test all hint levels
  - [ ] Use all chatbot features
  - [ ] Pass and fail quizzes
  - [ ] Go through review flow
  - [ ] Check progress updates

Manual Test:
  - New user journey from start to finish
  - Complete at least 1 full module
  - Test all AI features
  - Verify data flow
```

### Checkpoint 10: Final Testing (Day 10, End of Day)
**Goal**: Regression testing and polish

```yaml
Tests:
  - [ ] All previous checkpoints still pass
  - [ ] No new bugs introduced
  - [ ] Performance acceptable
  - [ ] Documentation complete
  - [ ] Ready for user testing

Manual Test:
  - Complete regression test suite
  - Test with fresh session
  - Verify all features work
  - Document any known issues
```

---

## Weekly Milestones

### Week 1 Milestone: Core Learning Experience
**Deliverables**:
- User can select a course and get AI greeting
- User can read theory content with AI Q&A support
- User can take quiz with immediate feedback
- Basic progress tracking works

**Success Criteria**:
- [ ] Can complete one full session (theory → quiz)
- [ ] AI responses are helpful and contextually relevant
- [ ] Quiz validates answers correctly
- [ ] No critical bugs blocking core flow

### Week 2 Milestone: Adaptive Learning Complete
**Deliverables**:
- Prerequisite review system works
- Progress dashboard available
- All AI features implemented
- UI polished and consistent

**Success Criteria**:
- [ ] Failing quiz triggers appropriate review
- [ ] Progress accurately reflects completion
- [ ] All hint levels work correctly
- [ ] Full learning journey functional (start → finish)

### Week 3 Milestone: Content Complete & Polish
**Deliverables**:
- Full course content (3 modules, 6+ sessions)
- Comprehensive testing complete
- Performance optimized
- Documentation updated

**Success Criteria**:
- [ ] At least 3 complete modules available
- [ ] All test cases pass
- [ ] App loads and responds quickly
- [ ] Documentation enables deployment

---

## Risk Management

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| OpenAI API rate limits | Medium | High | Implement caching, rate limiting, fallback messages |
| LangChain version conflicts | Low | Medium | Pin specific versions in requirements.txt |
| Streamlit session state loss | Medium | High | Implement state persistence, error handling |
| Content parsing errors | Low | Medium | Validate content files, handle gracefully |

### Content Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Insufficient content for testing | Medium | High | Create minimal viable content early |
| Quality of AI responses | Medium | High | Careful prompt engineering, testing |
| Quiz validation complexity | Medium | Medium | Start simple, add complexity gradually |

### Time Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Underestimated AI complexity | High | High | Prioritize simple chains, iterate |
| UI/UX polish takes too long | Medium | Medium | Focus on functional first, polish later |
| Testing reveals many bugs | Medium | Medium | Allocate buffer time at end |

---

## Success Metrics

### MVP Completion Criteria

**Functional Requirements**:
- [ ] 1 complete course with minimum 2 modules
- [ ] Each module has minimum 2 sessions
- [ ] All AI chains functional (greeting, explanation, hints, feedback, Q&A)
- [ ] Quiz system validates and scores correctly
- [ ] Prerequisite review triggers on < 70% score
- [ ] Progress tracking works end-to-end

**Quality Requirements**:
- [ ] No critical bugs
- [ ] AI responses under 5 seconds
- [ ] UI loads without visible lag
- [ ] Error messages are user-friendly
- [ ] Content displays correctly

**User Experience Requirements**:
- [ ] Clear navigation throughout app
- [ ] Helpful feedback on quiz answers
- [ ] AI responses are contextually relevant
- [ ] Progress indicators are accurate
- [ ] Review flow is helpful

---

## Next Steps

1. **Review this plan** with team/stakeholders
2. **Adjust priorities** based on feedback
3. **Set up development environment** if not already done
4. **Create project board** with these tasks
5. **Begin Day 1 tasks**

---

## Appendix: Sample Content Structure

### course.yaml Template
```yaml
id: python_basics
title: Python Basics
description: Learn the fundamentals of Python programming
difficulty: beginner
duration_hours: 10
objectives:
  - Understand Python syntax
  - Work with variables and data types
  - Use control flow structures
  - Define and use functions
modules:
  - id: 01_variables_and_types
    title: Variables and Data Types
  - id: 02_control_flow
    title: Control Flow
  - id: 03_functions
    title: Functions
```

### session.yaml Template
```yaml
id: 01_introduction
title: Introduction to Python
objectives:
  - Understand what Python is
  - Learn about variables
  - Practice creating variables
quiz_module: 01_variables_and_types
estimated_minutes: 15
```

### content.md Template
```markdown
# Introduction to Python

## Concept
Python is a high-level programming language known for its simplicity...

## Examples
\```python
# Creating a variable
name = "Alice"
age = 25
\```

## Practice Tasks
1. Create a variable called `city` with your city's name
2. Create a variable called `temperature` with a number
```

---

**Document End**

For questions or clarifications about this implementation plan, please refer to:
- `docs/new-project.md` - Detailed feature specifications
- `docs/project.md` - Original project concept
- Project README.md - General project information
