---
name: web-testing-setup
description: Set up Vitest and React Testing Library for a React or Next.js web project.
---

# Web Testing Setup

Use Vitest as the default test runner for web projects. Fall back to Jest when the project already uses Create React App or requires Jest-specific capabilities.

## Install (Vitest — preferred)

```bash
npm install --save-dev vitest @vitest/coverage-v8
npm install --save-dev @testing-library/react @testing-library/user-event @testing-library/jest-dom
npm install --save-dev jsdom
```

For Next.js or projects that need a global setup file, also install:

```bash
npm install --save-dev @vitejs/plugin-react
```

## Vite / Vitest Config

Add test configuration to `vite.config.ts` (or create `vitest.config.ts`):

```ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test/setup.ts',
  },
});
```

## Setup File

Create `src/test/setup.ts`:

```ts
import '@testing-library/jest-dom';
```

## Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage"
  }
}
```

If using TypeScript, add `"types": ["vitest/globals"]` to `compilerOptions` in `tsconfig.json`.

## Smoke Test

Create one passing smoke test when the repo has no tests yet:

```tsx
import { describe, it, expect } from 'vitest';

describe('smoke', () => {
  it('passes', () => {
    expect(true).toBe(true);
  });
});
```

Vitest recognises `*.test.ts`, `*.test.tsx`, `*.spec.ts`, and `*.spec.tsx` files.

## Jest (fallback)

If the project already uses Jest (e.g. Create React App):

```bash
npm install --save-dev jest jest-environment-jsdom @testing-library/react @testing-library/user-event @testing-library/jest-dom ts-jest
```

Add to `package.json`:

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "jest": {
    "preset": "ts-jest",
    "testEnvironment": "jsdom",
    "setupFilesAfterFramework": ["@testing-library/jest-dom"]
  }
}
```

## Notes

- Prefer `@testing-library/react` with `userEvent` over direct DOM manipulation.
- Ignore generated coverage output in git (`coverage/`).
- Do not test implementation details; test observable behaviour.
