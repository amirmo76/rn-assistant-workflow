# Component Spec Reference
> Used by **Component Spec Writer** at Step 4 (component mode).
> Defines the required structure and rules for `specs/components/[component-name]/spec.md`.

Permanent source-of-truth format for `specs/components/[component-name]/spec.md`.

## Required Sections

### 1. Summary

One short paragraph describing the component's standalone role, purpose, and behaviour. Write from the component's perspective, not from any specific usage context. Do not reference the objective, parent components, or screens that triggered its creation.

If `--context` returned a **global context** entry for this component (`=== Global Context ===`), use it to anchor the summary — it is the designer's concise statement of the component's intended scope and constraints. The summary must be consistent with that description.

### 3. Example Usage

Code snippet of example usage.

### 4. Architecture

- **Component tier:** `primitive | composite | domain`
  Use the Component Tier Classification rules in `ui-spec-writer.agent.md` to determine the correct tier. Only one tier per component. 
- **Component Dependencies:** a list of all the directly imported and dependent components.

### 5. External Dependencies

Packages it uses. Headless UI, animations, utility and etc.

### 6. Composition

Only required when the component belongs to a composition group. If this component is not part of a composition group: _Not part of a composition group._

- **Composition Group:** the name of the group this component belongs to.
- **Role:** one sentence describing this component's specific job within the composition and what it explicitly does **not** own (so there is no ambiguity with siblings).
- **Produced:** values, context, or styling this component is the sole owner of and surfaces to sibling consumers (e.g. provides `InputGroupContext` with `variant`; owns left/right border radius).
- **Consumed:** values or context this component receives from a sibling or the group container (e.g. reads `variant` from `InputGroupContext`; relies on `InputGroup` for outer border).

### 7. Public Contract

Props, callbacks, and named slots, if any.

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|

- Children prop is always optional even when the component expects a child.

### 8. Internal State

Internal state management.

If none: _No Internal_

### 9. Visual Contract

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
- **Only include design values that this component directly controls** — i.e. values applied to platform primitives rendered inside this component's own JSX. Do not include values that belong to a dependency component's own rendering (e.g. a Card's background color belongs in Card's spec, not in a component that merely renders a Card).

#### Layout

structure, alignment, and sizing rules. psuedo layout explanation.

#### Assets

static assets used by the component.

If none: _No Assets_

#### Variants

|  Variant Group | Variance | What differs |
|----------------|----------|--------------|

Example:

```markdown
| Variant Group | Variance | What differs |
| :--- | :--- | :--- |
| **Size** | `lg` | How it changes |
| **Size** | `md` | How it changes |
| **Size** | `sm` | How it changes |
| **Variant** | `primary` | How it changes |
| **Variant** | `outline` | How it changes |
| **Variant** | `ghost` | How it changes |
```

If `--context` returned **instance contexts** (`=== Instance Contexts ===`), cross-reference them when filling this table. Each `@context: variant=X, size=Y` entry is direct evidence of a real variant combination in use. Do not add variant rows that have no evidence in either the design or the instance contexts.

If none: _No variants_

#### Visual States

default, disabled, loading, error, focused, pressed, or any other visible state.

|  State | Trigger | Difference |
|--------|---------|------------|

If none: _No Visual State_

#### Animations/Gestures

gesture and animations details if any.

If none: _No Animation or Gesture_

### 10. Behaviour Contract

Interaction rules, possible user stories, controlled vs local state, accessibility requirements, and edge cases.

### 11. Coverage Contract

- Required story coverage.
- Required test coverage.

### 12. Acceptance Criteria

Observable facts that confirm the component matches this spec.

## Rules

- This file describes the component's current contract, not a change request.
- Always include a usage example with a code snippet.
- Rewrite the file when the contract changes. Do not append change notes.
- Keep implementation detail out unless it affects the public, visual, or behavioural contract.
- Write every section as if the component is standalone and reusable. Do not name specific parent components, screens, objectives, or usage instances unless that reference provides essential permanent reusability context that cannot be expressed any other way.

---

## Shadcn-Backed Primitive Spec (delta format)

This variant applies only when **all three** eligibility conditions are met:
1. The active project platform is **web** (not React Native / Expo).
2. The component is classified as a **Primitive**.
3. The component's root block in `tree.yaml` carries a `@source: shadcn/<id>` annotation.

If any condition is false, use the full spec format above without exception.

### 1. Summary

Same rule as the full spec. One paragraph describing the component's contract. Note the shadcn source in the opening sentence: "Button is a shadcn/button-backed primitive that [project-specific purpose]."

### 2. Registry Source

```
- **Source:** shadcn/<component-id> (version or commit hash if pinned, otherwise "latest at install")
- **Install command:** `npx shadcn@latest add <component-id>`
```

### 3. Local Overrides

A compact list of every deviation from the shadcn default. Each line follows the pattern: `[Category] <what was changed and why>`. If no overrides: *No local overrides.*

Categories: Props, Visual Tokens, Behaviour, Composition.

### 4. Public Contract

Same rules as the full spec. Props table, callbacks, named slots.

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|

- Children prop is always optional even when the component expects a child.

### 5. Visual Contract — Token Overrides Only

Same table format as the full spec, but only include rows for values that **differ** from the shadcn default. Rows the shadcn default covers with no project change are omitted.

|  Case | Resolved Token | Hard Coded Value |
|-------|----------------|------------------|

