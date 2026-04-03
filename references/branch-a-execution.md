# Branch A Execution Reference
> Used by the orchestrator, SDD UI Worker, and SDD Reviewer during Step 4.2.

## UI worker constraints
- one task per worker
- only approved spec inputs
- only declared target files
- no internal state unless the spec explicitly permits a controlled wrapper
- screenshot is visual guidance only
- tokenized JSON artifacts remain the style source of truth

## Required generated outputs
- Component.tsx or equivalent target component file
- matching Storybook story file
- required test file when declared by the spec

## Verification loop
- run the task-specific diagnostics listed in tasks.md
- reviewer checks spec alignment, token discipline, and diagnostic outcomes
- max 3 retries per task
- after a full batch passes, run aggregate verification before releasing the next batch