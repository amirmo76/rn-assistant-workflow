# Component Spec Reference
> Used by **RN Component Spec Writer** at Step 4 (component mode).
> Defines the required structure and rules for `specs/components/[component-name]/spec.md`.

Permanent source-of-truth format for `specs/components/[component-name]/spec.md`.

## Required Sections

### 1. Summary

One short paragraph describing the component's role and where it is used.

### 2. Architecture

- **Atomic level:** `atom | molecule | organism | template | page`
- **Component Dependencies:** a list of all the directly imported and dependent components.

### 3. Public Contract

Props, callbacks, and named slots, if any.

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|

### 4. Visual Contract

Describe only the current UI contract.

- **Layout:** structure, alignment, and sizing rules. psuedo layout explanation.
- **Tokens/Values:** design tokens and justified hard coded values.
- **assets:** static assets used by the component.
- **Variants:** what changes between variants.
- **States:** default, disabled, loading, error, focused, pressed, or any other visible state.
- **Animations/Gestures:** gesture and animations details if any.

### 5. Behaviour Contract

Interaction rules, possible user stories, controlled vs local state, accessibility requirements, and edge cases.

### 6. Coverage Contract

- Required story coverage.
- Required test coverage.

### 7. Acceptance Criteria

Observable facts that confirm the component matches this spec.

## Rules

- This file describes the component's current contract, not a change request.
- Rewrite the file when the contract changes. Do not append change notes.
- Keep implementation detail out unless it affects the public, visual, or behavioural contract.
