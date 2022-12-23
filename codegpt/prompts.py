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

nl = '\n'

def generate_mind_map_prompt(docs):
    return dedent(f"""
    Create a mindmap from the files below:

    {nl.join([f'```md{nl+doc+nl}```]n' for doc in docs])}

    1. Identify the relationships between the documents and any important bugs, vulnerabilities, or ideas that emerge in the summary documents.
    2. For each file, create a 'file' node with the following information: id, x and y coordinates, width and height, type ('file'), and file name.
    3. If the summary includes bugs, vulnerabilities, or ideas, create a 'text' node for each one and connect it to the relevant file node with an edge. In each 'text' node, set the type to 'text' and include the text of the bug, vulnerability, or idea as the value for the 'text' key.
    4. Add a 'text' node to the 'file' node with a summary of the important parts of the file contents not yet covered, with a markdown header.
    Use the following schema to send me the mindmap layout as YAML:

    nodes:
      - id: <arbitrary unique ID>
        x: <x coordinate>
        y: <y coordinate>
        width: <node width>
        height: <node height>
        type: file/text
        file: <node file name> (for file nodes only)
        text: <node text> (for text nodes only)
    edges:
      - id: <edge ID>
        fromNode: <ID of node the edge starts from>
        fromSide: <side of starting node that the
        toNode: <ID of node the edge ends at>
        toSide: <side of ending node that the edge is connected to>

    Remember, the goal is to create a mindmap that represents the relationships between the documents,
    and the problems and improvements we can make with them to guide us.

    Use the nodes and edges to show how it is all connected.""")
