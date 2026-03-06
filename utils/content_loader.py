"""Content loader for Maguru MVP.

This module provides functions to load course content from YAML and
Markdown files in the data/courses directory.
"""

import yaml
from typing import Dict, List, Optional


def load_course_metadata(course_id: str) -> Optional[Dict]:
    """Load course YAML file.

    Args:
        course_id: Course identifier (e.g., "python_basics")

    Returns:
        Dict with keys: id, title, description, difficulty, modules, learning_objectives
        None if file not found or malformed
    """
    filepath = f"data/courses/{course_id}/course.yaml"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data if data is not None else None
    except (FileNotFoundError, yaml.YAMLError, IOError):
        return None


def load_module_list(course_id: str) -> List[str]:
    """Get all modules for a course.

    Args:
        course_id: Course identifier

    Returns:
        List of module IDs from course metadata
        Empty list if course not found or modules key missing
    """
    metadata = load_course_metadata(course_id)
    if metadata is None:
        return []
    modules = metadata.get("modules", [])
    return modules if isinstance(modules, list) else []


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
    filepath = f"data/courses/{course_id}/modules/{module_id}/sessions/{session_id}.md"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, IOError):
        return None


def load_quiz_definition(course_id: str, module_id: str, quiz_id: str) -> Optional[Dict]:
    """Load quiz YAML file.

    Args:
        course_id: Course identifier
        module_id: Module identifier
        quiz_id: Quiz identifier (accepted for API consistency, not used in path)

    Returns:
        Dict with keys: id, title, passing_score, time_limit_minutes, questions
        None if file not found or malformed
    """
    filepath = f"data/courses/{course_id}/modules/{module_id}/quiz.yaml"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data if data is not None else None
    except (FileNotFoundError, yaml.YAMLError, IOError):
        return None


def get_next_session(course_id: str, module_id: str, current_session_id: str) -> Optional[str]:
    """Determine next session in learning path.

    Args:
        course_id: Course identifier
        module_id: Module identifier
        current_session_id: Current session identifier

    Returns:
        Next session ID in module's session list
        None if current session is last or module not found
    """
    module_path = f"data/courses/{course_id}/modules/{module_id}/module.yaml"
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            module_data = yaml.safe_load(f)
            if module_data is None:
                return None

            sessions = module_data.get("sessions", [])
            if not isinstance(sessions, list):
                return None

            try:
                current_index = sessions.index(current_session_id)
                if current_index + 1 < len(sessions):
                    return sessions[current_index + 1]
                return None
            except ValueError:
                return None
    except (FileNotFoundError, yaml.YAMLError, IOError):
        return None
