# Branch A Initialization Reference
> Used by the orchestrator, SDD Researcher, and SDD Initializer during Step 1.5.

## Required outputs
- active git branch or a recorded git blocker
- detected package manager
- resolved token source of truth or recorded blocker
- verified or scaffolded Storybook
- verified or scaffolded test runner
- existing or created .ui-state/pages and .ui-state/components
- smoke-check command list with pass/fail results

## Token source policy
- Prefer an existing design-system.ts or equivalent semantic token source.
- If the repo already uses a different token file, map that file explicitly in session state.
- If no compatible source exists, do not invent one unless the workflow explicitly allows scaffolding.

## Storybook policy
- Detect existing Storybook configuration first.
- If missing and scaffolding is allowed, create only the minimum setup needed for the project stack.
- Record the exact script or command used to verify Storybook presence.

## Testing policy
- Detect the existing test runner first.
- If missing and scaffolding is allowed, add only the minimum setup needed for smoke tests.
- Record the exact verification command and result.

## Dirty worktree policy
- Never discard unrelated changes.
- Record dirty-state observations in session state and continue unless the brief explicitly blocks progress.