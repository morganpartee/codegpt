import openai
import os
import typer
from dotenv import load_dotenv
import nltk

app = typer.Typer()

load_dotenv()


@app.command()
def refactor(
    file_path: str,
    refactor_instructions: str,
    explanation_file: str = None,
    model: str = "text-davinci-003",
    language: str = "python",
    debug: bool = False,
):
    # load credentials from dotenv file
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # open the file and escape the code as a code block
    with open(file_path, "r") as file:
        code = f"```{language}\n" + file.read() + "\n```"

    # specify the prompt
    prompt = f"{refactor_instructions}\n\nPlease provide an extremely succinct human explanation of the changes made to the code and return the refactored code in a new file, delimited by '==='. Don't use '===' other than between the sections, and don't add space between sections either.\n\n{code}"

    tokens = nltk.word_tokenize(prompt)

    typer.confirm(
        f"This prompt is {len(tokens)} tokens, are you sure you want to continue?\nThe most GPT-3 can return in response is {4097 - len(tokens)}.",
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
def configure(
    output_path: str = typer.Option(".env", help="The path to the output dotenv file.")
):
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

    # prompt the user for the secret key and obscure it

    # prompt the user for the secret key and obscure it
    secret_key = typer.prompt("Enter your OpenAI secret key:", hide_input=True)

    # create the .env file with the secret key
    with open(output_path, "w") as file:
        file.write(f"OPENAI_SECRET_KEY={secret_key}")


if __name__ == "__main__":
    app()
