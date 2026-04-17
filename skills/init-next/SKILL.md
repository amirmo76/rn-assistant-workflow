---
name: init-next
description: >
  Initialize a Next.js project with git, testing (Vitest + RTL), Storybook,
  Playwright, shadcn (Base UI variant), and project conventions.
  Trigger: /init-next, "init next", "setup next project", "initialize nextjs",
  "setup nextjs".
---

# Init Next

Sets up a Next.js project end-to-end. Run once before starting UI work.
All checks must pass before returning.

---

## Process

### 1 — Detect or create the project

Look for `package.json` in the current directory.

- **Found and contains `"next"` in dependencies** → project exists, continue to step 2.
- **Found but no `next`** → ask via `vscode/askQuestions` whether to add Next.js to the
  existing project or abort.
- **Not found** → scaffold a new project:

```bash
npx create-next-app@latest . \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --no-turbopack
```

Accept all defaults. Do not use `--turbopack` (Storybook requires the standard webpack/Vite builder).

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

### 3 — Testing (Vitest + React Testing Library)

Read `~/.copilot/skills/web-testing-setup/SKILL.md` and follow it exactly.

Key steps (summarised):

1. Install:
   ```bash
   npm install --save-dev vitest @vitest/coverage-v8 \
     @testing-library/react @testing-library/user-event @testing-library/jest-dom \
     jsdom @vitejs/plugin-react
   ```
2. Create `vitest.config.ts` at the project root:
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
3. Create `src/test/setup.ts`:
   ```ts
   import '@testing-library/jest-dom';
   ```
4. Add scripts to `package.json`:
   ```json
   {
     "scripts": {
       "test": "vitest run",
       "test:watch": "vitest",
       "test:coverage": "vitest run --coverage"
     }
   }
   ```
5. If no tests exist, create a smoke test at `src/test/smoke.test.ts`:
   ```ts
   import { describe, it, expect } from 'vitest';

   describe('smoke', () => {
     it('passes', () => {
       expect(true).toBe(true);
     });
   });
   ```
6. Run `npm test` — must pass before continuing.

---

### 4 — Storybook

Read `~/.copilot/skills/web-storybook-setup/SKILL.md` and follow it exactly.

Key steps (summarised):

1. Run the interactive initialiser:
   ```bash
   npx storybook@latest init
   ```
   Accept all defaults. The CLI auto-detects Next.js and installs `@storybook/nextjs`.

2. Ensure `package.json` has:
   ```json
   {
     "scripts": {
       "storybook": "storybook dev -p 6006",
       "build-storybook": "storybook build"
     }
   }
   ```

3. Create a smoke story at `src/components/smoke/smoke.stories.tsx`:
   ```tsx
   import type { Meta, StoryObj } from '@storybook/react';

   const SmokeComponent = () => <div data-testid="smoke">Smoke</div>;

   const meta: Meta<typeof SmokeComponent> = {
     title: 'Smoke/SmokeComponent',
     component: SmokeComponent,
   };
   export default meta;

   type Story = StoryObj<typeof SmokeComponent>;
   export const Default: Story = {};
   ```

4. Run `npm run build-storybook` — must succeed before continuing.

---

### 5 — Playwright

1. Install:
   ```bash
   npm install --save-dev @playwright/test
   npx playwright install --with-deps chromium
   ```

2. Create `playwright.config.ts` at the project root:
   ```ts
   import { defineConfig, devices } from '@playwright/test';

   export default defineConfig({
     testDir: './e2e',
     use: {
       baseURL: 'http://localhost:6006',
     },
     projects: [
       {
         name: 'chromium',
         use: { ...devices['Desktop Chrome'] },
       },
     ],
     webServer: {
       command: 'npm run storybook',
       url: 'http://localhost:6006',
       reuseExistingServer: !process.env.CI,
       timeout: 120_000,
     },
   });
   ```

3. Add a script to `package.json`:
   ```json
   {
     "scripts": {
       "e2e": "playwright test"
     }
   }
   ```

4. Create a smoke end-to-end test at `e2e/smoke.spec.ts`:
   ```ts
   import { test, expect } from '@playwright/test';

   test('storybook smoke story loads', async ({ page }) => {
     await page.goto('/?path=/story/smoke-smokecomponent--default');
     await expect(page.getByTestId('smoke')).toBeVisible();
   });
   ```

5. Run `npm run e2e` — must pass before continuing.

---

### 6 — shadcn (Base UI variant)

Use the Base UI headless primitives via the shadcn registry instead of Radix UI.

1. Initialise shadcn:
   ```bash
   npx shadcn@latest init
   ```
   When prompted for the style, choose **Default**. When asked about the base color,
   choose **Slate** (or user preference). Accept remaining defaults.

2. After init, open `components.json` and ensure the registry points to the Base UI
   variant. If the project uses Radix primitives after init, replace them by installing
   components from the `base-ui` registry source as needed during component work.

3. Install the `cn` utility if not already present (shadcn init does this automatically
   via `src/lib/utils.ts`):
   ```ts
   import { clsx, type ClassValue } from 'clsx';
   import { twMerge } from 'tailwind-merge';

   export function cn(...inputs: ClassValue[]) {
     return twMerge(clsx(inputs));
   }
   ```

---

### 7 — GitHub & Copilot instructions

1. Create `.github/` directory if it does not exist.

2. Create `.github/.copilot-instructions.md` only if it does not already exist:

```md
# Copilot Instructions — Next.js Project

## Project conventions

### structure
- shadcn components go under `src/components/ui`.
- Preferred layout:
  - `components/ui` for shared UI primitive components (e.g. `Button`, `Avatar`).
  - `components/` for domain-specific components
  - `stories/[component].stories.tsx` for stories.
  - `__tests__/[component].test.tsx` for tests.

### Implementation guidelines
- Prefer the simplest implementation that solves the requirement correctly.
- Reuse existing patterns, helpers, and tokens before introducing new abstractions.
- Preserve accessibility, performance, and maintainability over cleverness.
- Use `class-variance-authority` for complex Tailwind class combinations and conditional variants.
- Use the `cn` utility (from `@/lib/utils`) for Tailwind class combinations and conditional classes.

### UI primitives
- Use Base UI (`@base-ui/react`) as the headless primitive layer — not Radix UI.
- Install shadcn components from the Base UI registry variant.

### Tooling
- Test runner: Vitest + React Testing Library.
- Stories: Storybook (`@storybook/nextjs`).
- E2E: Playwright against Storybook.
- Styling: Tailwind CSS v4 + `class-variance-authority` + `cn`.
```

---

### 8 — Typecheck and lint

Ensure these scripts exist in `package.json` (Next.js scaffold adds them by default):

```json
{
  "scripts": {
    "lint": "next lint",
    "typecheck": "tsc --noEmit"
  }
}
```

Run both and fix any errors before returning.

---

### 9 — Final verification

Run the full check suite in order:

1. `npm run typecheck`
2. `npm run lint`
3. `npm test`
4. `npm run build-storybook`
5. `npm run e2e`

All must pass. Fix failures before reporting.

---

## Return summary

Report the following when done:

- Platform detected and project root
- Git status (initialised / already existed)
- Test runner: pass/fail
- Storybook build: pass/fail
- Playwright smoke: pass/fail
- shadcn: initialised / already present
- `.github/.copilot-instructions.md`: created / already existed
- Any blockers that required user input

---

## Rules

- Fix deterministic setup problems directly; don't ask for each one.
- Ask only when a genuine decision is required (e.g. conflicting existing config).
- Don't stop on first failure — fix and re-run.
- Never mix React Native tooling with web tooling.
- Do not return until all checks pass.
