import typer
import os
import re
import math
import gpt_interface as gpt
import files

app = typer.Typer()


@app.command()
def generate_documentation(
    filenames: List[Path] = typer.Argument(
        ...,
        help="List of filenames or folders to generate documentation for. If not provided, will prompt for input.",
    ),
    chunk_size: int = typer.Option(2000, help="Maximum number of tokens per chunk."),
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
        help="Raw code to generate documentation for. Overrides filenames. Use quotes to wrap the code.",
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
):
    """
    Generate documentation from a folder of code files.

    FILENAMES: list of filenames or folders to generate documentation for. If not provided, will prompt for input.
    """
    if not filenames and not raw_code:
        raise typer.BadParameter(
            "Either filenames or --raw-code (-c) must be provided."
        )

    if filenames:
        # Iterate over the provided filenames or folders
        for file_or_folder in filenames:
            # If the path is a folder, recursively crawl it
            if file_or_folder.is_dir():
                # Recursively crawl the folder
                for root, dirs, files in os.walk(file_or_folder):
                    for filename in files:
                        # Skip non-code files
                        if not filename.endswith(
                            (
                                ".py",
                                ".c",
                                ".cpp",
                                ".java",
                                ".rs",
                                "js",
                                "jsx",
                                "ts",
                                "tsx",
                                "html",
                                "css",
                                "scss",
                                "sass",
                                "less",
                                "json",
                            )
                        ):
                            continue

                        file_path = os.path.join(root, filename)
                        with open(file_path, "r") as f:
                            code = f.read()

                        # If the code is too large to send at once, split it into chunks
                        if len(code) > chunk_size:
                            chunks = split_code_into_chunks(code, chunk_size)
                            doc = ""
                            for chunk in chunks:
                                # Send the chunk to the documentation generator
                                doc_chunk = gpt.send_iffy_edit("docs", {"code": chunk})
                                # Process the response and add it to the final documentation
