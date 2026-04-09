---
name: rn-tree-decomposition
description: Define and review the component tree for a UI objective or a single component.
---

# RN Tree Decomposition

Use this skill to define the architecture for either:

- one objective's full component tree
- one component whose structure needs to be clarified

## Output

Return architecture in this exact shape:

```text
ARCHITECTURE: [Subject]

Root: [RootComponent]

Levels:
- ComponentA: atom
- ComponentB: molecule

Graph:
RootComponent -> ChildA, ChildB
ChildA -> LeafA, LeafB
ChildB
LeafA
LeafB

Notes:
- Optional clarifications.
```

Omit `Notes:` when there is nothing to add.

## Atomic Levels

- `atom`: single primitive or leaf
- `molecule`: small focused composition of atoms
- `organism`: larger section composed of molecules and atoms
- `template`: layout skeleton
- `page`: full screen or routed view

## Rules

- Name by role, not by screen-specific instance.
- Treat variants and content changes as props, not new component names.
- Split on responsibility boundaries, not on Figma layer boundaries.
- Reuse repeated structures instead of cloning near-identical components.
- Do not include implementation wrappers such as `SafeAreaView`, `ScrollView`, or `KeyboardAvoidingView`.
- Do not include styling, spacing, tokens, or business logic.

## Canonical Leaves

Use canonical names when they fit: `Button`, `Link`, `Input`, `Label`, `Icon`, `Image`, `Avatar`, `Badge`, `ListItem`, `Checkbox`, `Switch`, `Separator`, `Spinner`, `ProgressBar`, `NavBar`, `TabBar`, `Modal`, `Footer`.

Use card anatomy when relevant:

```text
Card -> CardHeader, CardContent, CardFooter
```

## Review Checklist

- The root component is correct.
- Each component has the right atomic level.
- The graph is in visual order.
- Names are semantic and reusable.
- Shared structures are reused instead of duplicated.
- The graph is deep enough to guide the objective, but not padded with implementation wrappers.
