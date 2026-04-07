# Skill: Setup Storybook in React Native

## 1. Initialization

Run the following command in your React Native project root. It auto-detects your environment and installs the correct `@storybook/react-native` dependencies.

```bash
npx storybook@latest init
```

## 2. Configuration (.storybook/main.ts)

Ensure Storybook knows where to look for your story files and addons.

```TypeScript
module.exports = {
  stories: ['../components/**/*.stories.?(ts|tsx|js|jsx)'],
  addons: [
    '@storybook/addon-ondevice-controls', 
    '@storybook/addon-ondevice-actions'
  ],
};
```

## 3. Entry Point & Toggling (App.tsx)

Because Storybook does not run on a separate port like the web, it must intercept your app's entry point. Do not use hardcoded booleans to toggle it, as they can accidentally ship to production.

Option A: Environment Variables (Recommended)
This build-time approach prevents accidental commits. (Example using Expo):

```TypeScript
import StorybookUIRoot from './.storybook';
import MainApp from './src/MainApp';

// For Expo, use EXPO_PUBLIC_ prefix. For bare RN, use react-native-config.
const SHOW_STORYBOOK = process.env.EXPO_PUBLIC_STORYBOOK === 'true';

export default SHOW_STORYBOOK ? StorybookUIRoot : MainApp;
```

Run App: `npx expo start`

Run Storybook: `EXPO_PUBLIC_STORYBOOK=true npx expo start`

Option B: Dev Menu Toggle (Advanced)
Use AsyncStorage and the React Native Dev Menu for a runtime toggle without restarting your server.

```TypeScript
import React, { useState, useEffect } from 'react';
import { DevSettings } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import StorybookUIRoot from './.storybook';
import MainApp from './src/MainApp';

export default function App() {
  const [showStorybook, setShowStorybook] = useState(false);

  useEffect(() => {
    AsyncStorage.getItem('SHOW_STORYBOOK').then((val) => setShowStorybook(val === 'true'));

    if (__DEV__) {
      DevSettings.addMenuItem('Toggle Storybook', () => {
        AsyncStorage.setItem('SHOW_STORYBOOK', showStorybook ? 'false' : 'true').then(() => {
          DevSettings.reload();
        });
      });
    }
  }, [showStorybook]);

  return showStorybook ? <StorybookUIRoot /> : <MainApp />;
}
```

## 4. Writing a Story (components/Button.stories.tsx)

Create a story using Component Story Format (CSF).

```TypeScript
import type { Meta, StoryObj } from '@storybook/react-native';
import { Button } from 'react-native';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    title: 'Click Me',
    onPress: () => console.log('Pressed!'),
  },
};
```

## 5. Running

Clear your bundler cache to ensure new files are picked up.

```Bash
npm start -- --reset-cache
```
