# Skill: Setup Unit Testing in React Native

## Installation and configuration

Follow Expo's current Jest setup for new or existing Expo projects.

Install the required dev dependencies:

```bash
npx expo install jest-expo jest @types/jest --dev
```

If the project does not use TypeScript, `@types/jest` is optional. If it does use TypeScript, add `jest` to the `types` array in `tsconfig.json` so Jest globals are available:

```json
{
  "compilerOptions": {
    "types": ["jest"]
  }
}
```

Add a test script and configure `jest-expo` as the preset in `package.json`:

```json
{
  "scripts": {
    "test": "jest --watchAll"
  },
  "jest": {
    "preset": "jest-expo"
  }
}
```

If the app depends on packages that Jest does not transpile by default, add a `transformIgnorePatterns` entry. Expo's recommended baseline is:

```json
{
  "jest": {
    "preset": "jest-expo",
    "transformIgnorePatterns": [
      "node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@sentry/react-native|native-base|react-native-svg)"
    ]
  }
}
```

## Install React Native Testing Library

Use React Native Testing Library for component tests:

```bash
npx expo install @testing-library/react-native --dev
```

This replaces the deprecated `react-test-renderer`, which does not support React 19 and above.

## Write tests

Expo's `jest-expo` preset recognizes files with `-test.ts` and `-test.tsx` extensions. A common layout is to keep tests in a root `__tests__` directory or in feature-specific `__tests__` folders next to the code they cover.

Prefer focused unit tests for behavior and logic. Example:

```tsx
import { render } from '@testing-library/react-native';

import HomeScreen, { CustomText } from '@/app/index';

describe('<HomeScreen />', () => {
  test('Text renders correctly on HomeScreen', () => {
    const { getByText } = render(<HomeScreen />);

    getByText('Welcome!');
  });
});
```

## Coverage

To generate coverage output, set coverage flags in `package.json` and include the files you want tracked:

```json
{
  "jest": {
    "preset": "jest-expo",
    "collectCoverage": true,
    "collectCoverageFrom": [
      "**/*.{ts,tsx,js,jsx}",
      "!**/coverage/**",
      "!**/node_modules/**",
      "!**/babel.config.js",
      "!**/expo-env.d.ts",
      "!**/.expo/**"
    ]
  }
}
```

Add `coverage/**/*` to `.gitignore` so generated reports are not committed.
