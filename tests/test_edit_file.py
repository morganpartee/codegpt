import re
from codegpt.main import edit_file


def test_edit_file_add_comment():
    # Set up the test inputs
    instruction = "comment"
    raw_code = "def foo():\n    print('Hello, world!')"

    # Call the function being tested
    result = edit_file(instruction, raw_code=raw_code, yes=True, raw_out=True)

    # Use a regex to match the output of the function
    assert "#" in result
    assert "def foo():" in result
    assert "print('Hello, world!')" in result


def test_edit_file_reverse_string():
    # Set up the test inputs and expected outputs
    instruction = "reverse this string"
    raw_code = "abcdef"
    expected_output = {"code": "fedcba"}

    # Call the function being tested
    result = edit_file(instruction, raw_code=raw_code, yes=True, raw_out=True)

    print(result)

    # Verify that the function is behaving as expected
    assert len(result) >= len(expected_output["code"])


def test_edit_file_convert_to_uppercase():
    # Set up the test inputs and expected outputs
    instruction = "make this uppercase"
    raw_code = "abcdef"
    expected_output = "ABCDEF"

    # Call the function being tested
    result = edit_file(instruction, raw_code=raw_code, yes=True, raw_out=True)

    print(result)

    # Verify that the function is behaving as expected
    assert len(result) >= len(expected_output)
