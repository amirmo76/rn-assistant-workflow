---
name: tamagui-compound
description: >
  How to build UI primitives in this project using Tamagui — covers the two-category rule (simple/structural from scratch vs complex/interactive wrappers) and the compound component pattern (createStyledContext + withStaticProperties). Triggers: "ui primitive", "compound component", "createStyledContext", "build a button", "build a card", "build a select", "build a dialog", "build a sheet", "tamagui primitive".
---

# Tamagui Compound Component Skill

## The Two-Category Rule

Every UI primitive belongs to one of two categories. Misidentifying leads to either over-engineering simple components or under-engineering complex ones.

---

## Category 1 — Simple / Structural Primitives (Build From Scratch)

**Applies to:** Button, Badge, Card, Divider, Avatar, Text / Heading, Container, Tag, Chip.

**Rule:** Use `styled()` from `@tamagui/core`. Never import these from the tamagui UI kit.

### When to use the Compound Component Pattern inside Category 1

Use `createStyledContext` + `withStaticProperties` **only when** the component has multiple interlocking sub-components that must share a variant prop from the parent, e.g.:

- `Card` with `Card.Header`, `Card.Body`, `Card.Footer` all sharing a `size` variant.
- `Button` with `Button.Text`, `Button.Icon` sharing a `size` variant.

Do **not** use it for components that have no sub-components (e.g., `Divider`, `Badge`).

### Structural — Single styled component (no sub-components)

```tsx
// src/components/ui/Divider.tsx
import { styled, View } from '@tamagui/core'

export const Divider = styled(View, {
  height: 1,
  backgroundColor: '$borderColor',

  variants: {
    orientation: {
      vertical: { width: 1, height: '100%' },
      horizontal: { width: '100%', height: 1 },
    },
  } as const,

  defaultVariants: {
    orientation: 'horizontal',
  },
})
```

### Structural — Compound (sub-components sharing a variant)

```tsx
// src/components/ui/Card.tsx
import { GetProps, SizeTokens, View, Text, createStyledContext, styled, withStaticProperties } from '@tamagui/core'

export const CardContext = createStyledContext({
  size: '$md' as SizeTokens,
})

export const CardFrame = styled(View, {
  name: 'Card',
  context: CardContext,
  backgroundColor: '$background',
  borderRadius: '$4',
  overflow: 'hidden',

  variants: {
    size: {
      '...size': (name, { tokens }) => ({
        padding: tokens.space[name],
      }),
    },
  } as const,

  defaultVariants: { size: '$md' },
})

export const CardHeader = styled(View, {
  name: 'CardHeader',
  context: CardContext,
  borderBottomWidth: 1,
  borderBottomColor: '$borderColor',

  variants: {
    size: {
      '...size': (name, { tokens }) => ({
        paddingBottom: tokens.space[name],
        marginBottom: tokens.space[name],
      }),
    },
  } as const,
})

export const Card = withStaticProperties(CardFrame, {
  Props: CardContext.Provider,
  Header: CardHeader,
})
```

Usage — `size` flows automatically to all sub-components:

```tsx
<Card size="$lg">
  <Card.Header>
    <Text>Title</Text>
  </Card.Header>
  <Text>Body</Text>
</Card>
```

---

## Category 2 — Complex / Interactive Primitives (Wrapper Approach)

**Applies to:** Dialog (Modal), Sheet (Bottom Sheet), Select (Dropdown), Accordion, Switch, Checkbox, Tabs, Popover, Slider, RadioGroup.

**Rule:** Never build these from scratch. Wrap the Tamagui UI kit component — like Shadcn wraps Radix.

1. Import the base component from `tamagui` (the UI kit package, not `@tamagui/core`).
2. Pass `unstyled={true}` to strip Tamagui's default visuals.
3. Apply project design tokens (`$background`, `$space.4`, `$radius.md`, etc.) to override the look.
4. Preserve all of Tamagui's anatomy (Trigger, Content, Viewport, etc.) — style each piece individually.
5. Export a clean API that hides the internal anatomy from consumers.

```tsx
// src/components/ui/Switch.tsx
import { Switch as TamaguiSwitch, styled } from 'tamagui'

const SwitchFrame = styled(TamaguiSwitch, {
  unstyled: true,
  backgroundColor: '$gray5',
  borderRadius: '$10',
  width: 50,
  height: 28,
  padding: 2,

  variants: {
    checked: {
      true: { backgroundColor: '$blue10' },
    },
  } as const,
})

const SwitchThumb = styled(TamaguiSwitch.Thumb, {
  unstyled: true,
  backgroundColor: '$white',
  width: 24,
  height: 24,
  borderRadius: '$10',
})

export const Switch = (props: React.ComponentProps<typeof SwitchFrame>) => (
  <SwitchFrame {...props}>
    <SwitchThumb />
  </SwitchFrame>
)
```

---

## Key APIs

| API | Purpose |
|-----|---------|
| `styled(Base, config)` | Create a styled component with variants |
| `createStyledContext(defaults)` | Create a shared context for compound components — variants set on the parent flow automatically to all children that declare the same variant name and reference the same context |
| `withStaticProperties(Frame, { Sub1, Sub2 })` | Attach sub-components as static properties (`Card.Header`) |
| `unstyled={true}` | Strip Tamagui's default visuals when wrapping kit components |
| `'...size'` spread variant | Map all size tokens automatically without listing each one |

---

## Rules Summary

| Situation | Approach |
|-----------|----------|
| Simple, structural, no sub-components | `styled(View/Text, {...})` |
| Structural with sub-components sharing a variant | `createStyledContext` + `withStaticProperties` |
| Interactive / animated (Dialog, Sheet, Select…) | Wrap tamagui kit with `unstyled={true}` + project tokens |
| Wrapping a third-party lib for theming | `styled(ThirdParty, {...})` with tokens |

---

## Imports

- Category 1 (build from scratch): `import { styled, View, Text, createStyledContext, withStaticProperties } from '@tamagui/core'`
- Category 2 (wrapper): `import { Dialog, Sheet, Select, ... } from 'tamagui'`
- Never import Category 1 primitives from `tamagui` (the kit) — they carry opinionated defaults.
