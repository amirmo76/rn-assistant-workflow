# Branch A Token Taxonomy Reference
> Used by SDD Token Synthesizer during Step 2.2 and by SDD UI Worker during Step 4.2.

## Absolute rule
No raw design literals survive past Step 2.2 when a semantic token is required.

## Must scrub
- hex colors
- absolute pixel values
- raw spacing literals
- raw border radius literals
- raw typography values when a semantic token exists

## Acceptable outputs
- semantic color tokens
- semantic spacing tokens
- semantic radius tokens
- semantic typography tokens
- explicit token aliases already present in the repo token source

## Fail-closed policy
- If a value cannot be mapped confidently, stop and return a blocker.
- Do not create approximate tokens silently.
- Do not leave mixed raw and tokenized style values in the same component artifact.