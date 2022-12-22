import nltk
import openai
import typer
from typing import Dict
from textwrap import dedent
from parse import parse_resp

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    typer.secho("Downloading punkt for nltk... Only once!", fg=typer.colors.GREEN, bold=True)
    nltk.download('punkt', quiet=True)

def confirm_send(prompt, max_tokens=4000, yes=False, silent=False):
    tokens = nltk.word_tokenize(prompt)

    #! Yeah this math is BS, closeish though...
    max_tokens = round(max_tokens - (7 / 4) * len(tokens))

    if silent:
        pass
    elif yes:
        typer.secho(f"This prompt is {len(tokens)}ish tokens, GPT-3 can return {max_tokens}ish.", color=typer.colors.GREEN)
    else:
        typer.confirm(
            f"This prompt is {len(tokens)}ish tokens, are you sure you want to continue?\nThe most GPT-3 can return in response is {max_tokens}ish.",
            default=True,
            abort=True,
        )

    return max_tokens

def send_iffy_edit(prompt: str, code: Dict[str, str], clipboard: bool = False, yes=False) -> str:
    full_prompt = "You are an expert developer. Given the following code:\n\n"

    for filename, code_string in code.items():
        if not clipboard:
            full_prompt += f"\n\nfilename:\n> {filename}\n"
        nl = '\n'
        full_prompt += f"code:\n{nl.join(f'> {x}' for x in code_string.splitlines())}\n\n"

    full_prompt += f"\n\nDo the following: {prompt}"

    if clipboard:
        full_prompt += dedent("""
        
        Answer in the following format:
        
        explanation:
        > <The changes that you made>
        code:
        > <the code to be output line 1>
        > <the code to be output, line n...>""")

    else:
        full_prompt += dedent("""

        You may only output complete files.

        If you add or modify a file, return it in this exact format:

        filename:
        > <the filename to be output>
        explanation:
        > <The changes that you made>
        code:
        > <code line 1>
        > <code line n...>""")

    max_tokens = confirm_send(full_prompt, yes=yes, silent=clipboard)

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=max_tokens,
        n=1,
        temperature=0.5,
    )
    
    try:
        parsed = parse_resp(response)
    except KeyError as e:
        print("ERROR: Response was malformed. Might still be usable, but is likely missing an explanation. Printing >\n")
        print(response["choices"][0]["text"])
    return parsed[0] if clipboard else parsed



if __name__ == "__main__":
    print(send_iffy_edit("Remove usless imports", {'filename': 'hello.py', 'code': """import os
import json
import sys
print("Hello, world!")"""}))
