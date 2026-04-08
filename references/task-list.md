# Task List Reference
> Used by the RN Tasker agent when authoring or updating `specs/tasks.md`.

---

## Purpose

The task list is the single, flat execution queue for all in-progress work.
It is derived from the phase plans of every spec dir currently in `doing`.
It is always located at **`specs/tasks.md`** — exactly one file, always at
the root of the `specs` directory.

---

## File Header

```markdown
# Task List

**Updated:** [ISO date and time]
**Source plans:**
- specs/doing/component-[name]/plan.md — Phase [N]
- …
```

---

## Task Format

Tasks are grouped into batches. Each batch maps to a single phase in a single
plan. Batches are listed in execution order across all active doing plans.

```markdown
## Batch [N] — [Phase name] ([Component name], Phase [X])

| ID | Task | Parallel | Status |
|----|------|----------|--------|
| T0001 | [Short imperative description] | no  | pending |
| T0002 | [Short imperative description] | yes | pending |
| T0003 | [Short imperative description] | no  | pending |
```

### Column definitions

| Column | Rules |
|--------|-------|
| `ID` | Stable four-digit identifier prefixed with `T`. Assigned once; never reused or recycled. Increment globally across all batches. |
| `Task` | Imperative phrase. Start with a verb. One sentence maximum. No code; no file paths unless essential for clarity. |
| `Parallel` | `yes` if this task can run simultaneously with the task immediately above it. `no` otherwise. The first task in a batch is always `no`. |
| `Status` | `pending` → `in-progress` → `done` \| `blocked`. Only one task may be `in-progress` at a time unless `Parallel` is `yes`. |

---

## Task Detail Block

After the table, include a detail block for every task. The RN Worker agent
reads this block to execute the task.

```markdown
### T0001 — [Task short name]

**Phase:** [Plan phase name]
**Spec:** [path to spec.md]
**Plan:** [path to plan.md]

**Description:**
[One paragraph. What must be done, why, and any constraints from the spec
or plan that apply specifically to this task.]

**Inputs:**
- [File, artifact, or fact required before this task can start.]

**Success criteria:**
- [Verifiable condition 1]
- [Verifiable condition 2]

**Acceptance check:**
Run RN Reviewer against: [what file or artifact to review]
Criteria: [short criteria string the RN Reviewer uses to evaluate]
```

---

## Rules

- There is exactly one `tasks.md` at `specs/tasks.md`. Never create a second
  task file in a subdirectory.
- IDs are global and never reused. When a task is removed, its ID is retired.
- When new doing plans are added, the RN Tasker appends new batches to the
  existing file and updates the header.
- A `done` task must never be removed from the file. Mark it `done` and leave
  the row in place so the history is preserved.
- The `Parallel: yes` marker means the RN Worker may delegate this task to a
  parallel subagent alongside the previous task. The orchestrator decides
  whether to use parallelism.
- Every task's `Status` column and detail block must be kept in sync as work
  progresses.
