import os
import typer

from refactor import edit_file

app = typer.Typer()


@app.command()
def unsafe(
    task: str,
    file_path: str,
    explanation_file: str = None,
    model: str = "text-davinci-003",
    debug: bool = False,
):
    """
    Refactor the given file according to the specified task.

    :param task: is the most important - The task to perform.

    "varnames" : Changes variable names to be more human readable.
    "comment" : Adds comments to the code, no other changes
    "edit" : A raw interface to send a prompt to gpt3. "Break this up into more functions" or something is fun to try!

    Args:
        task (str): The type of refactoring to perform on the file. Can be "varnames", "comment", or "edit".
        file_path (str): The path to the file to be refactored.
        explanation_file (str, optional): The path to the file to save the explanation. Defaults to None.
        model (str, optional): GPT-3 model to use. Defaults to "text-davinci-003".
        debug (bool, optional): If True, save the response from the model in a JSON file. Defaults to False.
    """
    # Dictionary of instructions for each refactoring task
    refactor_tasks = {
        "varnames": "In the following code, rename variables as you see appropriate for it to be easier to read. Don't touch any of the code otherwise, other than to update comments.",
        "comment": "In the following code, make no code changes but add comments. Keep them succinct, but explain everything you can if it's helpful. Add function or class strings where you can.",
        "edit": "",
    }
    # If the task is "edit", prompt the user for instructions
    if task == "edit":
        refactor_instructions = typer.prompt(
            "Please provide the instructions for editing the file: "
        )
    # Otherwise, look up the instructions in the dictionary
    else:
        refactor_instructions = refactor_tasks[task]
    # Call the edit_file function with the specified instructions
    edit_file(file_path, refactor_instructions, explanation_file, model, debug)


@app.command()
def configure():
    """
    Configure the OpenAI secret key for the codegpt CLI.
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
