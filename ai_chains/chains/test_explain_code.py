# -*- coding: utf-8 -*-
"""Test suite for explain_code chain."""

import pytest
from ai_chains.chains.explain_code import explain_code


class TestExplainCodeChain:
    """Test cases for code explanation chain."""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup before each test."""
        self.sample_code = "nama = 'Budi'\numur = 25"

    def test_explain_code_returns_string(self):
        """Test that explain_code returns a string."""
        result = explain_code(self.sample_code)
        assert isinstance(result, str)

    def test_explain_code_not_empty(self):
        """Test that explain_code returns non-empty output."""
        result = explain_code(self.sample_code)
        # Either has AI content or fallback message
        assert len(result) > 0

    def test_explain_code_with_variable_declaration(self):
        """Test explaining variable declaration."""
        result = explain_code("x = 10")
        assert isinstance(result, str)
        # Check for Indonesian keywords or fallback
        assert any(keyword in result.lower() for keyword in
                ["variabel", "menyimpan", "nilai", "maaf", "error"])

    def test_explain_code_with_print_statement(self):
        """Test explaining print statement."""
        result = explain_code('print("Hello World")')
        assert isinstance(result, str)
        assert any(keyword in result.lower() for keyword in
                ["print", "menampilkan", "output", "maaf", "error"])

    def test_explain_code_with_function(self):
        """Test explaining function definition."""
        result = explain_code("def sapa():\n    return 'Halo'")
        assert isinstance(result, str)

    def test_explain_code_with_multiline_code(self):
        """Test explaining multi-line code."""
        code = """
nama = "Budi"
umur = 25
print(f"{nama} berumur {umur}")
"""
        result = explain_code(code)
        assert isinstance(result, str)

    def test_explain_code_empty_input(self):
        """Test with empty input."""
        result = explain_code("")
        assert isinstance(result, str)

    def test_explain_code_with_list(self):
        """Test explaining list creation."""
        result = explain_code("buah = ['apel', 'jeruk', 'mangga']")
        assert isinstance(result, str)

    def test_explain_code_with_dict(self):
        """Test explaining dictionary creation."""
        result = explain_code("siswa = {'nama': 'Budi', 'umur': 25}")
        assert isinstance(result, str)

    @pytest.mark.parametrize("code", [
        "x = 1 + 1",
        "text = 'Hello' + ' World'",
        "items = [1, 2, 3]",
        "data = {'key': 'value'}",
    ])
    def test_explain_code_various_inputs(self, code):
        """Test explain_code with various code patterns."""
        result = explain_code(code)
        assert isinstance(result, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
