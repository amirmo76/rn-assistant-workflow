# Configuration (v5)

## Recommended Setup

```bash
npm install @tamagui/config
```

```tsx
import { defaultConfig } from '@tamagui/config/v5'
import { animations } from '@tamagui/config/v5-css' // or v5-rn, v5-reanimated, v5-motion
import { createTamagui } from 'tamagui'

export const config = createTamagui({
  ...defaultConfig,
  animations,
})

type AppConfig = typeof config
declare module 'tamagui' {
  interface TamaguiCustomConfig extends AppConfig {}
}
```

v5 base export includes **no animations** — import separately from a driver entry point.

## Animation Drivers

| Package | Best for |
|---------|----------|
| `@tamagui/config/v5-css` | Web (smallest bundle) |
| `@tamagui/config/v5-motion` | Spring physics, smooth |
| `@tamagui/config/v5-rn` | React Native Animated API |
| `@tamagui/config/v5-reanimated` | Best native performance |

Cross-platform setup:

```tsx
import { isWeb } from 'tamagui'
import { animations as animationsCSS } from '@tamagui/config/v5-css'
import { animations as animationsReanimated } from '@tamagui/config/v5-reanimated'

export const config = createTamagui({
  ...defaultConfig,
  animations: isWeb ? animationsCSS : animationsReanimated,
})
```

---

## Tokens

Static design variables mapped to CSS variables at build time.

```tsx
import { createTokens } from 'tamagui'

const tokens = createTokens({
  size: { sm: 8, md: 12, lg: 20, true: 12 }, // `true` = default
  space: { sm: 4, md: 8, lg: 12, true: 8 },
  radius: { none: 0, sm: 3 },
  color: { white: '#fff', black: '#000' },
  zIndex: { 0: 0, 1: 100 },
})
```

Token-to-property mapping:
- **Size** → width, height, minWidth, maxWidth, minHeight, maxHeight
- **Space** → padding, margin, gap, and all other properties
- **Radius** → borderRadius and corner variants
- **Color** → color, backgroundColor, borderColor
- **zIndex** → zIndex

Custom tokens with specific syntax: `width="$icon.small"`.

### Fonts

```tsx
import { createFont, isWeb } from 'tamagui'

const bodyFont = createFont({
  family: isWeb ? 'Inter, sans-serif' : 'Inter',
  size: { 1: 12, 2: 14, 3: 15 },
  lineHeight: { 1: 17, 2: 22 },
  weight: { 4: '300', 6: '600' },
  letterSpacing: { 4: 0, 8: -1 },
  // Required on Android for weights:
  face: {
    300: { normal: 'InterLight' },
    600: { normal: 'InterBold' },
  },
})
```

---

## Themes

Dynamic CSS-variable-like values that nest contextually via `<Theme>`.

```tsx
themes: {
  light: { background: '#f2f2f2', color: '#000' },
  dark: { background: '#111', color: '#fff' },
  // Sub-themes: accessed as <Theme name="pink"> inside a light/dark parent
  dark_pink: { background: tokens.color.pinkDark, color: tokens.color.pinkLight },
  light_pink: { background: tokens.color.pinkLight, color: tokens.color.pinkDark },
}
```

### v5 Theme Values

v5 themes include rich semantic colors:
- `background`, `backgroundHover`, `backgroundPress`, `backgroundFocus`
- `color`, `colorHover`, `colorPress`, `colorFocus`
- `borderColor`, `borderColorHover`, `borderColorPress`, `borderColorFocus`
- `color1`–`color12` (12-step palette scale)
- `shadow1`–`shadow8`, `highlight1`–`highlight8`
- Opacity variants: `color01` (10%), `background005` (5%), etc.
- `accentBackground`, `accentColor` (inverted palette)

### Customizing v5 Themes

```tsx
import { createV5Theme, defaultChildrenThemes } from '@tamagui/config/v5'
import { cyan, cyanDark } from '@tamagui/colors'

const themes = createV5Theme({
  childrenThemes: {
    ...defaultChildrenThemes,
    cyan: { light: cyan, dark: cyanDark },
  },
})

export const config = createTamagui({ ...defaultConfig, themes })
```

Default color themes: gray, blue, red, yellow, green, orange, pink, purple, teal, neutral, black, white.

---

## Media Queries

Responsive breakpoints used as `$sm`, `$md`, etc. on props and in `useMedia`.

### v5 Defaults (Tailwind-aligned)

| Name | Type | Value |
|------|------|-------|
| `xxxs` | minWidth | 260 |
| `xxs` | minWidth | 340 |
| `xs` | minWidth | 460 |
| `sm` | minWidth | 640 |
| `md` | minWidth | 768 |
| `lg` | minWidth | 1024 |
| `xl` | minWidth | 1280 |
| `xxl` | minWidth | 1536 |
| `max-sm` | maxWidth | 640 |
| `max-md` | maxWidth | 768 |
| `touchable` | pointer: coarse | Touch devices |
| `hoverable` | hover: hover | Devices with hover |

Height queries: `height-sm`, `height-md`, `height-lg` and max variants.

---

## Shorthands (v5 default)

| Short | Long | Short | Long |
|-------|------|-------|------|
| `p` | padding | `m` | margin |
| `pt` | paddingTop | `mt` | marginTop |
| `pb` | paddingBottom | `mb` | marginBottom |
| `pl` | paddingLeft | `ml` | marginLeft |
| `pr` | paddingRight | `mr` | marginRight |
| `px` | paddingHorizontal | `mx` | marginHorizontal |
| `py` | paddingVertical | `my` | marginVertical |
| `bg` | backgroundColor | `rounded` | borderRadius |
| `t` | top | `b` | bottom |
| `l` | left | `r` | right |
| `minW` | minWidth | `maxW` | maxWidth |
| `minH` | minHeight | `maxH` | maxHeight |
| `z` | zIndex | `text` | textAlign |
| `grow` | flexGrow | `shrink` | flexShrink |
| `items` | alignItems | `self` | alignSelf |
| `content` | alignContent | `justify` | justifyContent |
| `select` | userSelect | | |

With `onlyAllowShorthands: true` (v5 default), only short forms are available in types.

---

## v5 Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `defaultFont` | `"body"` | Default font family |
| `fastSchemeChange` | `true` | DynamicColorIOS for fast light/dark switch |
| `allowedStyleValues` | `"somewhat-strict-web"` | Allow web values like vh, vw |
| `onlyAllowShorthands` | `true` | Only allow shorthand props (no longhand) |
| `styleCompat` | `"react-native"` | `flexBasis: 0` default (RN-style) |

---

## Custom Config (from scratch)

```tsx
import { createFont, createTamagui, createTokens } from 'tamagui'

const tokens = createTokens({
  size: { sm: 8, md: 12, true: 12 },
  space: { sm: 4, md: 8, true: 8 },
  radius: { sm: 3 },
  color: { white: '#fff', black: '#000' },
})

const config = createTamagui({
  fonts: { heading: myFont, body: myFont },
  tokens,
  themes: {
    light: { bg: '#f2f2f2', color: '#000' },
    dark: { bg: '#111', color: '#fff' },
  },
  media: {
    sm: { maxWidth: 860 },
    gtSm: { minWidth: 861 },
  },
  shorthands: { px: 'paddingHorizontal' } as const,
})
```

> For `tamagui` UI kit components, define a `true` token in `size` and `space` as the default.
