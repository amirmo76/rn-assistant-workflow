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

## Step 2 — Initialize Project

- Spawn `UI Initializer` with the project root (infer from `tree.yaml` location or ask if ambiguous).
- Wait for the initializer to complete and return its readiness summary.
- If the initializer reports a blocker that cannot be auto-resolved, surface it to the user via `vscode/askQuestions` before continuing.
- Write the following key facts from the initializer brief into `/memories/session/ui-state.md` under an `## Init` section:
  - `platform` (e.g. React Native / Expo, Next.js, React)
  - `packageManager` (e.g. yarn, npm, pnpm)
  - `typescript` (true/false)
  - `stack` summary (notable libraries / framework flags)
  - `readiness` (PASS / PASS_WITH_WARNINGS / BLOCKED)
  - `blockers` list (empty when clean)

**Exit criteria:** project is ready for the workflow and init facts are persisted in `/memories/session/ui-state.md`.

---

## Step 3 — Detect Scope

- Call `python @~/.copilot/scripts/rn-architect.py --file <tree.yaml-path> --list-components` to get a full list of all the components in the scope of this objective.
- This is the list you will spawn spec writer agents per each in step 4.
- fully internalize the list.
- save the list in /memories/session/ui-state.md with status indicator for each component whether it is `pending`, `done`.

**Exit criteria:** component scope is clear and /memories/session/ui-state.md knows the exact list and proper status.

---

## Step 4 — Specify Objective

- Spawn one `Component Spec Writer` with a complete brief:
  - mode: `objective`
  - overall objective description
  - component scope
  - `tree.yaml` path
  - relevant visuals or Figma URLs
- The spec writer creates or updates `specs/queue/[objective-name]/spec.md`.
- Gate on explicit user approval.

**Exit criteria:** objective spec is approved by the user.

---

## Step 5 — Order Components

- Reorder the in-scope components from most primitive to most complex before any component spec writing begins.
- Use a bottom-to-top dependency view: lower-level building blocks first, composition layers after.
- Save the ordered list in /memories/session/ui-state.md and mark it as the required execution order for Step 6 and Step 8.
- Keep both the original detected scope and the ordered scope in state when useful, but the ordered scope is the source of truth for downstream execution.

**Exit criteria:** /memories/session/ui-state.md contains the approved bottom-to-top component order for this objective.

---

## Step 6 — Specify Components

- For each component in the ordered objective scope, spawn exactly one `Component Spec Writer` with a complete brief:
  - mode: `component`
  - component name and file path
  - overall objective description
  - `tree.yaml` path
  - relevant visuals or Figma URLs
- The spec writer creates or updates `specs/components/[component-name]/spec.md` and `changelog.md`.
- Follow the saved bottom-to-top order strictly.
- Gate on explicit user approval for each component spec before moving to the next.
- After approval update /memories/session/ui-state.md.
- Do not proceed to Step 7 until all component specs are approved.

**Exit criteria:** every component in scope has an approved spec and updated changelog.

---

## Step 7 — Review

- Spawn `UI Review` with:
  - path to the objective spec
  - paths to all affected component specs and their changelogs
- `UI Review` checks that every required change listed in the objective spec is explicitly present in the matching component spec.
- On **FAIL**: return to Step 6 for each failed component. Then re-run Step 7.
- On **PASS**: proceed to Step 8.

**Exit criteria:** `RN Review` returns PASS.

---

## Step 8 — Plan Implementation

- Spawn `UI Planner` with:
  - path to the approved objective spec
  - ordered bottom-to-top component scope from /memories/session/ui-state.md
  - paths to all affected component changelogs
- `UI Planner` writes `plan.md` beside the objective `spec.md`.
- The plan must consider the objective spec and every affected component changelog in scope.
- The plan must flow from primitive components upward.
- Components or workstreams that do not depend on each other must be batched into parallel phases or parallel work within a phase.

**Exit criteria:** `plan.md` exists beside the approved objective spec and reflects bottom-to-top, dependency-aware execution with justified parallel batching.

---

## Rules

- Initialize the project (Step 2) before doing any scope detection or spec work.
- First thing after init is to detect component scope of the objective using the script.
- The workflow is not done unless all of the components in the scope have `done` status.
- Objective spec is written before the component specs.
- Component ordering must be decided before component spec writing starts.
- Component spec writing and planning both follow the saved bottom-to-top order.
- Component specs describe the current contract. Rewrite them cleanly; do not append loose notes.
- Never pause the workflow with plain-text approval requests or questions. All questions and approvals must go through `vscode/askQuestions`.
- The workflow runs continuously until `plan.md` is written after a passing review.
