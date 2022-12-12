# Codegpt

## 0.1.5

A tool for using GPT just a little quicker. A nearly truly automated footgun. Learn how to revert with git before trying please.

Posting about progress here:

[![Twitter Follow](https://img.shields.io/twitter/follow/_JohnPartee?style=social)](https://twitter.com/_JohnPartee)

## Getting Started

`pip install codegpt --upgrade`

And set your openapi API key as an environment variable like they recommend:
[In their docs here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)

Windows users can also use `setx` like:

`$ setx OPENAI_SECRET_KEY=<YOUR_API_KEY>`

from an admin console.

## Be careful! But try this:

Usage
To try Codegpt, you can run the following command:

```bash
codegpt todo do <filename>
```

This will prompt you for a description of what needs to be done and give you the option to edit the todo list before refactoring the code.

Or use the gen command to generate docs.

```bash
codegpt gen docs <filename>
```

For more advanced users, you can use the codegpt unsafe command, which allows you to:

Change variable names

```bash
codegpt unsafe varnames <filename>
```

Add comments to your code automatically

```bash
codegpt unsafe comment <filename>
```

Edit any file

```bash
codegpt unsafe edit <filename> "Break this up into smaller functions where you can. Add google style docstrings. Feel free to rewrite any code doesn't make sense."
```

Keep in mind that using GPT-3 for code generation is paid, with a cost of 2 cents per 1,000 tokens.

Just like with a Jr Dev, it's best to break up your tasks into smaller pieces to improve the results.

Propose endpoints as issues, I've got a few ideas:

- Write tests for file
- Generate SQL query from table spec files
- Generate new file
