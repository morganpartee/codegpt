import os


def load_text(filename):
    with open(filename, "r") as f:
        code = f.read()
    return code


def write_text(filename, text, backup=False):
    # If the backup option is specified and the file exists,
    # write the existing file to <filename>.bak
    if backup and os.path.exists(filename):
        with open(filename, "r") as f_in:
            with open(f"{filename}.bak", "w") as f_out:
                f_out.write(f_in.read())

    # Write the new text to the file
    with open(filename, "w") as f:
        f.write(text)
