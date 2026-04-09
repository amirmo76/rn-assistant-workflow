# Task List Reference

Reference for `specs/tasks.md`.

## File Header

```markdown
# Task List

**Objective:** [Objective Name]
**Source plan:** specs/doing/[objective-name]/plan.md
```

## Batch Format

Each batch maps to one plan phase.

```markdown
## Batch [N] — [Phase Name]

| ID | Task | Depends on | Parallel | Status |
|----|------|------------|----------|--------|
| T001 | [Short task] | — | no | pending |
| T002 | [Short task] | T001 | yes | pending |
```

- `Depends on` points to the blocking task IDs.
- `Parallel` is `yes` only when the task can run alongside the immediately previous task.

## Task Detail Block

```markdown
### T001 — [Short task]

**Objective spec:** specs/doing/[objective-name]/spec.md
**Plan:** specs/doing/[objective-name]/plan.md
**Phase:** [Phase Name]

**Scope**
- Files, components, or behaviours this task is allowed to change.

**Work**
- What must be done.

**Checks**
- `typecheck`
- `lint`
- `test`

**Done when**
- Verifiable completion criteria.
```

## Rules

- Preserve the plan's dependency order and parallel structure.
- Group meaningful execution units together; do not split arbitrary tiny edits into separate tasks.
- `specs/tasks.md` is rewritten from the current objective plan.
- Only the current task, or justified parallel sibling tasks, may be `in-progress`.
