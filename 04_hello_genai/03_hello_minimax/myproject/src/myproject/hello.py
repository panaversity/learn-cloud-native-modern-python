from openai import OpenAI
import os


def minimax():
    """Send a chat completion request to MiniMax AI."""
    client = OpenAI(
        api_key=os.environ.get("MINIMAX_API_KEY", ""),
        base_url="https://api.minimax.io/v1",
    )

    response = client.chat.completions.create(
        model="MiniMax-M2.7",
        messages=[{"role": "user", "content": "Hello, how are you?"}],
        temperature=0.7,
    )

    print(response.choices[0].message.content)


def minimax_stream():
    """Send a streaming chat completion request to MiniMax AI."""
    client = OpenAI(
        api_key=os.environ.get("MINIMAX_API_KEY", ""),
        base_url="https://api.minimax.io/v1",
    )

    stream = client.chat.completions.create(
        model="MiniMax-M2.7",
        messages=[{"role": "user", "content": "Tell me a fun fact about octopuses."}],
        temperature=0.7,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print()
