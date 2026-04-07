# Plan File Reference
> Used by the Planner agent when authoring or updating a `plan.md`.

---

## Purpose

A plan file translates a completed spec into an ordered, phased roadmap that
a Tasker agent can convert into executable tasks. It is the single source of
truth for implementation intent. It lives next to the spec it describes.

**Location:** `specs/[queue|doing]/component-[name]/plan.md`

---

## Required Sections

All sections must appear in every plan, in this order. Sections with no
content use the `_Not applicable_` marker — never omit them.

---

### 1. Header

```markdown
# Plan: [Component Name]

**Spec:** [relative path to spec.md]
**Status:** draft | ready | in-progress | done
**Created:** [ISO date]
**Updated:** [ISO date]
```

- `draft` — plan is written but not yet reviewed or approved for execution.
- `ready` — plan is reviewed; spec dir may be moved to `doing`.
- `in-progress` — tasker has consumed this plan; tasks are being executed.
- `done` — all phases completed and verified.

---

### 2. Objective

One short paragraph. What the plan achieves when complete. Must match the
intent of the spec without repeating it verbatim.

---

### 3. Phases

Number phases sequentially starting from 1. Each phase is a logical unit of
work that can be verified independently before the next begins.

```markdown
### Phase [N] — [Short Name]

**Status:** pending | in-progress | done | skipped
**Depends on:** Phase [X] | —

#### Context
What the worker needs to know entering this phase. Reference relevant
sections of the spec, existing codebase facts, or prior-phase outputs.

#### Actions
Ordered bullet list of the concrete steps to perform in this phase.

#### Expected Outcome
One sentence. What the codebase looks like when this phase finishes.

#### Success Criteria
Bullet list of verifiable conditions. Each criterion must be checkable
without subjective judgment — a test passes, a file exists, a command
succeeds.
```

#### Mandatory phases for a component build

Include at minimum these phases when building a new component from spec.
Adapt names and details to the actual spec; do not add phases that have no
work.

| Phase | Name | Typical content |
|-------|------|-----------------|
| 1 | Implementation | Create the component file; wire props and design tokens per spec. |
| 2 | Tests | Write unit/snapshot tests; all pass. |
| 3 | Storybook | Add a story that exercises all props and visual states. |
| 4 | Verification | Run the full test suite and Storybook build; confirm no regressions. |
| 5 | Review | Reviewer agent checks the artifact; iterate until PASS. |

Additional phases (e.g. accessibility audit, performance profiling,
integration into a parent component) are permitted when the spec calls for them.

---

### 4. Open Questions

```markdown
### Open Questions

- [ID: Q1] [Question text] — raised by Planner, [date]
- [ID: Q2] [Question text] — raised by Planner, [date]
```

Use `—` if there are no open questions.

---

### 5. Assumptions

```markdown
### Assumptions

- [Assumption text, and the consequence if it turns out to be wrong.]
```

Use `—` if there are no assumptions.

---

## Rules

- Phases must be in execution order. Do not mix unrelated concerns in one phase.
- Every success criterion must be independently verifiable.
- Status markers on phases must be kept current as the Tasker and Worker
  agents progress through execution.
- The plan file must never contain implementation code. It describes _what_
  to do, not _how_ to write it.
- The plan header `Status` field must be updated at each stage:
  Planner sets `draft`; orchestrator sets `ready` before moving to `doing`;
  Tasker sets `in-progress`; final Reviewer sets `done`.
