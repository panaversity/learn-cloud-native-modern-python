"""Integration tests for MiniMax hello world example.

These tests make real API calls to MiniMax and require MINIMAX_API_KEY to be set.
Skip with: pytest -m "not integration"
"""

import os
import unittest

import pytest

MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
SKIP_REASON = "MINIMAX_API_KEY not set"


@pytest.mark.integration
class TestMiniMaxIntegration(unittest.TestCase):
    """Integration tests that call the real MiniMax API."""

    @unittest.skipUnless(MINIMAX_API_KEY, SKIP_REASON)
    def test_minimax_chat_completion(self):
        """Real API call should return a non-empty response."""
        from openai import OpenAI

        client = OpenAI(
            api_key=MINIMAX_API_KEY,
            base_url="https://api.minimax.io/v1",
        )

        response = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[{"role": "user", "content": "Say hello in one word."}],
            temperature=0.7,
            max_tokens=10,
        )

        self.assertIsNotNone(response.choices)
        self.assertGreater(len(response.choices), 0)
        self.assertIsNotNone(response.choices[0].message.content)
        self.assertGreater(len(response.choices[0].message.content.strip()), 0)

    @unittest.skipUnless(MINIMAX_API_KEY, SKIP_REASON)
    def test_minimax_streaming(self):
        """Real streaming API call should yield content chunks."""
        from openai import OpenAI

        client = OpenAI(
            api_key=MINIMAX_API_KEY,
            base_url="https://api.minimax.io/v1",
        )

        stream = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[{"role": "user", "content": "Say hi."}],
            temperature=0.7,
            max_tokens=10,
            stream=True,
        )

        collected = []
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                collected.append(chunk.choices[0].delta.content)

        full_response = "".join(collected)
        self.assertGreater(len(full_response.strip()), 0)

    @unittest.skipUnless(MINIMAX_API_KEY, SKIP_REASON)
    def test_minimax_highspeed_model(self):
        """MiniMax-M2.7-highspeed model should also work."""
        from openai import OpenAI

        client = OpenAI(
            api_key=MINIMAX_API_KEY,
            base_url="https://api.minimax.io/v1",
        )

        response = client.chat.completions.create(
            model="MiniMax-M2.7-highspeed",
            messages=[{"role": "user", "content": "Say hello."}],
            temperature=0.7,
            max_tokens=10,
        )

        self.assertIsNotNone(response.choices[0].message.content)


if __name__ == "__main__":
    unittest.main()
