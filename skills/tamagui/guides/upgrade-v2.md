# Upgrading to Tamagui v2

## 1. Update Dependencies

```bash
npx tamagui check   # find version mismatches first
npm install tamagui@latest @tamagui/config@latest @tamagui/core@latest
```

All `@tamagui/*` packages must be on the exact same version.

## 2. Config Migration (v4 → v5)

Animations are no longer bundled:

```tsx
// Before (v4)
import { config } from '@tamagui/config/v4'

// After (v5)
import { defaultConfig } from '@tamagui/config/v5'
import { animations } from '@tamagui/config/v5-css' // choose your driver
import { createTamagui } from 'tamagui'

export const config = createTamagui({ ...defaultConfig, animations })
```

Media query renames:
- `$2xl` → `$xxl`
- `$2xs` → `$xxs`
- `$max2Xl` → `$max-xxl`

Flex defaults changed: `flexBasis: 0` (RN-style). To restore v4 behavior: `styleCompat: 'legacy'`.

Position defaults changed: no `defaultPosition` set (browser `static`). To restore: `defaultPosition: 'relative'`.

## 3. Prop Renames

| v1 | v2 |
|----|-----|
| `bc` | `bg` |
| `br` | `rounded` |
| `ai` | `items` |
| `jc` | `justify` |
| `fw` | `shrink` (recheck usage) |
| `spacing` | `gap` |

## 4. Shadow Migration

Shadows now use `boxShadow` shorthand:

```tsx
// Before (v1)
<View shadowColor="black" shadowOffset={{ width: 0, height: 2 }} shadowRadius={4} />

// After (v2)
<View boxShadow="0px 2px 4px rgba(0,0,0,0.25)" />
```

## 5. Accessibility Props

```tsx
// Before (v1)
<View accessibilityRole="button" accessibilityLabel="Submit" />

// After (v2) - use web-standard props
<View role="button" aria-label="Submit" />
```

## 6. Component API Changes

### Button

Text styling no longer passed directly. Use `Button.Text`:

```tsx
// Before
<Button color="blue" fontSize="$5">Click</Button>

// After
<Button>
  <Button.Text color="blue" fontSize="$5">Click</Button.Text>
</Button>
```

Group theming via `Button.Apply`:

```tsx
<Button.Apply size="$2" variant="outlined">
  <Button>A</Button>
  <Button>B</Button>
</Button.Apply>
```

### Dialog, Popover, Select

Added `FocusScope` sub-component for focus management. Old `trapFocus`/`restoreFocus` props removed — use `<Dialog.FocusScope trapped loop>`.

### Checkbox, Switch, RadioGroup

Use `createCheckbox`, `createSwitch` for headless. API for indicators changed.

### Sheet

`native` prop deprecated → use `Adapt` instead.

## 7. Removed APIs

- `space` prop → use `gap`
- `spaceDirection` prop → removed
- Legacy shorthand aliases removed (use v5 shorthands)

## 8. Native Setup

For native portal support (Dialog, Sheet, Popover):

```tsx
import { PortalProvider, FullWindowOverlay } from '@tamagui/portal'

<PortalProvider shouldAddRootHost Component={FullWindowOverlay}>
  <App />
</PortalProvider>
```

## 9. Build Config

Rename to `tamagui.build.ts`. Use `satisfies TamaguiBuildOptions`.

## 10. Quick Find-and-Replace Patterns

```
bc= → bg=
br= → rounded=
ai= → items=
jc= → justify=
elevation= → (keep, but consider boxShadow)
accessibilityRole= → role=
accessibilityLabel= → aria-label=
$2xl → $xxl
$2xs → $xxs
```

## Migration Checklist

- [ ] Update all `@tamagui/*` to same version
- [ ] Add animation import to config
- [ ] Update media query names
- [ ] Review flex/position defaults
- [ ] Update renamed shorthand props
- [ ] Migrate shadow props to `boxShadow`
- [ ] Migrate accessibility props
- [ ] Update Button text styling
- [ ] Set up native portals
- [ ] Update build config
