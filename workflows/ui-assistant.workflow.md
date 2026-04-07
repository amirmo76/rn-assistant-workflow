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

## Phase 5 — Spec All Required Components

Identify every component that must exist before the target component can be
built. Walk the architecture tree (from Phase 4) and collect all child
components, recursively. Each component not yet specced in `specs/queue/`,
`specs/doing/`, or `specs/done/` is **required**.

### 5a — Write dependency specs first

For each required component, write its spec **before** writing the target
component's spec. Work leaves-first (most deeply nested first). For each
component:

1. Invoke the **UI Component Spec Writer** subagent with:
   - Component name, atomic level, architecture (direct children).
   - Any relevant visual context (images/Figma URLs) carried from Phase 3.
   - Whether an existing spec or implementation was found (from Phase 2 /
     Explore).
2. Present the draft spec to the user for review via `vscode/askQuestions`:
   - **Approve** — treat spec as done; continue.
   - **Request changes** — relay changes to the Spec Writer and loop back.
3. Do **not** advance to the next component until the current spec is approved.

### 5b — Write the target component's spec last

After every dependency spec is approved, invoke the **UI Component Spec
Writer** for the originally requested component, following the same
write → present → approve loop.

**Do not proceed to Phase 6 until every required spec is approved.**

---

## Phase 6 — Plan All Components

For each approved spec — in the same leaves-first dependency order used in
Phase 5 — produce a plan:

1. Invoke the **Planner** subagent with the path to the spec:
   `specs/queue/component-[name]/spec.md`.
2. The Planner writes `specs/queue/component-[name]/plan.md` with status
   `draft`.
3. Present the plan to the user for review via `vscode/askQuestions`:
   - **Approve** — continue to the next component.
   - **Request changes** — relay changes to the Planner and loop back.

**Do not proceed to Phase 7 until plans for every required component are
approved.**

---

## Phase 7 — Move All to Doing

Move every planned component directory from `specs/queue/` to `specs/doing/`
in dependency order (leaves first, so no `doing` entry depends on a component
still in `queue`). For each component:

1. Move the **entire** directory `specs/queue/component-[name]/` → `specs/doing/component-[name]/`
   **recursively in a single operation** (e.g. `mv specs/queue/component-[name] specs/doing/`). Do not copy files one by one. Do not leave an empty source directory behind.
2. Update the plan header `Status` from `draft` to `ready`.

Do not move a component if any of its dependencies are still in `queue`.
Resolve all dependency moves before moving a dependant.

---

## Phase 8 — Build Task List

Invoke the **Tasker** subagent. No arguments required; it scans `specs/doing`
automatically and reads plans in dependency order (leaves first).

The Tasker writes or updates `specs/tasks.md`, inserts parallel markers where
tasks across or within phases can safely run simultaneously, and updates each
plan's `Status` to `in-progress`. Review the generated task list and confirm
with the user before proceeding to execution.

---

## Phase 9 — Execute Tasks

**The orchestrator (UI Assistant) assigns every task. A Worker agent must
never choose its own task.**

Work through `specs/tasks.md` in order. For each `pending` task:

1. Mark the task `in-progress` in `specs/tasks.md`.
2. **Assign** the task: invoke the **Worker** subagent with the task's full
   detail block copied from `specs/tasks.md`.
3. Read the Worker's report.
   - If `blocked`: surface the blocker to the user and pause execution.
   - If `success`: proceed to review.
4. Invoke the **Reviewer** subagent with the artifact path, criteria, and
   spec path from the task detail block.
5. Read the Reviewer's verdict:
   - `PASS`: present artifact to the user for approval.
   - `WARN`: present artifact and warnings; await user decision.
   - `FAIL`: relay issues back to the Worker (re-assign) and repeat from
     step 2.
6. On user approval, mark the task `done` in `specs/tasks.md` and proceed
   to the next task.

### Parallel tasks

When a task has `Parallel: yes`, it can run simultaneously with the
task immediately above it. Invoke multiple **Worker** subagents in parallel
(one per parallel task). Collect all Workers' reports, then run Reviewers
in parallel, then present all artifacts to the user for sequential approval.

---

## Phase 10 — Wrap Up

After all tasks in `specs/tasks.md` that belong to a component are `done`:

1. Update the component's `plan.md` header `Status` to `done`.
2. Move the **entire** spec directory `specs/doing/component-[name]/` → `specs/done/component-[name]/`
   **recursively in a single operation** (e.g. `mv specs/doing/component-[name] specs/done/`). Do not copy files one by one. Do not leave an empty source directory behind.
3. Remove any leftover temporary files created during execution (e.g. draft
   snapshots, scratch notes). Do not remove the spec or plan.
4. Repeat steps 1–3 for every component that has all tasks done, in
   dependency order.
5. Confirm the completed work to the user with a summary listing each spec
   and its implementation path.
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
