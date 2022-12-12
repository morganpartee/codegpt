from pathlib import Path
import json
import typer

from .handle_input import process_file_path_or_raw

from commands.refactor import edit_file
from .gpt_interface import send_prompt_to_model

from textwrap import dedent

app = typer.Typer()


@app.command("do")
def todo(
    file_path_or_raw: str,
    model: str = "text-davinci-003",
    debug: bool = False,
    raw: bool = False,
    do_it: bool = True,
    language: str = None,
):
    language, file_path, code = process_file_path_or_raw(
        file_path_or_raw, language, raw
    )

    instructions = typer.prompt("What do you want done with this code?")
    prompt = dedent(
        f"""
Generate a list of tasks that could be performed to improve the code, according to these instructions:

{instructions}

Your response must be json in this (simplified) schema, with only one object you return:

```json
    {{
    "filename": <filename: string>,
    "todo": <todos: string>
    }}
```

For the `todo`, explain exactly what you would to the provided code. Make sure to include line numbers. Keep it succinct, in a bullet list.

Break up large tasks to small ones, especially if there are multiple inputs or outputs.

If you're unsure of anything, ask for clarification in the summary section. The user will be sending this off as a work order, so those help a lot.

Return the `todo` in this format:

`## Summary

<A summary of what you would do>

## Todos

[ ] - todo #1
etc
...`

You are an expert, ensure that your answer is technically correct, well documented and formatted.

{code}
"""
    )

    response = send_prompt_to_model(prompt, model, debug, file_path)

    todo_file_path = f"{response['filename']}.todo"
    with open(todo_file_path, "w") as file:
        file.write(response["todo"])

    typer.launch(todo_file_path)

    if not do_it:
        typer.secho("done.", color=typer.colors.BRIGHT_BLUE)
        return

    while True:
        with open(todo_file_path, "r") as f:
            content = f.read()
        typer.secho(content, color=typer.colors.BRIGHT_BLUE)
        if typer.confirm(
            "Do you want GPT to try the list on this file? n to refresh the list.",
            default=False,
        ):
            break

    edit_file(file_path_or_raw, content, debug=debug, raw=raw)


@app.command("list")
def list_command(
    file_path_or_raw: str,
    model: str = "text-davinci-003",
    debug: bool = False,
    raw: bool = False,
):
    return todo(file_path_or_raw, model, debug, raw, do_it=False)
