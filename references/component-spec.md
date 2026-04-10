# Component Spec Reference
> Used by **RN Component Spec Writer** at Step 4 (component mode).
> Defines the required structure and rules for `specs/components/[component-name]/spec.md`.

Permanent source-of-truth format for `specs/components/[component-name]/spec.md`.

## Required Sections

### 1. Summary

One short paragraph describing the component's standalone role, purpose, and behaviour. Write from the component's perspective, not from any specific usage context. Do not reference the objective, parent components, or screens that triggered its creation.

### 2. Architecture

- **Atomic level:** `atom | molecule | organism | template | page`
- **Component Dependencies:** a list of all the directly imported and dependent components.

### 3. Public Contract

Props, callbacks, and named slots, if any.

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|

- Children prop is always optional even when the component expects a child.

### 4. Visual Contract

Describe only the current UI contract.

#### Values and Design System Tokens

|  Case | Resolved Token | Hard Coded Value |
|-------|----------------|------------------|

Example:

|         Case              | Resolved Token  | Hard Coded Value |
| Border color of the input | `colors.border` |        -         |
| Border width of the input |        -        |       1px        |

- Case is a usage instance.
- A case resolves to either a resolved design system token or a hardcoded value.
- A case can not have both resolved token and hard coded value.
- **Only include design values that this component directly controls** — i.e. values applied to primitives (View, Text, Image, etc.) rendered inside this component's own JSX. Do not include values that belong to a dependency component's own rendering (e.g. a Card's background color belongs in Card's spec, not in a component that merely renders a Card).

#### Layout

structure, alignment, and sizing rules. psuedo layout explanation.

#### Assets

static assets used by the component.

If none: _No Assets_

#### Variants

|  Variant | What is different |
|----------|-------------------|

If none: _No variants_

#### Visual States

default, disabled, loading, error, focused, pressed, or any other visible state.

|  State | Trigger | Difference |
|--------|---------|------------|

If none: _No Visual State_

#### Animations/Gestures

gesture and animations details if any.

If none: _No Animation or Gesture_

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
- Write every section as if the component is standalone and reusable. Do not name specific parent components, screens, objectives, or usage instances unless that reference provides essential permanent reusability context that cannot be expressed any other way.
