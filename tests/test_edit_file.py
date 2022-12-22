from main import app

from typer.testing import CliRunner

run = CliRunner()


def test_edit_file_add_comment():
    # Set up the test inputs
    instruction = "Add one comment with a '#'"
    raw_code = "def foo():\n    print('Hello, world!')"

    # Call the function being tested
    result = run.invoke(app, ['do', instruction, "--yes", "--raw-out", "--raw-code", f"'{raw_code}'"])

    # Use a regex to match the output of the function
    assert "#" in result.stdout
    assert "def foo():" in result.stdout
    assert "print('Hello, world!')" in result.stdout


def test_varnames():
    # Set up the test inputs and expected outputs
    instruction = "varnames"
    raw_code = """
    v0 = 0.2
    a = 2
    n = 21  # No of t values for plotting

    t = np.linspace(0, 2, n+1)
    s = v0*t + 0.5*a*t**2
    """

    # Call the function being tested
    result = run.invoke(app, ['do', instruction, "--yes", "--raw-out", "--raw-code", f"'{raw_code}'"])

    assert 'v0 = 0.2' in result.stdout
    assert 'a = 2' not in result.stdout
    assert 'n = 21' not in result.stdout
    assert 't = np.linspace(0, 2, n+1)' not in result.stdout
    assert's = v0*t + 0.5*a*t**2' not in result.stdout

if __name__ == "__main__":
    import pytest
    
    pytest.main([__file__])
