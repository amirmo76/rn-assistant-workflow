---
name: rn-storybook-setup
description: >
  Use when setting up or repairing Storybook for an Expo React Native project
  (including Expo Router). Covers install, environment bridge, metro config,
  entry gating, scripts, notes addon, and a smoke story. Triggers: "storybook expo",
  "storybook react native", "rn storybook", "expo storybook", "sb-rn-get-stories".
---

# RN Storybook Setup

Standard baseline for Expo React Native projects, including Expo Router.

## Rules

- Use `npx expo install` for native Expo dependencies.
- Clear Metro cache when switching app and Storybook modes: `expo start -c`.
- Regenerate `.rnstorybook/storybook.requires.ts` when stories or addons drift.
- Always use `--legacy-peer-deps` when installing Storybook-related packages; peer
  dep conflicts are common with React 19.

## Install

```bash
npx storybook@latest init
npm install --save-dev cross-env @storybook/addon-ondevice-notes --legacy-peer-deps
npx expo install expo-constants
```

## Metro Config (REQUIRED)

`storybook.requires.ts` uses `require.context`, which Metro does not support by
default. Without this file, the Storybook bundle will fail at runtime.

Create `metro.config.js` in the project root:

```js
const { getDefaultConfig } = require("expo/metro-config");
const { withStorybook } = require("@storybook/react-native/metro/withStorybook");
const path = require("path");

const defaultConfig = getDefaultConfig(__dirname);

module.exports = withStorybook(defaultConfig, {
  enabled: process.env.STORYBOOK_ENABLED === "true",
  configPath: path.resolve(__dirname, "./.rnstorybook"),
});
```

> **Why**: `withStorybook` patches Metro to support `require.context`. Without it,
> the generated `storybook.requires.ts` will throw at bundle time.

## Environment Bridge

Use `app.config.js` to expose the Storybook flag to the runtime bundle.

> **Critical**: `process.env.STORYBOOK_ENABLED` is NOT automatically inlined by
> Metro in React Native bundles (unlike `NODE_ENV`). You MUST bridge it through
> `app.config.js` → `Constants.expoConfig.extra` so it is readable at runtime.

```js
// app.config.js
export default ({ config }) => ({
  ...config,
  extra: {
    ...config.extra,
    storybookEnabled: process.env.STORYBOOK_ENABLED === "true",
  },
});
```

## Expo Router Entry Gate

Gate Storybook from `src/app/_layout.tsx` (or `app/_layout.tsx`). Read the flag from
`Constants.expoConfig?.extra?.storybookEnabled` — NOT from `process.env`.

The `require` must be **inside** the `if` block so Storybook modules are never loaded
in normal app mode (they use `require.context` which would error otherwise):

```tsx
import Constants from "expo-constants";
import { Stack } from "expo-router";

export default function RootLayout() {
  if (Constants.expoConfig?.extra?.storybookEnabled) {
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const StorybookUI = require("../../.rnstorybook").default;
    return <StorybookUI />;
  }
  return <Stack />;
}
```

> **Why not `process.env`**: Metro only inlines `NODE_ENV` automatically. Any other
> `process.env` variable read inside the bundle will always be `undefined` at runtime.

## Addons

Register in `.rnstorybook/main.ts`:

```ts
addons: [
  "@storybook/addon-ondevice-controls",
  "@storybook/addon-ondevice-actions",
  "@storybook/addon-ondevice-notes",
],
```

`addon-ondevice-notes` is the on-device equivalent of web autodocs. Use it with
`parameters.notes` in stories:

```ts
parameters: {
  notes: "Markdown description of the component.",
},
```

## Scripts

```json
{
  "scripts": {
    "storybook": "cross-env STORYBOOK_ENABLED='true' expo start",
    "storybook:clear": "cross-env STORYBOOK_ENABLED='true' expo start -c",
    "storybook:generate": "sb-rn-get-stories"
  }
}
```

## Smoke Story

Create `src/stories/Smoke.stories.tsx` (creates the `src/stories/` directory):

```tsx
import type { Meta, StoryObj } from "@storybook/react-native";
import { Text, View } from "react-native";

function Placeholder() {
  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      <Text>Storybook is working</Text>
    </View>
  );
}

const meta: Meta<typeof Placeholder> = {
  title: "Smoke/Placeholder",
  component: Placeholder,
  parameters: {
    notes: "A minimal smoke-test story that verifies Storybook is configured correctly.",
  },
};

export default meta;

type Story = StoryObj<typeof Placeholder>;

export const Default: Story = {};
```

## Verification

Run in order after setup — all must succeed:

```bash
npm run typecheck
npm run lint
npm test
npm run storybook:generate
```

Then launch with `npm run storybook:clear` (cache clear is important on first run)
and confirm the Storybook UI appears on-device with a Notes tab.

## Troubleshooting

- **Storybook UI never appears**: Check that `_layout.tsx` reads
  `Constants.expoConfig?.extra?.storybookEnabled`, NOT `process.env.STORYBOOK_ENABLED`.
- **`require.context` error at runtime**: `metro.config.js` is missing or `withStorybook`
  is not applied. Create/fix the file and restart with cache clear.
- **Missing addon module**: install it, regenerate stories, restart with cache clear.
- **Native addon crash**: install required native packages with `expo install`, rebuild.
- **Peer dep conflicts**: always use `--legacy-peer-deps` with Storybook packages on
  projects using React 19.


