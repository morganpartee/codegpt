import typer
from textwrap import dedent

from refactor import edit_file


app = typer.Typer()


@app.command()
def varnames(
    file_path_or_raw: str,
    refactor_instructions: str = "In the following code, rename variables as you see appropriate for it to be easier to read. Don't touch any of the code otherwise, other than to update comments.",
    explanation_file: str = None,
    model: str = "text-davinci-003",
    debug: bool = False,
):
    edit_file(file_path_or_raw, refactor_instructions, explanation_file, model, debug)


@app.command()
def comment(
    file_path_or_raw: str,
    refactor_instructions: str = None,
    explanation_file: str = None,
    model: str = "text-davinci-003",
    debug: bool = False,
):
    if not refactor_instructions:
        refactor_instructions = dedent(
            """Add comments where helpful, but make no code changes
    If you think you see a bug, say so in a comment starting with `BUG: `
    Keep them succinct, but explain everything you can if it's helpful.
    Add function or class string comments where you can figure out what a function does.
    If you're unsure, note it in the explanation, and leave a placeholder comment with
    as much as you can figure out to make it easier for a user to do."""
        )
    edit_file(file_path_or_raw, refactor_instructions, explanation_file, model, debug)


@app.command()
def edit(
    file_path_or_raw: str,
    edit_instructions: str,
    explanation_file: str = None,
    model: str = "text-davinci-003",
    debug: bool = False,
):
    edit_file(file_path_or_raw, edit_instructions, explanation_file, model, debug)
