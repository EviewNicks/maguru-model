# Task 1: Week 1 Foundation Implementation

> **Focus**: Building the core foundation for Maguru MVP - Directory structure, utilities, AI chains, sample content, and basic UI.

---

## 📋 Overview

**Duration**: 5 Working Days
**Goal**: Create complete foundation for MVP with working course content and basic AI capabilities
**Deliverables**: Functional prototype with 1 complete module

---

## 🎯 Week 1 Objectives

By the end of Week 1, you will have:

- ✅ Complete project directory structure
- ✅ Core utility modules (session, content, quiz)
- ✅ Working LangChain AI chains (explain, hint, feedback)
- ✅ First course module with content (Variables & Data Types)
- ✅ Multi-page Streamlit UI
- ✅ Interactive chatbot component
- ✅ Tested and working prototype

---

## 📅 Day-by-Day Breakdown

### Day 1: Project Structure & Core Utilities (6 hours)

**Morning (3 hours)**

#### Task 1.1: Create Directory Structure
```bash
# Create all directories
mkdir -p data/courses/python_basics/modules/module_1/sessions
mkdir -p langchain/chains langchain/graphs langchain/prompts
mkdir -p ui/pages ui/components
mkdir -p utils styles

# Create __init__.py files for Python packages
touch langchain/__init__.py
touch langchain/chains/__init__.py
touch langchain/graphs/__init__.py
touch langchain/prompts/__init__.py
touch ui/__init__.py
touch ui/pages/__init__.py
touch ui/components/__init__.py
touch utils/__init__.py
```

**Deliverable**: Complete directory structure ready for development

#### Task 1.2: Create Session Manager
**File**: `utils/session_manager.py`

**Purpose**: Manage user session state in Streamlit

**Functions to implement**:
```python
- init_session()          # Initialize session state
- update_progress()        # Update learning progress
- get_current_session()    # Get current session data
- save_quiz_score()        # Save quiz results
- get_chat_history()       # Get chat conversation history
- add_chat_message()       # Add message to history
- is_session_completed()   # Check if session is done
```

**Key Features**:
- Track current course, module, session
- Store completed sessions list
- Save quiz scores with timestamps
- Maintain chat history for context

**Afternoon (3 hours)**

#### Task 1.3: Create Content Loader
**File**: `utils/content_loader.py`

**Purpose**: Load course content from YAML and Markdown files

**Functions to implement**:
```python
- load_course_metadata()   # Load course.yaml
- load_module_list()       # Get all modules
- load_session_content()   # Load session markdown
- load_quiz_definition()   # Load quiz.yaml
- get_next_session()       # Get next session after current
- get_prerequisites()      # Get prerequisite sessions
```

**Key Features**:
- Parse YAML files for structured data
- Load Markdown content with frontmatter
- Handle missing files gracefully
- Cache loaded content for performance

**Testing**: Verify loading from sample files

---

### Day 2: Content Creation & Quiz Validation (6 hours)

**Morning (3 hours)**

#### Task 2.1: Create Course Metadata
**File**: `data/courses/python_basics/course.yaml`

**Content Structure**:
```yaml
id: python_basics
title: "Python Basics for Beginners"
description: "Learn fundamental Python programming concepts"
difficulty: beginner
duration_hours: 10
prerequisites: []
modules:
  - module_1
  - module_2  # placeholder
learning_objectives:
  - Understand Python variables and data types
  - Master basic control flow
  - Write simple Python programs
```

#### Task 2.2: Create Module 1 Metadata
**File**: `data/courses/python_basics/modules/module_1/module.yaml`

**Content Structure**:
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

#### Task 2.3: Create Session Contents
**Files**:
- `data/courses/python_basics/modules/module_1/sessions/session_1_1.md`
- `data/courses/python_basics/modules/module_1/sessions/session_1_2.md`

**Session Template**:
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

**Afternoon (3 hours)**

#### Task 2.4: Create Quiz Definition
**File**: `data/courses/python_basics/modules/module_1/quiz.yaml`

**Content Structure**:
```yaml
id: quiz_module_1
title: "Variables & Data Types Quiz"
passing_score: 70
time_limit_minutes: 10
questions:
  - type: multiple_choice
    question: "How do you create a variable in Python?"
    options:
      - "var name = 'value'"
      - "name = 'value'"
      - "let name = 'value'"
    correct: 1
    points: 10
    explanation: "Python uses direct assignment..."

  - type: code_completion
    question: "Complete the code to create a variable called 'city':"
    template: "___ = 'Jakarta'"
    answer: "city"
    points: 15
    explanation: "Variable names go on the left side..."
```

#### Task 2.5: Create Quiz Validator
**File**: `utils/quiz_validator.py`

**Functions to implement**:
```python
- validate_answer()         # Check if answer is correct
- calculate_score()         # Calculate total score
- get_passed_status()       # Check if passed (>=70%)
- identify_weak_areas()     # Find topics to review
- generate_feedback()       # Generate feedback message
```

**Key Features**:
- Handle multiple choice validation
- Handle code completion validation
- Support partial scoring if needed
- Generate detailed feedback per question

**Testing**: Test with sample quiz data

---

### Day 3: LangChain AI Chains (6 hours)

**Morning (3 hours)**

#### Task 3.1: Setup Prompts
**Files**:
- `langchain/prompts/explain_code.yaml`
- `langchain/prompts/hint_generator.yaml`
- `langchain/prompts/quiz_feedback.yaml`
- `langchain/prompts/qa_chatbot.yaml`

**Prompt Template Structure**:
```yaml
name: "code_explanation"
template: |
  You are a friendly coding tutor for Indonesian students.

  Explain this code clearly in Indonesian:
  ```python
  {code}
  ```

  Focus on:
  1. What each line does
  2. Why it works that way
  3. Common mistakes to avoid

  Keep it simple and encouraging!
input_variables:
  - code
```

**Afternoon (3 hours)**

#### Task 3.2: Implement Code Explanation Chain
**File**: `langchain/chains/explain_code.py`

**Purpose**: Explain Python code to students

**Functions to implement**:
```python
- create_explain_chain()    # Create LCEL chain
- explain_code()            # Execute explanation
- explain_with_level()      # Explain with complexity level
```

**Key Features**:
- Use LCEL (LangChain Expression Language)
- Support different explanation levels
- Return Indonesian language responses
- Handle code syntax errors gracefully

#### Task 3.3: Implement Hint Generator Chain
**File**: `langchain/chains/hint_generator.py`

**Purpose**: Generate 3-level progressive hints

**Functions to implement**:
```python
- create_hint_chain()      # Create hint generation chain
- generate_hint()           # Generate hint for specific level
- get_all_hints()           # Get all 3 hint levels
```

**Hint Levels**:
- **Level 1 (Gentle)**: Subtle guidance, point to right direction
- **Level 2 (Conceptual)**: Explain the concept, give similar example
- **Level 3 (Direct)**: Show approach with missing pieces

#### Task 3.4: Implement Quiz Feedback Chain
**File**: `langchain/chains/quiz_feedback.py`

**Purpose**: Generate feedback for quiz answers

**Functions to implement**:
```python
- create_feedback_chain()   # Create feedback generation chain
- generate_feedback()        # Generate feedback for answer
- generate_correct_feedback()
- generate_incorrect_feedback()
```

**Key Features**:
- Positive reinforcement for correct answers
- Gentle correction for incorrect answers
- Explain misconceptions
- Suggest review topics

**Testing**: Test all chains with sample inputs

---

### Day 4: Multi-Page UI & Chatbot (6 hours)

**Morning (3 hours)**

#### Task 4.1: Create Home Page
**File**: `ui/pages/home.py`

**Purpose**: Course selection and landing page

**Components to implement**:
```python
- render_course_list()      # Display available courses
- render_course_card()      # Show course details
- handle_course_selection() # Process course choice
```

**UI Elements**:
- Course cards with title, description, difficulty
- "Start Learning" button
- Progress indicator for returning users

#### Task 4.2: Create Learn Page
**File**: `ui/pages/learn.py`

**Purpose**: Main learning interface with theory and chatbot

**Components to implement**:
```python
- render_session_content()  # Display theory content
- render_practice_task()    # Show practice exercise
- render_navigation()       # Next/Previous buttons
- integrate_chatbot()       # Chatbot component
```

**UI Layout**:
```
┌─────────────────────────────────────┐
│          Header: Progress Bar       │
├─────────────────┬───────────────────┤
│                 │                   │
│   Theory        │   Chatbot Q&A     │
│   Content       │                   │
│                 │   Chat Here       │
│                 │                   │
├─────────────────┴───────────────────┤
│      [Previous]  [Take Quiz]        │
└─────────────────────────────────────┘
```

**Afternoon (3 hours)**

#### Task 4.3: Create Chatbot Component
**File**: `ui/components/chatbot.py`

**Purpose**: Interactive Q&A chatbot interface

**Functions to implement**:
```python
- render_chat_interface()  # Display chat UI
- handle_user_message()    # Process user input
- display_ai_response()    # Show AI response
- maintain_history()       # Keep conversation context
```

**UI Elements**:
- Message history display
- Chat input field
- Send button
- Hint button (3-level hints)

**Integration**:
- Connect to LangChain chains
- Use session state for history
- Context-aware responses

#### Task 4.4: Update Main App
**File**: `app.py`

**Changes**:
```python
# Add multi-page navigation
import ui.pages.home
import ui.pages.learn
import ui.pages.quiz
import ui.pages.progress

# Update routing logic
```

---

### Day 5: Integration & Testing (6 hours)

**Morning (3 hours)**

#### Task 5.1: Create Quiz Page
**File**: `ui/pages/quiz.py`

**Purpose**: Quiz taking interface

**Components to implement**:
```python
- render_quiz_intro()      # Quiz instructions
- render_question()        # Display question
- handle_answer()           # Process answer submission
- render_results()          # Show score and feedback
- handle_retry()            # Allow retry options
```

**UI Flow**:
```
Quiz Intro → Question 1 → Question 2 → ...
         → Submit → Results → Pass/Fail Decision
```

#### Task 5.2: Create Progress Page
**File**: `ui/pages/progress.py`

**Purpose**: Track and display learning progress

**Components to implement**:
```python
- render_overall_progress() # Course completion percentage
- render_module_progress()  # Module-by-module status
- render_quiz_history()     # Past quiz scores
- render_recommendations()  # What to study next
```

**UI Elements**:
- Progress bars
- Session checklists (completed/pending)
- Quiz score history
- Next session recommendations

**Afternoon (3 hours)**

#### Task 5.3: Integration Testing
**Test Scenarios**:

1. **Happy Path**:
```
Select course → View session → Chat with bot → Take quiz → Pass
```

2. **Fail Path**:
```
Select course → View session → Take quiz → Fail → See recommendations
```

3. **Navigation**:
```
Home → Learn → Progress → Learn → Quiz → Home
```

4. **Chatbot**:
```
Ask question → Get answer → Ask follow-up → Get context-aware response
```

5. **Hint System**:
```
Get stuck → Request hint → Level 1 → Level 2 → Level 3
```

#### Task 5.4: Bug Fixes & Polish
**Checklist**:
- [ ] Fix any bugs found during testing
- [ ] Improve error messages
- [ ] Add loading indicators
- [ ] Polish UI styling
- [ ] Verify all links work
- [ ] Test on different screen sizes

---

## 📊 Deliverables Checklist

By end of Week 1, ensure these are complete:

### Files Created (35+ files)

**Core Structure (3 files)**
- [ ] `app.py` - Updated with routing
- [ ] `requirements.txt` - Dependencies
- [ ] `.env` - Environment configuration

**Utils (3 files)**
- [ ] `utils/session_manager.py`
- [ ] `utils/content_loader.py`
- [ ] `utils/quiz_validator.py`

**LangChain (7 files)**
- [ ] `langchain/chains/explain_code.py`
- [ ] `langchain/chains/hint_generator.py`
- [ ] `langchain/chains/quiz_feedback.py`
- [ ] `langchain/prompts/explain_code.yaml`
- [ ] `langchain/prompts/hint_generator.yaml`
- [ ] `langchain/prompts/quiz_feedback.yaml`
- [ ] `langchain/prompts/qa_chatbot.yaml`

**UI (6 files)**
- [ ] `ui/pages/home.py`
- [ ] `ui/pages/learn.py`
- [ ] `ui/pages/quiz.py`
- [ ] `ui/pages/progress.py`
- [ ] `ui/components/chatbot.py`
- [ ] `ui/components/progress_bar.py`

**Content (7 files)**
- [ ] `data/courses/python_basics/course.yaml`
- [ ] `data/courses/python_basics/modules/module_1/module.yaml`
- [ ] `data/courses/python_basics/modules/module_1/sessions/session_1_1.md`
- [ ] `data/courses/python_basics/modules/module_1/sessions/session_1_2.md`
- [ ] `data/courses/python_basics/modules/module_1/quiz.yaml`
- [ ] `data/courses/python_basics/modules/module_1/sessions/.gitkeep`

**__init__.py files (9 files)**
- [ ] All Python package directories have `__init__.py`

### Functionality Verified

**Core Features (Must Work)**
- [ ] Can select and start a course
- [ ] Can view session content (theory + examples)
- [ ] Can chat with AI tutor
- [ ] Can take quiz with immediate feedback
- [ ] Progress is tracked correctly
- [ ] Navigation between pages works

**AI Features (Must Work)**
- [ ] Code explanation generates responses
- [ ] Hint generation works for all 3 levels
- [ ] Quiz feedback is accurate and helpful
- [ ] Chatbot maintains conversation context

**Data Loading (Must Work)**
- [ ] Course metadata loads correctly
- [ ] Session content displays properly
- [ ] Quiz questions render correctly
- [ ] YAML parsing handles errors gracefully

---

## 🔧 Technical Notes

### Dependencies Used

**Streamlit**: UI framework
- Multi-page navigation
- Session state management
- Chat interface components

**LangChain**: AI orchestration
- LCEL chains for simple flows
- Prompt templates
- OpenAI integration

**PyYAML**: Content parsing
- Course metadata
- Quiz definitions

**python-dotenv**: Configuration
- Environment variables
- API keys

### Key Design Decisions

1. **Session State Storage**: Using Streamlit's built-in session state (no database for MVP)
2. **Content Format**: YAML for metadata, Markdown for content
3. **AI Integration**: Direct OpenAI API calls via LangChain
4. **Language**: All AI responses in Indonesian
5. **Quiz Format**: Multiple choice + code completion only (MVP)

---

## ⚠️ Potential Issues & Solutions

| Issue | Solution |
|-------|----------|
| Session state resets on refresh | Add warning message to user |
| Slow AI responses | Add loading indicators |
| Content not loading | Add error handling & fallback |
| Quiz validation errors | Add input sanitization |
| Chatbot memory loss | Implement conversation window limit |

---

## 🎯 Success Criteria

Week 1 is successful when:

1. **User can complete a full learning cycle**:
   - Select course → Learn session → Take quiz → See results

2. **AI features work end-to-end**:
   - Chatbot responds to questions
   - Code explanations are generated
   - Quiz feedback is accurate

3. **No critical bugs**:
   - App doesn't crash on normal usage
   - Navigation works smoothly
   - Data loads correctly

4. **Code is maintainable**:
   - Clear file structure
   - Documented functions
   - Consistent naming conventions

---

## 📝 Week 1 Summary

**What You Built**:
- Complete foundation for Maguru MVP
- Working AI tutor with basic capabilities
- First course module with content
- Functional multi-page UI

**What's Next (Week 2)**:
- Adaptive learning flow (LangGraph)
- Prerequisite review system
- Enhanced progress tracking
- Full integration testing

---

**Task Status**: 🟡 Ready to Start
**Estimated Time**: 30 hours (5 days × 6 hours)
**Dependencies**: None (can start immediately)

**Next Action**: Run `mkdir` commands to create directory structure
