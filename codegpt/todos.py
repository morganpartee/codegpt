from pathlib import Path
import json
import typer
import openai
import os
from refactor import edit_file, send_prompt_to_model
from textwrap import dedent

app = typer.Typer()


def send_prompt_to_model(prompt, model):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(engine=model, prompt=prompt)
    return response


@app.command("do")
def todo(
    file_path_or_raw: str,
    model: str = "text-davinci-003",
    debug: bool = False,
    raw: bool = False,
):
    path = Path(file_path_or_raw)
    if not path.is_file():
        if " " not in file_path_or_raw:
            typer.confirm(
                "Hmm, didn't find a file by that name, want to proceed with plaintext?",
                abort=True,
            )
            raw = True

    language = file_path_or_raw.split(".")[-1]

    if raw:
        code = (
            f"This was copied from a larger piece of code.\n```\n"
            + file_path_or_raw
            + "\n```\n"
        )
        file_path_or_raw = "out.txt"
    else:
        with open(file_path_or_raw, "r") as file:
            code = f"# {file_path_or_raw}\n```{language}\n" + file.read() + "\n```\n"

    instructions = typer.prompt("What do you want done with this code?")
    prompt = dedent(
        f"""
Generate a list of tasks that could be performed to improve the code, according to these instructions:

{instructions}

Your response must be json in this (simplified) schema, with only one object you output:

```json
    {{
    "filename": <filename: string>,
    "todo": <code: string>
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
...`

You are an expert, ensure that your answer is technically correct, well documented and formatted.

:
{code}

"""
    )

    response = send_prompt_to_model(prompt, model)

    if debug:
        with open(file_path_or_raw + ".resp.json", "w") as file:
            response.update({"prompt": prompt})
            file.write(json.dumps(response))

    try:
        todo_list = json.loads(response["choices"][0]["text"])
    except json.JSONDecodeError:
        typer.secho(
            f"Json load failed, writing fail file you can manually work with.",
            color=typer.colors.BRIGHT_RED,
        )
        with open(file_path_or_raw + ".fail.json", "w") as file:
            file.write(json.dumps(response))
        typer.launch(file_path_or_raw + ".fail.json")
        quit()

    todo_file_path = f"{todo_list['filename']}.todo"
    with open(todo_file_path, "w") as file:
        file.write(todo_list["todo"])

    typer.launch(todo_file_path)
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
