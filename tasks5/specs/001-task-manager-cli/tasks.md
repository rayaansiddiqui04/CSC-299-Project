---
description: "Task list for CLI Task Manager"
---

# Tasks: CLI Task Manager

**Input**: Design documents from `/specs/001-task-manager-cli/`  
**Prerequisites**: plan.md (required), spec.md (required), research.md (n/a), data-model.md (n/a), contracts/ (n/a)

**Tests**: Spec explicitly requires unit tests for add/list/complete/delete flows. Each user story therefore includes test tasks prior to implementation.

**Organization**: Tasks are grouped by user story (P1–P3) so each slice can be implemented and tested independently after the shared setup/foundational work.

## Format: `[ID] [P?] [Story] Description`

- `[P]` → Safe to run in parallel (different files, no blocking dependency)
- `[Story]` → One of `[US1]`, `[US2]`, `[US3]` mirroring the priorities in spec.md
- Each description cites the concrete file(s) to touch so an implementing agent can act without more context

## Path Conventions

Single-project CLI per plan.md:

```text
app/models.py    # domain models + validation helpers
storage.py       # JSON storage + atomic writes
cli.py           # argparse wiring + command handlers
__main__.py      # python -m entry point
tests/           # pytest suites exercising models and CLI
```

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project bootstrap so later work has a runnable skeleton.

- [ ] T001 Create initial CLI skeleton directories and placeholder modules in `app/models.py`, `storage.py`, `cli.py`, `__main__.py`, and `tests/__init__.py`.
- [ ] T002 Define `pyproject.toml` with Python 3.11 metadata, `pytest` dependency, and a console-script entry that points to `cli:main`.
- [ ] T003 Configure `tests/conftest.py` to expose a temporary task-file fixture and shared argparse runner helpers.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Domain, persistence, and CLI plumbing that every user story depends on.

- [ ] T004 Implement the `Task` dataclass, `Priority` enum, and validation exceptions in `app/models.py`.
- [ ] T005 [P] Add serialization/deserialization helpers (`task_to_dict`, `task_from_dict`) that normalize ISO timestamps in `app/models.py`.
- [ ] T006 Build `TaskStorage` path resolution (default `~/.tasks.json`, `TASK_FILE`, `--data` override) and lazy file creation in `storage.py`.
- [ ] T007 [P] Implement atomic save logic that writes to a temp file then renames in `storage.py`.
- [ ] T008 Wire an `argparse` application with shared options `--data`, `--color`, `--dry-run`, and stub subparsers in `cli.py`.
- [ ] T009 [P] Implement CLI table formatting utilities (status glyphs, aligned columns, minimal color toggle) in `cli.py`.
- [ ] T010 Connect `__main__.py` to `cli.main()` so `python -m tasker` invokes the CLI entrypoint.

**Checkpoint**: All core plumbing exists; user story work can start.

---

## Phase 3: User Story 1 - Capture and review tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with description/priority/due metadata and list pending/all tasks with sorting.

**Independent Test**: Use temporary storage to `add` multiple tasks (varied metadata) and `list` with default/pending filters plus `--all`/`--sort due`, verifying JSON persistence and readable table output.

### Tests for User Story 1 (required per spec)

- [ ] T011 [P] [US1] Extend `tests/test_models.py` to cover description validation, priority parsing, due-date parsing, and auto-incremented IDs when creating tasks.
- [ ] T012 [P] [US1] Add CLI integration tests in `tests/test_cli.py` that run `add`, `list`, `list --all`, and `list --sort due` using temp task files.

### Implementation for User Story 1

- [ ] T013 [P] [US1] Implement `create_task` helper in `app/models.py` that validates input, normalizes timestamps, and computes the next ID.
- [ ] T014 [P] [US1] Implement filtering/sorting helpers (pending/all/completed, priority/due ordering) in `app/models.py` for reuse by CLI list output.
- [ ] T015 [US1] Implement the `add` subcommand in `cli.py` to parse args, call `create_task`, and persist via `TaskStorage.save_tasks()`.
- [ ] T016 [US1] Implement the `list` subcommand in `cli.py` to apply filters/sorts, format table columns, and support `--all`, `--completed`, `--pending`, `--sort priority|due`.

**Checkpoint**: Add/list flows are fully functional and independently testable.

---

## Phase 4: User Story 2 - Complete tasks (Priority: P2)

**Goal**: Users can mark pending tasks complete, capture completion timestamps, and prevent repeat completions.

**Independent Test**: Add a task, run `complete <id>`, re-run `list --completed` to see status/checkmark update; attempt re-complete to confirm error path and exit code.

### Tests for User Story 2

- [ ] T017 [P] [US2] Extend `tests/test_models.py` with `mark_task_complete` cases covering timestamp assignment and double-completion errors.
- [ ] T018 [P] [US2] Extend `tests/test_cli.py` with end-to-end coverage for `complete`, including already-complete error messages and `--dry-run` behavior.

### Implementation for User Story 2

- [ ] T019 [P] [US2] Implement `mark_task_complete` in `app/models.py` that flips `completed`, sets `completed_at`, and errors when already complete.
- [ ] T020 [US2] Implement the `complete` subcommand in `cli.py` with `--dry-run`, exit-status signaling, and integration with `TaskStorage`.

**Checkpoint**: Completion workflow is independently usable once US1 is present.

---

## Phase 5: User Story 3 - Delete tasks safely (Priority: P3)

**Goal**: Users can delete tasks with interactive confirmation by default or bypass prompts using `--force`, ensuring IDs are never reused.

**Independent Test**: Delete a task interactively (`y/N` prompt) and via `--force`; verify JSON rewrite is atomic and remaining tasks keep original IDs.

### Tests for User Story 3

- [ ] T021 [P] [US3] Extend `tests/test_models.py` with delete-task cases ensuring filtered lists keep other IDs untouched.
- [ ] T022 [P] [US3] Extend `tests/test_cli.py` with delete scenarios for confirmation prompts, `--force`, and `--dry-run` preview output.

### Implementation for User Story 3

- [ ] T023 [P] [US3] Implement `delete_task` helper in `app/models.py` that removes the matching task, keeps IDs stable, and surfaces removed metadata.
- [ ] T024 [US3] Implement the `delete` subcommand in `cli.py` that prompts when stdin is interactive, supports `--force` & `--dry-run`, and persists via `TaskStorage`.

**Checkpoint**: All CRUD paths work independently; destructive operations are guarded.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final docs and manual verification for release readiness.

- [ ] T025 [P] Document CLI usage, environment overrides, and sample outputs in `README.md`.
- [ ] T026 Capture manual verification script (add/list/complete/delete walkthrough) in `specs/001-task-manager-cli/quickstart.md`.

---

## Dependencies & Execution Order

- Setup (Phase 1) → Foundational (Phase 2) → Stories P1 → P2 → P3 → Polish.
- User stories depend only on completion of Phase 2 and earlier stories if their features are prerequisites (US2 expects add/list; US3 expects add/list/complete available for testing).
- Tests precede implementation within each story so failures guide development.
- Atomic storage helpers (T006–T007) must land before any command writes to disk.

## Parallel Opportunities

- `[P]` tasks can run concurrently because they operate on separate files or pure helpers.
- During Phase 2, T005, T007, T009 can progress in parallel after T004 & T006 shape shared interfaces.
- After Phase 2, different developers can tackle T013/T014 vs CLI handlers, or split stories by priority.
- Test tasks for each story (e.g., T011/T012) can run simultaneously.

## Parallel Execution Examples

### User Story 1

```bash
# Parallel workstream 1: domain helpers
task run T013 && task run T014

# Parallel workstream 2: CLI behaviors
task run T015 && task run T016

# Parallel test writing before implementation
task run T011 &
task run T012 &
wait
```

### User Story 2

```bash
# Write tests while implementation stubs exist
task run T017 &
task run T018 &
wait

# Parallelize domain vs CLI implementation
task run T019 &
task run T020
wait
```

### User Story 3

```bash
# Tests for delete behaviors
task run T021 &
task run T022 &
wait

# Implementation split between domain helper and CLI prompt
task run T023 &
task run T024
wait
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Deliver Phases 1–3 (T001–T016) to ship add/list functionality backed by JSON storage (MVP).
2. Run the US1 independent test scenario from spec.md plus automated tests T011–T012.

### Incremental Delivery

1. After MVP, execute Phase 4 (T017–T020) to add completion without destabilizing add/list.
2. Proceed to Phase 5 (T021–T024) for delete safety once completion stabilizes.
3. Finish with Phase 6 polish tasks (T025–T026) before tagging a release.

### Parallel Team Strategy

- Dev A: Focus on `app/models.py` tasks (T004, T005, T013, T014, T019, T023).
- Dev B: Focus on `storage.py` + CLI handlers (T006–T008, T015, T016, T020, T024).
- Dev C: Own tests/documentation (T003, T011–T012, T017–T018, T021–T022, T025–T026).
- Sync after each phase checkpoint to ensure interfaces remain aligned.

## Notes

- Tasks IDs encode execution order; stop after any checkpoint to demo completed stories.
- Keep destructive commands idempotent by reusing `--dry-run` patterns started in Phase 2.
- Update plan.md if new dependencies emerge during implementation.
