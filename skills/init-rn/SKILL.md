---
name: init-rn
description: >
  Use when initializing an Expo React Native project end-to-end for UI work:
  git, Jest + React Native Testing Library, on-device Storybook, and project
  conventions. Triggers: /init-rn, "init rn", "init react native", "setup expo",
  "setup react native project".
---

# Init RN

Sets up an Expo React Native project end-to-end. Run once before starting UI work.
All checks must pass before returning.

> **Visual check note:** React Native has no web-based Storybook to drive with
> Playwright. The UI Assistant workflow's visual check step is not applicable
> to RN projects — the worker reports "visual check: not applicable on RN" and
> the user performs manual verification in the on-device Storybook.

---

## Process

### 1 — Detect or create the project

Look for `package.json` in the current directory.

- **Found and contains `expo` in dependencies** → project exists, continue to step 2.
- **Found but no `expo`** → ask via `vscode/askQuestions` whether to add Expo to the
  existing project or abort.
- **Not found** → scaffold a new project with the default Expo template:

  ```bash
  npx create-expo-app@latest . --template default
  ```

  Accept all defaults.

---

### 2 — Git

Check for a `.git` directory.

- **Exists** → skip.
- **Missing** → run:

  ```bash
  git init
  git add -A
  git commit -m "chore: initial commit"
  ```

---

### 3 — Testing (Jest + React Native Testing Library)

Read `~/.copilot/skills/rn-testing-setup/SKILL.md` and follow it exactly.

Run `npm test` — must pass before continuing.

---

### 4 — Storybook (on-device)

Read `~/.copilot/skills/rn-storybook-setup/SKILL.md` and follow it exactly.

Run `npm run storybook:generate` — must succeed before continuing. Do not start the
Metro server from this skill; the developer launches it interactively.

---

### 5 — Copilot instructions

1. Create `.github/` if it does not exist.

2. Create `.github/copilot-instructions.md` only if it does not already exist:

   ```md
   # Copilot Instructions — Expo React Native Project

   ## Project conventions

   ### Structure
   - Domain-specific components: `components/`.
   - Shared primitive components: `components/ui/`.
   - Stories live next to the component: `components/<Name>/<Name>.stories.tsx`.
   - Tests live next to the component: `components/<Name>/<Name>.test.tsx` or
     `__tests__/<Name>-test.tsx` (jest-expo recognises both `.test.*` and `-test.*`).

   ### Implementation guidelines
   - Prefer the simplest implementation that solves the requirement correctly.
   - Reuse existing patterns, helpers, and tokens before introducing new abstractions.
   - Preserve accessibility, performance, and maintainability over cleverness.

   ### UI primitives
   - Use Expo-compatible libraries only. Do not assume DOM APIs.
   - For styling, prefer the project's existing approach (StyleSheet, Tamagui,
     NativeWind, etc.) — do not introduce a parallel system.

   ### Tooling
   - Test runner: Jest + `@testing-library/react-native` (via `jest-expo` preset).
   - Stories: on-device Storybook, gated by `STORYBOOK_ENABLED=true`.
   - Visual verification: manual on-device (no Playwright).
   ```

---

### 6 — Typecheck and lint

If the project uses TypeScript, ensure `package.json` has:

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit"
  }
}
```

Run `npm run typecheck` and fix any errors.

If the project has ESLint configured (`create-expo-app` adds it by default),
run `npm run lint` and fix any errors.

---

### 7 — Final verification

Run in order:

1. `npm run typecheck` (if TypeScript)
2. `npm run lint` (if configured)
3. `npm test`
4. `npm run storybook:generate`
