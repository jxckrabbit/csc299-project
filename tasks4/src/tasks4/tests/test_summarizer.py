import os
import sys
import types

# Ensure the package src directory is on sys.path so tests can import tasks4
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import tasks4


def test_summarize_two_paragraphs(monkeypatch):
    """Verify two paragraphs each produce an independent short-phrase summary."""

    # Prepare two fake responses (one per paragraph)
    responses = [
        {"choices": [{"message": {"content": "Brief task A."}}]},
        {"choices": [{"message": {"content": "Brief task B."}}]},
    ]

    class MockChatCompletion:
        @staticmethod
        def create(*args, **kwargs):
            # Return and remove the first prepared response
            if not responses:
                raise AssertionError("More calls than expected to ChatCompletion.create")
            return responses.pop(0)

    # Create a mock openai namespace and set it on the tasks4 module
    mock_openai = types.SimpleNamespace(ChatCompletion=MockChatCompletion)
    monkeypatch.setattr(tasks4, "openai", mock_openai)

    text = """
    This is the first paragraph, describing task A in several sentences.

    This is the second paragraph. It explains task B with a bit more text and
    context so we can ensure the summarizer returns a short phrase for it.
    """

    summaries = tasks4.summarize_paragraphs(text, api_key="test")
    # Print the generated summaries (for visibility in test output)
    print("Generated summaries:", summaries)

    # Expect exactly two summaries and that trailing punctuation was removed
    assert summaries == ["Brief task A", "Brief task B"]
