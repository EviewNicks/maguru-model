"""Simple test script for AI greeting chain.

This script tests the ai_greeting.generate_greeting() function
to verify it works correctly with real API calls.
"""

import os
from dotenv import load_dotenv

# Add parent directory to path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_chains import ai_greeting
from utils.content_loader import load_course_metadata


def test_greeting():
    """Test AI greeting generation with actual course data."""
    load_dotenv()

    print("=" * 50)
    print("Testing AI Greeting Chain")
    print("=" * 50)

    # Load actual course metadata
    course_id = "python_basics"
    metadata = load_course_metadata(course_id)

    if metadata is None:
        print("❌ Gagal memuat course metadata")
        return

    print(f"\n✅ Course metadata dimuat:")
    print(f"   ID: {metadata.get('id')}")
    print(f"   Title: {metadata.get('title')}")
    print(f"   Description: {metadata.get('description')}")
    print(f"   Difficulty: {metadata.get('difficulty')}")

    # Test with sample student name
    student_name = "Budi"
    print(f"\n👤 Student: {student_name}")

    try:
        print("\n🔄 Memanggil ai_greeting.generate_greeting()...")

        greeting = ai_greeting.generate_greeting(student_name, metadata)

        print("\n✅ Greeting berhasil dihasilkan:")
        print("-" * 40)
        print(greeting)
        print("-" * 40)

        # Verify greeting contains key elements
        assert student_name in greeting, f"❌ Greeting tidak berisi nama '{student_name}'"
        assert metadata.get('title') in greeting, f"❌ Greeting tidak berisi judul kursus"

        print("\n✅ Semua assertion passed!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nIni mungkin karena:")
        print("   1. OPENROUTER_API_KEY tidak diset")
        print("   2. ZAI_API_KEY tidak diset")
        print("   3. Masalah koneksi API")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    test_greeting()
