---
name: rn-testing-setup
description: >
  Use when setting up or repairing Jest + React Native Testing Library for an
  Expo React Native project. Covers install, jest-expo preset, scripts, and a
  smoke test. Triggers: "jest expo", "rn testing", "react native test setup",
  "jest-expo", "@testing-library/react-native".
---

# RN Testing Setup

Use Expo's Jest setup as the default baseline.

## Install

```bash
npx expo install jest-expo jest @types/jest --dev
npx expo install @testing-library/react-native --dev
```

If the project uses TypeScript, add `jest` to `compilerOptions.types`.

## Package.json

Use `jest-expo` as the preset and ensure these scripts exist:

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "jest": {
    "preset": "jest-expo"
  }
}
```

Add Expo's baseline `transformIgnorePatterns` when packages need transpilation.

## Smoke Test

Create one passing smoke test when the repo has no tests yet, for example:

```tsx
it('smoke', () => {
  expect(true).toBe(true);
});
```

`jest-expo` recognizes `-test.ts` and `-test.tsx` files.

## Notes

- Prefer `@testing-library/react-native` over `react-test-renderer`.
- Ignore generated coverage output in git.
