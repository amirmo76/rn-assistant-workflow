# Questioning Reference
> Used by the orchestrator during Steps 2 and 3.
> Defines HOW the orchestrator asks questions — strategy, not format.

## Core principle
Ask only when the answer changes what gets built.
Not when it changes how it looks. Not when it changes wording.
Only when a different answer produces a different set of files, functions, or behaviors.

## Pre-question triage (enforced)
Before forming any question, the orchestrator must have:
- Spawned researchers to scan the codebase
- Read the constitution
- Checked user-profile.md and learned-rules.md for known preferences
Questions the codebase already answers are BUCKET-A. Do not ask them.

## Question formation rules
- Max 4 questions per #tool:vscode/askQuestions call. Hard limit.
- Batch all into one call. Never sequential.
- Every bounded question (2–5 valid answers) MUST use options, not free text.
- Put the recommended option first. Mark it "(Recommended)" in the label only.
- Write one sentence of context before each question.
- Never ask about: naming conventions, comment style, import ordering,
  log format, error message wording — decide from existing code.
- Never ask: "would you like me to..." — decide yourself and present as default.

## Question types
TYPE-CHOICE: Bounded, one correct answer. 2–4 options.
TYPE-MULTI: Bounded, multiple may apply. 2–4 options.
TYPE-OPEN: No bounded options. Rare. Inline free-text question.

## After answers received
- Integrate immediately. No follow-up questions. No re-runs.
- Surface remaining ambiguities as BUCKET-B assumptions.
