# Installation & Bundler Setup

## Quick Start

```bash
npm install tamagui @tamagui/config
```

Minimal `tamagui.config.ts`:

```tsx
import { defaultConfig } from '@tamagui/config/v5'
import { createTamagui } from 'tamagui'

export const config = createTamagui(defaultConfig)

type AppConfig = typeof config
declare module 'tamagui' {
  interface TamaguiCustomConfig extends AppConfig {}
}

export default config
```

Wrap your app:

```tsx
import { TamaguiProvider } from 'tamagui'
import config from './tamagui.config'

export default function App() {
  return (
    <TamaguiProvider config={config} defaultTheme="light">
      <AppContents />
    </TamaguiProvider>
  )
}
```

---

## Compiler Setup (Optional)

The compiler extracts styles to CSS at build time. Configure via `tamagui.build.ts`:

```ts
import type { TamaguiBuildOptions } from 'tamagui'

export default {
  config: './tamagui.config.ts',
  components: ['tamagui'],
  outputCSS: './public/tamagui.generated.css',
  disableExtraction: process.env.NODE_ENV === 'development',
} satisfies TamaguiBuildOptions
```

All bundler plugins read from this file automatically.

---

## Expo / React Native (Metro)

The babel plugin is **optional** on native — Tamagui works without it. Add it only if you want compiler optimizations:

```bash
yarn add -D @tamagui/babel-plugin
```

`babel.config.js`:

```js
module.exports = {
  plugins: ['@tamagui/babel-plugin'], // reads from tamagui.build.ts
}
```

### Metro Plugin (Recommended for Expo)

```bash
yarn add -D @tamagui/metro-plugin
```

`metro.config.js`:

```js
const { withTamagui } = require('@tamagui/metro-plugin')
module.exports = withTamagui(getDefaultConfig(__dirname))
```

### Loading Fonts on Native

```tsx
import { useFonts } from 'expo-font'

function App() {
  const [loaded] = useFonts({
    Inter: require('@tamagui/font-inter/otf/Inter-Medium.otf'),
    InterBold: require('@tamagui/font-inter/otf/Inter-Bold.otf'),
  })
  if (!loaded) return null
  return <MyApp />
}
```

On Android, you must set the `face` option in `createFont` for different weights.

---

## Next.js (Turbopack — default)

Works in dev with zero config. For production, use the CLI:

```bash
yarn add -D @tamagui/cli
```

`next.config.ts`:

```ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  transpilePackages: ['@tamagui/lucide-icons-2'],
  experimental: {
    turbo: {
      resolveAlias: {
        'react-native': 'react-native-web',
        'react-native-svg': '@tamagui/react-native-svg',
      },
    },
  },
}
export default nextConfig
```

Build scripts:

```json
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "tamagui build --target web ./src -- next build"
  }
}
```

### CSS Setup

Import the generated CSS in `app/layout.tsx`:

```tsx
import '../public/tamagui.generated.css'
```

Run `npx tamagui build` once to generate it, then commit.

### Themes (light/dark)

```bash
yarn add @tamagui/next-theme
```

```tsx
'use client'
import { NextThemeProvider, useRootTheme } from '@tamagui/next-theme'
import { TamaguiProvider } from 'tamagui'
import config from '../tamagui.config'

export function NextTamaguiProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useRootTheme()
  return (
    <NextThemeProvider skipNextHead onChangeTheme={(next) => setTheme(next as any)}>
      <TamaguiProvider config={config} disableRootThemeClass defaultTheme={theme}>
        {children}
      </TamaguiProvider>
    </NextThemeProvider>
  )
}
```

### Next.js (Webpack — older)

```bash
yarn add @tamagui/next-plugin
```

```js
// next.config.js
const { withTamagui } = require('@tamagui/next-plugin')

module.exports = function (name, { defaultConfig }) {
  const tamaguiPlugin = withTamagui({
    config: './tamagui.config.ts',
    components: ['tamagui'],
    appDir: true, // for app router
  })
  return { ...defaultConfig, ...tamaguiPlugin(defaultConfig) }
}
```

---

## Vite

```bash
yarn add @tamagui/vite-plugin
```

`@tamagui/vite-plugin` is ESM-only — your project needs `"type": "module"` in package.json.

```tsx
import { tamaguiPlugin } from '@tamagui/vite-plugin'

export default defineConfig({
  plugins: [tamaguiPlugin()], // reads from tamagui.build.ts
})
```

---

## Webpack

```bash
yarn add tamagui-loader
```

```js
const { TamaguiPlugin } = require('tamagui-loader')

module.exports = {
  resolve: {
    alias: {
      'react-native$': require.resolve('react-native-web'),
      'react-native-svg': require.resolve('@tamagui/react-native-svg'),
    },
  },
  plugins: [new TamaguiPlugin()], // reads from tamagui.build.ts
}
```

---

## CLI-Based Compilation (any bundler)

For bundlers without a plugin (e.g. Turbopack):

```bash
yarn add -D @tamagui/cli

# Wrap your build — files optimized then restored automatically
npx tamagui build --target web ./src -- next build

# Or output to separate dir (never modifies source)
npx tamagui build --target web --output ./dist ./src
```

---

## TamaguiProvider Props

| Prop | Type | Description |
|------|------|-------------|
| `config` | `TamaguiConfig` | Required. Your `createTamagui()` result. |
| `defaultTheme` | `string` | Required. Initial top-level theme name. |
| `disableInjectCSS` | `boolean` | Disable runtime CSS injection (use with SSR + `outputCSS`). |
| `disableRootThemeClass` | `boolean` | Don't add theme className to root — useful with `@tamagui/next-theme`. |

## Compiler Plugin Props

| Prop | Type | Description |
|------|------|-------------|
| `config` | `string` | Path to `tamagui.config.ts`. |
| `components` | `string[]` | Packages containing Tamagui components (e.g. `['tamagui']`). |
| `outputCSS` | `string` | Path to write extracted CSS. |
| `disableExtraction` | `boolean` | Skip CSS extraction (faster dev). |
| `importsWhitelist` | `string[]` | Files the compiler may import at build-time for partial evaluation. |
| `logTimings` | `boolean` | Log per-file compile timings. |
