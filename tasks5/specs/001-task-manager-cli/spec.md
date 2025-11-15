# Feature Specification: CLI Task Manager

**Feature Branch**: `001-task-manager-cli`  
**Created**: 2024-03-15  
**Status**: Draft  
**Input**: User description: "I want a command-line task manager with add, list, complete, delete, and JSON storage."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Capture and review tasks (Priority: P1)

Busy command-line users want to quickly add tasks with optional priority/due metadata and immediately list pending work without touching other tools.

**Why this priority**: Without being able to create and view tasks, the tool provides zero value. It is the minimum slice that demonstrates persistence and formatting.

**Independent Test**: Run `tasker add` to create several tasks with different metadata, then `tasker list` (default filters) and verify tasks persist in the JSON file with correct columns and sorting.

**Acceptance Scenarios**:

1. **Given** the task file is empty, **When** the user runs `tasker add "Write spec" --priority high --due 2024-03-20`, **Then** a new pending task appears in `tasker list` with ID 1, stored in JSON with the provided metadata.
2. **Given** multiple tasks exist, **When** the user runs `tasker list --all --sort due`, **Then** the CLI prints a table of all tasks ordered by due date with readable columns.

---

### User Story 2 - Complete tasks (Priority: P2)

Users must mark tasks done, update status, and keep a history of completion timestamps to track progress.

**Why this priority**: Completion is the next most common action after creation and is needed to keep the list meaningful.

**Independent Test**: Add a pending task, run `tasker complete <id>`, rerun `tasker list --completed` and verify status/checkmark updates while preventing double completion.

**Acceptance Scenarios**:

1. **Given** a pending task ID, **When** `tasker complete <id>` executes, **Then** the task JSON entry flips `completed` to true and sets `completed_at` ISO timestamp.
2. **Given** a task already completed, **When** a user attempts to complete it again, **Then** the CLI exits with error code and message indicating it is already complete.

---

### User Story 3 - Delete tasks safely (Priority: P3)

Users occasionally need to remove tasks, so the CLI must confirm destructive intent and support automation via `--force`.

**Why this priority**: Deleting tasks is less frequent than completing them but necessary for housekeeping errors or duplicates.

**Independent Test**: From a list of tasks, delete one interactively (confirm prompt) and another via `--force`, ensuring IDs do not get reused and the JSON file rewrites atomically.

**Acceptance Scenarios**:

1. **Given** interactive `stdin`, **When** `tasker delete <id>` runs, **Then** the CLI prompts for confirmation (`y/N`) before removing and saving.
2. **Given** `tasker delete --force <id>`, **When** executed, **Then** it deletes immediately with a success message suitable for scripts.

---

### Edge Cases

- Handling invalid task IDs for complete/delete should result in clear errors.
- Adding a task with an invalid priority or malformed date should be rejected before touching the JSON file.
- Running `tasker list` on an empty task file should show an informational message while still respecting filters.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add a task with description, priority, and due date via CLI flags.
- **FR-002**: System MUST list tasks filtered by pending/all/completed with configurable sorting.
- **FR-003**: Users MUST be able to mark pending tasks complete, capturing completion timestamp and preventing duplicates.
- **FR-004**: System MUST remove tasks with confirmation prompts unless `--force` skips interaction.
- **FR-005**: System MUST persist tasks to a JSON file with atomic writes and never reuse IDs within the file.
- **FR-006**: CLI MUST validate user input and exit non-zero on invalid requests.

### Key Entities

- **Task**: Represents a single todo with `id`, `description`, `priority`, `due`, `created_at`, `completed`, and `completed_at` attributes persisted in JSON.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add, list, complete, and delete tasks entirely offline via CLI.
- **SC-002**: Re-running CLI commands on the same JSON file never corrupts or loses tasks, even if the process is interrupted mid-write.
- **SC-003**: Each user story can be demonstrated independently by running CLI commands as described in acceptance scenarios.
- **SC-004**: Validation rejects 100% of malformed inputs tested (bad dates/priorities/IDs) with descriptive errors.
