# SKILL: Storybook Setup for Expo React Native (with Expo Router)

## Context

This guide defines the standard operating procedure for integrating Storybook into an Expo React Native project that uses **Expo Router** and **Custom Development Builds** (not Expo Go).

## The Golden Rules

Before executing any steps, the AI must adhere to these strict constraints:

1. **The Cache is the Enemy:** React Native's Metro bundler aggressively caches environment variables and module paths. When switching between Storybook and the main app, or when fixing a missing module, ALWAYS start the server with the clear cache flag: `expo start -c`.
2. **Expo Install over NPM Install:** For any package that interacts with the native layer (e.g., `expo-constants`, `@react-native-async-storage/async-storage`), ALWAYS use `npx expo install`. Standard `npm install` will fetch bleeding-edge versions that break the current Expo SDK's autolinker.
3. **Dynamic Imports Don't Exist:** React Native cannot resolve dynamic imports. Storybook relies on a generated file (`.rnstorybook/storybook.requires.ts`). If stories aren't updating or addon imports are broken, manually delete the file and run `npx sb-rn-get-stories` to rebuild it.
4. **Native Modules Require Rebuilds:** If utilizing `@storybook/addon-ondevice-controls`, it relies on native UI elements (Sliders, DatePickers). This will crash Expo Go. It requires installing the native community packages and compiling a fresh development build (`npx expo run:android` / `run:ios`).

---

## The Standard Workflow

### Step 1: Initialization & Base Dependencies

Run the standard Storybook initialization, then safely install environment bridging tools.

```bash
npx storybook@latest init
npm install --save-dev cross-env
npx expo install expo-constants
```

*(Note: If npm throws an `ERESOLVE` peer dependency error on `expo-constants`, completely uninstall it via npm first, then run the `npx expo install` command to lock it to the correct SDK version).*

### Step 2: Environment Variable Bridge

Do not modify the static `app.json` for dynamic variables. Create an `app.config.js` file alongside it to merge in the environment state.

```javascript
// app.config.js
export default ({ config }) => ({
  ...config,
  extra: {
    ...config.extra,
    storybookEnabled: process.env.STORYBOOK_ENABLED === 'true',
  },
});
```

### Step 3: Expo Router Entry Point

With Expo Router, the root entry point is `app/_layout.tsx`, not `index.tsx` or `App.tsx`. Intercept the routing logic here.

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router'; 
import Constants from 'expo-constants';
import StorybookUIRoot from '../.storybook'; // Adjust path if needed

const STORYBOOK_ENABLED = Constants.expoConfig?.extra?.storybookEnabled;

export default function RootLayout() {
  if (STORYBOOK_ENABLED) {
    return <StorybookUIRoot />;
  }

  return <Stack />; 
}
```

### Step 4: Addons & Native Dependencies (Dev Build Only)

If the project requires on-device controls, install the specific native dependencies using Expo to prevent Gradle/CocoaPods build failures (like the `org.asyncstorage.shared_storage` crash).

```bash
# Safely install native dependencies for UI controls and storage
npx expo install @react-native-community/slider @react-native-community/datetimepicker @react-native-async-storage/async-storage

# Rebuild the app binary to inject the new native code
npx expo run:android
# or npx expo run:ios
```

### Step 5: NPM Scripts

Provide reliable scripts that utilize `cross-env` for cross-platform compatibility.

```json
{
  "scripts": {
    "storybook": "cross-env STORYBOOK_ENABLED='true' expo start",
    "storybook:clear": "cross-env STORYBOOK_ENABLED='true' expo start -c",
    "storybook:generate": "sb-rn-get-stories"
  }
}
```

*(Note: If the user is operating directly in a shell that doesn't support `VAR=true command` syntax, like Fish shell, instruct them to use `env STORYBOOK_ENABLED=true npx expo start -c` directly in the terminal).*

### Step 6: The Smoke Test

Create `components/Smoke.stories.tsx` to verify the setup.

```tsx
import React from 'react';
import { View, Text } from 'react-native';

export default { title: 'Health/SmokeTest' };

export const Basic = () => (
  <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
    <Text style={{ fontSize: 20 }}>Storybook is healthy! 🚀</Text>
  </View>
);
```

### Troubleshooting Checklist for AI

* **"Module not found: .../preview"** -> The addon is in `main.ts` but not installed. Install it, run `storybook:generate`, and start with `-c`.
* **"Missing required default export in _layout.tsx"** -> This is often a ghost error masking a native crash. Check if a native UI element (like `RNCDatePicker`) was requested but the app wasn't rebuilt.
* **Gradle Build Failure on AsyncStorage** -> The user has a bleeding-edge version. `npm uninstall @react-native-async-storage/async-storage`, then `npx expo install` it, clean the android build folder, and recompile.
