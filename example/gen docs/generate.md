# .\generate.py

This file contains all the logic for the `docs` command. It is responsible for processing the input and sending the prompt to the GPT-3 model. It also handles the response, writing the generated documentation to the appropriate file.

## Usage

The `docs` command takes two arguments: `file_path_or_raw` and `model`.

### file_path_or_raw

This argument is the path to the file you want to generate documentation for, or the raw code to be documented.

### model

This argument is the name of the GPT-3 model to use for generating the documentation. The default is `text-davinci-003`.

## Options

The `docs` command has two optional arguments: `debug` and `raw`.

### debug

The `debug` argument allows you to enable debugging mode, which will print the request and response from the GPT-3 model to the console.

### raw

The `raw` argument allows you to specify that the `file_path_or_raw` argument is the raw code to be documented, instead of a file path. If this argument is `true`, the `language` argument must also be provided.

### language

The `language` argument is required if the `raw` argument is `true`. It is the language of the raw code being documented.

## Example

Generate documentation for the `generate.py` file, using the `text-davinci-003` model in debugging mode:

```
docs generate.py --model text-davinci-003 --debug
```

Generate documentation for the provided raw code, using the `text-davinci-003` model:

```
docs 'import sys
print(sys.version)' --model text-davinci-003 --raw --language python
```