# Implementation Plan: User Task Manager

**Branch**: `1-user-task-manager` | **Date**: 2025-11-18 | **Spec**: ../spec.md
**Input**: Feature specification from `/specs/1-user-task-manager/spec.md`

## Summary

Build a minimal, test-first CLI application to manage per-user task lists with due dates and categories.
Primary deliverable is a command-driven prototype using local JSON persistence that implements the
P1 flows: list users, create-user, select-user, add-task, list-tasks, remove-task.

## Technical Context

**Language/Version**: Python 3.11 (recommended)
**Primary Dependencies**: `pytest` (tests), `black`/`flake8` (format/lint), `python-dotenv` (env optional)
**Storage**: Local file-based JSON (`data/tasks.json`) mapping user IDs to arrays of tasks
**Testing**: `pytest` with unit tests and an integration test simulating CLI flows
**Target Platform**: Local workstation (Windows), CLI-based
**Project Type**: Single small CLI tool (no web server for v0)
**Performance Goals**: Responsiveness: list and display operations <2s on typical workstation
**Constraints**: Keep implementation minimal; avoid external services for v0
**Scale/Scope**: Designed for single-user local use prototype (small data size — <<10k tasks)

## Constitution Check

- Code Quality: Use `black` for formatting and `flake8` (or `ruff`) for linting. Include a pre-commit config.
- Simplicity: Single-file JSON storage and CLI interface to minimize complexity.
- Test-First: Write failing `pytest` tests for core logic and integration before implementation.
- Performance: Declare target <2s interactive operations; add a benchmark test if needed.
- UX/API Consistency: CLI commands and error formats will be documented in `quickstart.md` and `contracts/`.

## Project Structure

```text
specs/1-user-task-manager/
├── plan.md            # This file
├── research.md        # Phase 0 output
├── data-model.md      # Phase 1 output
├── quickstart.md      # Phase 1 output
├── contracts/         # Phase 1 output (CLI commands)
├── tasks.md           # Phase 2 tasks (generated below)
└── checklists/
    └── requirements.md
```

**Structure Decision**: Single small CLI tool implemented in `src/` with tests in `tests/`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Phase 0: Research Tasks (resolve any NEEDS_CLARIFICATION)

- Research: Confirm CLI runtime vs ASGI/web requirement (resolved: CLI chosen based on spec/commands).
- Research: Best practices for local JSON persistence and atomic writes on Windows.
- Research: Concurrency safety for file writes (use file lock or atomic replace pattern).

## Phase 1: Design & Contracts

- Data model: `data-model.md` will declare `User` and `Task` shapes and validation rules.
- Contracts: `contracts/commands.md` will list the CLI commands and expected I/O and exit codes.
- Quickstart: `quickstart.md` will include setup and example commands to run locally.
- Agent context: Update agent context using repo script to reflect chosen tech (Python, CLI, pytest).

## Phase 2: Tasks (high level)

- T001 Initialize project layout, `src/` + `tests/` + `data/` and create `pyproject.toml` or `requirements.txt`.
- T002 Add formatting/lint config and pre-commit hooks (`black`, `flake8`/`ruff`).
- T003 [P] Write unit tests for Task model validation (test-first).
- T004 [P] Implement Task and User model code to satisfy unit tests.
- T005 Write contract tests for CLI commands (simulate invocations).
- T006 Implement CLI commands (`list-users`, `create-user`, `add-task`, `list-tasks`, `remove-task`).
- T007 Integration test: CLI flow create-user → add-task → list-tasks → remove-task → restart simulation → verify persistence.
- T008 Documentation: quickstart and command reference in `contracts/commands.md`.

## Deliverables

- `research.md`, `data-model.md`, `contracts/commands.md`, `quickstart.md`, `plan.md`, and `tasks.md` in the feature directory.

*** End Plan
