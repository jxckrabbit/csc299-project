# Data Model: User Task Manager

## Entities

### User
- id: string (UUID or short unique token)
- display_name: string (non-empty)

### Task
- id: string (UUID)
- user_id: string (references User.id)
- title: string (non-empty)
- due_date: string (ISO 8601 date)
- category: string (optional, non-empty when present)
- created_at: string (ISO 8601 datetime)

## Relationships
- One-to-many: User -> Task

## Validation Rules
- `title` must be non-empty and trimmed
- `due_date` must parse as an ISO date; past dates allowed but a warning may be shown
- `category` limited to 50 chars

## Persistence Format (data/tasks.json)

```json
{
  "users": [
    { "id": "u1", "display_name": "Alice" }
  ],
  "tasks": [
    { "id": "t1", "user_id": "u1", "title": "Buy milk", "due_date": "2025-11-19", "category": "errands", "created_at": "2025-11-18T12:00:00Z" }
  ]
}
```

## State Transitions
- Task: created -> removed (removed means deleted from store; no soft-delete in v0)

## Concurrency Notes
- Implement atomic file replace on write. For multi-process safety, optionally use a file-lock when performing writes.
