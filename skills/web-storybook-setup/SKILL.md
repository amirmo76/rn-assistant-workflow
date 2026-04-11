---
name: web-storybook-setup
description: Set up Storybook for a React or Next.js web project.
---

# Web Storybook Setup

Standard baseline for React and Next.js web projects.

## Rules

- Use the Storybook CLI to initialise; it auto-detects the framework.
- Prefer `@storybook/react-vite` for Vite-based projects and `@storybook/nextjs` for Next.js.
- Keep `.storybook/` config minimal and framework-idiomatic.

## Install

Run the interactive initialiser from the project root:

```bash
npx storybook@latest init
```

The CLI detects the framework (React + Vite, Next.js, CRA, etc.) and installs the correct builder and preset automatically.

For Next.js projects the CLI installs `@storybook/nextjs`. Accept the defaults.

## Manual install (Vite + React)

If the auto-init is not suitable:

```bash
npm install --save-dev @storybook/react-vite @storybook/addon-essentials @storybook/blocks storybook
```

Create `.storybook/main.ts`:

```ts
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: ['../src/**/*.stories.@(ts|tsx)'],
  addons: ['@storybook/addon-essentials'],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
};
export default config;
```

## Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "storybook": "storybook dev -p 6006",
    "storybook:build": "storybook build"
  }
}
```

## Smoke Story

Create one simple story when the repo has none, for example `src/components/Button/Button.stories.tsx`:

```tsx
import type { Meta, StoryObj } from '@storybook/react';

const meta: Meta = {
  title: 'Example/Placeholder',
  component: () => <div>Placeholder story</div>,
};
export default meta;

type Story = StoryObj<typeof meta>;
export const Default: Story = {};
```

## Next.js Notes

- Use `@storybook/nextjs` (auto-installed by the CLI for Next.js projects).
- The preset handles `next/image`, `next/font`, and routing mocks automatically.
- Do not add a custom Webpack or Babel config unless strictly necessary.

## Troubleshooting

- **Missing peer dependency**: run `npx storybook@latest doctor` to identify and fix version conflicts.
- **CSS modules not resolving**: ensure `@storybook/react-vite` or `@storybook/nextjs` version is up to date.
- **Stories not found**: verify the `stories` glob in `.storybook/main.ts` matches the file naming convention used in the project.
