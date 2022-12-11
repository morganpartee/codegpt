import nltk
import openai
import os
import typer
import json
from textwrap import dedent
from pathlib import Path


def edit_file(
    file_path_or_raw: str,
    refactor_or_edit_instructions: str,
    explanation_file: str = None,
    model: str = "text-davinci-003",
    debug: bool = False,
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
    path = Path(file_path_or_raw)
    if not path.is_file():
        if " " not in file_path_or_raw:
            typer.confirm(
                "Hmm, didn't find a file by that name, want to proceed with plaintext?",
                abort=True,
            )
    language = file_path_or_raw.split(".")[-1]

    # open the file and escape the code as a code block
    with open(file_path_or_raw, "r") as file:
        code = f"# {file_path_or_raw}\n```{language}\n" + file.read() + "\n```"

    # specify the prompt
    prompt = generate_prompt(refactor_or_edit_instructions, code, language)

    # send the prompt to the model
    response = send_prompt_to_model(prompt, model)

    if debug:
        # write the response
        with open(file_path_or_raw + ".resp.json", "w") as file:
            response.update({"prompt": prompt})
            file.write(json.dumps(response))

    # print the response from the model
    try:
        resp = json.loads(response["choices"][0]["text"])
    except json.JSONDecodeError:
        typer.secho(
            f"Json load failed, writing fail file you can manually work with.",
            color=typer.colors.BRIGHT_RED,
        )
        with open(file_path_or_raw + ".fail.json", "w") as file:
            file.write(json.dumps(response))

        typer.launch(file_path_or_raw + ".fail.json", locate=True)
        quit()

    for f in resp:
        typer.secho(f"Writing `{f['filename']}`", fg=typer.colors.BRIGHT_CYAN)
        refactor_and_explain_code(
            f["filename"], f["code"], f["explanation"], explanation_file
        )
        typer.secho(f["explanation"], fg=typer.colors.BRIGHT_GREEN)


def refactor_and_explain_code(
    file_path, refactored_code, explanation, explanation_file=None
):
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

    For the `explanation`, explain exactly what you did to the provided code. Make sure to include line numbers. Keep it very succinct, in a bullet list.

    You must return an explanation, even if you do nothing.


    You are an expert, ensure that code is technically correct, well documented and formatted.
    {"Use google docstrings and black formatting."if language == "py" else ""}
    {"This is likely an article or blog post, maintain the authors tone and voice while you edit." if language == "md" else ""}

    You must explain what you did, even if you don't make a change.

    Code:
    {code}
    
    ONLY return valid json in the schema outlined in the instructions, so it may be loaded by python's json.loads.
    You may not return anything outside of the json, or anything not explicitly in the schema.
    The only whitespace allowed is in the values of the entries, for the explanation and code.
    Do not return any additional whitespace, unless it is required to be valid json. No leading space.
    Start right on the response line.
    RESPONSE:
    """
    )


def send_prompt_to_model(prompt, model):
    """Send the given prompt to the given model.

    Args:
        prompt (str): The prompt to be sent to the model.
        model (str): GPT-3 model to use.

    Returns:
        dict: The response from the model.
    """
    tokens = nltk.word_tokenize(prompt)

    #! Yeah this math is BS, closeish though...
    max_tokens = round(4097 - (7 / 4) * len(tokens))

    typer.confirm(
        f"This prompt is {len(tokens)}ish tokens, are you sure you want to continue?\nThe most GPT-3 can return in response is {max_tokens}ish.",
        default=True,
        abort=True,
    )

    return openai.Completion.create(
        max_tokens=max_tokens,
        engine=model,
        prompt=prompt,
        n=1,
        stop=None,
        temperature=0.6,
    )
