import openai
import os
import typer
from dotenv import load_dotenv
import nltk

app = typer.Typer()


@app.command()
def refactor(
    file_path: str,
    refactor_instructions: str,
    explanation_file: str = None,
    model: str = "text-davinci-003",
    language: str = "python",
    debug: bool = False,
):
    """Refactor a code file using GPT-3 and provide a human-readable explanation of the changes made.

    Args:
        file_path (str): The path to the file that should be refactored.
        refactor_instructions (str): A prompt specifying the desired changes to the code.
        explanation_file (str, optional): The file path where the human-readable explanation of the changes should be written. Defaults to None.
        model (str, optional): The GPT-3 model to use for generating text. Defaults to "text-davinci-003".
        language (str, optional): The programming language of the file to be refactored. Defaults to "python".
        debug (bool, optional): A flag indicating whether debug information should be written to a file. Defaults to False.

    Returns:
        None
    """
    # load credentials from dotenv file
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # open the file and escape the code as a code block
    with open(file_path, "r") as file:
        code = f"```{language}\n" + file.read() + "\n```"

    # specify the prompt
    prompt = f"""
    Perform the following on the code to follow: {refactor_instructions}
    
    Please provide an extremely succinct human explanation of the changes made to the code
    and return the edited code in a new file, delimited by '==='. Don't use '===' other than
    between the sections, and don't add space between sections either.
    
    Take liberties to fix technical problems if you find them, but make sure to explain it clearly in comments
    and the explanation section, and include line numbers in the explanation section if you do.
    
    Ensure that code is well documented and formatted.
    {" Use google docstrings and black formatting."if language == "python" else ""}
    {code}""".strip()

    tokens = nltk.word_tokenize(prompt)

    typer.confirm(
        f"This prompt is {len(tokens)} tokens, are you sure you want to continue?\nThe most GPT-3 can return in response is {4097 - len(tokens)}.",
        default=True,
        abort=True,
    )

    # send the prompt to the model
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        n=1,
        max_tokens=round(4097 - (7 / 4) * len(tokens)),
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


@app.command()
def edit(
    file_path: str,
    edit_instructions: str,
    explanation_file: str = None,
    model: str = "text-davinci-003",
    language: str = "md",
    debug: bool = False,
):
    # load credentials from dotenv file
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # open the file and escape the code as a code block
    with open(file_path, "r") as file:
        code = f"```{language}\n" + file.read() + "\n```"

    # specify the prompt
    prompt = f"""
    You are going to edit an article. Please provide an extremely succinct human explanation of the changes made
    and return the edited article in a new file, delimited by '==='. Don't use '===' other than
    between the sections, and don't add space between sections either.
    
    Be very careful to maintain the original author's tone, but feel free to take liberties to
    fix coding errors, or to make things more clear. If you modify code, make sure to include a
    line number in the explanation document.

    There may be code blocks in the article, don't edit the code, other than to add comments
    or unless you were told to above. Ensure code blocks have a language marked above.
    
    Do the following to the article below: {edit_instructions}

    {code}""".strip()

    tokens = nltk.word_tokenize(prompt)

    typer.confirm(
        f"This prompt is {len(tokens)} tokens, are you sure you want to continue?\nThe most GPT-3 can return in response is {4097 - len(tokens)}.",
        abort=True,
        default=True,
    )

    # send the prompt to the model
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        n=1,
        max_tokens=round(4097 - (7 / 4) * len(tokens)),
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


@app.command()
def configure():
    """
    Configure the OpenAI secret key for the codegpt CLI.

    If the OPENAI_SECRET_KEY is already set in the environment variables, this command will not do anything.
    Otherwise, it will prompt the user for the secret key and create a .env file with the secret key.

    :param output_path: The path to the output dotenv file (default: .env).
    """
    # check if the secret key is already set in the environment variables
    if "OPENAI_SECRET_KEY" in os.environ:
        print("The OPENAI_SECRET_KEY is already set in the environment variables.")
        return
    else:
        typer.confirm(
            """
We no longer handle this, it felt a little iffy security wise. I recommend setting your API key as an environment variable:
https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety

Windows users can also use `setx` like:

`$ setx OPENAI_SECRET_KEY=<YOUR_API_KEY>`

from an admin console.
        """.strip()
        )


if __name__ == "__main__":
    app()
