"""Simple test runner used by `uv run tasks4`.

This module runs pytest programmatically against the package's tests
directory and exits with pytest's return code so the caller sees success/failure.
"""
from __future__ import annotations

import os
import sys


def run(argv: list[str] | None = None) -> None:
    """Run pytest on the package tests directory and exit with its return code.

    This function is intended to be used as an entrypoint from `uv run`.
    """
    # Import here so tests can run even if pytest isn't installed until now.
    try:
        import pytest
    except Exception as exc:  # pragma: no cover - environment issue
        print("pytest is required to run tests. Install it with `pip install pytest`.")
        raise

    # Determine the tests directory relative to this file
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "tests"))

    # Allow passing extra args via argv (not used by uv runner typically)
    args = [tests_dir]
    if argv:
        args.extend(argv)

    # Run pytest programmatically and capture its return code
    return_code = pytest.main(args)

    # After tests, attempt to produce and print example summaries so that
    # `uv run tasks4` shows both test results and a sample output of the
    # summarizer. If the OpenAI API key or client is not available, fall
    # back to a tiny local summarizer so the command is non-blocking.
    # Require OPENAI_API_KEY to be present; fail if missing.
    sample_text = (
        "This is an example paragraph describing task A in a few sentences. "
        "It should be summarized into a short phrase.\n\n"
        "This is an example paragraph describing task B. It contains more "
        "context and should produce a separate short phrase."
    )

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("\nERROR: OPENAI_API_KEY environment variable not set. Aborting.")
        # Exit with non-zero status to indicate failure as requested
        raise SystemExit(2)

    # Try to use the real summarizer and fail if it errors
    try:
        from . import summarize_paragraphs

        summaries = summarize_paragraphs(sample_text, api_key=api_key)
        print("\nSummaries (from gpt-5-mini):")
        for s in summaries:
            print("-", s)
    except Exception as exc:  # pragma: no cover - runtime/network
        print("\nFailed to run remote summarizer:", exc)
        raise SystemExit(3)

    # Exit with the pytest return code so CI or callers can observe test status
    raise SystemExit(return_code)
