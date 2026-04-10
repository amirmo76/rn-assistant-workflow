# UI Assistant Workflow

One UI objective moves through these steps at a time.

## Spec Model

### Component spec

- Path: `specs/components/[component-name]/spec.md`
- Permanent source of truth for one component's current visual and behavioural contract.

### Objective spec

- Path: `specs/queue/[objective-name]/spec.md`
- Describes the current UI objective: new component, update, or bug fix.

---

## Step 1 — Receive Objective

- Accept the UI objective from the user along with any supporting visuals, files, or Figma URLs.
- Read /memories/session/ui-state.md to detect a resume path.
  - If resuming: re-anchor to the correct step and continue.
  - If fresh: create the state file and proceed to Step 2.
- Ask clarifying questions with `vscode/askQuestions` only when the objective is ambiguous.

**Exit criteria:** objective is clear and the route (fresh or resume) is decided.

---

## Step 2 — Detect Scope

- Call `python @~/.copilot/scripts/rn-architect.py --file <tree.yaml-path> --list-components` to get a full list of all the components in the scope of this objective.
- This is the list you will spawn spec writer agents per each in step 3.
- fully internalize the list.
- save the list in /memories/session/ui-state.md with status indicator for each component whether it is `pending`, `done`.

**Exit criteria:** component scope is clear and /memories/session/ui-state.md knows the exact list and proper status.

---

## Step 3 — Specify Objective

- Spawn one `RN Component Spec Writer` with a complete brief:
  - mode: `objective`
  - overall objective description
  - component scope
  - `tree.yaml` path
  - relevant visuals or Figma URLs
- The spec writer creates or updates `specs/queue/[objective-name]/spec.md`.
- Gate on explicit user approval.

**Exit criteria:** objective spec is approved by the user.

---

## Step 4 — Specify Components

- For each component in the objective scope, spawn exactly one `RN Component Spec Writer` with a complete brief:
  - mode: `component`
  - component name and file path
  - overall objective description
  - `tree.yaml` path
  - relevant visuals or Figma URLs
- The spec writer creates or updates `specs/components/[component-name]/spec.md` and `changelog.md`.
- Gate on explicit user approval for each component spec before moving to the next.
- After approval update /memories/sessions/ui-state.md.
- Do not proceed to Step 4 until all component specs are approved.

**Exit criteria:** every component in scope has an approved spec and updated changelog.

---

## Step 5 — Review

- Spawn `RN Review` with:
  - path to the objective spec
  - paths to all affected component specs and their changelogs
- `RN Review` checks that every required change listed in the objective spec is explicitly present in the matching component spec.
- On **FAIL**: return to Step 4 for each failed component. Then re-run Step 5.
- On **PASS**: the workflow is complete.

**Exit criteria:** `RN Review` returns PASS.

---

## Rules

- First thing you do is to detect component scop of the objective using the script.
- The workflow is not done unless all of the components in the scope have `done` status.
- objective spec is written before the comopnent specs.
- Component specs describe the current contract. Rewrite them cleanly; do not append loose notes.
- Never pause the workflow with plain-text approval requests or questions. All questions and approvals must go through `vscode/askQuestions`.
- The workflow runs continuously until `RN Review` returns PASS.
