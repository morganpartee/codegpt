This is the codegpt CLI. It provides a few commands to help you work with OpenAI's GPT-3 API.

## Commands

### unsafe
This command runs the `unsafe` command from the OpenAI CLI. This allows you to run operations without having to set up an OpenAI secret key.

### todo
This command runs the `todo` command from the OpenAI CLI. This allows you to list and manage your pending OpenAI tasks.

### generate
This command runs the `generate` command from the OpenAI CLI. This allows you to generate text from GPT-3.

## Usage
To use the codegpt CLI, simply run the following command: 

`python main.py <command> <args>`

where `<command>` is one of the commands listed above and `<args>` are the arguments to the command.

For more information on a particular command, you can use the `--help` flag.

For example: `python main.py generate --help`