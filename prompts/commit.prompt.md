---
description: >
  Review uncommitted changes against SDD specs, update artifacts if needed,
  then commit with a conventional commit message.
agent: agent
tools:
  - read
  - search/codebase
  - edit/editFiles
  - edit/createFile
  - execute
  - diagnostics
---

You are running the SDD commit prompt. Follow these steps exactly.

## Step 1 — Gather changes

Run `git status` via terminal. Capture modified, added, and deleted files.
Run `git diff` (and `git diff --cached` if staged) to see actual changes.
If no changes → "Nothing to commit." and stop.

## Step 2 — Find related spec artifacts

For each changed file, determine which SDD feature it belongs to by scanning
`specs/doing/`, `specs/queue/`, `specs/done/` for matching plan.md/tasks.md references.

## Step 3 — Check if spec artifacts need updating

Compare changes against artifacts:
- tasks.md: mark completed tasks `[x]`, note unplanned changes
- plan.md: check for deviations from planned approach
- spec.md: check if requirements changed (rare)

## Step 4 — Apply updates

Update artifacts as needed. Keep changes minimal.

## Step 5 — Commit

1. `git add -A`
2. Generate conventional commit message: `type(scope): subject`
3. Show message, ask for approval
4. `git commit -m "[message]"`
5. Confirm: `✅ Committed: [hash] [subject]`
