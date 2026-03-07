(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> flake8 . --exclude=.git,__pycache__,.claude,node_modules,...
>> 
.\ai_chains\chains\__init__.py:12:1: E302 expected 2 blank lines, found 1
def get_llm():
^
.\ai_chains\chains\ai_greeting.py:11:1: E302 expected 2 blank lines, found 1
def _get_chain():
^
.\ai_chains\chains\ai_greeting.py:19:1: E302 expected 2 blank lines, found 1
def _get_fallback_greeting(student_name: str, course_title: str) -> str:
^
.\ai_chains\chains\ai_greeting.py:33:1: E302 expected 2 blank lines, found 1
def generate_greeting(student_name: str, course_metadata: dict) -> str:
^
.\ai_chains\chains\ai_greeting.py:63:5: F841 local variable 'e' is assigned to but never used
    except Exception as e:
    ^
.\ai_chains\chains\explain_code.py:10:1: E302 expected 2 blank lines, found 1
def _get_chain():
^
.\ai_chains\chains\explain_code.py:18:1: E302 expected 2 blank lines, found 1
def explain_code(code_snippet: str) -> str:
^
.\ai_chains\chains\hint_generator.py:10:1: E302 expected 2 blank lines, found 1
def _get_chain():
^
.\ai_chains\chains\hint_generator.py:18:1: E302 expected 2 blank lines, found 1
def generate_hint(task: str, student_attempt: str, level: int) -> str:
^
.\ai_chains\chains\hint_generator.py:41:1: E302 expected 2 blank lines, found 1
def get_all_hints(task: str, student_attempt: str) -> list:
^
.\ai_chains\chains\qa_chatbot.py:11:1: E302 expected 2 blank lines, found 1
def _get_chain():
^
.\ai_chains\chains\qa_chatbot.py:21:1: E302 expected 2 blank lines, found 1
def answer_question(question: str, session_title: str,
^
.\ai_chains\chains\qa_chatbot.py:22:20: E128 continuation line under-indented for visual indent
                   session_content: str, chat_history: list) -> str:
                   ^
.\ai_chains\chains\qa_chatbot.py:47:1: E302 expected 2 blank lines, found 1
def _format_history(messages: list) -> str:
^
.\ai_chains\chains\quiz_feedback.py:10:1: E302 expected 2 blank lines, found 1
def _get_chain():
^
.\ai_chains\chains\quiz_feedback.py:18:1: E302 expected 2 blank lines, found 1
def generate_feedback(question: str, student_answer: str,
^
.\ai_chains\chains\quiz_feedback.py:19:22: E128 continuation line under-indented for visual indent
                     correct_answer: str, is_correct: bool) -> str:
                     ^
.\ai_chains\chains\quiz_feedback.py:40:5: F841 local variable 'e' is assigned to but never used  
    except Exception as e:
    ^
.\server.py:14:1: F401 'asyncio' imported but unused
import asyncio
^
.\server.py:15:1: F401 'typing.Optional' imported but unused
from typing import Optional, AsyncGenerator
^
.\server.py:15:1: F401 'typing.AsyncGenerator' imported but unused
from typing import Optional, AsyncGenerator
^
.\server.py:19:1: F401 'fastapi.responses.StreamingResponse' imported but unused
from fastapi.responses import StreamingResponse
^
.\server.py:50:1: E302 expected 2 blank lines, found 1
def _with_fallback(func, fallback_msg: str, **kwargs):
^
.\tests\test_ai_chains_simple.py:77:128: E501 line too long (164 > 127 characters)
        "Variabel adalah wadah untuk menyimpan data. Di Python, membuat variabel sangat mudah - cukup tulis nama variabel diikuti tanda sama dengan (=) dan nilai.",
                                                                                                 
                              ^
.\tests\test_ai_chains_simple.py:80:11: F541 f-string is missing placeholders
    print(f"Question: Apa itu variabel?")
          ^
.\tests\test_ai_chains_simple.py:102:11: F541 f-string is missing placeholders
    print(f"Student: Budi")
          ^
.\utils\quiz_validator.py:7:1: F401 'typing.Optional' imported but unused
from typing import Dict, List, Any, Optional
^
.\utils\session_manager.py:9:1: F401 'typing.Optional' imported but unused
from typing import Dict, List, Optional
^
28
(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> 