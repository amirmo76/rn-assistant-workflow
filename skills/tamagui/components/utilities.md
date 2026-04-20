# Utility Components

## Portal

Renders children into a separate layer above all content.

```bash
npm install @tamagui/portal  # or use from 'tamagui'
```

```tsx
import { Portal } from 'tamagui'

<Portal>
  <YStack fullscreen backgroundColor="rgba(0,0,0,0.5)">
    {/* overlay content */}
  </YStack>
</Portal>
```

### Native Portal Setup (recommended)

Default portal on native breaks React context. Install native portals to preserve context inside Sheet, Dialog, Popover:

```bash
npm install react-native-teleport
```

```tsx
// App.tsx — before any Tamagui imports
import '@tamagui/native/setup-teleport'
```

---

## VisuallyHidden

Hides content visually but keeps it accessible to screen readers.

```bash
npm install @tamagui/visually-hidden  # or use from 'tamagui'
```

```tsx
import { VisuallyHidden } from 'tamagui'

<VisuallyHidden>
  <Text>Screen reader only text</Text>
</VisuallyHidden>
```

Useful for wrapping required `Dialog.Title` or `Dialog.Description` when you want them hidden.

---

## FocusScope

Traps or loops keyboard focus within a boundary.

```bash
npm install @tamagui/focus-scope  # or use from 'tamagui'
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `loop` | `boolean` | `false` | Tab wraps from last→first |
| `trapped` | `boolean` | `false` | Focus cannot escape |
| `enabled` | `boolean` | `true` | Enable/disable scope |
| `focusOnIdle` | `boolean \| number` | `false` | Wait for idle before focusing |
| `onMountAutoFocus` | `(event) => void` | — | Focus callback on mount |
| `onUnmountAutoFocus` | `(event) => void` | — | Focus callback on unmount |

Used internally by Dialog, Popover, Select. Exposed as `*.FocusScope` sub-component.

---

## RovingFocus

Arrow-key navigation for toolbar/tab-like groups.

```bash
npm install @tamagui/roving-focus  # or use from 'tamagui'
```

```tsx
import { RovingFocusGroup } from '@tamagui/roving-focus'

<RovingFocusGroup orientation="horizontal" loop>
  <RovingFocusGroup.Item focusable>
    <Button>A</Button>
  </RovingFocusGroup.Item>
  <RovingFocusGroup.Item focusable>
    <Button>B</Button>
  </RovingFocusGroup.Item>
</RovingFocusGroup>
```

---

## Shapes — Square, Circle

Convenience components for common shapes.

```bash
npm install @tamagui/shapes  # or use from 'tamagui'
```

```tsx
import { Square, Circle } from 'tamagui'

<Square size={100} backgroundColor="$red10" />
<Circle size={100} backgroundColor="$blue10" />
```

Both accept all View/Stack style props. `size` sets both width and height.

---

## ZIndex

Helper component that automatically manages z-index stacking for overlays.

Tamagui overlays (Dialog, Sheet, Popover, Menu, Toast) automatically stack in order they open. Use `zIndex` prop on these components to override.

---

## LinearGradient

Gradient backgrounds.

```bash
npm install @tamagui/linear-gradient  # or use from 'tamagui'
```

```tsx
import { LinearGradient } from 'tamagui'

<LinearGradient colors={['$red10', '$blue10']} start={[0, 0]} end={[1, 1]}>
  <Text>Gradient background</Text>
</LinearGradient>
```

| Prop | Type | Description |
|------|------|-------------|
| `colors` | `string[]` | Array of color values or tokens |
| `start` | `[number, number]` | Start point `[x, y]` (0–1) |
| `end` | `[number, number]` | End point `[x, y]` (0–1) |
| `locations` | `number[]` | Position of each color stop (0–1) |

Native setup: `npm install expo-linear-gradient` then `import '@tamagui/native/setup-expo-linear-gradient'`.

---

## AnimatePresence

Animate components in and out of the tree. See [core/animations.md](../core/animations.md) for full docs.

```tsx
import { AnimatePresence } from 'tamagui'

<AnimatePresence>
  {show && (
    <YStack
      key="content"
      animation="quick"
      enterStyle={{ opacity: 0, y: -10 }}
      exitStyle={{ opacity: 0, y: 10 }}
    >
      <Text>Animated content</Text>
    </YStack>
  )}
</AnimatePresence>
```

---

## Lucide Icons

Tree-shakeable icon set for Tamagui.

```bash
npm install @tamagui/lucide-icons-2
```

```tsx
import { Activity, Airplay, Settings } from '@tamagui/lucide-icons-2'

<Activity size={24} color="$color" />
<Settings size="$1" />
```

Icons accept all Tamagui style props plus `size` and `color`.
