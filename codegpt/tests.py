import os
from files import write_text


def test_write_text():
    # Test writing text to a file without creating a backup
    filename = "test.txt"
    text = "Hello, world!"
    write_text(filename, text)

    # Check if the file was created and contains the correct text
    assert os.path.exists(filename)
    with open(filename, "r") as f:
        assert f.read() == text

    # Test writing text to a file with backup enabled
    text = "Hello, world!"
    write_text(filename, text, backup=True)

    # Check if the file and backup file were created and contain the correct text
    assert os.path.exists(filename)
    assert os.path.exists(f"{filename}.bak")
    with open(filename, "r") as f:
        assert f.read() == text
    with open(f"{filename}.bak", "r") as f:
        assert f.read() == text

    # Clean up
    os.remove(filename)
    os.remove(f"{filename}.bak")


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
