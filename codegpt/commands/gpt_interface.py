import nltk
import openai
import typer
from textwrap import dedent


def send_prompt_to_model(prompt, model, debug, file_path):
    """Send the given prompt to the given model.

    Args:
        prompt (str): The prompt to be sent to the model.
        model (str): GPT-3 model to use.

    Returns:
        dict: The response from the model.
    """

    tokens = nltk.word_tokenize(prompt)

    #! Yeah this math is BS, closeish though...
    max_tokens = round(4097 - (7 / 4) * len(tokens))

    typer.confirm(
        f"This prompt is {len(tokens)}ish tokens, are you sure you want to continue?\nThe most GPT-3 can return in response is {max_tokens}ish.",
        default=True,
        abort=True,
    )

    response = openai.Completion.create(
        max_tokens=max_tokens,
        engine=model,
        prompt=prompt + "\n\nREPLY:",
        n=1,
        stop=None,
        temperature=0.6,
    )

    return response
