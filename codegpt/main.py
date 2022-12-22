import os
import typer
import json
import logging


import gpt_interface as gpt

import prompts
import files

from typing import List, Optional
from pathlib import Path

app = typer.Typer(
    no_args_is_help=True,
)

app = typer.Typer()


@app.command("do")
def edit_file(
    instruction: str = typer.Argument(
        ...,
        help="Instruction to edit the file(s). Keep it short! Wrap with quotes.",
    ),
    backup: bool = typer.Option(
        False,
        "--backup",
        "-b",
        help="Whether to create a backup of the original file(s).",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Don't ask for confirmation.",
    ),
    raw_code: str = typer.Option(
        None,
        "--raw-code",
        "-c",
        help="Raw code to edit. Overrides filenames. Use quotes to wrap the code.",
    ),
    json_out: bool = typer.Option(
        False, "--json-out", "-j", help="Output the response in raw json format."
    ),
    raw_out: bool = typer.Option(
        False,
        "--raw-out",
        "-r",
        help="Output the raw 'code' from the response and exit the function.",
    ),
        filenames: Optional[List[Path]] = typer.Argument(None, help="File(s) to edit or for context."),
    ):
    """
    Do something given some code for context. Asking for documents, queries, etc. should work okay. Edits are iffy, but work a lot of the time.

    Your code better be in git before you use this. If the instruction is one of the quick prompt options (like 'comment' or 'docs'), it will do that prompt automatically. For more info, run 'codegpt quick --help'.

    FILENAMES: list of filenames to edit. If not provided, will prompt for input.
    INSTRUCTION: the instruction to edit the file(s). Keep it short!
    """
    
    if raw_out or json_out:
        logging.basicConfig(level=logging.CRITICAL)

    if not filenames and not raw_code:
        raise typer.BadParameter(
            "Either --filenames (-f) or --raw-code (-c) must be provided."
        )

    code = {"code": raw_code} if raw_code else files.load_text(filenames)

    if instruction in prompts.prompts:
        instruction = prompts.prompts[instruction]

    result = gpt.send_iffy_edit(instruction, code, yes=yes, clipboard=bool(raw_code))

    if json_out:
        print(json.dumps(result, sort_keys=True, indent=4))
        return

    if raw_out:
        print(result['code'])
        return

    files.write_text(result, backup)
    typer.secho("Done!", color=typer.colors.BRIGHT_BLUE)


@app.command("quick")
def quick_edit_file(
    option: str = typer.Argument(..., help=f"{{{'|'.join(prompts.prompts.keys())}}}"),
    backup: bool = typer.Option(
        False,
        "--backup",
        "-b",
        help="Whether to create a backup of the original file(s).",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Don't ask for confirmation.",
    ),
    raw_code: str = typer.Option(
        None,
        "--raw-code",
        "-c",
        help="Raw code to edit. Overrides filenames. Use quotes to wrap the code.",
    ),
    json_out: bool = typer.Option(
        False, "--json-out", "-j", help="Output the response in raw json format."
    ),
    raw_out: bool = typer.Option(
        False,
        "--raw-out",
        "-r",
        help="Output the raw 'code' from the response and exit the function.",
    ),
    filenames: Optional[List[Path]] = typer.Argument(None, help="File(s) to edit or for context."),
):
    """
    Edit a file using codegpt's built in prompts.

    Arguments for `option`:
    - comment - Adds or updates comments
    - varnames - Makes variable names reasonable
    - ugh - Do anything GPT can to make the code suck less (might break stuff...)
    - docs - Generate (or update) docs, including README.md
    - bugs - Comment in code where the bugs are if GPT sees them (iffy)
    - vulns - Comment in code where the vulns are if GPT sees them (iffy)
    """
    if option not in prompts.prompts:
        raise typer.BadParameter(
            f"{option} is not a valid option. Must be one of {list(prompts.prompts.keys())}"
        )
    
    if not filenames and not raw_code:
        raise typer.BadParameter(
            "Either FILENAMES or --raw-code (-c) must be provided."
        )

    code = {"code": raw_code} if raw_code else files.load_text(filenames)
    result = gpt.send_iffy_edit(
        prompts.prompts[option], code, yes=yes, clipboard=bool(raw_code)
    )

    if json_out:
        print(json.dumps(result, sort_keys=True, indent=4))
        return

    if raw_out: 
        print(result['code'])
        return

    files.write_text(result, backup)
    typer.secho("Done!", color=typer.colors.BRIGHT_BLUE)


@app.command("config")
def config():
    """
    Configuration instructions for the OpenAI secret key for the codegpt CLI.
    """
    # check if the secret key is already set in the environment variables
    if "OPENAI_SECRET_KEY" in os.environ:
        typer.secho(
            "OPENAI_SECRET_KEY is already set in the environment! You probably don't need this.",
            typer.colors.BRIGHT_BLUE,
        )
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
