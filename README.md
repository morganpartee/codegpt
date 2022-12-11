# Codegpt

A tool for using GPT just a little quicker. A nearly truly automated footgun. Learn how to revert with git before trying please.

Posting about progress here:

[![Twitter Follow](https://img.shields.io/twitter/follow/_JohnPartee?style=social)](https://twitter.com/_JohnPartee)

# Getting Started

`pip install codegpt`

And set your openapi API key as an environment variable like they recommend:
[In their docs here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)

Windows users can also use `setx` like:

`$ setx OPENAI_SECRET_KEY=<YOUR_API_KEY>`

from an admin console.

## Be careful! But let's go.

### Now with 10% less footgun!

Try this new command to see how it works:

`codegpt todo do app.py`

It'll prompt you for what needs done, and give you an option to edit the todo list before we attempt to refactor it.

### The rest

The fun stuff is in the `unsafe` command.

Find a file you hate (Back it up! Don't do it live!) and give it a shot.

`codegpt unsafe edit .\helper.py "Break this up into smaller functions where you can. Add google style docstrings. Feel free to rewrite any code doesn't make sense."`

You'll see something like:

```sh
This prompt is 254 tokens, are you sure you want to continue?
The most GPT-3 can return in response is 3843. [y/N]: y

(and after a short wait...)

Explanation: The code has been refactored into smaller functions to improve readability, and Google style docstrings have been added.
```

Other things to try:

- `codegpt unsafe edit` - Try it with anything. Markdown blog posts, js, yaml, python, whatever.
- `codegpt unsafe varnames` - Changes variable names (and supposed to only be variable names...) to be readable
- `codegpt unsafe comment` - Automatically add comments to a file.

Propose endpoints as issues, I've got a few ideas:

- Explain file
- Write tests for file
- Generate SQL query from table spec files
- Generate new file
- Generate documentation from a file

Just remember this is paid - 2 cents per 1k tokens is a lot when you're working on files with a few hundred lines.

And remember to break up what you're working on - Results will be better with less moving parts and things to do.
