import nltk
import openai
import os
import typer


def edit_file(
    file_path: str,
    refactor_or_edit_instructions: str,
    explanation_file: str = None,
    model: str = "text-davinci-003",
    debug: bool = False,
):
    """Edit the given file.

    Args:
        file_path (str): The path to the file to be refactored or edited.
        refactor_or_edit_instructions (str): Instructions for refactoring or editing the code.
        explanation_file (str, optional): The path to the file to save the explanation. Defaults to None.
        model (str, optional): GPT-3 model to use. Defaults to "text-davinci-003".
        language (str, optional): The language of the code. Defaults to "python".
        debug (bool, optional): If True, save the response from the model in a JSON file. Defaults to False.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    language = file_path.split(".")[-1]

    # open the file and escape the code as a code block
    with open(file_path, "r") as file:
        code = f"###{file_path}\n```{language}\n" + file.read() + "\n```"

    # specify the prompt
    prompt = generate_prompt(refactor_or_edit_instructions, code, language)
    tokens = nltk.word_tokenize(prompt)

    #! Yeah this math is BS, closeish though...
    max_tokens = round(4097 - (7 / 4) * len(tokens))

    typer.confirm(
        f"This prompt is {len(tokens)} tokens, are you sure you want to continue?\nThe most GPT-3 can return in response is {max_tokens}.",
        default=True,
        abort=True,
    )

    # send the prompt to the model
    response = openai.Completion.create(
        max_tokens=max_tokens,
        engine=model,
        prompt=prompt,
        n=1,
        stop=None,
        temperature=0.6,
    )

    if debug:
        import json

        # write the response
        with open(file_path + ".resp.json", "w") as file:
            file.write(json.dumps(response))

    # print the response from the model
    refactored_code = response["choices"][0]["text"]

    explanation = refactored_code.split("===")[0]
    refactored_code = "".join(refactored_code.split("===")[1:])
    print(explanation)

    old_file_path = file_path + ".old"
    os.rename(file_path, old_file_path)

    # write the refactored code to the original file
    with open(file_path, "w") as file:
        file.write(refactored_code)

    # write the refactored code to the original file
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
    return f"""
    {'Refactor' if 'refactor' in refactor_or_edit_instructions.lower() else 'Edit'} the code below, to: {refactor_or_edit_instructions}

    Write a short summary of the changes made to the code and return the edited code in a new section,
    delimited by '==='. Don't use '===' other than between the sections, and don't add space between sections.

    You are an expert, ensure that code is technically correct, well documented and formatted.
    {"Use google docstrings and black formatting."if language == "py" else ""}
    {"This is likely an article or blog post, maintain the authors tone and voice while you edit." if language == "md" else ""}

    You must explain what you did, even if you don't make a change.

    Code:
    {code}""".strip()
