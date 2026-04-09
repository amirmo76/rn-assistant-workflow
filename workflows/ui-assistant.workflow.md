# UI Assistant Workflow

One UI objective moves through this workflow at a time.

## Spec Model

### Component spec

- Path: `specs/components/[component-name]/spec.md`
- Permanent source of truth for one component's current visual and behavioural contract.
- Never queued, planned, taskified, or moved through workflow states.

### Objective spec

- Path: `specs/[queue|doing|done]/[objective-name]/spec.md`
- Describes the current UI objective: new component, update, or bug fix.
- Lifecycle: `queue -> doing -> plan -> tasks -> execute -> approve -> done`

## Flow

1. Start from the UI objective and any supporting visuals, files, or Figma URLs.

2. Ask clarifying questions with `vscode/askQuestions` only when needed.

3. Run `RN Initializer`.

4. Create the objective spec in `specs/queue/[name]/spec.md`. Run `RN Architect` first and finalize the full architecture before finalizing the rest of the objective spec. The architecture is not finalized until every component in the tree — at every level — is recursively resolved to atoms; every non-atom component must have its own approved dependency list before its parent is considered done. Ask only for information required to make the objective spec unambiguous.

5. Read every existing component spec affected by the objective. Update each affected file in `specs/components/` so it matches the new objective. If a component architecture is unclear or must change, run `RN Architect` for that component and get approval on the final architecture before rewriting its spec. Each component-spec change needs explicit user approval.

6. Get final approval for the objective spec.

7. Move the objective directory from `specs/queue/[name]/` to `specs/doing/[name]/`.

8. Run `RN Planner` to create one objective-level plan at `specs/doing/[name]/plan.md`. The plan is phase-based, dependency-aware, and explicit about sequential work vs justified parallel work. Any component creation or change includes tests and story coverage.

9. Run `RN Tasker` to create `specs/tasks.md` from that plan. Tasks preserve the plan's dependency order and parallel structure and group meaningful execution units.

10. Assign tasks to `RN Worker` one at a time. The worker completes the assigned task, runs typecheck, lint, and tests, fixes direct issues, and reports back. The user approves each task result before the next task is treated as complete.

11. When the objective is complete, get final approval and move the objective directory to `specs/done/[name]/`.

## Rules

- Architecture is the first priority. Do not finalize an objective spec before the architecture is approved.
- Component specs are rewritten as current source-of-truth files. Do not append loose notes.
- Planning is objective-level, not component-by-component micro-planning.
- Never pause the workflow with plain-text approval requests or questions. All questions and approvals must go through `vscode/askQuestions`. The workflow runs continuously until final approval at step 11.
