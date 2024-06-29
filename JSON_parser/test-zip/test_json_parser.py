import os
import sys
import pytest

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from json_parser import JsonParser

# List of test files
invalid_files = [f"fail{i}.json" for i in range(1, 34) if i != 18]
valid_files = [f"pass{i}.json" for i in range(1, 4)]
test_files = invalid_files + valid_files

# Parametrize to run the same test for each file
@pytest.mark.parametrize("test_file", test_files)
def test_json_file(test_file):
    test_path = os.path.join(os.path.dirname(__file__), test_file)
    parser = JsonParser(test_path)
    is_valid = parser.validate()

    if test_file.startswith("fail"):
        assert not is_valid, f"{test_file} should be invalid\nErrors: {parser.error_messages}"
        assert len(parser.error_messages) > 0, f"Expected errors in {test_file}"
    else:
        assert is_valid, f"{test_file} should be valid\nErrors: {parser.error_messages}"
        assert len(parser.error_messages) == 0, f"Unexpected errors in {test_file}"
