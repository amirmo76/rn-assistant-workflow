# Update

Update the workflow and the required agent/reference files to support a two-spec model.

Keep every file compact. Remove anything that does not belong to this workflow. Do not add extra explanation, duplicated steps, or obsolete process details.

## Spec model

There are two kinds of specs:

1. Component specs
   - Each component has exactly one source-of-truth spec at `specs/components/[component-name]/spec.md`.
   - A component spec describes the current visual and behavioural contract clearly enough to implement the component without follow-up questions.
   - Component specs are permanent source-of-truth files.
   - Component specs are not queued, planned, taskified, or moved through workflow states.

2. Objective specs
   - An objective spec represents the current UI objective: a new component, a component update, or a bug fix.
   - Objective specs move through the workflow stages `queue -> doing -> plan -> tasks -> execute -> approve -> done`.
   - The objective spec file is created in `specs/queue/[name]/`, moved to `specs/doing/[name]/` after approval, stays there while plan/tasks/execution happen, and is moved to `specs/done/[name]` only after final approval.

## Workflow

1. Start from a UI objective, usually supported by visuals, files, or Figma URLs.
2. Ask clarifying questions with `vscode/askQuestions` only when needed.
3. Run the initializer.
4. Build the objective spec in `specs/queue`.
   - Use the architect agent to define the full component architecture first.
   - Architecture is the first priority and must be clarified and approved before the rest of the objective spec is finalized.
   - The architect agent must support review, discussion, and finalization of the architecture.
   - Ask about anything else needed to make the objective spec unambiguous.
   - The rn-tree-decomposition skill reference file must be updated to match this format.
5. Check the existing component specs related to the objective.
   - Update every affected component spec so it matches the new objective.
   - If a component architecture is unclear or needs to change, use the architect agent for that component and get approval on the final architecture.
   - Rewrite component specs as needed so each one remains the current source of truth. Do not just append loose notes.
   - The user must approve each component-spec change.
6. Get final user approval for the objective spec.
7. Move the objective spec to `specs/doing/[name]`.
8. Build one overall plan for the objective spec.
   - The plan must focus on the objective, not on tiny component-by-component micro-steps.
   - The plan should follow the implementation path from lower-level dependencies upward where that helps execution order.
   - The plan must be phase-based and dependency-aware.
   - The planner should explicitly identify which work can run in parallel and which work must stay sequential.
   - Parallelism should be used when it is justified by clear dependency independence. Do not force parallelism when dependencies are uncertain.
   - As soon as a component has everything it needs, it may be planned for parallel implementation with other ready components.
   - Any component creation or change must include tests and story coverage.
   - The plan reference file must be updated to match this format.
9. Create `specs/tasks.md` from the plan.
   - Tasks must preserve the dependency and parallel structure of the plan.
   - Tasks should group work by meaningful execution units, not by arbitrary tiny edits.
   - The task-list reference file must be updated to match this format.
10. The orchestrator assigns tasks to workers one by one.
    - Each worker completes the assigned task, runs typecheck, lint, and tests, fixes issues until clean, and reports back.
    - The user approves each task result before the next task is considered complete.
11. When the objective is fully complete, get final user approval and move the objective spec to `specs/done/[name]`.

## Cleanup

- Remove the reviewer agent from the workflow completely.
- Update the remaining agents so they support only this workflow and only contain what they need.
- Update skill files so they are in `skills/[skill-name-kebab]/SKILL.md`.
- Update the `install.py`.
- Remove obsolete content from workflow, agent, and reference files.
- Keep the resulting files short, explicit, and unambiguous.
