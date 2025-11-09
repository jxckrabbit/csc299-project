"""tasks4 summarizer

This module provides a tiny CLI and function to summarize paragraphs into
very short phrases using the `gpt-5-mini` model. It sends one request per
paragraph so summaries are independent.

Requirements
- Set the environment variable `OPENAI_API_KEY` with your API key.
- Install the official OpenAI Python package, e.g.:
	pip install openai

Usage (example):
	python -m tasks4  # then paste or pipe multi-paragraph text on stdin

Functions
- summarize_paragraphs(text, model='gpt-5-mini') -> list[str]
	Splits `text` into paragraphs and returns a list of short phrase summaries.
"""

from __future__ import annotations

import os
import re
import sys
from typing import List, Optional

try:
	import openai
except Exception as e:  # pragma: no cover - runtime/import error
	openai = None


def _split_into_paragraphs(text: str) -> List[str]:
	"""Split text into non-empty paragraphs.

	Paragraphs are separated by one or more blank lines. Strips whitespace.
	"""
	parts = re.split(r"\n\s*\n+", text.strip())
	return [p.strip() for p in parts if p.strip()]


def summarize_paragraphs(text: str, model: str = "gpt-5-mini", *,
						 api_key: Optional[str] = None,
						 max_tokens: int = 16,
						 temperature: float = 0.2) -> List[str]:
	"""Summarize each paragraph in `text` into a short phrase.

	Sends one independent request per paragraph so results don't bleed.

	Returns a list of summary strings (one per paragraph, same order).
	"""
	if openai is None:
		raise RuntimeError(
			"openai package not installed - run `pip install openai`"
		)

	key = api_key or os.environ.get("OPENAI_API_KEY")
	if not key:
		raise RuntimeError("OPENAI_API_KEY environment variable not set")

	# Configure client
	openai.api_key = key

	paragraphs = _split_into_paragraphs(text)
	summaries: List[str] = []

	system_prompt = (
		"You are a concise summarizer. For the given paragraph, produce a very short"
		" phrase (roughly 1-6 words) that captures the main idea. Return only the"
		" phrase, with no explanation or extra punctuation."
	)

	for para in paragraphs:
		# Make a single request per paragraph to keep responses independent.
		response = openai.ChatCompletion.create(
			model=model,
			messages=[
				{"role": "system", "content": system_prompt},
				{"role": "user", "content": para},
			],
			temperature=temperature,
			max_tokens=max_tokens,
		)

		# Extract and sanitize the text
		choice = response.get("choices", [])[0]
		content = ""
		# ChatCompletion sometimes returns message under 'message'
		if isinstance(choice, dict):
			msg = choice.get("message") or choice.get("delta") or {}
			if isinstance(msg, dict):
				content = msg.get("content", "")
		if not content:
			# Fallback to 'text' or 'content' top-level
			content = choice.get("text") or ""

		summary = content.strip().strip('"').strip()
		# Normalize whitespace and remove trailing periods
		summary = re.sub(r"\s+", " ", summary)
		summary = summary.rstrip(".!")
		summaries.append(summary)

	return summaries


def main(argv: Optional[List[str]] = None) -> int:
	"""CLI entrypoint: read stdin (or file given as first arg) and print summaries."""
	argv = argv if argv is not None else sys.argv[1:]

	if argv:
		# treat first arg as filename
		path = argv[0]
		with open(path, "r", encoding="utf-8") as fh:
			text = fh.read()
	else:
		# read from stdin
		text = sys.stdin.read()

	if not text.strip():
		print("No input text provided on stdin or file.")
		return 2

	try:
		summaries = summarize_paragraphs(text)
	except Exception as exc:
		print(f"Error: {exc}")
		return 3

	for s in summaries:
		print(s)

	return 0


if __name__ == "__main__":
	raise SystemExit(main())


