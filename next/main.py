import os
import typer
import sys

import prompts
import gpt_interface as gpt
import files

app = typer.Typer(
    no_args_is_help=True,
)


@app.command("edit")
def edit_file(
    instruction: str = typer.Option(
        help="Instructions to edit the file. Keep it short!", default=None
    ),
    filename: str = typer.Option(
        dir_okay=False, help="File to be edited", default=None
    ),
    backup=False,
):
    code = files.load_text(filename)
    result = gpt.send_edit(instruction, code)
    files.write_text(filename, result, backup)
    typer.secho("done", color=typer.colors.BRIGHT_BLUE)


@app.command("quick")
def quick_edit_file(
    filename: str,
    option: prompts.PromptKeys,
    backup=False,
):
    code = files.load_text(filename)
    result = gpt.send_edit(prompts.prompts[option.value], code)
    files.write_text(filename, result, backup)
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

from an admin console.
        """.strip()
        )


if __name__ == "__main__":
    app()
