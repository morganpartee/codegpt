prompts = {
    "comment": "Add or update comments according to the given language's standards. Add or update function, module, or class level comments if they're appropriate.",
    "varnames": "Change variable names, but nothing else, to make the code more readable. For example, instead of using 'x' and 'y', use 'width' and 'height'.",
    "ugh": "Do anything you can to make this code more readable. Add comments, change variable and function names, add whitespace, whatever. Add a readme to explain what the code does and where it could be improved.",
    "docs": "Generate documentation in markdown format for the given files. Make sure to include a README.md for github. If provided markdown files, update them and use their current structure.",
    "bugs": """Find any bugs you can, note them in comments prefixed with BUG:

Before:
def divide(a, b):
    return a / b

After:
def divide(a, b):
    # BUG: This function should check for division by zero.
    return a / b
""",
    "vulns": """Find any vulnerabilities you can, note them in comments prefixed with VULN:

Before:
def set_username(username):
    this.username = username

After:
def set_username(username):
    # VULN: This function should validate the input to prevent injection attacks.
    this.username = username
""",
}
