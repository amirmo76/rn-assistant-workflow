# UI Assistant Workflow

This workflow governs how the UI Assistant agent handles requests to build
or update a React Native component. The agent follows these phases in order,
adapting based on what context was already provided.

---

## Phase 0 — Initialize

Run the **Initializer** subagent before any planning or implementation work.

The Initializer:
- Verifies the test runner is configured and passing.
- Verifies Storybook is installed and has at least one story.
- Creates minimal smoke pieces if either is missing.
- Returns a readiness report.

Read the report. If `status` is `blocked`, stop and tell the user what must
be fixed before proceeding. If `status` is `partial` or `success`, continue
to the next phase and surface any warnings to the user.

The Initializer runs **once per session**. If it has already been run and
returned `success` or `partial`, skip this phase.

---

## Phase 1 — Understand the Request

Parse the user's message to determine:

- **Component name** — must be known before any other phase can start.
- **Task type** — `build` (new component), `update` (modify existing), or
  ambiguous.
- **Provided context** — what the user has already supplied:
  - Atomic level
  - Architecture (direct children)
  - Visual context: local image paths and/or Figma URLs

If the component name is missing, ask for it immediately via
`vscode/askQuestions` before continuing.

---

## Phase 2 — Explore Current State

Run the **Explore** subagent with a focused brief:

- Does `specs/queue/component-[name]/spec.md` already exist? What does it contain?
- Is there an existing implementation of this component in the codebase?
  Where is it? What does its current props interface look like?
- Are there any closely related components already specced or implemented?

Collect the findings. They will inform every subsequent phase.

---

## Phase 3 — Collect Missing Context

Review what the user provided and what Explore found. Determine the minimum
additional context needed to proceed.

Use a **single** `vscode/askQuestions` call to collect everything that is
missing. Do not ask piecemeal.

Gather:

| Context | Needed when |
|---------|-------------|
| Atomic level | Not provided and not deducible from existing spec/code. |
| Architecture (direct children) | Not provided, no existing spec describes it, and the task is `build` or a structural `update`. |
| Visual context (Figma URL or image) | Not provided and the task involves visual changes or a new component. If the user has no visual, proceed without it but note its absence. |
| Scope of update | Task type is `update` — what specifically needs to change? |

**Never ask for information already supplied by the user or found by Explore.**
If the user did not provide visuals but the task can proceed without them,
skip that question entirely.

---

## Phase 4 — Architecture (conditional)

Run this phase **only when** one of the following is true:
- Task is `build` and no architecture was provided or found in an existing spec.
- Task is `update` and the update requires structural changes (adding, removing,
  or renaming direct children).

If architecture is already known (provided by user or found in existing spec
and unchanged by the update), skip to Phase 5.

### When running:

Invoke the **UI Architect** subagent. Provide:
- Component name and a one-line description of its role.
- Atomic level (if known).
- Any visual context available (image paths and/or Figma URLs).
- Findings from Phase 2 (existing related components).

The Architect will discuss the architecture with the user and return a
finalized architecture in arrow notation:

```
ComponentName -> ChildA, ChildB, ChildC
```

Capture this output for Phase 5.

---

## Phase 5 — Spec Writing

Invoke the **UI Component Spec Writer** subagent. Provide all gathered context:

- Component name.
- Atomic level.
- Architecture in arrow notation.
- Visual context: local image paths and/or Figma URLs (pass everything available).
- Brief from Phase 2: whether a spec already exists and any relevant
  findings about existing implementations or related components.

The Spec Writer handles its own research, drafting, and iterative review
loop with the user. It writes the final spec to
`specs/queue/component-[component-name-kebab]/spec.md`.

---

## Phase 6 — Plan

Invoke the **Planner** subagent. Provide:
- Path to the approved spec: `specs/queue/component-[name]/spec.md`.

The Planner researches the codebase, derives phased work, and writes
`specs/queue/component-[name]/plan.md` with status `draft`.

After the Planner returns, present the plan to the user for review via
`vscode/askQuestions`:

- **Approve** — proceed to Phase 7.
- **Request changes** — relay the changes to the Planner and loop back.

---

## Phase 7 — Move to Doing

Before moving, confirm the spec is not blocked by another spec currently
in `doing`. A spec is blocked if it depends on a component whose spec is
still in `queue` or `doing`.

- If **unblocked**: move the entire `specs/queue/component-[name]/` directory
  to `specs/doing/component-[name]/`. Update the plan header `Status` from
  `draft` to `ready`.
- If **blocked**: inform the user which dependency must be resolved first.
  Do not move the directory. Return to Phase 6 for the blocking dependency.

---

## Phase 8 — Tasking

Invoke the **Tasker** subagent. No arguments required; it scans `specs/doing`
automatically.

The Tasker writes or updates `specs/tasks.md` and updates the plan status
to `in-progress`. Review the generated task list and confirm with the user
before proceeding to execution.

---

## Phase 9 — Execute Tasks

Work through `specs/tasks.md` task by task. For each `pending` task:

1. Mark the task `in-progress` in `specs/tasks.md`.
2. Invoke the **Worker** subagent with the task's full detail block.
3. Read the Worker's report.
   - If `blocked`: surface the blocker to the user and pause execution.
   - If `success`: proceed to review.
4. Invoke the **Reviewer** subagent with the artifact path, criteria, and
   spec path from the task detail block.
5. Read the Reviewer's verdict:
   - `PASS`: present artifact to the user for approval.
   - `WARN`: present artifact and warnings; await user decision.
   - `FAIL`: relay issues back to the Worker and repeat from step 2.
6. On user approval, mark the task `done` and proceed to the next task.

### Parallel tasks

When a task has `Parallel: yes`, it can be run simultaneously with the
preceding task. Invoke two Worker subagents in parallel and collect both
reports before either Reviewer step.

---

## Phase 10 — Wrap Up

After all tasks in `specs/tasks.md` are `done`:

1. Update the plan header `Status` to `done`.
2. Move the spec dir from `specs/doing/` to `specs/done/`.
3. Confirm the completed component to the user with the spec and
   implementation paths.
4. Suggest any natural next steps (sibling components, integration work,
   or documentation).

---

## Decision Tree (quick reference)

```
User request
  │
  ├─ Phase 0: Initializer (once per session)
  │    blocked? → stop; tell user what to fix
  │
  ├─ Phase 1: Understand request
  │    Component name missing? → ask via vscode/askQuestions
  │
  ├─ Phase 2: Explore current state
  │
  ├─ Phase 3: Collect missing context (single askQuestions if needed)
  │
  ├─ Architecture needed?
  │    yes → Phase 4: UI Architect
  │    no  → skip
  │
  ├─ Phase 5: UI Component Spec Writer (iterates until user approves)
  │
  ├─ Phase 6: Planner → user approves plan
  │
  ├─ Phase 7: Move queue → doing (if unblocked)
  │
  ├─ Phase 8: Tasker → user confirms task list
  │
  ├─ Phase 9: Worker → Reviewer → user approval (loop per task)
  │
  └─ Phase 10: Wrap up
```

---

## Rules

- **Single interruption per phase.** Batch all questions for a given phase
  into one `vscode/askQuestions` call. Do not ask multiple rounds unless a
  blocking ambiguity surfaces mid-phase.
- **Never re-ask for provided context.** If the user supplied something in
  their initial message, do not ask for it again.
- **Exploration before questions.** Always run Explore before asking the user.
  Do not ask the user for information that can be found in the codebase.
- **Delegate, do not duplicate.** Do not perform spec writing, planning,
  architecture review, implementation, or artifact review inline — always
  delegate to the appropriate subagent.
- **Never skip the Reviewer.** Every artifact produced by the Worker must
  pass through the Reviewer before the user is asked to approve it.
- **One task in-progress at a time** unless the task carries `Parallel: yes`.
