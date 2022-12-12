import nltk
import openai
import typer
import json
from textwrap import dedent


def send_prompt_to_model(prompt, model, debug, file_path):
    """Send the given prompt to the given model.

    Args:
        prompt (str): The prompt to be sent to the model.
        model (str): GPT-3 model to use.

    Returns:
        dict: The response from the model.
    """
    full_prompt = prompt + (
        "\n\n"
        + dedent(
            """ONLY return valid json in the schema outlined in the instructions, so it may be loaded by python's json.loads.
            You may not return anything outside of the json, or anything not explicitly in the schema.
            The only whitespace allowed is in the values of the entries in your response.
            Do not return any additional whitespace, unless it is required to be valid json. No leading space.

            ONLY RAW VALID JSON. json.loads(response) with your raw text must work! Make sure not to include characters python's json library would reject.

            JSON:
            """
        ).strip()
    )

    tokens = nltk.word_tokenize(full_prompt)

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
        prompt=full_prompt,
        n=1,
        stop=None,
        temperature=0.6,
    )

    if debug:
        with open(file_path + ".resp.json", "w") as file:
            response.update({"prompt": prompt})
            file.write(json.dumps(response))

    try:
        response = json.loads(
            response["choices"][0]["text"].strip().strip("```json").strip("```").strip()
        )
    except json.JSONDecodeError:
        typer.secho(
            f"Json load failed, writing fail file you can manually work with.",
            color=typer.colors.BRIGHT_RED,
        )
        with open(file_path + ".fail.json", "w") as file:
            file.write(json.dumps(response))
        typer.launch(file_path + ".fail.json")
        quit()
    return response
