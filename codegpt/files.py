import os
import typer
import math
import re


def load_text(filenames):
    out = {}
    for filename in filenames:
        with open(filename, "r") as f:
            out[filename] = f.read()
    return out


def write_text(files, backup=False):
    # If the backup option is specified and the file exists,
    # write the existing file to <filename>.bak
    for i, out in enumerate(files):
        filename = out.get("filename", f"{i}.txt")
        typer.secho(
            f"Hmm, didn't find a filename, writing to {filename}",
            color=typer.colors.MAGENTA,
        )
        if backup and os.path.exists(filename):
            with open(filename, "r") as f_in:
                with open(f"{filename}.bak", "w") as f_out:
                    f_out.write(f_in.read())

        # Write the new text to the file
        with open(filename, "w") as f:
            f.write(out["code"])

        typer.secho(f"{filename} - " + out["explanation"], color=typer.colors.BLUE)


def split_code_into_chunks(folder_path, chunk_size):
    chunks = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r") as f:
            code = f.read()

        # Split the code into tokens using a regular expression
        tokens = re.findall(r"\b\w+\b", code)

        # Determine the number of chunks needed
        num_chunks = math.ceil(len(tokens) / chunk_size)

        # Split the tokens into chunks
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size
            chunk = tokens[start:end]
            chunks.append(chunk)

    return chunks
