import nltk
import openai
import typer

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

models = openai.Model.list()

def confirm_send(prompt, max_tokens=4000):
    tokens = nltk.word_tokenize(prompt)

    #! Yeah this math is BS, closeish though...
    max_tokens = round(max_tokens - (7 / 4) * len(tokens))

    typer.confirm(
        f"This prompt is {len(tokens)}ish tokens, are you sure you want to continue?\nThe most GPT-3 can return in response is {max_tokens}ish.",
        default=True,
        abort=True,
    )

    return max_tokens


def send_completion(prompt, model):
    """Send the given prompt to the given model.

    Args:
        prompt (str): The prompt to be sent to the model.
        model (str): GPT-3 model to use.

    Returns:
        dict: The response from the model.
    """

    max_tokens = confirm_send(prompt)

    return openai.Completion.create(
        engine=model,
        max_tokens=max_tokens,
        prompt=prompt + "\n\nREPLY:",
        n=1,
        temperature=0.7,
    )["data"][0]["text"]


def send_edit(prompt, code):
    """Send the given prompt to the given model.

    Args:
        prompt (str): The prompt to be sent to the model.
        model (str): GPT-3 model to use.

    Returns:
        str: The top result from the model.
    """

    max_tokens = confirm_send(prompt, 8000)
    response = openai.Edit.create(
        model="code-davinci-edit-001",
        input=code,
        instruction=prompt,
        n=1,
        temperature=0.7,
    )

    resp = response["choices"][0]["text"]

    return resp

if __name__ == "__main__":
    print(send_edit("Remove usless imports", """import os
import json
import sys
print("Hello, world!")"""))