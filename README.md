# Simple Todo CLI

This small command-line application stores tasks in a JSON file and supports adding, listing, and searching tasks.

Files:
- `todo.py`: the CLI script
- `tasks.json`: default JSON data file (created automatically)

Examples:

Add a task:

```powershell
python todo.py add "Buy groceries" --tags shopping,errand
```

List incomplete tasks:

```powershell
python todo.py list
```

List all tasks including completed:

```powershell
python todo.py list --all
```

Search tasks:

```powershell
python todo.py search groceries
```

The script defaults to `tasks.json` next to the script but you can use `--file` to point elsewhere.
