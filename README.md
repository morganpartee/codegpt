# Codegpt

A tool for using GPT just a little quicker. A nearly truly automated footgun. Learn how to revert with git before trying please.

# Getting Started

`pip install codegpt`

Then find a file you hate (Back it up! Don't do it live!) and give it a shot.

`codegpt refactor .\helper.py "Break this up into smaller functions where you can. Add google style docstrings. Feel free to rewrite any code doesn't make sense."`

You'll see something like:

```sh
This prompt is 254 tokens, are you sure you want to continue?
The most GPT-3 can return in response is 3843. [y/N]: y

(and after a short wait...)

Explanation: The code has been refactored into smaller functions to improve readability, and Google style docstrings have been added.
```

Other things to try:

- `codegpt edit` - For editing markdown files, including code blocks. Hello, blog editor!
- `codegpt varnames` - Changes variable names (and supposed to only be variable names...) to be readable
- `codegpt comment` - Automatically add comments to a file.

Propose endpoints as issues, I've got a few ideas:

- Explain file
- Write tests for file
- Generate SQL query from table spec files
- Generate new file
- Generate documentation from a file

Just remember this is paid - 2 cents per 1k tokens is a lot when you're working on files with a few hundred lines.

And remember to break up what you're working on - Results will be better with less moving parts and things to do.
