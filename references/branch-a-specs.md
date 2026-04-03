# Branch A Spec Reference
> Used by the orchestrator, SDD Spec Writer, and SDD Reviewer during Step 3.1.

## Required spec sections
- component header with source JSON and diff status
- props contract
- visual variants
- interaction states
- accessibility requirements
- explicit non-goals
- target files and required imports
- Storybook coverage expectations
- required tests and verification commands
- reference screenshot path

## Required contract rules
- Components are presentational only.
- No internal state unless the approved spec explicitly allows a controlled wrapper.
- Tokens, not raw style literals, define visual values.
- Accessibility requirements must be explicit for interactive and semantic elements.
- Hidden dependencies are not allowed.

## Reviewer fail conditions
- missing props, variants, or states
- missing screenshot path or verification expectations
- token leaks
- illegal internal state allowance
- unspecified target files