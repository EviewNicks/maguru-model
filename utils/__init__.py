"""Maguru utility modules."""

from .session_manager import (init_session,
    update_progress,
    get_current_session,
    save_quiz_score,
    get_chat_history,
    add_chat_message,
    is_session_completed,
)

from .content_loader import (load_course_metadata,
    load_module_list,
    load_session_content,
    load_quiz_definition,
    get_next_session,
)

from .quiz_validator import (validate_answer,
    calculate_score,
    get_passed_status,
    identify_weak_areas,
)

__all__ = [
    # Session Manager exports
    "init_session",
    "update_progress",
    "get_current_session",
    "save_quiz_score",
    "get_chat_history",
    "add_chat_message",
    "is_session_completed",
    # Content Loader exports
    "load_course_metadata",
    "load_module_list",
    "load_session_content",
    "load_quiz_definition",
    "get_next_session",
    # Quiz Validator exports
    "validate_answer",
    "calculate_score",
    "get_passed_status",
    "identify_weak_areas",
]
