# Codegpt

## 0.3

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

## Your first (safe) command

One cool thing is generating documentation. GPT-3 has a token limit of 4000 for completions, so larger files will be chunked up.

```bash
codegpt docs <paths>
```

And it'll generate docs, one per file. This is great when you're coming into a codebase you've never seen before.

## Unsafe Commands

Everything else can modify files. Have someone hold your beer and try some of these (after you check it into git):

Usage
To try Codegpt, you can run the following command:

```bash
codegpt do <instructions (quoted)> -f readme.md 
```

It can do basically anything. Try handing in some files for context and telling it to generate something new - SQL queries, new features, documentation, whatever.

Or use the quick command to do some neat stuff, like:

Generate docs

```bash
codegpt quick docs <filenames>
```

Change variable names to be more readable

```bash
codegpt quick varnames <filenames>
```

Add comments to your code automatically

```bash
codegpt quick comment <filenames>
```

Check for bugs (iffy, but worth a shot)

```bash
codegpt quick bugs <filenames>
```

Check for vulnerabilities (even more iffy, but worth a shot)

```bash
codegpt quick vulns <filenames>
```

Try to make code less miserable

```bash
codegpt quick ugh <filenames>
```

Keep in mind that using GPT-3 for code generation is paid, with a cost of 2 cents per 1,000 tokens.

Just like with a Jr Dev, it's best to break up your tasks into smaller pieces to improve the results.
