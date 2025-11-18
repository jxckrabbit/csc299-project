---
description: "Task list for feature implementation: User Task Manager"
---

# Tasks: User Task Manager

**Input**: `spec.md`, `plan.md`, `data-model.md`, `contracts/commands.md`
**Prerequisites**: `plan.md` (required), `research.md` (required)

**Tests**: Tests are MANDATORY for P1 user stories per project constitution. Tests MUST be written
first (test-first) and should fail before implementation. Each user story below includes test tasks.

## Path Conventions
- Source: `src/`
- Tests: `tests/` (unit, integration)
- Data: `data/tasks.json`

## Phase 1: Setup (Shared Infrastructure)

 - [X] T001 Initialize repo layout (create `src/`, `tests/`, `data/`, `docs/`) — Path: repository root
  - Create `src/`, `tests/`, `data/`, and `docs/` if missing
  - Add `pyproject.toml` or `requirements.txt` with `pytest`, `typer` (or `argparse`), `python-dotenv` (optional)
  - Create `.gitignore` entry for `data/tasks.json` if desired (or include sample data file)
  - Output: created files and scaffolding
  - Parallel: yes

- [ ] T002 [P] Configure linting and formatting (black, ruff/flake8, pre-commit) — Path: repo config files
  - Add `black` and `ruff` (or `flake8`) config and pre-commit hooks
  - CI pipeline must run `black --check` and `ruff`/`flake8` as part of checks
  - Parallel: yes

- [ ] T003 Add CI job skeleton (lint, unit tests, integration tests) — Path: .github/workflows/ci.yml
  - Add a GitHub Actions workflow (or existing CI) that runs: lint, unit tests, integration tests
  - Ensure tests run in a clean environment and that `data/` is writable
  - Parallel: no (depends on T001)

## Phase 2: Core Models & Persistence (Blocking)

 - [X] T010 [P] Write unit tests for User & Task validation (test-first) — Path: tests/unit/test_models.py
  - Tests: validate title non-empty, due_date iso parse, category length, id uniqueness

 - [X] T011 [P] Implement `src/models.py` to satisfy tests — Path: src/models.py
  - Provide `User` and `Task` classes, validation functions, and factory helpers
  - Use UUIDs for `id` by default

 - [X] T012 [P] Write unit tests for persistence layer (atomic write, read) — Path: tests/unit/test_storage.py
  - Tests: writing tasks to `data/tasks.json`, atomic replace; simulate partial write protection

 - [X] T013 [P] Implement `src/storage.py` (local JSON) to satisfy tests — Path: src/storage.py
  - API: `load_data()`, `save_data(obj)` using atomic write (temp file + rename)
  - Optional: lightweight file-lock for multi-process safety using `msvcrt` or `portalocker`

## Phase 3: CLI Contracts & Command Tests

 - [X] T020 [P] Write contract tests for CLI commands (fail first) — Path: tests/contract/test_commands.py
  - Tests simulate CLI invocations and assert outputs and exit codes per `contracts/commands.md`
  - Use `subprocess` or `typer`/`click` testing helpers

 - [X] T021 [P] Implement CLI command scaffolding (test-driven) — Path: src/cli.py
  - Commands: `list-users`, `create-user <display_name>`, `list-tasks <user-id>`,
    `add-task <user-id> --title --due --category`, `remove-task <user-id> <task-id>`
  - Prefer `typer` for concise CLI building; fallback to `argparse` if minimal dependencies desired

## Phase 4: Integration Flow & Acceptance Tests

 - [X] T030 Integration test: end-to-end CLI flow (test-first) — Path: tests/integration/test_flow.py
  - Flow: create-user -> add-task -> list-tasks -> remove-task -> restart simulation -> verify persistence

 - [X] T031 Implement application logic to satisfy integration test — Path: src/
  - Wire models, storage, and CLI handlers
  - Ensure error codes and structured error output match `contracts/commands.md`

## Phase 5: Documentation & Quickstart

 - [X] T040 Document CLI commands and examples in `quickstart.md` and `contracts/commands.md` — Path: specs/1-user-task-manager/quickstart.md
  - Include examples for typical flows and error scenarios
  - Path: docs/quickstart.md

- [ ] T041 Add README snippet for feature-specific developer instructions — Path: specs/1-user-task-manager/README.md

## Phase 6: Polish, Observability, and Release Prep

- [ ] T050 Add logging & observability hooks — Path: src/logging_config.py
  - Structured logging for create/add/remove operations
  - Optional: small metrics counters for number of tasks created/removed

- [ ] T051 Performance & regression tests (optional) — Path: tests/perf/test_perf.py
  - Add a small benchmark to assert list and display operations <2s for typical data sizes

- [ ] T052 Final CI gating and merge checklist — Path: .github/workflows/ci.yml
  - Verify linting, tests, and documentation pass in CI

## Task Details & Acceptance

- Each implementation task with `[P]` must be accompanied by one or more tests written before code implementation.
- All tasks must reference exact file paths where code or tests will live.
- Tests must fail initially and pass after implementation; CI must assert pass before merge.

## Parallel Opportunities

- Model unit tests and storage tests (T010/T012) can be written in parallel by different devs.
- CLI contract tests (T020) can be authored while storage implementation is underway but will fail until storage exists.

## Ownership & Estimates (suggested)

- T001-T003: 0.5 - 1 day
- T010-T013: 1 - 2 days
- T020-T021: 1 day
- T030-T031: 1 - 2 days
- T040-T052: 0.5 - 1 day

## Notes

- Follow the project constitution: test-first, linters, and measurable success criteria.
- Keep data file small in repo; consider seeding test fixtures in `tests/fixtures/`.


