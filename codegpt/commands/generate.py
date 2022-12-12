# .\generate.py
from pathlib import Path
import json
import typer

from .gpt_interface import send_prompt_to_model
from .handle_input import process_file_path_or_raw

from textwrap import dedent

app = typer.Typer()


@app.command("docs")
def gendocs(
    file_path_or_raw: str,
    model: str = "text-davinci-003",
    debug: bool = False,
    raw: bool = False,
    language: str = None,
):
    language, file_path, raw_code = process_file_path_or_raw(
        file_path_or_raw, language, raw
    )

    if raw:
        code = f"This was copied from a larger piece of code.\n```{language or ''}\n{raw_code}\n```\n"
    else:
        code = f"# {file_path}\n```{language}\n{raw_code}\n```\n"

    instructions = typer.prompt("What do you want documented?")
    prompt = dedent(
        f"""
Generate documentation in (github style unless told otherwise) markdown format following the following instructions:

{instructions}

Your response must be json in this (simplified) schema, with one object per file you wish to output:

```json
    [{{
    "filename": <filename: string>,
    "doc": <documentation: string>
    }}]
```

You are an expert, ensure that your answer is technically correct, succinct, well documented and formatted.

{code}

"""
    )

    response = send_prompt_to_model(prompt, model, debug, file_path)

    for doc in response:
        doc_file_path = f"{doc['filename']}.md"
        with open(doc_file_path, "w") as file:
            file.write(doc["doc"])
