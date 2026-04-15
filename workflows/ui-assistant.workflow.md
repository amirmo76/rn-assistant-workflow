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

- Accept objective + any visuals, files, or Figma URLs from user.
- Read /memories/session/ui-state.md to detect resume path.
  - If resuming: re-anchor to correct step and continue.
  - If fresh: create state file and proceed to Step 2.
- Ask clarifying questions via `vscode/askQuestions` only when objective is ambiguous.

**Exit criteria:** objective is clear and route (fresh or resume) is decided.

---

## Step 2 — Initialize Project

- Spawn `UI Initializer` with project root (infer from `tree.yaml` location or ask if ambiguous).
- Wait for initializer to complete and return its readiness summary.
- If initializer reports a blocker that can't be auto-resolved, surface it via `vscode/askQuestions` before continuing.
- Write key init facts to `/memories/session/ui-state.md` under an `## Init` section:
  - `platform` (e.g. React Native / Expo, Next.js, React)
  - `packageManager` (e.g. yarn, npm, pnpm)
  - `typescript` (true/false)
  - `stack` summary (notable libraries / framework flags)
  - `readiness` (PASS / PASS_WITH_WARNINGS / BLOCKED)
  - `blockers` list (empty when clean)

**Exit criteria:** project is ready, testing and storybook setup, init facts persisted in `/memories/session/ui-state.md`.

### Shadcn Readiness Check (web projects only)

After UI Initializer completes:

1. Run `python ~/.copilot/scripts/ui-architect.py --file <tree.yaml-path> --list-components` and scan source column for `shadcn/...` entries.
2. If found: check whether `shadcn MCP` tools are available. Record `shadcnMcpAvailable: true` or `shadcnMcpAvailable: false` in `/memories/session/ui-state.md` under `## Init`.
3. If shadcn primitives in scope and `shadchnMcpAvailable: false`: warn user via `vscode/askQuestions` — they can continue (spec writer falls back to full spec) or pause to configure MCP.
4. If platform is React Native / Expo, skip this check entirely.

---

## Step 3 — Detect Scope

- Call `python @~/.copilot/scripts/ui-architect.py --file <tree.yaml-path> --list-components` to get all components in scope. Output is tab-separated: `ComponentName<TAB>shadcn/<id> or none`. Record component name and source annotation for each.
- For each component, call `python @~/.copilot/scripts/ui-architect.py --file <tree.yaml-path> --context <component-name>` to collect available context. If output is "No context found", skip silently.
- Internalize both component list and context output.
- Save list in /memories/session/ui-state.md with status indicator per component (`pending` / `done`). Record source annotation per component. If context found, note it briefly beside the entry.

**Exit criteria:** component scope is clear, context gathered, and /memories/session/ui-state.md has exact list, source annotations, and status for each component.

---

## Step 4 — Specify Objective

- Spawn one `Component Spec Writer` with a complete brief:
  - mode: `objective`
  - overall objective description
  - component scope
  - `tree.yaml` path
  - relevant visuals or Figma URLs
- Spec writer creates or updates `specs/queue/[objective-name]/spec.md`.
- Gate on explicit user approval.

**Exit criteria:** objective spec is approved by user.

---

## Step 5 — Order Components

- Reorder in-scope components from most primitive to most complex before any component spec writing.
- Use bottom-to-top dependency view: lower-level building blocks first, composition layers after.
- Save ordered list in /memories/session/ui-state.md as required execution order for Steps 6 and 8.
- Keep both original detected scope and ordered scope in state when useful; ordered scope is source of truth for downstream execution.

### Composition Group Detection

After bottom-to-top order is determined, detect composition groups before spec writing.

**Detection method:** infer groups from naming patterns (shared prefix, e.g. `Card`, `CardHeader`, `CardFooter`, `CardBody`). Also use component list and `--context` output.

Present proposed groups via `vscode/askQuestions` for approval. User can accept, edit, or reject any grouping. Components not in any group stay in individual order unchanged.

**Restructure ordered list in `/memories/session/ui-state.md`:**

- **Overall order remains bottom-to-top**, driven by hard dependencies.
- Composition group treated as a **unit** placed at position of its most foundational member.
- **Within a group**, members ordered foundational-first: container/root first, then members that depend on or extend it.
- Groups listed under named group header in session state.

**Exit criteria:** composition groups approved and recorded in `/memories/session/ui-state.md`. Ordered list (including groups) is source of truth for Step 6.

---

## Step 6 — Specify Components

- For each component in ordered scope, spawn exactly one `Component Spec Writer` with a complete brief:
  - mode: `component`
  - component name and file path
  - overall objective description
  - `tree.yaml` path
  - relevant visuals or Figma URLs
  - if component belongs to composition group: a **composition brief** containing:
    - name of the composition group
    - list of all member components
    - each member's distinct responsibility (draft; spec writer may refine)
    - any known shared contracts: shared React Context, design tokens, spacing or border strategy
  - if session state records sibling conflict: include in brief so it is addressed during spec writing
  - **shadcn source check:** look up component source from session state. If `shadchnMcpAvailable: true` AND source is `shadcn/<id>`, add `shadchnSource: <component-id>` to brief and note it is a delta spec. Otherwise full spec process applies.
- Spec writer creates or updates `specs/components/[component-name]/spec.md` and `changelog.md`.
- If spec writer reports **sibling conflict**:
  - **Sibling not yet spec'd** (upcoming): record conflict in session state beside sibling's entry. Include in sibling brief when its turn arrives.
  - **Sibling already spec'd** (turn passed): after current spec approved, immediately spawn spec writer for sibling out of order. Gate on approval, then resume original order. Track in session state.
- Follow saved bottom-to-top order strictly.
- After all specs in a composition group approved, proceed to Step 7 for that group before next group.
- Gate on explicit user approval for each component spec before moving to next.
- After approval, update /memories/session/ui-state.md.
- Don't proceed to Step 8 until all component specs approved and all composition groups passed Step 7.

**Exit criteria:** every component has approved spec and updated changelog; every composition group conflict resolved and recorded in session state.

---

## Step 7 — Composition Review

After all component specs in a composition group are approved, spawn `Composition Reviewer` for that group before moving to next group or global review.

**Trigger:** immediately after last component spec in a group is user-approved.

- Spawn `Composition Reviewer` with:
  - name of the composition group
  - paths to all member component specs
  - objective spec path
- Wait for result: `PASS` or `FAIL` with actionable issues keyed to component name and spec section.
- On **FAIL**: route failing components back through Step 6, then re-run Step 7 for that group.
- On **PASS**: continue to next group, or Step 8 once all groups passed.

No composition groups in scope: skip to Step 8.

**Exit criteria:** every composition group has `PASS` from Composition Reviewer.

---

## Step 8 — Review

- Spawn `UI Review` with:
  - path to objective spec
  - paths to all affected component specs and their changelogs
- `UI Review` checks every required change in objective spec is explicitly present in matching component spec.
- On **FAIL**: return to Step 6 for each failed component. Re-run Step 8.
- On **PASS**: proceed to Step 9.

**Exit criteria:** `UI Review` returns PASS.

---

## Step 9 — Plan Implementation

- Spawn `UI Planner` with:
  - path to approved objective spec
  - ordered bottom-to-top component scope from /memories/session/ui-state.md
  - paths to all affected component changelogs
- `UI Planner` writes `plan.md` beside the objective `spec.md`.
- Plan must consider objective spec and every affected component changelog in scope.
- Plan must flow from primitive components upward.
- Independent components or workstreams must be batched into parallel phases or parallel work within a phase.

**Exit criteria:** `plan.md` exists beside approved objective spec, reflects bottom-to-top dependency-aware execution with justified parallel batching.

---

## Step 10 — Execute

Read `Execution Map` from `plan.md`. Execute plan phase by phase in strict sequence.

### Per Phase

1. Spawn one `UI Worker` per component in the phase — all in parallel.
   Each worker receives:
   - component name
   - path to component spec (`specs/components/[component-name]/spec.md`)
   - path to objective spec
   - phase's work items from `plan.md` scoped to that component
   - project init facts from `/memories/session/ui-state.md` (package manager, stack)
   - **for shadcn-backed primitives** (web only): if component spec has a **Registry Source** section, worker must:
     1. Run install command from spec: `npx shadcn@latest add <component-id>`.
     2. After install, apply only local overrides from **Local Overrides** section.
     3. If install fails: surface error via `vscode/askQuestions` before continuing. Don't guess or proceed silently.
     4. If no Registry Source section, proceed with standard worker process.
2. Wait for all workers to report `done` or `blocked`.
3. After all workers complete, ask user to verify phase via `vscode/askQuestions`:
   - **Approved** → update phase status in `/memories/session/ui-state.md`, proceed to next phase.
   - **Change requested** → apply change, re-present for approval. Loop until explicit approval.

### After All Phases

- Update `/memories/session/ui-state.md` to mark objective as complete.
- Announce completion to user.

**Exit criteria:** every phase in Execution Map is complete and approved by user.

---

## Rules

- Initialize project (Step 2) before any scope detection or spec work.
- After init, detect component scope and context using architect script (`--list-components` then `--context` per component).
- Workflow is not done until all execution phases are approved and complete.
- Write objective spec before component specs.
- Decide component ordering before component spec writing starts.
- Composition group detection (Step 5) runs after ordering and before spec writing (Step 6).
- Spec writing and planning both follow saved bottom-to-top order.
- Component Spec Writer must never modify sibling spec files. Sibling conflicts reported in spec writer output and routed by assistant.
- Composition Review (Step 7) fires per group after group's last spec approved. Doesn't replace global Review (Step 8).
- Component specs describe current contract. Rewrite cleanly; don't append loose notes.
- Never pause workflow with plain-text questions or approvals. All questions and approvals via `vscode/askQuestions`.
- Execution begins directly after planning — no intermediate tasking step.
- One worker per component per phase; workers within a phase run in parallel.
- Phases run strictly sequentially; no phase begins until previous is user-approved.
- Workflow runs continuously until all execution phases are approved and complete.
