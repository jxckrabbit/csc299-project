# Quickstart: User Task Manager (CLI)

## Prerequisites
- Python 3.11 installed
- From repo root, create a virtualenv and install dev deps (if provided)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt  # or: pip install pytest
```

## Running (development)

From the repository root (after activating venv):

```powershell
# run the CLI implementation (example placeholder)
python -m src.cli list-users

# create a user
python -m src.cli create-user "Alice"

# add a task
python -m src.cli add-task u1 --title "Buy milk" --due 2025-11-19 --category errands

# list tasks for user
python -m src.cli list-tasks u1

# remove a task
python -m src.cli remove-task u1 t1
```

## Tests

```powershell
pytest tests/
```

## Notes about "uv"

This feature is currently a CLI application (no ASGI web server). If you require a web-based
interface run under `uvicorn` (ASGI), we can add an optional small ASGI wrapper in a follow-up.
