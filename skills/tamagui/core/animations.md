# Animations

## Setup

Choose a driver and add to your config:

```tsx
import { createAnimations } from '@tamagui/animations-react-native'

export default createTamagui({
  animations: createAnimations({
    bouncy: { damping: 10, mass: 0.9, stiffness: 100 },
    lazy: { damping: 18, stiffness: 50 },
    quick: { damping: 20, mass: 1.2, stiffness: 250 },
  }),
})
```

Or use v5 config with a driver:

```tsx
import { defaultConfig } from '@tamagui/config/v5'
import { animations } from '@tamagui/config/v5-css'
export const config = createTamagui({ ...defaultConfig, animations })
```

### Available Drivers

| Package | Use case |
|---------|----------|
| `@tamagui/animations-css` | CSS transitions (lightest, web) |
| `@tamagui/animations-react-native` | RN Animated API |
| `@tamagui/animations-reanimated` | Reanimated (best native perf) |
| `@tamagui/animations-motion` | Motion (spring physics) |

### v5 Preset Animations

**Timing:** `0ms`, `50ms`, `75ms`, `100ms`, `200ms`, `250ms`, `300ms`, `400ms`, `500ms`

**Springs:** `superBouncy`, `bouncy`, `superLazy`, `lazy`, `medium`, `slow`, `slowest`, `quick`, `quickLessBouncy`, `quicker`, `quickerLessBouncy`, `quickest`, `quickestLessBouncy`

---

## The transition Prop

```tsx
// Simple — all properties animate
<View transition="bouncy" hoverStyle={{ bg: '$color5' }} />

// Per-property
<View transition={{ x: 'bouncy', y: { type: 'bouncy', overshootClamping: true } }} />

// Default + overrides
<View transition={['bouncy', { y: 'slow', scale: { type: 'fast', repeat: 2 } }]} />

// With delay
<View transition={['bouncy', { delay: 200 }]} />

// Staggered children
{items.map((_, i) => (
  <Square key={i} transition={['bouncy', { delay: i * 100 }]}
    enterStyle={{ opacity: 0, scale: 0.5 }} />
))}
```

**Important:** Once `transition` is set, keep it on the component. Disable with `null`:

```tsx
<View transition={condition ? 'bouncy' : null} />
```

### Enter/Exit Transitions

```tsx
<View
  transition={{ enter: 'lazy', exit: 'quick', default: 'bouncy' }}
  enterStyle={{ opacity: 0, y: 20 }}
  exitStyle={{ opacity: 0, y: -20 }}
/>
```

### Pseudo-State Transitions

CSS-like semantics: entering a state uses that state's transition, exiting uses the base:

```tsx
<Square
  transition="1000ms"          // slow exit (back to base)
  hoverStyle={{
    transition: '200ms',       // fast enter (to hover)
    bg: '$color10',
  }}
  pressStyle={{
    transition: 'bouncy',
    scale: 0.95,
  }}
/>
```

---

## enterStyle / exitStyle

```tsx
// Mount animation: starts at enterStyle, animates to base
<View
  transition="bouncy"
  enterStyle={{ opacity: 0, scale: 0.9, y: 10 }}
  opacity={1}
  scale={1}
  y={0}
/>
```

---

## AnimatePresence

Animate components on mount/unmount:

```tsx
import { AnimatePresence } from 'tamagui'

function App({ show }) {
  return (
    <AnimatePresence>
      {show && (
        <View
          key="panel"
          transition="bouncy"
          enterStyle={{ opacity: 0, y: 20 }}
          exitStyle={{ opacity: 0, y: -20 }}
          opacity={1}
          y={0}
        />
      )}
    </AnimatePresence>
  )
}
```

The `custom` prop passes data to exit animations for directional transitions.

---

## animateOnly

Limit which properties animate:

```tsx
<View transition="bouncy" animateOnly={['opacity', 'transform']} />
```

---

## Notes

- Animation hooks are expensive — only enabled when `transition` is present in props.
- Adding `transition` after initial render in HMR may cause errors; save again or reload.
- Drivers are swappable per-platform without changing component code.
- SSR-safe: `enterStyle` animations work correctly with server rendering.
