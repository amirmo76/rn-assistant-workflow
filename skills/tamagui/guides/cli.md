# Tamagui CLI

```bash
yarn add -D @tamagui/cli
```

## Commands

### build

Pre-compile components for production. Wrap your build command with `--` so files are restored after.

```bash
# Optimize then run bundler (files restored automatically)
npx tamagui build --target web ./src -- next build

# Native
npx tamagui build --target native ./src -- eas build --platform ios

# Output to separate dir (source unchanged)
npx tamagui build --output ./dist ./src

# Dry run
npx tamagui build --dry-run ./src

# CI: fail if fewer than N components optimized
npx tamagui build --target web --expect-optimizations 10 ./src -- next build
```

Flags: `--target web|native|both`, `--include <glob>`, `--exclude <glob>`, `--output <path>`, `--output-around`, `--expect-optimizations <n>`, `--dry-run`.

Platform-specific files (`.web.tsx`, `.native.tsx`, `.ios.tsx`, `.android.tsx`) are handled automatically.

### generate

Build full config, output CSS and LLM prompt:

```bash
npx tamagui generate
```

Outputs to `.tamagui/` directory including `prompt.md`.

### generate-css

Generate `tamagui.generated.css`:

```bash
npx tamagui generate-css --output ./public/styles/tamagui.generated.css
```

### generate-themes

Pre-build theme config for faster runtime:

```bash
npx tamagui generate-themes ./themes/input.ts ./themes/generated.ts
```

### check

Find inconsistent `@tamagui/*` versions:

```bash
npx tamagui check
```

### add (Pro only)

Add pre-configured fonts/icons:

```bash
npx tamagui add font
npx tamagui add icon
```

### generate-prompt

Generate LLM-friendly markdown of your design system:

```bash
npx tamagui generate-prompt --output .tamagui/prompt.md
```

## Global Flags

`--debug`, `--verbose`, `--help`, `--version`
