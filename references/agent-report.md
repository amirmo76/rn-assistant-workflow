# Agent Report Reference
> Used by every agent in this workflow when returning a result to its caller.

---

## Purpose

A structured report is the only output contract between agents. Every agent
must return exactly one report shaped as described here. The calling agent
or orchestrator reads the report and decides the next step without
interpreting free-form text.

---

## Required Fields

All agents must return every field below. Fields that have no content must
still be present with the `—` placeholder. Do not omit or rename fields.

```
status:    success | partial | blocked
summary:   [One short paragraph. What happened, at a glance.]
inputs:    [Bullet list of what was received before starting work.]
actions:   [Bullet list — what the agent actually did, in order.]
findings:  [Bullet list — important observations about the target artifact,
            codebase state, or environment. Omit trivial detail.]
outputs:   [Bullet list — every file or artifact created or updated,
            with its path. Use — if nothing was produced.]
blockers:  [Bullet list — anything preventing progress or requiring
            a decision before work can continue. Use — if none.]
next_step: [Single sentence — the exact next action the orchestrator
            should take.]
```

### Status definitions

| Value | Meaning |
|-------|---------|
| `success` | All responsibilities completed; no unresolved blockers. |
| `partial` | Some responsibilities completed; blockers or missing inputs prevented the rest. List them under `blockers`. |
| `blocked` | No progress made; the agent cannot proceed without external input. All blockers listed. |

---

## Reviewer Extension

The Reviewer agent must include two additional fields after `findings`:

```
verdict: PASS | FAIL | WARN
issues:  [Bullet list — concrete findings that support the verdict.
          Required when verdict is FAIL or WARN. Use — for PASS.]
```

### Verdict definitions

| Value | Meaning |
|-------|---------|
| `PASS` | Artifact meets all criteria. Ready for user approval. |
| `WARN` | Artifact is acceptable but has risks or minor gaps. List them. User decides whether to approve or request fixes. |
| `FAIL` | Artifact does not meet the criteria. Must be reworked before approval. |

---

## Example Report

```
status:    success
summary:   Created plan.md for the PrimaryButton component covering five
           phases from implementation through Storybook verification.

inputs:
  - spec.md at specs/doing/component-primary-button/spec.md
  - references/plan.md (structure reference)

actions:
  - Read spec.md in full.
  - Searched codebase for existing button implementations.
  - Identified five logical phases.
  - Wrote plan.md to specs/doing/component-primary-button/plan.md.

findings:
  - A legacy Button component exists at src/components/Button.tsx but is
    not covered by tests.
  - The design system token file is at src/tokens/tokens.ts.

outputs:
  - specs/doing/component-primary-button/plan.md

blockers:
  —

next_step: Run the Tasker agent, pointing it at
           specs/doing/component-primary-button/plan.md.
```

---

## Rules

- Never return narrative prose in place of structured fields.
- Never skip a field.
- Keep `summary` to one paragraph; put detail in `findings`.
- `next_step` must be actionable and specific enough for the orchestrator
  to proceed without asking a follow-up question.
