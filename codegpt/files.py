import os
import typer
import math
import re
import magic


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
        if backup and os.path.exists(filename):
            with open(filename, "r") as f_in:
                with open(f"{filename}.bak", "w") as f_out:
                    f_out.write(f_in.read())

        # Write the new text to the file
        with open(filename, "w") as f:
            f.write(out["code"])
        if "explanation" in out:
            typer.secho(f"{filename} - " + out["explanation"], color=typer.colors.BLUE)
        

def split_code_into_chunks(paths, chunk_size):
    chunks = {}
    for path in paths:
        if path.is_dir():
            # Crawl the directory and process each file
            for root, _, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    process_file(file_path, chunk_size, chunks)
        else:
            # Process the file directly
            process_file(path, chunk_size, chunks)

    return chunks

def process_file(file_path, chunk_size, chunks):
    # Use the python-magic library to identify the type of the file
    mime = magic.from_file(file_path, mime=True)
    if mime.split("/")[0] != "text":
        # If the file is not a text file, skip it
        return

    with open(file_path, "r") as f:
        code = f.read()

    # Split the code into tokens using a regular expression
    tokens = re.findall(r"\b\w+\b", code)

    # Determine the number of chunks needed
    num_chunks = math.ceil(len(tokens) / chunk_size)

    # Split the tokens into chunks with a hundred token overlap
    for i in range(num_chunks):
        start = i * chunk_size - 100
        if start < 0:
            start = 0
        end = start + chunk_size + 100
        if end > len(tokens):
            end = len(tokens)
        chunk = tokens[start:end]
        if num_chunks > 1:
            # If the file was split into multiple chunks, use a key of the form {filename} - {chunk_num}
            key = f"{file_path.stem} - {i + 1}"
        else:
            # If the file was not split, use the file path as the key
            key = file_path
        if key not in chunks:
            chunks[key] = []
        chunks[key].append(chunk)