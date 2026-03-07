# -*- coding: utf-8 -*-
"""Simple manual testing for all AI chains."""

import sys
sys.path.insert(0, '.')

print("=" * 60)
print("Testing Maguru AI Chains")
print("=" * 60)

# Test 1: Code Explanation
print("\n[TEST 1] Code Explanation Chain")
print("-" * 40)
try:
    from ai_chains.chains.explain_code import explain_code

    code = "nama = 'Budi'\numur = 25"
    result = explain_code(code)
    print(f"Input code:\n{code}\n")
    print(f"Output:\n{result}")
    print("[PASS] Test 1 completed")
except Exception as e:
    print(f"[FAIL] Test 1: {e}")

# Test 2: Hint Generator
print("\n" + "=" * 60)
print("[TEST 2] Hint Generator Chain")
print("-" * 40)
try:
    from ai_chains.chains.hint_generator import generate_hint

    task = "Buat variabel bernama 'kota'"
    attempt = ""

    for i in range(1, 4):
        hint = generate_hint(task, attempt, i)
        print(f"\nLevel {i}:")
        print(hint)
    print("[PASS] Test 2 completed")
except Exception as e:
    print(f"[FAIL] Test 2: {e}")

# Test 3: Quiz Feedback
print("\n" + "=" * 60)
print("[TEST 3] Quiz Feedback Chain")
print("-" * 40)
try:
    from ai_chains.chains.quiz_feedback import generate_feedback

    # Test correct answer
    print("\n[Correct Answer Test]")
    feedback = generate_feedback(
        "Apa output print(2+2)?", "4", "4", True
    )
    print(f"Feedback: {feedback}")

    # Test incorrect answer
    print("\n[Incorrect Answer Test]")
    feedback = generate_feedback(
        "Apa output print(2+2)?", "5", "4", False
    )
    print(f"Feedback: {feedback}")
    print("[PASS] Test 3 completed")
except Exception as e:
    print(f"[FAIL] Test 3: {e}")

# Test 4: Q&A Chatbot
print("\n" + "=" * 60)
print("[TEST 4] Q&A Chatbot Chain")
print("-" * 40)
try:
    from ai_chains.chains.qa_chatbot import answer_question

    answer = answer_question(
        "Apa itu variabel?",
        "Pengenalan Variabel",
        "Variabel adalah wadah untuk menyimpan data. Di Python, membuat variabel sangat mudah - cukup tulis nama variabel diikuti tanda sama dengan (=) dan nilai.",
        []
    )
    print(f"Question: Apa itu variabel?")
    print(f"Answer:\n{answer}")
    print("[PASS] Test 4 completed")
except Exception as e:
    print(f"[FAIL] Test 4: {e}")

# Test 5: AI Greeting
print("\n" + "=" * 60)
print("[TEST 5] AI Greeting Chain")
print("-" * 40)
try:
    from ai_chains.chains.ai_greeting import generate_greeting

    course = {
        "title": "Python Basics",
        "learning_objectives": [
            "Memahami variabel",
            "Belajar tipe data"
        ]
    }

    greeting = generate_greeting("Budi", course)
    print(f"Student: Budi")
    print(f"Course: {course['title']}")
    print(f"Greeting:\n{greeting}")
    print("[PASS] Test 5 completed")
except Exception as e:
    print(f"[FAIL] Test 5: {e}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
