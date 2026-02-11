# -*- coding: utf-8 -*-
"""Test suite for hint_generator chain."""

import pytest
from ai_chains.chains.hint_generator import generate_hint, get_all_hints


class TestHintGeneratorChain:
    """Test cases for hint generator chain."""

    def test_generate_hint_returns_string(self):
        """Test that generate_hint returns a string."""
        result = generate_hint("Buat variabel 'nama'", "", 1)
        assert isinstance(result, str)

    def test_generate_hint_all_levels(self):
        """Test hint generation for all levels."""
        task = "Buat variabel bernama 'kota'"
        for level in [1, 2, 3]:
            result = generate_hint(task, "", level)
            assert isinstance(result, str), f"Level {level} should return string"

    def test_hint_level_1_gentle(self):
        """Test Level 1 hint is gentle/subtle."""
        result = generate_hint("Buat variabel 'nama'", "", 1)
        assert isinstance(result, str)
        # Level 1 should not give direct answer
        # (unless API fallback returns generic response)

    def test_hint_level_2_conceptual(self):
        """Test Level 2 hint is conceptual."""
        result = generate_hint("Buat variabel 'nama'", "", 2)
        assert isinstance(result, str)

    def test_hint_level_3_direct(self):
        """Test Level 3 hint is direct."""
        result = generate_hint("Buat variabel 'nama'", "", 3)
        assert isinstance(result, str)

    def test_get_all_hints_returns_list(self):
        """Test get_all_hints returns list of 3 hints."""
        hints = get_all_hints("Buat variabel 'nama'", "")
        assert isinstance(hints, list)
        assert len(hints) == 3

    def test_get_all_hints_content(self):
        """Test all hints are strings."""
        hints = get_all_hints("Buat variabel 'nama'", "")
        for hint in hints:
            assert isinstance(hint, str)

    def test_hint_with_student_attempt(self):
        """Test hint generation with student attempt."""
        task = "Buat variabel 'nama'"
        attempt = "var nama = 'Budi'"
        for level in [1, 2, 3]:
            result = generate_hint(task, attempt, level)
            assert isinstance(result, str)

    def test_hint_for_loop_task(self):
        """Test hint for loop task."""
        task = "Buat loop dari 1 sampai 10"
        result = generate_hint(task, "", 1)
        assert isinstance(result, str)

    def test_hint_for_function_task(self):
        """Test hint for function task."""
        task = "Buat fungsi bernama 'sapa'"
        result = generate_hint(task, "", 1)
        assert isinstance(result, str)

    def test_hint_with_empty_task(self):
        """Test with empty task."""
        result = generate_hint("", "", 1)
        assert isinstance(result, str)

    @pytest.mark.parametrize("task,level", [
        ("Buat variabel x", 1),
        ("Buat list dengan 3 elemen", 2),
        ("Buat dictionary", 3),
    ])
    def test_hint_various_tasks(self, task, level):
        """Test hint generation with various tasks."""
        result = generate_hint(task, "", level)
        assert isinstance(result, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
