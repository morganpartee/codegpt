import os
import typer
import sys

from os.path import dirname

sys.path.append(dirname(__file__))

from commands import unsafe, todos, generate

app = typer.Typer(
    no_args_is_help=True,
)

app.add_typer(
    unsafe.app,
    name="unsafe",
    no_args_is_help=True,
    help="Unsafe commands - edit, varnames, comment",
)

app.add_typer(
    todos.app,
    name="todo",
    no_args_is_help=True,
    help="Todos commands - do (semi-unsafe), list",
)

app.add_typer(
    generate.app, name="gen", no_args_is_help=True, help="Generate commands - docs"
)


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
