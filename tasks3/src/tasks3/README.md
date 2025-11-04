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

Add a task with a category (e.g. household or schoolwork):

```powershell
python todo.py add "Clean the kitchen" --tags chores --category household
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

Filter list by category:

```powershell
python todo.py list --category household
```

Search and restrict to a category:

```powershell
python todo.py search kitchen --category household
```

Recommend N tasks to complete (random selection):

```powershell
# Recommend 3 household tasks (only incomplete tasks by default)
python todo.py recommend 3 --category household

# Recommend 2 tasks across all categories, including completed tasks
python todo.py recommend 2 --all
```

The script defaults to `tasks.json` next to the script but you can use `--file` to point elsewhere.
