# Implementation Plan: Foundation

## Overview

This implementation plan breaks down the Maguru MVP Foundation into discrete, actionable coding tasks. Each task builds incrementally toward a functional prototype with core learning features, AI assistance, and progress tracking.

## Tasks

- [x] 1. Setup project structure and dependencies
  - Create directory structure (data, langchain, ui, utils)
  - Create `__init__.py` files for Python packages
  - Setup `requirements.txt` with dependencies (streamlit, langchain, openai, pyyaml, python-dotenv)
  - Create `.env` file for API keys
  - _Requirements: All requirements (foundation setup)_

- [x] 2. Implement Session Manager
  - [x] 2.1 Create `utils/session_manager.py` with core functions
    - Implement `init_session()` - initialize state with default values
    - Implement `update_progress()` - mark sessions as completed
    - Implement `get_current_session()` - retrieve active session
    - Implement `save_quiz_score()` - store quiz results with timestamp
    - Implement `get_chat_history()` - retrieve last 10 messages
    - Implement `add_chat_message()` - append message, maintain 10-message limit
    - Implement `is_session_completed()` - check completion status
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

  - [x]* 2.2 Write unit tests for Session Manager
    - Test session initialization completeness (Property 1)
    - Test chat history 10-message limit (Property 4)
    - Test quiz score storage
    - _Requirements: 1.1, 1.4, 1.3_

- [x] 3. Implement Content Loader
  - [x] 3.1 Create `utils/content_loader.py` with parsing functions
    - Implement `load_course_metadata()` - parse course.yaml
    - Implement `load_module_list()` - get modules from course
    - Implement `load_session_content()` - parse session markdown
    - Implement `load_quiz_definition()` - parse quiz.yaml
    - Implement `get_next_session()` - determine next session in path
    - Implement error handling for missing/malformed files (return None)
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

  - [x]* 3.2 Write unit tests for Content Loader
    - Test loading valid YAML/Markdown files
    - Test graceful error handling for missing files
    - Test content hierarchy integrity (Property 5)
    - _Requirements: 2.1, 2.3, 2.5, 8.5_

- [x] 4. Implement Quiz Validator
  - [x] 4.1 Create `utils/quiz_validator.py` with validation logic
    - Implement `validate_answer()` - check multiple choice and code completion
    - Implement `calculate_score()` - sum points from correct answers
    - Implement `get_passed_status()` - check if score >= 70%
    - Implement `identify_weak_areas()` - map incorrect answers to topics
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [x]* 4.2 Write unit tests for Quiz Validator
    - Test score calculation accuracy (Property 2)
    - Test pass/fail threshold enforcement at 70% (Property 3)
    - Test multiple choice validation
    - Test code completion with whitespace normalization
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 5. Create course content files
  - [x] 5.1 Create `data/courses/python_basics/course.yaml`
    - Define course metadata (id, title, description, difficulty, modules, objectives)
    - _Requirements: 8.1, 11.1_

  - [x] 5.2 Create `data/courses/python_basics/modules/module_1/module.yaml`
    - Define module metadata (id, title, description, sessions, quiz)
    - _Requirements: 8.2, 11.2_

  - [x] 5.3 Create session content files
    - Create `session_1_1.md` - Introduction to Variables
    - Create `session_1_2.md` - Data Types in Python
    - Include learning objectives, concepts, examples, practice tasks
    - _Requirements: 8.3, 11.3, 11.4_

  - [x] 5.4 Create `data/courses/python_basics/modules/module_1/quiz.yaml`
    - Define quiz with multiple choice and code completion questions
    - Set passing_score to 70
    - Include explanations for each question
    - _Requirements: 8.4, 11.5_

- [x] 6. Implement AI Chains (LangChain LCEL)
  - [x] 6.1 Create prompt templates
    - Create `langchain/prompts/explain_code.yaml`
    - Create `langchain/prompts/hint_generator.yaml`
    - Create `langchain/prompts/quiz_feedback.yaml`
    - Create `langchain/prompts/qa_chatbot.yaml`
    - Create `langchain/prompts/ai_greeting.yaml`
    - All prompts should specify Indonesian language output
    - _Requirements: 4.1, 5.1, 6.1, 7.1, 16.3_

  - [x] 6.2 Implement Code Explanation Chain
    - Create `langchain/chains/explain_code.py`
    - Implement `create_explain_chain()` - build LCEL chain
    - Implement `explain_code()` - execute explanation
    - Add basic error handling (return fallback message on API failure)
    - _Requirements: 4.1, 4.4_

  - [x] 6.3 Implement Hint Generator Chain
    - Create `langchain/chains/hint_generator.py`
    - Implement `create_hint_chain()` - build LCEL chain
    - Implement `generate_hint()` - generate hint for specific level (1-3)
    - Support 3 hint levels: gentle, conceptual, direct
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 6.4 Implement Quiz Feedback Chain
    - Create `langchain/chains/quiz_feedback.py`
    - Implement `create_feedback_chain()` - build LCEL chain
    - Implement `generate_feedback()` - generate feedback for answers
    - Support both correct and incorrect answer feedback
    - _Requirements: 6.1, 6.2, 6.5_

  - [x] 6.5 Implement Q&A Chatbot Chain
    - Create `langchain/chains/qa_chatbot.py`
    - Implement `create_qa_chain()` - build LCEL chain
    - Implement `answer_question()` - answer with session context
    - Include chat history (last 10 messages) in context
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [x] 6.6 Implement AI Greeting Chain
    - Create `langchain/chains/ai_greeting.py`
    - Implement `create_greeting_chain()` - build LCEL chain
    - Implement `generate_greeting()` - personalized greeting
    - Include student name and course objectives in greeting
    - _Requirements: 16.1, 16.2, 16.3_

- [x] 7. Checkpoint - Test AI chains manually
  - Test each chain with sample inputs
  - Verify Indonesian language responses
  - Verify error handling for API failures
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement Home Page
  - [x] 8.1 Create `ui/pages/home.py`
    - Implement `render_course_list()` - display available courses
    - Implement `render_course_card()` - show course details
    - Implement `handle_course_selection()` - process selection
    - Trigger AI greeting on first course selection (Property 8)
    - _Requirements: 9.1, 9.2, 16.1_

- [x] 9. Implement Learn Page
  - [x] 9.1 Create `ui/pages/learn.py`
    - Implement `render_session_content()` - display theory and examples
    - Implement `render_practice_task()` - show practice exercises
    - Implement `render_navigation()` - previous/next/quiz buttons
    - Integrate chatbot component
    - Show progress indicator at top
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [x] 10. Implement Chatbot Component
  - [x] 10.1 Create `ui/components/chatbot.py`
    - Implement `render_chat_interface()` - display chat UI
    - Implement `handle_user_message()` - process input
    - Implement `display_ai_response()` - show AI message
    - Show message history with role distinction (student/AI)
    - Include hint button for 3-level hints
    - _Requirements: 10.1, 10.2, 10.4, 10.5_

- [x] 11. Implement Quiz Page
  - [x] 11.1 Create `ui/pages/quiz.py`
    - Implement `render_quiz_intro()` - show instructions and time limit
    - Implement `render_question()` - display question with options/input
    - Implement `handle_answer()` - process answer submission
    - Implement `render_results()` - show score, pass/fail, feedback
    - Implement `handle_retry()` - allow unlimited retries
    - Show retry option when score < 70% (Property 20)
    - Unlock next session when passed (Property 7)
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 15.1, 15.2, 15.3, 15.4, 15.5_

- [x] 12. Implement Progress Page
  - [x] 12.1 Create `ui/pages/progress.py`
    - Implement `render_overall_progress()` - course completion percentage
    - Implement `render_module_progress()` - module-by-module status
    - Implement `render_quiz_history()` - past quiz scores with timestamps
    - Implement `render_recommendations()` - next session to study
    - Use visual indicators (progress bars, checklists)
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [x] 13. Implement main app routing
  - [x] 13.1 Update `app.py`
    - Import all page modules
    - Implement multi-page navigation logic
    - Initialize session state on app start
    - Preserve state across page navigations (Property 6)
    - _Requirements: 9.6_

- [ ] 14. Checkpoint - Integration testing
  - Manually test all 5 E2E scenarios:
    1. Complete learning flow (select → learn → chat → quiz → pass → progress)
    2. Failed quiz flow (fail → recommendations → retry → pass)
    3. Chat context flow (10+ messages, verify limit)
    4. Navigation flow (home → learn → progress → quiz → home, verify state)
    5. AI greeting flow (first course selection with student name)
  - See docs/test.md for detailed step-by-step testing guide
  - Report bugs found during testing
  - Ensure all tests pass before proceeding to Task 15

- [ ] 15. Polish and bug fixes
  - Fix any bugs found during integration testing
  - Add loading indicators for AI responses
  - Improve error messages for user-friendly experience
  - Test on different screen sizes (responsive design)
  - Verify all navigation links work correctly

## Notes

- Tasks marked with `*` are optional unit tests - can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Manual testing is primary validation method for MVP
- Focus on getting core functionality working before polish

---

**Document Version**: 1.0
**Last Updated**: 2025-02-10
**Status**: Ready for Execution
