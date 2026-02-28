# llm-bot

An LLM-powered bot for automating development tasks, built with the Google Gemini API.

## Features

- **AI-Powered Coding Assistant**: Uses the `gemini-2.5-flash` model to understand and execute complex development tasks.
- **Tool Integration**: Equipped with a suite of tools for file system interaction and code execution.
- **Secure Execution**: Tools are designed with path normalization and restricted to a specific working directory (`./calculator`).

## LLM Capabilities

The bot leverages Gemini's function-calling capabilities to perform the following actions:

- **`get_files_info`**: Lists files and directories, providing metadata such as file sizes.
- **`get_file_content`**: Reads the content of files (truncated at 10,000 characters to manage context window).
- **`write_file`**: Creates new files or overwrites existing ones with provided content.
- **`run_python_file`**: Executes Python scripts and captures their standard output and error.

## Architecture

- `main.py`: The entry point that manages the conversation loop, tool registration, and response processing.
- `functions/`: Contains individual tool implementations and their corresponding JSON schemas for the LLM.
- `prompts.py`: Defines the system instruction that shapes the bot's behavior and persona.
- `config.py`: Centralized configuration for operational limits like `MAX_CHARS` and `MAX_MODEL_ITERATIONS`.

## Setup

This project uses `uv` for package management.

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed on your machine.
- Python 3.13 or higher.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd llm-bot
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   uv sync
   ```

### Configuration

Create a `.env` file in the root directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

### Usage

Run the bot with a prompt:

```bash
uv run main.py "your task description"
```

Use the `--verbose` flag for more detailed output:

```bash
uv run main.py "your task description" --verbose
```

### Activating the Environment (Optional)

You can activate the virtual environment using:

```bash
source .venv/bin/activate
```
