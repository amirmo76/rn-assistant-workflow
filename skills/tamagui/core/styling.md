# Styling — styled(), Variants, Props

## styled()

Create components by extending existing ones:

```tsx
import { GetProps, View, styled } from 'tamagui' // or '@tamagui/core'

export const Card = styled(View, {
  p: '$4',
  bg: '$background',
  rounded: '$4',
})

export type CardProps = GetProps<typeof Card>
```

Works with Tamagui views, React Native views, and any component accepting `style`. For external components with `className` support:

```tsx
const TamaguiCustom = styled(SomeComponent, { acceptsClassName: true })
```

### render prop

Control the rendered element:

```tsx
// HTML element (compiler-optimized)
const Button = styled(View, { render: 'button' })
const Anchor = styled(Text, { render: 'a' })
const Nav = styled(View, { render: 'nav' })

// Runtime override
<Box render="button">Click me</Box>

// JSX element (not compiler-optimized)
<Stack render={<a href="/about" />}>About</Stack>

// Function (not compiler-optimized)
<Stack render={(props, state) => <Custom {...props} isHovered={state.hover} />} />
```

### styleable

Wrap functional components that return styled components so they can be further `styled()`:

```tsx
const StyledText = styled(Text)

const HigherOrder = StyledText.styleable<{ custom: boolean }>((props, ref) => (
  <StyledText ref={ref} {...props} />
))

// Now this works correctly:
const Enhanced = styled(HigherOrder, { variants: { /* ... */ } as const })
```

### accept

Let styled components accept token/theme values for non-standard props:

```tsx
const StyledSVG = styled(SVG, {}, { accept: { fill: 'color' } as const })
// Now: <StyledSVG fill="$blue10" />

const MyScrollView = styled(ScrollView, {}, {
  accept: { contentContainerStyle: 'style' } as const,
})
```

---

## Variants

Typed prop-to-style mappings. Always use `as const`.

```tsx
const Circle = styled(View, {
  rounded: 100_000,

  variants: {
    // Boolean variant
    centered: {
      true: { items: 'center', justify: 'center' },
      false: { items: 'flex-start' },
    },

    // Enum variant
    pin: {
      top: { position: 'absolute', t: 0 },
      bottom: { position: 'absolute', b: 0 },
    },

    // Spread variant — maps to all tokens in a category
    size: {
      '...size': (size, { tokens }) => ({
        width: tokens.size[size] ?? size,
        height: tokens.size[size] ?? size,
      }),
    },

    // Dynamic variant
    doubleMargin: (val: number) => ({ m: val * 2 }),

    // String/number catch-all
    color: {
      ':string': (color) => ({ color, borderColor: color }),
    },

    // Catch-all (grabs unmatched values)
    colorful: {
      true: { color: 'red' },
      '...': (val: string) => ({ color: val }),
    },
  } as const,

  defaultVariants: {
    size: '$10',
  },
})
```

Spread variant categories: `...color`, `...size`, `...space`, `...radius`, `...fontSize`, `...lineHeight`, `...letterSpace`, `...zIndex`.

Spread variant function signature: `(value, { theme, tokens, props, font, fonts, context }) => styles`.

Variants support pseudo states and media queries inside them:

```tsx
size: {
  md: {
    fontSize: '$sm',
    $gtMd: { fontSize: '$md' },
  },
}
```

---

## Style Props

Tamagui accepts all React Native View/Text style props plus these cross-platform additions:

- `boxShadow` — string, object, or array
- `filter` — brightness, opacity cross-platform
- `backgroundImage` — linear-gradient, radial-gradient (supports `$tokens`)
- `cursor` — web + iOS 17+
- `border` — shorthand: `"1px solid $borderColor"` (expands on native)
- `outline` — shorthand: `"2px solid $outlineColor"` (expands on native)
- `position: 'fixed'` — converts to `absolute` on native

Flat transforms: `x`, `y`, `scale`, `scaleX`, `scaleY`, `rotate`, `rotateX`, `rotateY`, `rotateZ`, `skewX`, `skewY`, `perspective`, `matrix`.

### CSS Shorthand with Variables

```tsx
<View boxShadow="0 0 10px $shadowColor" />
<View backgroundImage="linear-gradient(to bottom, $background, $color)" />
<View border="1px solid $borderColor" />
<View filter="blur($2)" />
```

Works in `boxShadow`, `backgroundImage`, `filter`, `border`, `outline`.

---

## Pseudo States

```tsx
<View
  bg="$background"
  hoverStyle={{ bg: '$backgroundHover' }}
  pressStyle={{ bg: '$backgroundPress', scale: 0.98 }}
  focusStyle={{ outlineColor: '$blue10', outlineWidth: 2, outlineStyle: 'solid' }}
  focusVisibleStyle={{ outlineColor: '$blue10' }}
  focusWithinStyle={{ borderColor: '$blue10' }}
  disabledStyle={{ opacity: 0.5 }}
  enterStyle={{ opacity: 0, y: 20 }}  // animate FROM on mount
  exitStyle={{ opacity: 0, y: -20 }}  // animate TO on unmount
/>
```

---

## Event Props (built-in Pressable)

No need for `Pressable` or `TouchableOpacity` — all views support:

- `onPress`, `onPressIn`, `onPressOut`, `onLongPress`
- `onHoverIn`, `onHoverOut` (web only)
- `onFocus`, `onBlur`
- `disabled`, `focusable`, `hitSlop`
- All pointer events: `onPointerDown`, `onPointerUp`, `onPointerMove`, etc.
- Web-only: `onClick`, `onKeyDown`, `onScroll`, `onDrag`, etc.

---

## Parent-Based Styling

```tsx
// Media query
<Text color="red" $sm={{ color: 'blue' }} />

// Theme
<Text $theme-dark={{ color: 'white' }} />

// Platform
<Text $platform-ios={{ color: 'white' }} $platform-web={{ cursor: 'pointer' }} />

// Group
<View group="header">
  <Text $group-header={{ color: 'white' }} />
  <Text $group-header-hover={{ color: 'blue' }} />
</View>

// Group container query
<View group>
  <Text $group-sm={{ color: 'white' }} $group-sm-hover={{ color: 'green' }} />
</View>
```

Type group names:
```tsx
declare module 'tamagui' {
  interface TypeOverride {
    groupNames(): 'card' | 'header'
  }
}
```

---

## Order is Important

Props are applied left-to-right. Later props override earlier ones:

```tsx
// background can be overridden by props, but width is always 200
<View background="red" {...props} width={200} />

// scale depends on order — huge overrides scale, or scale overrides huge
<MyView huge scale={3} />  // scale = 3  (scale wins)
<MyView scale={3} huge />  // scale = 2  (huge wins)
```

---

## Other Props

| Prop | Type | Description |
|------|------|-------------|
| `theme` | `string` | Apply a sub-theme |
| `themeInverse` | `boolean` | Invert light/dark |
| `group` | `boolean \| string` | Mark as group for child styling |
| `asChild` | `boolean \| 'except-style'` | Pass props to single child element |
| `className` | `string` | Web only — merged with generated classes |
| `tag` | `string` | Web only — rendered HTML tag |
| `debug` | `boolean \| 'verbose'` | Debug styling output |
| `forceStyle` | `'hover' \| 'press' \| 'focus'` | Force pseudo state |
| `animateOnly` | `string[]` | Limit animated properties |
| `role` | `Role` | Accessibility role |
| `tabIndex` | `number` | Focus order |
