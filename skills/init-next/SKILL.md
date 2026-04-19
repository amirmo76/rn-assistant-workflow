---
name: init-next
description: >
  Use when initializing a Next.js project end-to-end for UI work: git, Vitest + React Testing Library, Storybook, Playwright against Storybook, shadcn, and project conventions. Triggers: /init-next, "init next", "setup next project", "initialize nextjs", "setup nextjs".
---

# Init Next

Sets up a Next.js project end-to-end. Run once before starting UI work. All checks must pass before returning.

---

## Process

### 1 — Detect or create the project

Look for `package.json` in the current directory.

- **Found and contains `next`** → project exists, continue to step 2.
- **Found but no `next`** → ask via `vscode/askQuestions` whether to add Next.js to the existing project or abort.
- **Not found** → scaffold a new project:

  ```bash
  npx create-next-app@latest . \
    --typescript \
    --tailwind \
    --eslint \
    --app \
    --import-alias "@/*"
  ```

  Accept all defaults. When asked about Turbopack, say **no** — Storybook's Next.js framework preset expects the standard builder.

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

### 3 — Copilot instructions

Establish project conventions before any tooling is added so subsequent steps can follow them.

1. Create `.github/` if it does not exist.

2. Create `.github/copilot-instructions.md` only if it does not already exist:

   ```md
   # Copilot Instructions — Next.js Project

   ## Project conventions

   ### Structure

   - shadcn components go under `components/ui/`.
   - Domain-specific components: `components/`.
   - Stories: `stories/<Name>.stories.tsx`.
   - Tests: `__tests__/<Name>.test.tsx`.

   ### Implementation guidelines

   - Prefer the simplest implementation that solves the requirement correctly.
   - Reuse existing patterns, helpers, and tokens before introducing new abstractions.
   - Preserve accessibility, performance, and maintainability over cleverness.
   - Use `class-variance-authority` for complex Tailwind class combinations and conditional variants.
   - Use the `cn` utility (from `@/lib/utils`) for Tailwind class combinations.

   ### Tooling

   - Test runner: Vitest + React Testing Library.
   - Stories: Storybook (`@storybook/nextjs`).
   - E2E / visual: Playwright against Storybook.
   - Styling: Tailwind CSS (v4 if installed, otherwise v3) + `class-variance-authority` + `cn`.
   ```

---

### 4 — Testing (Vitest + React Testing Library)

Read `~/.copilot/skills/web-testing-setup/SKILL.md` and follow it exactly.

Run `npm test` — must pass before continuing.

---

### 5 — Storybook

Read `~/.copilot/skills/web-storybook-setup/SKILL.md` and follow it exactly. The CLI auto-detects Next.js and installs `@storybook/nextjs`.

Run the build-storybook script — must succeed before continuing.

---

### 6 — Playwright (against Storybook)

1. Install:

   ```bash
   npm install --save-dev @playwright/test
   npx playwright install --with-deps chromium
   ```

2. Create `playwright.config.ts` at the project root:

   ```ts
   import { defineConfig, devices } from "@playwright/test";

   export default defineConfig({
     testDir: "./e2e",
     use: { baseURL: "http://localhost:6006" },
     projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
     webServer: {
       command: "npm run storybook",
       url: "http://localhost:6006",
       reuseExistingServer: !process.env.CI,
       timeout: 120_000,
     },
   });
   ```

3. Add a script to `package.json`:

   ```json
   { "scripts": { "e2e": "playwright test" } }
   ```

4. Create a smoke end-to-end test at `e2e/smoke.spec.ts`:

   ```ts
   import { test, expect } from "@playwright/test";

   test("storybook smoke story loads", async ({ page }) => {
     await page.goto("/?path=/story/smoke-smokecomponent--default");
     await expect(page.getByTestId("smoke")).toBeVisible();
   });
   ```

5. Run `npm run e2e` — must pass before continuing.

---

### 7 — shadcn

Read `~/.copilot/skills/shadcn/SKILL.md` for full reference.

Initialise:

```bash
npx shadcn@latest init
```

When prompted, choose the **Default** style and a base color (Slate is a good default, but follow user preference). Accept remaining defaults. The init writes `components.json`, adds the `cn` utility at `src/lib/utils.ts`, and installs `class-variance-authority`, `clsx`, and `tailwind-merge`.

---

### 9 — Typecheck and lint

`create-next-app` already adds `lint`. Ensure `typecheck` exists:

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

### 10 — Final verification

Run the full check suite in order:

1. `npm run typecheck`
2. `npm run lint`
3. `npm test`
4. The build-storybook script
5. `npm run e2e`

---

## Return summary

Report the following when done:

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
