import openai
import os
import typer
import json
from textwrap import dedent
from pathlib import Path
from .gpt_interface import send_prompt_to_model
from .handle_input import process_file_path_or_raw


def edit_file(
    file_path_or_raw: str,
    refactor_or_edit_instructions: str,
    explanation_file: str = None,
    model: str = "text-davinci-003",
    debug: bool = False,
    raw: bool = False,
    language: str = None,
):
    """Edit the given file.

    Args:
        file_path_or_raw (str): The path to the file to be refactored or edited, or raw text. If we can't find the file,
        we'll treat it as raw text. Hell yeah that's lazy. If it warns you it didn't find the file, abort.
        refactor_or_edit_instructions (str): Instructions for refactoring or editing the code.
        explanation_file (str, optional): The path to the file to save the explanation. Defaults to None.
        model (str, optional): GPT-3 model to use. Defaults to "text-davinci-003".
        language (str, optional): The language of the code. Defaults to "python".
        debug (bool, optional): If True, save the response from the model in a JSON file. Defaults to False.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    language, file_path, raw_code = process_file_path_or_raw(
        file_path_or_raw, language, raw
    )

    code = f"# {file_path_or_raw}\n```{language}\n{raw_code}\n```"

    # specify the prompt
    prompt = generate_prompt(refactor_or_edit_instructions, code, language)

    # send the prompt to the model
    response = send_prompt_to_model(prompt, model, debug, file_path)

    for f in response:
        typer.secho(f"Writing `{f['filename']}`", fg=typer.colors.BRIGHT_CYAN)
        refactor_and_explain_code(
            f["filename"], f["code"], f["explanation"], explanation_file
        )
        typer.secho(f["explanation"], fg=typer.colors.BRIGHT_GREEN)


def refactor_and_explain_code(
    file_path,
    refactored_code,
    explanation,
    explanation_file=None,
    raw_text: bool = None,
):
    if not raw_text:
        old_file_path = file_path + ".old"
        os.rename(file_path, old_file_path)

    with open(file_path, "w") as file:
        file.write(refactored_code)

    with open(
        explanation_file if explanation_file else file_path + ".explained.txt", "w"
    ) as file:
        file.write(explanation)


def generate_prompt(refactor_or_edit_instructions, code, language):
    """Generate a prompt from the given instructions and code.

    Args:
        refactor_or_edit_instructions (str): Instructions for refactoring or editing the code.
        code (str): The code to be refactored or edited.
        language (str): The language of the code.

    Returns:
        str: The generated prompt.
    """
    return dedent(
        f"""
    {'Refactor' if 'refactor' in refactor_or_edit_instructions.lower() else 'Edit'} the code below, to:
    
    {refactor_or_edit_instructions}

    Your response must be json in this (simplified) schema, with one object in the array for each file you output:

    ```json
    [
        {{
        "explanation": <explanation: string>,
        "filename": <filename: string>,
        "code": <code: string>
        }}
    ]
    ```

    For the `explanation`, explain exactly what you did to the provided code. You must include line numbers when you make changes.
    
    Write it as a succinct bullet list, line numbers first.

    You must return an explanation, even if you do nothing.

    You are an expert, ensure that code is technically correct, well documented and formatted.
    {"Use google docstrings and black formatting."if language == "py" else ""}
    {"This is likely an article or blog post, maintain the authors tone and voice while you edit." if language == "md" else ""}

    You must explain what you did, even if you don't make a change.

    If you're provided a todo list, return that too. Put an X in each box if you could do the task, but leave it empty if you couldn't. Explain why you couldn't! Whitespace is fine in explanations.

    Code:
    {code}
    
"""
    )
