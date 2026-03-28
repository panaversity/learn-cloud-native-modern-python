"""Unit tests for MiniMax hello world example."""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch


class TestMiniMaxHello(unittest.TestCase):
    """Unit tests for MiniMax hello functions."""

    @patch("myproject.hello.OpenAI")
    def test_minimax_creates_client_with_correct_base_url(self, mock_openai_cls):
        """Client should use MiniMax API base URL."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello!"
        mock_client.chat.completions.create.return_value = mock_response

        from myproject.hello import minimax

        minimax()

        mock_openai_cls.assert_called_once()
        call_kwargs = mock_openai_cls.call_args
        self.assertEqual(call_kwargs.kwargs["base_url"], "https://api.minimax.io/v1")

    @patch("myproject.hello.OpenAI")
    def test_minimax_uses_correct_model(self, mock_openai_cls):
        """Should request MiniMax-M2.7 model."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hi there!"
        mock_client.chat.completions.create.return_value = mock_response

        from myproject.hello import minimax

        minimax()

        call_kwargs = mock_client.chat.completions.create.call_args
        self.assertEqual(call_kwargs.kwargs["model"], "MiniMax-M2.7")

    @patch("myproject.hello.OpenAI")
    def test_minimax_uses_valid_temperature(self, mock_openai_cls):
        """Temperature must be in (0.0, 1.0] range for MiniMax."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello!"
        mock_client.chat.completions.create.return_value = mock_response

        from myproject.hello import minimax

        minimax()

        call_kwargs = mock_client.chat.completions.create.call_args
        temp = call_kwargs.kwargs["temperature"]
        self.assertGreater(temp, 0.0)
        self.assertLessEqual(temp, 1.0)

    @patch("myproject.hello.OpenAI")
    def test_minimax_reads_api_key_from_env(self, mock_openai_cls):
        """Client should read MINIMAX_API_KEY from environment."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello!"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {"MINIMAX_API_KEY": "test-key-123"}):
            from myproject.hello import minimax

            minimax()

        call_kwargs = mock_openai_cls.call_args
        self.assertEqual(call_kwargs.kwargs["api_key"], "test-key-123")

    @patch("myproject.hello.OpenAI")
    def test_minimax_stream_uses_streaming(self, mock_openai_cls):
        """Streaming function should set stream=True."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = "Hello"
        mock_client.chat.completions.create.return_value = [mock_chunk]

        from myproject.hello import minimax_stream

        minimax_stream()

        call_kwargs = mock_client.chat.completions.create.call_args
        self.assertTrue(call_kwargs.kwargs["stream"])

    @patch("myproject.hello.OpenAI")
    def test_minimax_stream_uses_correct_model(self, mock_openai_cls):
        """Streaming function should use MiniMax-M2.7 model."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = "Hi"
        mock_client.chat.completions.create.return_value = [mock_chunk]

        from myproject.hello import minimax_stream

        minimax_stream()

        call_kwargs = mock_client.chat.completions.create.call_args
        self.assertEqual(call_kwargs.kwargs["model"], "MiniMax-M2.7")


class TestMiniMaxStreamOutput(unittest.TestCase):
    """Test streaming output handling."""

    @patch("myproject.hello.OpenAI")
    def test_stream_handles_none_content(self, mock_openai_cls):
        """Streaming should skip chunks with None content."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        chunk_with_content = MagicMock()
        chunk_with_content.choices = [MagicMock()]
        chunk_with_content.choices[0].delta.content = "Hello"

        chunk_without_content = MagicMock()
        chunk_without_content.choices = [MagicMock()]
        chunk_without_content.choices[0].delta.content = None

        mock_client.chat.completions.create.return_value = [
            chunk_without_content,
            chunk_with_content,
        ]

        from myproject.hello import minimax_stream

        minimax_stream()

    @patch("myproject.hello.OpenAI")
    def test_stream_handles_multiple_chunks(self, mock_openai_cls):
        """Streaming should process multiple content chunks."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        chunks = []
        for text in ["Hello", " ", "World"]:
            chunk = MagicMock()
            chunk.choices = [MagicMock()]
            chunk.choices[0].delta.content = text
            chunks.append(chunk)

        mock_client.chat.completions.create.return_value = chunks

        from myproject.hello import minimax_stream

        minimax_stream()


class TestLiteLLMMiniMax(unittest.TestCase):
    """Unit tests for MiniMax in LiteLLM example."""

    @patch("litellm.completion")
    def test_litellm_minimax_uses_openai_prefix(self, mock_completion):
        """LiteLLM MiniMax should use openai/ model prefix."""
        mock_response = MagicMock()
        mock_completion.return_value = mock_response

        import importlib
        import sys

        litellm_hello_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "02_litellm",
            "myproject",
            "src",
            "myproject",
        )
        sys.path.insert(0, os.path.abspath(litellm_hello_path))
        try:
            if "myproject.hello" in sys.modules:
                del sys.modules["myproject.hello"]
            spec = importlib.util.spec_from_file_location(
                "litellm_hello",
                os.path.join(os.path.abspath(litellm_hello_path), "hello.py"),
            )
            litellm_hello = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(litellm_hello)
            litellm_hello.minimax()

            call_kwargs = mock_completion.call_args
            self.assertEqual(call_kwargs.kwargs["model"], "openai/MiniMax-M2.7")
            self.assertEqual(
                call_kwargs.kwargs["api_base"], "https://api.minimax.io/v1"
            )
        finally:
            sys.path.pop(0)

    @patch("litellm.completion")
    def test_litellm_minimax_passes_temperature(self, mock_completion):
        """LiteLLM MiniMax should pass temperature parameter."""
        mock_response = MagicMock()
        mock_completion.return_value = mock_response

        import importlib

        litellm_hello_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "02_litellm",
            "myproject",
            "src",
            "myproject",
        )
        sys.path.insert(0, os.path.abspath(litellm_hello_path))
        try:
            spec = importlib.util.spec_from_file_location(
                "litellm_hello2",
                os.path.join(os.path.abspath(litellm_hello_path), "hello.py"),
            )
            litellm_hello = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(litellm_hello)
            litellm_hello.minimax()

            call_kwargs = mock_completion.call_args
            temp = call_kwargs.kwargs["temperature"]
            self.assertGreater(temp, 0.0)
            self.assertLessEqual(temp, 1.0)
        finally:
            sys.path.pop(0)


if __name__ == "__main__":
    unittest.main()
