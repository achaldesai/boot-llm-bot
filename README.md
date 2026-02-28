# llm-bot

An LLM-powered bot for automating development tasks.

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

### Activating the Environment

You can activate the virtual environment using:

```bash
source .venv/bin/activate
```

Alternatively, you can run commands directly using `uv run`:

```bash
uv run main.py
```

## Configuration

Create a `.env` file in the root directory and add your configuration:

```env
# Example configuration
API_KEY=your_api_key_here
```
