from textwrap import dedent

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


def generate_review_instructions(filename, code):
    instructions = dedent(
        f"""
    Please review the code in the file "{filename}" and document your findings in a markdown file. The code is shown below for reference:
    
    ```
    {code}
    ```
    
    In your markdown file, please include the following information:
    
    1. A summary of the purpose of the file and its contents.
    2. A list of all classes and functions defined in the file, along with a brief description of their purpose.
    3. A list of any external dependencies used in the file, including any libraries or modules imported from outside the project.
    4. Any bugs or issues you identified while reviewing the code.
    5. Any areas of the code that you consider to be particularly well-written or poorly-written, and why.
    
    Please also include any questions or comments you have about the code in your markdown file.
    
    When you have finished reviewing the code and documenting your findings, please submit your markdown file for review.
    
    Here is a sample markdown file format you can follow:
    
    ```md
    # Code Review: {filename}
    
    ## Summary
    
    [Insert summary of the purpose of the file and its contents here.]
    
    ## Classes and Functions
    
    [Insert a list of all classes and functions defined in the file, along with a brief description of their purpose.]
    
    ## External Dependencies
    
    [Insert a list of any external dependencies used in the file, including any libraries or modules imported from outside the project.]
    
    ## Bugs and Issues
    
    [Insert any bugs or issues you identified while reviewing the code.]
    
    ## Code Quality
    
    [Insert any comments you have on the quality of the code, including any areas that you consider to be particularly well-written or poorly-written, and why.]
    
    ## Questions and Comments
    
    [Insert any questions or comments you have about the code.]
    ```
    
    You are an expert, senior developer, give helpful feedback if you find problems. Return your whole response, markdown formatted for github, below.

    Review Doc:
    ```md
    """
    )
    return instructions
