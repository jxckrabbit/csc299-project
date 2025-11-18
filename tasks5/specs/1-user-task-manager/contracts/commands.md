# CLI Contracts: User Task Manager

This document lists the CLI commands, input, output, and exit codes for the feature.

## Commands

### `list-users`
- Description: Print an ordered list of users (id and display_name).
- Output: lines of `id \t display_name`
- Exit codes: 0 success, non-zero on error

### `create-user <display_name>`
- Description: Create a user with the provided display name and return the new user id.
- Output: `CREATED <user-id>` on success
- Exit codes: 0 success, 2 invalid input

### `list-tasks <user-id>`
- Description: List tasks for the given user, ordered by due_date ascending.
- Output: each line: `task-id \t due_date \t category \t title`
- Exit codes: 0 success, 3 user-not-found

### `add-task <user-id> --title "..." --due YYYY-MM-DD --category "..."`
- Description: Add a task for specified user. Returns created task id.
- Output: `TASK-ADDED <task-id>`
- Exit codes: 0 success, 2 invalid input, 3 user-not-found

### `remove-task <user-id> <task-id>`
- Description: Remove the task with id for given user.
- Output: `TASK-REMOVED <task-id>`
- Exit codes: 0 success, 3 user-not-found, 4 task-not-found

### Error output
- Structured error format: `ERROR <code> <message>` written to stderr

## Examples
- `create-user "Alice"` -> `CREATED u1`
- `add-task u1 --title "Pay rent" --due 2025-12-01 --category "finance"` -> `TASK-ADDED t1`

