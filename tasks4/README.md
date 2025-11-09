(This README provides quick usage for the `tasks4` package.)

Try it — run tests and the CLI
--------------------------------

Run the package tests using the project's script entrypoint (this runs the
pytest-based test runner added to the package):

PowerShell:

```powershell
# Install the package in editable mode (one-time)
Set-Location 'c:\Users\erina\OneDrive\Documents\GitHub\csc299-project\tasks4'
pip install -e .

# Run the test runner via the project's `uv` runner (executes pytest)
uv run tasks4
```

If you prefer to run pytest directly without `uv`:

```powershell
pytest -q "c:\Users\erina\OneDrive\Documents\GitHub\csc299-project\tasks4\src\tasks4\tests"
```

Run the summarizer CLI
-----------------------

You can run the summarizer CLI directly with Python. It reads text from
stdin (or accepts a filename as the first argument) and prints one short
phrase summary per paragraph.

PowerShell examples:

```powershell
# Read text from a file
python -m tasks4 .\input.txt

# Pipe text via stdin
Get-Content .\input.txt -Raw | python -m tasks4
```

Environment
-----------

- The CLI and module expect the environment variable `OPENAI_API_KEY` to be
	set for network calls, e.g.:

```powershell
$env:OPENAI_API_KEY = 'sk-...'
```

Notes
-----
- The tests mock the OpenAI client, so they don't perform network calls.
- The `tasks4` project script `tasks4` is configured to run the test runner
	(so `uv run tasks4` executes the test suite). If you'd like separate
	`uv` commands for the CLI, I can add them (e.g. `tasks4-cli`).

