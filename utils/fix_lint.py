#!/usr/bin/env python3
"""
Auto-fix common flake8 lint errors.
Run: python fix_lint.py
"""

import os
import re
from pathlib import Path


def fix_blank_lines(file_path):
    """Fix E302: expected 2 blank lines, found 1."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    for i, line in enumerate(lines):
        # Check if this is a function/class definition
        if line.strip().startswith(('def ', 'class ')) and i > 0:
            # Check previous non-empty line
            prev_line_idx = i - 1
            while prev_line_idx >= 0 and not lines[prev_line_idx].strip():
                prev_line_idx -= 1
            
            if prev_line_idx >= 0:
                # Count blank lines before this definition
                blank_count = i - prev_line_idx - 1
                
                # If previous line is not a decorator and not inside a class
                prev_line = lines[prev_line_idx].strip()
                if not prev_line.startswith('@') and blank_count < 2:
                    # Check if we're at module level (not inside a class)
                    indent = len(line) - len(line.lstrip())
                    if indent == 0:  # Module level
                        # Add extra blank line
                        fixed_lines.append('\n')
        
        fixed_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)


def fix_unused_variables(file_path):
    """Fix F841: local variable assigned but never used."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace 'except Exception:' with 'except Exception:'
    content = re.sub(r'except\s+(\w+)\s+as\s+e:', r'except \1:', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def fix_fstring_placeholders(file_path):
    """Fix F541: f-string is missing placeholders."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    for line in lines:
        # Replace "text" with "text" if no placeholders
        if '"' in line or "'" in line:
            # Check if there are any {} placeholders
            if '{' not in line:
                line = line.replace('"', '"').replace("'", "'")
        fixed_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)


def fix_continuation_indent(file_path):
    """Fix E128: continuation line under-indented."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    for i, line in enumerate(lines):
        # If line starts with spaces and previous line ends with '('
        if i > 0 and lines[i-1].rstrip().endswith('('):
            # Ensure proper indentation (align with opening parenthesis)
            if line.strip() and not line.strip().startswith('#'):
                # Find the position of '(' in previous line
                prev_line = lines[i-1]
                paren_pos = prev_line.rfind('(')
                if paren_pos > 0:
                    # Indent to align with character after '('
                    expected_indent = paren_pos + 1
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent < expected_indent:
                        line = ' ' * expected_indent + line.lstrip()
        fixed_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)


def main():
    """Run all fixes on Python files."""
    # Get all Python files in project
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.claude', '.kiro'}]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                python_files.append(file_path)
    
    print(f"Found {len(python_files)} Python files")
    
    for file_path in python_files:
        print(f"Fixing {file_path}...")
        try:
            fix_unused_variables(file_path)
            fix_fstring_placeholders(file_path)
            fix_continuation_indent(file_path)
            # fix_blank_lines(file_path)  # This one is tricky, skip for now
        except Exception as error:
            print(f"  Error: {error}")
    
    print("\nDone! Run 'flake8 .' to check remaining issues.")


if __name__ == '__main__':
    main()
