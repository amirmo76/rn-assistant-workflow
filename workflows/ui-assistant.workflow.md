# UI Assistant Workflow

**Every user message is an objective. Treat each one as "follow this workflow for: [prompt]". Never skip a step. Never skip an approval gate — the active mode (strict/loose) only changes *when* the gate happens, never whether it happens.**

One UI objective moves through the steps below. Components are built in isolation using Storybook (on web: driven by Playwright; on React Native: verified manually by the user on-device). The code is the permanent state; the spec is the working memory for this objective.

## Spec Model

One spec per objective. It records where we are and what we're doing, then is archived when done.

- **Path:** `specs/doing/[objective-name]/spec.md`
- **Stages:** `queue → doing → done`
- **Structure:** see `~/.copilot/references/spec.md`

Specs live in `specs/doing/` while active and move to `specs/done/` on archive.

---

## Step 0 — Start or Resume

Check `specs/doing/` for an active spec.

- **Resume path:** if a spec exists and is related to the new prompt, ask via `vscode/askQuestions` whether to resume it or start fresh. On resume, load the spec and read `## State` first — it holds `Current Step`, `Last Action`, `Next`, `Remaining this step`, and `Mode`. Use these to orient immediately without re-reading the full history.
- **Fresh path:** if no spec exists, or the user chooses to start fresh, continue to Step 1.

**Exit criteria:** either a spec is loaded and the workflow picks up from its State, or we start fresh with no spec loaded.

---

## Step 1 — Objective & Scope

Accept the objective. Inputs may include free-text description, Figma URLs, images/screenshots, and a `tree.yaml` path. Ask clarifying questions via `vscode/askQuestions` only when genuinely ambiguous — infer what you can.

Gather facts, in order:

1. **Project facts.** Run `python ~/.copilot/scripts/detect-project.py --project-dir .`. Record `platform`, `package_manager`, `stack`, `typescript` from the JSON output. These are handed to every worker.

2. **Lint the tree.** If a `tree.yaml` was provided, run `python ~/.copilot/scripts/ui-lint.py --file <tree.yaml>`. If it reports errors, ask the user to fix them before continuing — do not try to parse a malformed tree.

3. **List components.** `python ~/.copilot/scripts/ui-architect.py --file <tree.yaml> --list-components`
   Output: `ComponentName<TAB>shadcn/<id> or none` per component.

4. **Gather context.** For each component: `python ~/.copilot/scripts/ui-architect.py --file <tree.yaml> --context <name>`
   Output: global role description and instance-level annotations. Use for edge cases. Skip silently when "No context found".

5. **Resolve dependencies.** For each component: `python ~/.copilot/scripts/ui-architect.py --file <tree.yaml> --deps <name>`
   Output: direct dependencies. Use to determine primitive → composite ordering. Cross-reference each dependency against the codebase so the worker knows to import it rather than reimplement it.

6. **Classify each component** against the codebase:
   - `new` — does not exist; implement from scratch.
   - `update` — exists but the spec or design requires changes.
   - `unchanged` — exists and no changes are required; **skip**, do not spawn a worker.

   Only `new` and `update` components proceed to implementation.

Order the implementation list: **shadcn-sourced components always go first** — they have no dependencies on custom components by definition, making them the most primitive. Within the shadcn group, preserve the order they were listed. After the shadcn group, order remaining components bottom-up by dependency: primitives first, composites after.

Write `specs/doing/[objective-name]/spec.md` using `~/.copilot/references/spec.md` as the format. The spec must contain:
- The objective
- All design inputs (Figma URLs, image paths, `tree.yaml` path)
- Project facts from step 1
- The ordered component list with `Source`, `Classification`, and `Status: pending`
- Edge cases derived from context output
- Acceptance criteria

Present the spec to the user via `vscode/askQuestions` and loop until approved.

Once approved, write the initial `## State`:
- `Current Step`: Step 2 — Implement Loop
- `Last Action`: Spec created and approved
- `Next`: Implement [first `new`/`update` component]
- `Remaining this step`: [all `new`/`update` components, comma-separated]

**Exit criteria:** spec approved and saved, component order determined, State written.

---

## Step 1b — Select Implementation Mode

Ask the user via `vscode/askQuestions`:

- **strict** — gate after every component; loop continues only on explicit approval.
- **loose** — implement all components without per-component gates, then gate once at the end.

Record in `## State` → `Mode`: `strict | loose`.

**Exit criteria:** mode recorded in State.

---

## Step 2 — Implement Loop

Work through components one at a time in the spec order. **One `UI Worker` handles exactly one component. Never assign more than one component to a single worker invocation.** This applies equally to regular and shadcn components.

### 2-pre — Loose mode: parallel shadcn batch (loose mode only)

_Skip this section entirely when mode is **strict**._

Before starting the per-component loop, take advantage of the fact that shadcn-sourced components are already at the front of the spec order and share no dependencies:

1. Mark all shadcn-sourced components `Status: implementing` in the spec simultaneously.
2. Spawn exactly one `UI Worker` per shadcn component **in parallel** — all workers run at the same time. Each worker receives the same brief inputs as described in 2b.
3. Wait for all workers to finish and collect their reports.
4. Continue to the per-component loop for the remaining (non-shadcn) components. Do not re-run 2-pre for those.

**Exit criteria:** all shadcn-sourced components built and reported; remaining component list contains only non-shadcn entries.

---

### Per Component

**2a — Mark In Progress**

Update spec: set this component's `Status` to `implementing`. Update `## State`:
- `Current Step`: Step 2 — Implement Loop
- `Last Action`: [previous component] — done (or "Spec approved" on the first)
- `Next`: Implement [this component]
- `Remaining this step`: [this component + all remaining after it]

**2b — Build**

Spawn one `UI Worker` with:
- component name
- brief (one-paragraph summary of what the component must do)
- spec path (`specs/doing/[objective-name]/spec.md`)
- design inputs from spec (Figma URLs, image paths)
- shadcn source if the spec lists `shadcn/<id>` for this component
- context from `--context` for this component
- dependency list from `--deps` and their codebase status (exists / missing)
- project facts (`platform`, `package_manager`, `stack`, `typescript`)

Worker delivers: implementation (customized from shadcn if applicable) + tests for all states/interactions + Storybook story covering all visual states. Files placed according to project instruction files. Visual-check artifacts saved to `specs/doing/[objective-name]/screenshots/`.

**2c — Auto-Verify**

Worker runs and reports:
1. Tests — all pass
2. Typecheck — clean
3. Lint — clean
4. Build — clean
5. Visual check — **web**: Playwright screenshot of the story vs Figma design screenshot; report match or diff. **React Native**: report "not applicable on RN — user verifies on-device".

If tests/typecheck/lint/build fail, the worker fixes and re-runs before reporting. Obvious visual diffs the worker fixes itself; ambiguous ones are reported for user judgment.

**2d — Gate (strict mode only)**

_Skip this section entirely when mode is **loose**._

Present verification results via `vscode/askQuestions` — automated summary, visual result, and a prompt for the user to verify in Storybook (on web) or on-device (on RN) and approve or give feedback. Apply **[Gate rules](#gate-rules)**.

On approval: re-run automated checks to confirm any user-driven changes didn't break anything; if they did, loop back. If clean, update the spec: set this component's `Status` to `done`. Update `## State`:
- `Last Action`: [this component] — done
- `Next`: Implement [next component] (or "Archive spec" if last)
- `Remaining this step`: [remaining components] (or `none` if last)

Move to the next component.

**Repeat for every component in spec order.**

**Exit criteria (strict):** every `new`/`update` component has `Status: done`.

---

**2e — Bulk Gate (loose mode only)**

_Run this only after every `new`/`update` component has been built and auto-verified._

Present a combined summary via `vscode/askQuestions` — per-component automated results, per-component visual results, and a prompt for the user to verify all stories and approve or give feedback. Apply **[Gate rules](#gate-rules)**.

On approval: re-run all automated checks; if any broke, loop back. If clean, set every `new`/`update` component's `Status` to `done`. Update `## State`:
- `Last Action`: All components approved
- `Next`: Archive spec
- `Remaining this step`: none

**Exit criteria (loose):** every `new`/`update` component has `Status: done`.

---

### Gate Rules

Identical in strict and loose mode. The only difference is *when* the gate runs.

- Never skip the gate. Every `new`/`update` component, including shadcn-sourced ones, passes through it.
- Never exit the gate loop without an explicit user approval. Do not assume approval after making changes.
- When the user gives feedback: apply the fix, re-run checks, present updated results — then wait for the user to verify and explicitly approve via `vscode/askQuestions`.
- The loop continues until the user says something that clearly signals approval (e.g. "approved", "looks good", "ship it"). Anything else is feedback, not approval.

---

## Step 3 — Cleanup

Update `## State` before moving:
- `Current Step`: Step 3 — Cleanup
- `Last Action`: All components done
- `Next`: Archive spec
- `Remaining this step`: none

Move the spec directory from `specs/doing/[objective-name]/` to `specs/done/[objective-name]/`. Update the spec's `Stage` field to `done`.

All artifacts generated during the objective (screenshots, diffs) remain inside the spec directory and are archived with it.

Announce completion to the user.

**Exit criteria:** spec archived under `specs/done/`.

---

## Rules

- Spec is the single source of truth for work status. Keep it updated at every status change.
- `## State` is the primary handoff record — update it after every action and at every step transition.
- Component order (primitive → composite) is set in Step 1 and never changed.
- Mode is set once in Step 1b and never changed mid-objective.
- Never gate with plain text — always use `vscode/askQuestions`.
- Never end the session to ask for feedback. Stay in chat and ask inline.
- Every `new`/`update` component must have tests and a Storybook story before it is marked done, including shadcn components.
- All component files, tests, and stories must be placed in locations required by the project's instruction files. Verify placement before marking done.
- shadcn installs must target the project-mandated path (read `components.json` and project instruction files first).
- All temporary artifacts (screenshots, diffs) must be saved inside the spec directory — never scattered elsewhere.
- All automated checks must pass before presenting to the user.
- Visual check is mandatory on web; on React Native it is recorded as "not applicable on RN" and the user verifies on-device.
- One component at a time. One `UI Worker` per component, always.
