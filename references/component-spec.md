# Component Spec Reference
> Used by UI Spec WriteArrow iconr and UI Spec Orchestrator when authoring or reviewing a `spec.md` for any component.

---

## Purpose

A component spec is the single source of truth for implementing one React Native component. It is written before any code is produced. Its job is to answer every structural, visual, and behavioural question a developer would have — without referencing pixels, raw hex colours, or Figma layer names.

---

## Required Sections

The sections below must appear in every spec, in this order. Sections that are genuinely not applicable must still be present with the _Not applicable_ marker — never omitted.

---

### 1. Overview

One short paragraph. State what the component is, what visual role it plays, and where it appears in the product. Do not describe implementation. Do not mention props or children here.

---

### 2. Architecture

**Atomic design level** — one of: `atom`, `molecule`, `organism`, `template`, `page`.

**Dependency graph** — list every component this component directly renders.

```
ComponentName -> ChildA, ChildB, ChildC
```

---

### 3. Props

Fully typed props table. Every prop must have a name, TypeScript type, whether it is required or optional, its default value (if optional), and a plain-English description.

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `label` | `string` | yes | — | Primary display text rendered inside the component. |
| `onPress` | `() => void` | no | `undefined` | Called when the component receives a tap gesture. |
| `variant` | `'primary' \| 'secondary'` | no | `'primary'` | Controls the colour scheme applied to the component. |

Rules:
- Use TypeScript union literals for constrained string values.
- Callback prop names start with `on`.
- Do not list internal implementation details as props.

---

### 4. State

Describe whether the component manages internal state or whether all state is passed in through props (controlled).

For each piece of state, specify: name, type, initial value, what triggers changes, and which parts of the UI it affects.

If the component is purely presentational with no internal state:

_Not applicable — presentational component._

---

### 5. Design Tokens

List every token consumed by this component. Group by category. Use the project's canonical token names exactly as they appear in the token source.

#### 5.1 Colors
| Token | Usage |
|-------|-------|
| `color.surface.primary` | Background fill of the container. |
| `color.text.on-primary` | Label text colour. |

#### 5.2 Typography
| Token | Usage |
|-------|-------|
| `typography.label.md` | Font style applied to the main label. |

#### 5.3 Spacing
| Token | Usage |
|-------|-------|
| `spacing.md` | Horizontal padding inside the component. |
| `spacing.sm` | Gap between icon and label. |

#### 5.4 Shadows, Radii, and Other
| Token | Usage |
|-------|-------|
| `radius.md` | Border radius of the outer container. |
| `shadow.sm` | Elevation applied in the default state. |

If you can not infer a value's token, You should mark it as conflict:

`<!-- unresolved: Figma uses Gray Dark/900 (#373836) for the header title; closest available token in design-system.ts is colors.foreground (#50524E). -->`

If a category has no tokens:

_None._

---

### 6. Static Assets

List every static asset (images, icons, Lottie files, SVGs etc.) this component references directly. Include the asset path relative to the project root and the purpose.

| Asset | Path | Purpose |
|-------|------|---------|
| Arrow icon | `assets/icons/arrow-right.svg` | Trailing navigation indicator. |

If icons in the project are treated as components they should appear in the architecture not here.

If the component uses no static assets:

_Not applicable — no static assets._

---

### 7. Layout

Describe the visual structure in plain English prose followed by a pseudo-layout block. No pixel values. Use spacing tokens by name when distances matter.

**Prose description:**
The component is a horizontally arranged row. The leading slot holds an optional icon. The centre slot contains a stack of label and sublabel. The trailing slot contains the arrow icon, pinned to the right edge.

**Pseudo-layout:**
```
┌─────────────────────────────────────────┐
│  [Icon?]  [Label        ]  [ArrowIcon]  │
│           [Sublabel?    ]               │
└─────────────────────────────────────────┘

Outer padding:   spacing.md (horizontal), spacing.sm (vertical)
Icon size:       icon.size.md
Gap (icon→text): spacing.sm
Gap (text→arrow): auto (flex: 1 on center slot)
```

---

### 8. Variants

List every visual variant. For each, describe only what changes from the base/default state. Never repeat unchanged properties.

| Variant | Changes from base |
|---------|-------------------|
| `primary` | Background → `color.surface.primary`. Label → `color.text.on-primary`. |
| `secondary` | Background → `color.surface.secondary`. Label → `color.text.on-secondary`. Border → 1px `color.border.default`. |
| `destructive` | Background → `color.surface.danger`. Label → `color.text.on-danger`. |

If the component has no variants:

_Not applicable — single visual style._

---

### 9. Visual States

Describe every interactive visual state the component can enter. For each state, list which tokens or styles change and what triggers the transition.

| State | Trigger | Visual change |
|-------|---------|---------------|
| Default | — | Base styles apply. |
| Pressed | Active touch | Background → `color.surface.primary-pressed`. Scale → 0.97. |
| Disabled | `disabled` prop is `true` | All colours shift to `color.surface.disabled`. Opacity → `opacity.disabled`. |
| Focused | Keyboard / accessibility focus | `color.border.focus` outline, width `border.focus`. |

If the component has no interactive states beyond rendering:

_Not applicable — non-interactive component._

---

### 10. Animations

Describe each animation. For every animation specify: trigger, property animated, duration token, easing token, and directionality (in, out, in-out, looping).

| Animation | Trigger | Property | Duration | Easing | Direction |
|-----------|---------|----------|----------|--------|-----------|
| Press feedback | `onPressIn` | `scale` | `duration.fast` | `easing.standard` | in-out |
| Mount fade | Component mounts | `opacity` | `duration.normal` | `easing.decelerate` | in |

If the component has no animations:

_Not applicable — no animated behaviour._

---

### 11. Gestures

List gesture handlers beyond basic tap (`onPress`). For each gesture specify: type, handler prop or library API used, and what behaviour it triggers.

| Gesture | Library | Handler | Behaviour |
|---------|---------|---------|-----------|
| Swipe left | `react-native-gesture-handler` | `onSwipeLeft` | Reveals destructive action row. |
| Long press | React Native core | `onLongPress` | Opens context menu. |

Note the gesture library being used once at the top of this section if any non-core gestures are present.

If the component handles no gestures beyond tap:

_Not applicable — tap only._

---

### 12. Accessibility

State every accessibility requirement explicitly. Do not use vague language like "follows best practices".

- **Role:** `accessibilityRole="button"` on the root Pressable.
- **Label:** `accessibilityLabel` must be passed as a prop; defaults to the value of `label`.
- **State:** When `disabled` is true, set `accessibilityState={{ disabled: true }}`.
- **Hint:** `accessibilityHint` prop, optional, forwarded directly to the root element.
- **Minimum tap area:** Root element must be at least 44 × 44 dp. Use `hitSlop` if the visible size is smaller.
- **Focus order:** Logical reading order must match visual left-to-right, top-to-bottom order.
- **Contrast:** All label/background token pairings must meet WCAG AA (4.5:1 for normal text).

---

### 13. User Stories / Scenarios

Include only when the component has meaningfully different scenarios that affect its visual behaviour across data or user-state conditions.

**Scenario 1 — Empty state**
When `items` is an empty array, the component renders the `EmptyState` child instead of the list. The header and footer remain visible.

**Scenario 2 — First-time user**
When `isFirstVisit` is `true`, an inline tooltip is overlaid on the trailing icon on mount and dismissed after `duration.tooltip-auto-dismiss`.

If no meaningful scenarios exist:

_Not applicable — behaviour does not vary by data or user-state context._

---

### 14. Success Criteria

Bullet list of observable, verifiable facts that confirm correct implementation. Visual and interaction only — no references to test IDs or code structure.

- Renders with the correct background token for each variant.
- Label text is visible and uses the correct typography token.
- Pressing the component triggers the press animation within one frame of `onPressIn`.
- Disabled state is visually distinguished from the default state using the disabled token.
- The component fills its parent width and does not overflow horizontally on a 320 dp screen.
- All interactive areas meet the 44 dp minimum tap target.
- Screen reader announces the correct role and label on focus.

---

### 15. Edge Cases

List concrete edge cases the implementation must handle gracefully. For each, state the input condition and the required visual outcome.

| Condition | Required behaviour |
|-----------|-------------------|
| `label` is an empty string | Component renders but label slot collapses; no visible gap left behind. |
| `label` is longer than the available width | Text truncates with ellipsis after one line. No overflow. |
| Both `icon` and `trailingIcon` are absent | Centre slot expands to fill the full width. |
| `onPress` is not provided | Component renders as non-interactive; no pressed state applies. |
| Rendered in RTL locale | Layout mirrors: icon moves to the right, arrow moves to the left. |

---

## Authoring Rules

1. **Never use raw style literals.** All colours, spacing, radii, typography, and shadow values must reference a named design token.
2. **Never reference Figma layer names.** Use semantic component and prop names only.
3. **No pixel values.** Use token names or relative descriptors (e.g., "half the container height").
4. **Every section must be present.** Use the _Not applicable_ marker for sections with nothing to document.
5. **Props must be typed.** All props use TypeScript types with explicit union literals for constrained values.
6. **Mandatory sections never omitted.** Sections 1–4, 7, 9, 12, 14, and 15 are always required with substantive content.
