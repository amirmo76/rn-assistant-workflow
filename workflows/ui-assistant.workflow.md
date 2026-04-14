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

- Call `python @~/.copilot/scripts/ui-architect.py --file <tree.yaml-path> --list-components` to get a full list of all the components in the scope of this objective.
- For each component in the list, also call `python @~/.copilot/scripts/ui-architect.py --file <tree.yaml-path> --context <component-name>` to collect any available context. If the output is "No context found", skip silently — this is expected when no context annotations exist for that component.
- Fully internalize both the component list and any context output.
- Save the list in /memories/session/ui-state.md with a status indicator for each component (`pending` / `done`). If context was found for a component, note it briefly beside its entry so spec writers can reference it without re-running the script.

**Exit criteria:** component scope is clear, context is gathered, and /memories/session/ui-state.md knows the exact list and proper status.

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

### Composition Group Detection

After the bottom-to-top order is determined, detect composition groups within the in-scope components before spec writing begins.

**Detection method:** infer groups from component naming patterns (shared prefix, e.g. `Card`, `CardHeader`, `CardFooter`, `CardBody`). Also use the component list and any available `--context` output to reason about likely groupings.

Present proposed composition groups to the user via `vscode/askQuestions` for approval. The user can accept, edit, or reject any grouping. Components not part of any group remain in the individual order unchanged.

**Restructure the ordered list in `/memories/session/ui-state.md`:**

- The **overall order remains bottom-to-top**, driven by hard dependencies — the same rule as before.
- A composition group is treated as a **unit** placed at the position of its most foundational member.
- **Within a composition group**, members are ordered foundational-first: the container or root member first, then members that depend on or extend it.
- Groups are listed under a named group header in session state so the boundary is visually clear.

**Exit criteria:** composition groups are approved by the user and recorded in `/memories/session/ui-state.md`. The ordered list (including groups) is the source of truth for Step 6.

---

## Step 6 — Specify Components

- For each component in the ordered objective scope, spawn exactly one `Component Spec Writer` with a complete brief:
  - mode: `component`
  - component name and file path
  - overall objective description
  - `tree.yaml` path
  - relevant visuals or Figma URLs
  - if the component belongs to a composition group: a **composition brief** containing:
    - the name of the composition group
    - the list of all member components in the group
    - each member's distinct responsibility within the composition (draft; spec writer may refine)
    - any known shared contracts: shared React Context, shared design tokens, shared spacing or border strategy
  - if session state records a sibling conflict for this component: include it in the brief so it is addressed during spec writing
- The spec writer creates or updates `specs/components/[component-name]/spec.md` and `changelog.md`.
- If the spec writer reports a **sibling conflict** in its output:
  - **Sibling not yet spec'd** (upcoming in order): record the conflict in session state beside the sibling's entry. Include it in the sibling's spec writer brief when its turn arrives.
  - **Sibling already spec'd** (turn already passed): after the current spec is user-approved, immediately spawn a spec writer for the sibling — out of normal order — to apply the specific adjustment. Gate on user approval of the updated spec. Then resume the original order. Track resolution in session state.
- Follow the saved bottom-to-top order strictly.
- After all component specs in a composition group are approved, proceed to Step 7 (Composition Review) for that group before continuing to the next group.
- Gate on explicit user approval for each component spec before moving to the next.
- After approval update /memories/session/ui-state.md.
- Do not proceed to Step 8 until all component specs are approved and all composition groups have passed Step 7.

**Exit criteria:** every component in scope has an approved spec and updated changelog; every composition group conflict is resolved and recorded in session state.

---

## Step 7 — Composition Review

After all component specs in a composition group are approved, spawn a `Composition Reviewer` for that group before moving to the next group or to the global review step.

**Trigger:** immediately after the last component spec in a composition group is user-approved.

- Spawn `Composition Reviewer` with:
  - the name of the composition group
  - paths to all member component specs
  - the objective spec path
- Wait for the result: `PASS` or `FAIL` with a specific, actionable list of issues keyed to component name and spec section.
- On **FAIL**: route failing components back through Step 6 (spec writing), then re-run Step 7 for that group.
- On **PASS**: continue to the next group, or to Step 8 once all groups have passed.

If there are no composition groups in scope, this step is a no-op; proceed directly to Step 8.

**Exit criteria:** every composition group has a `PASS` from the Composition Reviewer.

---

## Step 8 — Review

- Spawn `UI Review` with:
  - path to the objective spec
  - paths to all affected component specs and their changelogs
- `UI Review` checks that every required change listed in the objective spec is explicitly present in the matching component spec.
- On **FAIL**: return to Step 6 for each failed component. Then re-run Step 8.
- On **PASS**: proceed to Step 9.

**Exit criteria:** `RN Review` returns PASS.

---

## Step 9 — Plan Implementation

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

## Step 10 — Execute

Read the `Execution Map` from `plan.md`. Execute the plan phase by phase in strict sequence.

### Per Phase

1. Spawn one `UI Worker` per component listed in the phase — all in parallel.
   Each worker receives:
   - component name
   - path to component spec (`specs/components/[component-name]/spec.md`)
   - path to objective spec
   - the phase's work items from `plan.md` scoped to that component
   - project init facts from `/memories/session/ui-state.md` (package manager, stack)
2. Wait for all workers in the phase to report `done` or `blocked`.
3. After all workers complete, ask the user to verify the phase via `vscode/askQuestions`:
   - **Approved** → update phase status in `/memories/session/ui-state.md`, proceed to next phase.
   - **Change requested** → apply the requested change directly, then re-present for approval. Loop until explicit approval.

### After All Phases

- Update `/memories/session/ui-state.md` to mark the objective as complete.
- Announce completion to the user.

**Exit criteria:** every phase in the Execution Map is complete and approved by the user.

---

## Rules

- Initialize the project (Step 2) before doing any scope detection or spec work.
- First thing after init is to detect component scope and context using the architect script (`--list-components` then `--context` per component).
- The workflow is not done unless all phases of execution are approved and complete.
- Objective spec is written before the component specs.
- Component ordering must be decided before component spec writing starts.
- Composition group detection (Step 5) must run after ordering and before spec writing (Step 6).
- Component spec writing and planning both follow the saved bottom-to-top order.
- Component Spec Writer must never modify sibling spec files. Sibling conflicts must be reported in the spec writer's output and routed by the assistant.
- Composition Review (Step 7) fires per group after the group's last spec is approved. It does not replace the global Review step (Step 8).
- Component specs describe the current contract. Rewrite them cleanly; do not append loose notes.
- Never pause the workflow with plain-text approval requests or questions. All questions and approvals must go through `vscode/askQuestions`.
- Execution begins directly after planning — no intermediate tasking step.
- One worker per component per phase; workers within a phase run in parallel.
- Phases run strictly sequentially; no phase begins until the previous is user-approved.
- The workflow runs continuously until all execution phases are approved and complete.
