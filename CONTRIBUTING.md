# Contributing to Maguru

Thank you for your interest in contributing to Maguru! This document provides guidelines and instructions for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title** describing the bug
- **Description** of what happened
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Clear title** describing the enhancement
- **Detailed description** of the proposed feature
- **Use cases** and benefits
- **Potential implementation** approach (if known)

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Make your changes** following the coding standards
4. **Write tests** for new features (if applicable)
5. **Ensure all tests pass**
6. **Commit your changes** with clear commit messages
7. **Push to your fork** and submit a Pull Request

## 📝 Coding Standards

### Python Code Style

- Follow **PEP 8** guidelines
- Use **meaningful variable and function names**
- Write **docstrings** for functions and classes
- Keep functions **focused and concise**
- Add **type hints** where appropriate

### Code Example

```python
"""
Module for managing user sessions in Maguru.

This module provides functionality for creating, updating,
and retrieving user session data.
"""

from typing import Dict, Optional


def create_session(user_id: str, course_id: str) -> Dict[str, any]:
    """
    Create a new user session.

    Args:
        user_id: Unique identifier for the user
        course_id: ID of the selected course

    Returns:
        Dictionary containing session initialization data

    Example:
        >>> session = create_session("user123", "python_basics")
        >>> print(session["status"])
        'initialized'
    """
    session = {
        "user_id": user_id,
        "course_id": course_id,
        "status": "initialized",
        "progress": 0
    }
    return session
```

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(chatbot): add hint generation system`
- `fix(quiz): correct scoring logic for code completion`
- `docs(readme): update installation instructions`

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_chatbot.py
```

### Writing Tests

- Test files should be named `test_*.py`
- Use descriptive test names
- Follow AAA pattern: Arrange, Act, Assert
- Mock external dependencies (API calls, database)

## 📚 Documentation

### Code Documentation

- Write **clear docstrings** for all public functions and classes
- Include **parameter descriptions** and return types
- Add **usage examples** for complex functions

### Project Documentation

- Update **README.md** for user-facing changes
- Update **docs/** directory for technical documentation
- Keep **CHANGELOG.md** updated for version changes

## 🎨 UI/UX Guidelines

### Streamlit Best Practices

- Use **st.columns()** for layout organization
- Provide **clear labels** for all inputs
- Add **help text** where needed
- Use **appropriate widgets** for the data type
- Include **loading indicators** for long operations

## 🔒 Security

- **Never commit** API keys or sensitive data
- Use **environment variables** for configuration
- Validate **all user inputs**
- Sanitize data before display
- Follow **OWASP guidelines** for security

## 📧 Contact

For questions or discussions:
- Open an **issue** on GitHub
- Start a **discussion** in the Discussions tab

## 🌟 Recognition

Contributors will be acknowledged in the project documentation.

Thank you for contributing to Maguru! 🎉
