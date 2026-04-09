---
name: rn-storybook-setup
description: Set up Storybook for an Expo React Native project, including Expo Router projects.
---

# RN Storybook Setup

Standard baseline for Expo React Native projects, including Expo Router.

## Rules

- Use `npx expo install` for native Expo dependencies.
- Clear Metro cache when switching app and Storybook modes: `expo start -c`.
- Regenerate `.rnstorybook/storybook.requires.ts` when stories or addons drift.

## Install

```bash
npx storybook@latest init
npm install --save-dev cross-env
npx expo install expo-constants
```

## Environment Bridge

Use `app.config.js` to expose Storybook mode:

```js
export default ({ config }) => ({
  ...config,
  extra: {
    ...config.extra,
    storybookEnabled: process.env.STORYBOOK_ENABLED === 'true',
  },
});
```

## Expo Router Entry

Gate Storybook from `app/_layout.tsx` and return Storybook when the flag is enabled.

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

Create one simple story when the repo has none.

## Troubleshooting

- Missing addon module: install it, regenerate stories, restart with cache clear.
- Native Storybook addon crash: install required native packages with `expo install`, then rebuild the dev app.
