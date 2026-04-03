# SDD Execution Reference
> Loaded by the orchestrator during Step 5 (Execute).
> Defines how the orchestrator manages code workers, handles failures,
> and maintains build discipline.

## Architecture: Orchestrator-Driven Execution

There is NO executor subagent. The orchestrator (GPT-5.4) directly
manages `SDD Code Worker` (GPT-5 mini) spawns. This gives the smart
model full control over task decomposition, error recovery, and checkpoint management.

## Build System Detection

Detect once at start of Step 5, cache for the session:

| Indicator | Build Command | Test Command |
|-----------|--------------|-------------|
| `go.mod` | `go build ./...` | `go test ./...` |
| `package.json` | `npm run build` (if script exists) | `npm test` (if script exists) |
| `pyproject.toml` or `setup.py` | — | `python -m pytest` |
| `Cargo.toml` | `cargo build` | `cargo test` |
| `pom.xml` | `mvn compile` | `mvn test` |
| `build.gradle` / `build.gradle.kts` | `./gradlew build` | `./gradlew test` |
| `Makefile` | `make` (if `build` target exists) | `make test` (if target exists) |
| `CMakeLists.txt` | `cmake --build .` | `ctest` |

Priority: `go.mod` > `Cargo.toml` > `pom.xml` > `build.gradle` > `package.json` > `pyproject.toml` > `Makefile`

## Worker Spawn Protocol

### Crafting Worker Prompts

Each `SDD Code Worker` prompt must be SELF-CONTAINED:
```
TASK: T00N — [description]
FILE(S): [exact path(s) to create or modify]
ACTION: CREATE | MODIFY
BUILD_CMD: [detected command or "none"]
CONTEXT:
- [Types, imports, function signatures the worker needs]
- [Existing code snippets from files being modified]
- [Interface contracts from other files this code must satisfy]
CRITERIA: [acceptance criteria for this specific task]
```

Rules:
- Do NOT include the full spec, plan, or task list
- DO include relevant code snippets (not just file names)
- DO include type signatures of dependencies
- Keep context to what THIS task needs — nothing more

### Task Complexity Assessment

Before spawning a worker, classify the task:

**SIMPLE** (spawn directly) — GPT-5 mini handles easily:
- Create one new file from scratch with clear structure
- Add one function/method to an existing file
- Create a test file for an existing module
- Add configuration or migration file
- Simple CRUD operation

**MEDIUM** (spawn with extra context) — GPT-5 mini needs help:
- Modify multiple functions in one file
- Implement business logic with 2-3 conditions
- Create file that depends on understanding 2-3 other files
→ Include more code snippets in context

**COMPLEX** (break down first) — too complex for GPT-5 mini:
- Touches >2 files
- Requires understanding cross-module data flow
- Has branching logic with >3 paths
- Integrates multiple services/layers
→ Split into 2-3 SIMPLE sub-tasks

### Splitting Complex Tasks

When a task needs splitting:
1. Identify the independent parts
2. Create sub-task IDs (T005a, T005b, T005c)
3. Save checkpoint:
   ```
   # Checkpoint: Task T005 Split
   Original: T005 — [description]
   ## Sub-tasks
   - [ ] T005a: [part 1 — e.g., create interface/types]
   - [ ] T005b: [part 2 — e.g., implement core logic]
   - [ ] T005c: [part 3 — e.g., wire up to handler]
   ## Dependencies
   T005a → T005b → T005c (sequential)
   or: T005a + T005b parallel → T005c after both
   ```
4. Spawn sub-tasks according to dependencies
5. After all complete → verify integration, mark original task done

## Parallel Execution Rules

### Batch Size
- Maximum 5 simultaneous workers per batch
- If >5 parallel tasks → batch in groups of 5
- Wait for batch to complete before starting next batch

### Phase Protocol
```
═══ Phase N: [Phase Name] ═══
▶ Tasks T001, T002, T003 — [P] Parallel execution (3 workers)
✓ T001 complete — Created user model in internal/models/user.go
✓ T002 complete — Created migration in migrations/001_users.sql
✓ T003 complete — Created auth config in internal/config/auth.go
✓ Phase N complete — Checkpoint: [condition verified]
```

### After Each Batch
1. Collect all worker reports
2. Handle non-DONE statuses:
   - BLOCKED → analyze root cause, break down further, re-spawn
   - DEVIATION → ask user via #tool:vscode/askQuestions
   - BUILD_FAIL → diagnose, create targeted fix, spawn fix worker
3. Run build + test ONCE for entire batch
4. Mark completed tasks in tasks.md

## Failure Recovery

### Fix Attempt Budget
- Per task: 3 total fix attempts (across original + fix workers)
- Per batch: if batch build fails, you get 3 attempts to fix across all workers

### Fix Worker Pattern
When a code worker reports BUILD_FAIL:
1. Read the error from the worker's report
2. Read the file(s) the worker modified
3. Diagnose the root cause yourself (you're the smart model)
4. Spawn a new `SDD Code Worker` with a targeted fix:
   ```
   TASK: T00N-fix — Fix build error in [file]
   FILE(S): [exact path]
   ACTION: MODIFY
   BUILD_CMD: [command]
   CONTEXT:
   - Current file content: [the broken code]
   - Error message: [exact error]
   - Root cause: [your diagnosis]
   - Fix approach: [exactly what to change]
   CRITERIA: Build passes with zero errors
   ```

### Escalation
After 3 fix attempts → stop and ask user:
```
⚠ 3 fix attempts exhausted for Task T00N.
Error: [last error]
Attempted fixes: [list]
Options: A) I'll fix manually  B) Skip task  C) Abort
```

## Analysis Paralysis Guard
5+ consecutive reads without any worker spawn → STOP.
Either spawn a worker or report "blocked".

## Scope Discipline
Changes outside the task list → STOP and ask user.
Workers that report DEVIATION → ask user before proceeding.
