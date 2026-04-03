# SDD Tasking Reference
> Used by the orchestrator during Step 4 and by the SDD Task Writer.
> Defines task format, phase structure, and brief format.

## Task ID Format
- Pattern: `T001`, `T002`, `T003` … sequential, zero-padded 3-digit
- Sub-tasks when splitting: `T005a`, `T005b`, `T005c`
- Each task: `- [ ] T00N [markers] Description with file path`

## Markers
- `[P]` — Safe to run in parallel (different files, no shared state)
- `[USN]` — Which user story (e.g., `[US1]`, `[US2]`)
- Setup/Foundational tasks omit `[USN]`

## Phase Structure

### Phase 1: Setup
- Create directories, init project, configure tooling
- All tasks can be `[P]`

### Phase 2: Foundational (Blocking Prerequisites)
- Database setup, auth framework, routing, base models
- **⚠ CRITICAL**: No user story work until complete

### Phase 3+: User Stories (one phase per story, priority order)
```
## Phase N: User Story M — [Title] (Priority: PM) [🎯 MVP if P1]
**Goal**: [What this delivers]
**Independent Test**: [How to verify]
- [ ] T0XX [P] [USM] task with file path
**Checkpoint**: [verification condition]
```

### Final Phase: Polish & Cross-Cutting

## Task Complexity Guide for GPT-5 mini Workers

Each task MUST be achievable by a GPT-5 mini model in a single focused session:

**GOOD tasks** (GPT-5 mini can do these):
- `Create internal/models/user.go with User struct and email validation`
- `Add SignupHandler to internal/auth/handler.go parsing JSON body`
- `Create migrations/001_create_users.sql with users table DDL`
- `Add test cases for signup: success, duplicate, short password`

**BAD tasks** (too complex, need splitting):
- `Implement the complete authentication flow` → split into handler, service, store tasks
- `Create the API with all endpoints` → split per endpoint
- `Add full CRUD for users with validation` → split into create, read, update, delete

**SPLITTING RULE**: If a task description needs the word "and" or touches >1 file → split it.

## Completeness Rule
Every acceptance scenario from spec.md MUST map to ≥1 task.
Every entity from data-model.md → creation task.
Every contract → implementation task.

## Orchestrator Brief Format for Task Writer

```
WRITE tasks to: specs/queue/[###-feature-name]/tasks.md
SPEC_PATH: [path]
PLAN_PATH: [path]
FEATURE_NAME: [name]

PHASE_1_SETUP:
- T001 [P]: [description with file path]
- T002 [P]: [description with file path]
Checkpoint: [condition]

PHASE_2_FOUNDATION:
- T003: [description with file path]
- T004: [description with file path] (depends on T003)
Checkpoint: [condition]

PHASE_3_US1: User Story 1 — [Title] (P1) [🎯 MVP]
Goal: [what this delivers]
Independent Test: [how to verify]
- T005 [P] [US1]: [description with file path]
- T006 [US1]: [description with file path] (needs T005)
Checkpoint: [condition]

[continue for all phases]

FINAL_PHASE_POLISH:
- T0XX [P]: [description]
Checkpoint: [condition]

COVERAGE_MAP:
- US1 scenario 1 → T005, T006
- US1 scenario 2 → T007
- Entity: User → T003
- Contract: signup API → T005, T006
```
