# Skill: Setup Unit Testing in React Native

## 1. Installation

React Native and Expo projects generally come with `jest` pre-installed. You need to add React Native Testing Library (RNTL) and custom Jest matchers for native elements.

```bash
npm install --save-dev @testing-library/react-native @testing-library/jest-native
```

## 2. Configuration

Create or update your Jest configuration files so your tests understand React Native components and have access to native assertions.

`jest.config.js`

```JavaScript
module.exports = {
  preset: 'react-native', // Or 'jest-expo' if using Expo
  setupFilesAfterEnv: ['./jest.setup.js'],
  transformIgnorePatterns: [
    'node_modules/(?!(react-native|@react-native|react-native-button)/)',
  ],
};
```

`jest.setup.js`

Create this file in your root directory to extend Jest with React Native specific matchers.

```JavaScript
// Adds custom matchers like .toBeVisible(), .toHaveTextContent(), etc.
import '@testing-library/jest-native/extend-expect';

// Example: Silence reanimated warnings in tests (if using Reanimated)
jest.mock('react-native-reanimated', () => {
  const Reanimated = require('react-native-reanimated/mock');
  return Reanimated;
});
```

## 3. Writing a Test (components/Button.test.tsx)

Write your tests by interacting with the component exactly as a user would.

```TypeScript
import React from 'react';
import { Button } from 'react-native';
import { render, screen, fireEvent } from '@testing-library/react-native';

describe('Button Component', () => {
  it('renders correctly and handles presses', () => {
    const mockFn = jest.fn();
    
    render(<Button title="Submit" onPress={mockFn} />);
    
    // Find the element by its text
    const buttonElement = screen.getByText('Submit');
    
    // Assert it exists and is visible
    expect(buttonElement).toBeVisible();
    
    // Simulate a user tap
    fireEvent.press(buttonElement);
    
    // Assert the function was called
    expect(mockFn).toHaveBeenCalledTimes(1);
  });
});
```

## 4. Running Tests

Run your test suite via the terminal.

```Bash
# Run all tests
npm test
```

### Clear Jest cache (useful if tests act weirdly after a config change)

```Bash
npm test -- --clearCache
```

### Important Notes

* **Behavior Over Implementation:** We use `@testing-library/react-native` instead of `react-test-renderer` because it encourages testing *how the app behaves* rather than its internal state. You find elements by text, accessibility labels, or placeholders (how a user finds them), rather than by component instances.
* **The Node.js Limitation (Mocking):** Jest runs in a Node.js environment on your computer, not on an actual iOS or Android device. Therefore, any library that relies on native code (Camera, AsyncStorage, Reanimated, Gesture Handler) will crash your tests unless you **mock** it. `transformIgnorePatterns` in your config tells Jest to compile specific node_modules that ship as raw ES6/JSX instead of standard CommonJS.
* **`@testing-library/jest-native`:** Standard Jest only knows about basic JavaScript types. This library bridges the gap by providing React Native specific DOM-like assertions. Instead of checking if a property exists in an object tree, you can simply write `expect(element).toBeDisabled()` or `expect(element).toHaveStyle({ opacity: 0.5 })`.
