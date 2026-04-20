---
name: tamagui
description: >
  Tamagui — a complete cross-platform UI solution for React Native and Web. Provides a styling engine, optimizing compiler, and a full component kit. Use this skill when building UIs with Tamagui on Expo, Next.js, Vite, or Webpack. Triggers: "tamagui", "@tamagui/core", "createTamagui", "styled(View", "tamagui.config".
---

# Tamagui Skill

**What it is:** A universal UI system for React Native + Web with a styling engine (`@tamagui/core`), an optimizing compiler, and a full component library (`tamagui`).

**When to use:** Any project using Tamagui for cross-platform or web-only UI.

## How to use this skill

This file is the **router**. Read only the sub-files relevant to your task. Do NOT load everything at once.

### Guides — setup & tooling

| File | When to read |
| --- | --- |
| [guides/installation.md](guides/installation.md) | Installing Tamagui into Expo, Next.js, Vite, Webpack, or Metro projects. Bundler plugins and compiler setup. |
| [guides/configuration.md](guides/configuration.md) | Creating `tamagui.config.ts` — tokens, themes, fonts, media queries, shorthands, TamaguiProvider, config v5. |
| [guides/upgrade-v2.md](guides/upgrade-v2.md) | Migrating from Tamagui v1 to v2. Prop renames, API changes, find-and-replace patterns. |
| [guides/cli.md](guides/cli.md) | `@tamagui/cli` commands: `build`, `generate`, `generate-css`, `check`, `add`. |

### Core — styling APIs

| File | When to read |
| --- | --- |
| [core/styling.md](core/styling.md) | `styled()`, variants, style props, pseudo states, shorthands, CSS shorthand with variables, parent-based styling, order-of-props rules. |
| [core/animations.md](core/animations.md) | Animation drivers (CSS, RN, Reanimated, Motion), `transition` prop, enterStyle/exitStyle, AnimatePresence, per-property animations. |
| [core/hooks.md](core/hooks.md) | `useMedia` (responsive), `useTheme` (theme access), `Theme` component, `createStyledContext`. |

### Components — the UI kit

| File | When to read |
| --- | --- |
| [components/layout.md](components/layout.md) | View, Text, XStack, YStack, ZStack, Group, Separator, ScrollView, Unspaced. |
| [components/typography.md](components/typography.md) | SizableText, Paragraph, Headings, Anchor, HTML elements. |
| [components/forms.md](components/forms.md) | Button, Input, TextArea, Checkbox, RadioGroup, Switch, Slider, Select, Label, Form, ToggleGroup. |
| [components/feedback.md](components/feedback.md) | Dialog, AlertDialog, Sheet, Popover, Tooltip, Toast, ContextMenu, Menu, Spinner, Progress. |
| [components/data-display.md](components/data-display.md) | Accordion, Avatar, Card, Image, ListItem, Tabs. |
| [components/utilities.md](components/utilities.md) | Portal, VisuallyHidden, FocusScope, RovingFocus, Shapes, ZIndex, LinearGradient, AnimatePresence, Lucide Icons. |

## Quick reference

```bash
# Install
npm install tamagui @tamagui/config

# Minimal config
import { defaultConfig } from '@tamagui/config/v5'
import { createTamagui } from 'tamagui'
export const config = createTamagui(defaultConfig)
```

```tsx
// Provider (wrap your app root)
<TamaguiProvider config={config} defaultTheme="light">
  <App />
</TamaguiProvider>
```

```tsx
// Basic usage
import { View, Text, Button, XStack, YStack, styled } from "tamagui";

const Card = styled(YStack, {
  p: "$4",
  bg: "$background",
  rounded: "$4",
  variants: {
    elevated: {
      true: { elevation: "$2" },
    },
  } as const,
});
```

### Key concepts

- **Tokens** — static design variables (size, space, color, radius). Use as `$tokenName`.
- **Themes** — contextual CSS-variable-like values that nest via `<Theme name="dark">`. Access with `$background`, `$color`, etc.
- **Shorthands** — Tailwind-aligned abbreviations: `p`, `m`, `bg`, `rounded`, `px`, etc. (v5 default config).
- **Media queries** — Responsive props: `$sm`, `$md`, `$lg`. Mobile-first (min-width).
- **Variants** — Typed prop-to-style mappings on `styled()`. Use `as const`.
- **Pseudo states** — `hoverStyle`, `pressStyle`, `focusStyle`, `focusVisibleStyle`, `disabledStyle`, `enterStyle`, `exitStyle`.
- **Compiler** — Optional. Extracts styles to CSS at build time. Configure via `tamagui.build.ts`.
