# UI Assistant Workflow

This workflow governs how the UI Assistant agent handles requests to build
or update a React Native component. The agent follows these phases in order,
adapting based on what context was already provided.

---

## Phase 0 — Understand the Request

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

## Phase 1 — Explore Current State

Run the **Explore** subagent with a focused brief:

- Does `specs/component-[name]/spec.md` already exist? What does it contain?
- Is there an existing implementation of this component in the codebase?
  Where is it? What does its current props interface look like?
- Are there any closely related components already specced or implemented?

Collect the findings. They will inform every subsequent phase.

---

## Phase 2 — Collect Missing Context

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

## Phase 3 — Architecture (conditional)

Run this phase **only when** one of the following is true:
- Task is `build` and no architecture was provided or found in an existing spec.
- Task is `update` and the update requires structural changes (adding, removing,
  or renaming direct children).

If architecture is already known (provided by user or found in existing spec
and unchanged by the update), skip to Phase 4.

### When running:

Invoke the **UI Architect** subagent. Provide:
- Component name and a one-line description of its role.
- Atomic level (if known).
- Any visual context available (image paths and/or Figma URLs).
- Findings from Phase 1 (existing related components).

The Architect will discuss the architecture with the user and return a
finalized architecture in arrow notation:

```
ComponentName -> ChildA, ChildB, ChildC
```

Capture this output for Phase 4.

---

## Phase 4 — Spec Writing

Invoke the **UI Component Spec Writer** subagent. Provide all gathered context:

- Component name.
- Atomic level.
- Architecture in arrow notation.
- Visual context: local image paths and/or Figma URLs (pass everything available).
- Brief from Phase 1: whether a spec already exists and any relevant
  findings about existing implementations or related components.

The Spec Writer will handle its own research, drafting, and iterative review
loop with the user. It will write the final spec to
`specs/component-[component-name-kebab]/spec.md`.

---

## Phase 5 — Wrap Up

After the Spec Writer has confirmed the spec is written:

1. Confirm the output path to the user.
2. If the task was `update`, briefly state what changed at a high level.
3. Suggest any natural next steps (e.g. sibling components that may need
   updating given this component's new contract, or implementation if the
   project uses a queue).

---

## Decision Tree (quick reference)

```
User request
  │
  ├─ Component name missing? → ask via vscode/askQuestions
  │
  ├─ Phase 1: Explore current state
  │
  ├─ Phase 2: Collect missing context (single askQuestions if needed)
  │
  ├─ Architecture needed?
  │    yes → Phase 3: UI Architect
  │    no  → skip
  │
  └─ Phase 4: UI Spec Writer → Phase 5: Wrap up
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
- **Delegate, do not duplicate.** Do not perform spec writing or architecture
  review inline — always delegate to the appropriate subagent.
