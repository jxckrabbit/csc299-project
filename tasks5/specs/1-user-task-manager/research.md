# Research: User Task Manager (Phase 0)

## Decision: Runtime (CLI vs ASGI)

- Decision: CLI (command-line interface)
- Rationale: The feature description specifies task removal via a command and lists command-driven UX (select user, run add/remove). A CLI allows fast, testable delivery for v0 and aligns with test-first approach.
- Alternatives considered:
  - ASGI/web app (uvicorn): would enable GUI/web UX but adds infra and CI complexity. Recommend for v1 if user requests web UI.

## Decision: Storage

- Decision: Local file-based JSON at `data/tasks.json`.
- Rationale: Minimizes infra and CI complexity for prototype, easy to test locally, and straightforward to migrate via an adapter layer.
- Alternatives considered:
  - SQLite: better concurrency, still lightweight.
  - Postgres/remote: production-ready but adds infra burden.

## Atomic writes and concurrency

- Decision: Use atomic write pattern (write to temp file then rename) to avoid partial writes on Windows and protect against corruption.
- Rationale: Simple and effective for single-writer scenarios and small data sizes.

## Testing approach

- Use `pytest` for unit and integration tests.
- Integration test will simulate CLI invocations using `subprocess` or `click`/`typer` test helpers.

## Recommendation summary

- Proceed with CLI + local JSON and enforce atomic writes; use Python 3.11 and `pytest` for tests.
