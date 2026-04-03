# Branch A Questioning Reference
> Used by the orchestrator at Step 0, Step 1.0, Step 3.2, and Step 5.1.
> Defines when the workflow may interrupt execution for explicit user input.

## Core principle
Ask only when the workflow requires a decision that changes routing, approval, or
blocking setup.

For Branch A this means:
- malformed or incomplete Figma targeting at Step 1.0
- resume versus restart decisions when prior artifacts already exist
- token-source or scaffolding decisions the initializer is not allowed to infer
- spec approval or rejection at Step 3.2
- final commit confirmation at Step 5.1

## Hard rules
- All required user interaction must go through vscode/askQuestions.
- Max 4 questions per call.
- Batch questions into one call whenever possible.
- Use fixed options for bounded choices.
- Freeform text is allowed only for feedback or missing identifiers.
- Do not ask questions the repo, workflow state, or Figma metadata can answer.

## Required approval tokens
- Step 3.2 approval must record exactly `APPROVE` or `REJECT_WITH_FEEDBACK`.
- Step 5.1 commit confirmation must record an explicit yes/no style decision in the askQuestions result.

## Recommended question shapes
- Resume choice: `Resume existing artifacts` or `Restart from fresh extraction`
- Token-source choice: `Use existing token source`, `Map alternate token source`, or `Block and decide later`
- Spec gate: `APPROVE` or `REJECT_WITH_FEEDBACK`

## After answers received
- Update /memories/session/sdd-state.md immediately.
- Resume exactly from the recorded checkpoint.
- Do not ask follow-up questions unless the workflow still cannot proceed safely.
