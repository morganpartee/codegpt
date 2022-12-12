import typer
from pathlib import Path


def process_file_path_or_raw(file_path_or_raw: str, language: str, raw: str):
    path = Path(file_path_or_raw)
    if not raw and not path.is_file():
        if " " not in file_path_or_raw:
            typer.confirm(
                "Hmm, didn't find a file by that name, want to proceed with plaintext?",
                abort=True,
            )
            raw = True

    if raw:
        language = language or ""
        file_path = "out.txt"
        raw_code = file_path_or_raw
    else:
        language = file_path_or_raw.split(".")[-1]
        file_path = file_path_or_raw
        with open(file_path_or_raw, "r") as f:
            raw_code = f.read()

    # Handle copied code and code blocking
    if raw:
        code = (
            f"This was copied from a larger piece of code.\n```\n"
            + file_path_or_raw
            + "\n```\n"
        )
    else:
        code = f"# {file_path_or_raw}\n```{language}\n{raw_code}\n```\n"

    return language, file_path, code
