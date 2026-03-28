# Hello MiniMax AI

[MiniMax](https://www.minimax.io/) is an AI company that provides large language models with OpenAI-compatible APIs. Their latest model, **MiniMax-M2.7**, offers a 1M token context window and strong performance across reasoning, coding, and multilingual tasks.

## Key Features

- **OpenAI-Compatible API**: Use the familiar OpenAI SDK with MiniMax models by simply changing the `base_url`
- **1M Context Window**: MiniMax-M2.7 supports up to 1 million tokens of context
- **Multiple Models**: Choose from `MiniMax-M2.7` (latest flagship) or `MiniMax-M2.7-highspeed` (faster variant)

## Getting Started

### 1. Get an API Key

Sign up at [MiniMax Platform](https://platform.minimax.io/) to obtain your API key.

### 2. Set Environment Variable

```bash
export MINIMAX_API_KEY="your_minimax_api_key"
```

### 3. Run the Example

```bash
cd myproject
uv venv
source .venv/bin/activate
uv run minimax
uv run minimax_stream
```

## API Reference

- **Base URL**: `https://api.minimax.io/v1`
- **Models**: `MiniMax-M2.7`, `MiniMax-M2.7-highspeed`
- **Docs**: [MiniMax API Documentation](https://platform.minimax.io/document/introduction)
