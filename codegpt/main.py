import os
import typer

import prompts
import gpt_interface as gpt
import files

from typing import List
from pathlib import Path

app = typer.Typer(
    no_args_is_help=True,
)

app = typer.Typer()

@app.command("do")
def edit_file(
    filenames: List[Path] = typer.Argument(
        None, help="List of filenames to edit. If not provided, will prompt for input.",
    ),
    instruction: str = typer.Option(
        None, '--instruction', '-i', help="Instruction to edit the file(s). Keep it short!",
    ),
    backup: bool = typer.Option(
        False, "--backup", "-b", help="Whether to create a backup of the original file(s).",
    ),
    ):
    """
    Edit one or more files using codegpt.

    FILENAMES: list of filenames to edit. If not provided, will prompt for input.
    INSTRUCTION: the instruction to edit the file(s). Keep it short!
    """
    if not filenames:
        filenames = typer.prompt("Enter the filenames to edit, separated by spaces").split()
    code = files.load_text(filenames)
    result = gpt.send_iffy_edit(instruction, code)
    files.write_text(result, backup)
    typer.secho("Done!", color=typer.colors.BRIGHT_BLUE)


@app.command("quick")
def quick_edit_file(
    filename: str,
    option: prompts.PromptKeys,
    backup=False,
    ):
    """
    Edit a file using codegpt's built in prompts
    """
    code = files.load_text(filename)
    result = gpt.send_iffy_edit(prompts.prompts[option.value], code)
    files.write_text(result, backup)
    typer.secho("done", color=typer.colors.BRIGHT_BLUE)


@app.command()
def config():
    """
    Configuration instructions for the OpenAI secret key for the codegpt CLI.
    """
    # check if the secret key is already set in the environment variables
    if "OPENAI_SECRET_KEY" in os.environ:
        print("The OPENAI_SECRET_KEY is already set in the environment variables.")
        return
    else:
        typer.confirm(
            """
I recommend setting your API key as an environment variable:
https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety

Windows users can also use `setx` like:

`$ setx OPENAI_SECRET_KEY=<YOUR_API_KEY>`

from an admin console.""".strip()
        )


if __name__ == "__main__":
    app()
