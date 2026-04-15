# Component Spec Reference
> Used by **Component Spec Writer** at Step 4 (component mode).
> Defines required structure for `specs/components/[component-name]/spec.md`.

Permanent source-of-truth format for `specs/components/[component-name]/spec.md`.

## Required Sections

### 1. Summary

One short paragraph describing the component's standalone role, purpose, and behaviour. Write from component's perspective, not any specific usage context. Don't reference the objective, parent components, or screens that triggered its creation.

If `--context` returned a **global context** entry (`=== Global Context ===`), use it to anchor the summary — it is the designer's concise statement of intended scope and constraints. Summary must be consistent with that description.

### 3. Example Usage

Code snippet of example usage.

### 4. Architecture

- **Component tier:** `primitive | composite | domain`
  Use Component Tier Classification rules in `ui-spec-writer.agent.md`. Only one tier per component.
- **Component Dependencies:** list of all directly imported and dependent components.

### 5. External Dependencies

Packages it uses. Headless UI, animations, utility and etc.

### 6. Composition

Only required when component belongs to a composition group. If not: _Not part of a composition group._

- **Composition Group:** group this component belongs to.
- **Role:** one sentence: this component's specific job within the composition and what it explicitly does **not** own.
- **Produced:** values, context, or styling this component solely owns and surfaces to sibling consumers.
- **Consumed:** values or context received from a sibling or group container.

### 7. Public Contract

Props, callbacks, and named slots, if any.

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|

- Children prop is always optional even when component expects a child.

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
- **Only include design values this component directly controls** — applied to platform primitives inside this component's own JSX. Don't include values belonging to a dependency component (e.g. Card's background color belongs in Card's spec, not in a component that merely renders a Card).

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

If `--context` returned **instance contexts** (`=== Instance Contexts ===`), cross-reference when filling this table. Each `@context: variant=X, size=Y` entry is direct evidence of a real variant combination in use. Don't add variant rows with no evidence in either design or instance contexts.

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
- Rewrite file when contract changes. Don't append change notes.
- Keep implementation detail out unless it affects the public, visual, or behavioural contract.
- Write every section as if component is standalone and reusable. Don't name specific parent components, screens, objectives, or usage instances unless essential permanent reusability context can't be expressed any other way.

---

## Shadcn-Backed Primitive Spec (delta format)

This variant applies only when **all three** eligibility conditions are met:
1. Active project platform is **web** (not React Native / Expo).
2. Component is classified as a **Primitive**.
3. Component's root block in `tree.yaml` carries a `@source: shadcn/<id>` annotation.

If any condition is false, use the full spec format above without exception.

### 1. Summary

Same rule as full spec. One paragraph describing component's contract. Note shadcn source in opening sentence: "Button is a shadcn/button-backed primitive that [project-specific purpose]."

### 2. Registry Source

```
- **Source:** shadcn/<component-id> (version or commit hash if pinned, otherwise "latest at install")
- **Install command:** `npx shadcn@latest add <component-id>`
```

### 3. Local Overrides

Compact list of every deviation from shadcn default. Each line: `[Category] <what changed and why>`. If no overrides: *No local overrides.*

Categories: Props, Visual Tokens, Behaviour, Composition.

### 4. Public Contract

Same rules as full spec. Props table, callbacks, named slots.

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|

- Children prop is always optional even when component expects a child.

### 5. Visual Contract — Token Overrides Only

Same table format as full spec, but only include rows for values that **differ** from shadcn default. Rows shadcn default covers with no project change are omitted.

|  Case | Resolved Token | Hard Coded Value |
|-------|----------------|------------------|

