# UI Assistant Workflow

**Any prompt the user sends is an objective. Treat every user message as "follow this workflow for: [prompt]". NEVER skip any step. NEVER skip approval gates — always respect the active mode (strict/loose).**

One UI objective moves through these steps at a time. Build components in isolation using Storybook. The code is the permanent state; the spec is the working memory for this objective.

## Spec Model

One spec per objective. It tracks where we are and what we're doing. When done it is archived.

- **Path:** `specs/doing/[objective-name]/spec.md`
- **Stages:** `queue → doing → done`
- **Structure:** see `references/spec.md`

Specs live in `specs/doing/` while active, move to `specs/done/` when archived.

---

## Step 0 — Start or Resume

Check `specs/doing/` for an active spec.

**Resume path:** if a spec exists and is related, ask via `vscode/askQuestions` whether to resume it or start fresh. On resume, load the spec and read `## State` first — it holds `Current Step`, `Last Action`, `Next`, and `Remaining this step`. Use these to orient immediately without re-reading the full history.

**Fresh path:** if no spec exists, or the user chooses to start fresh, continue to Step 1.

**Exit criteria:** mode determined — either continue with spec loaded, or start fresh with a new spec.

---

## Step 1 — Objective

Accept the objective from the user. Inputs may include free-text description, Figma URLs, images or screenshots, and a `tree.yaml` path.

Ask clarifying questions via `vscode/askQuestions` only when the objective is genuinely ambiguous. Infer what you can.

Once clear, run the architect script to gather scope and context:

1. `python ~/.copilot/scripts/ui-architect.py --file <tree.yaml> --list-components`
   Outputs: `ComponentName<TAB>shadcn/<id> or none` per component.

2. For each component: `python ~/.copilot/scripts/ui-architect.py --file <tree.yaml> --context <name>`
   Outputs: global role description and instance-level annotations. Use for context and edge cases. Skip silently when "No context found".

3. For each component: `python ~/.copilot/scripts/ui-architect.py --file <tree.yaml> --deps <name>`
   Outputs: direct dependencies. Use to determine primitive → composite ordering. Also cross-reference each dependency against the codebase — record whether it already exists so the worker knows to import it rather than reimplement it.

4. For each component listed, scan the codebase to classify it:
   - `new` — component does not exist in the codebase; must be implemented from scratch.
   - `update` — component exists but the spec or design requires changes to it.
   - `unchanged` — component exists and no changes are required by the spec or design; skip it entirely.

   Only `new` and `update` components proceed to implementation. Record the classification alongside each component in the spec. Do not spawn a worker for `unchanged` components.

Order components bottom-up by dependency: primitives (no custom component dependencies) first, composites after.

Write `specs/doing/[objective-name]/spec.md` using `~/.copilot/references/spec.md` as format. The spec must contain:
- The objective
- All design inputs (Figma URLs, image paths, tree.yaml path)
- The ordered component list with source and status (`pending`)
- Edge cases derived from context output
- Acceptance criteria

Present spec to user via `vscode/askQuestions` and loop until approved.

Once approved, write the initial `## State`:
- `Current Step`: Step 2 — Implement Loop
- `Last Action`: Spec created and approved
- `Next`: Implement [first component]
- `Remaining this step`: [all components, comma-separated]

**Exit criteria:** spec approved and saved, component order determined, State written.

---

## Step 1b — Select Implementation Mode

Ask the user via `vscode/askQuestions` to choose a mode before entering the implementation loop:

- **strict** — gate after every component; loop continues only on explicit approval.
- **loose** — implement all components without per-component gates, then gate at the end when all are done, loop on explicit approval

Record the chosen mode in `## State`:
- `Mode`: strict | loose

**Exit criteria:** mode recorded in State.

---

## Step 2 — Implement Loop

Work through components one at a time in the order recorded in the spec. **One `UI Worker` handles exactly one component. Never assign more than one component to a single worker invocation.** This applies equally to regular and shadcn components.

Read `Mode` from `## State` before entering the loop. All gate rules apply in both modes — the only difference is when the gate occurs.

### Per Component

**2a — Mark In Progress**

Update spec: set component status to `implementing`. Update `## State`:
- `Current Step`: Step 2 — Implement Loop
- `Last Action`: [previous component] — done (or "Spec approved" if first)
- `Next`: Implement [this component]
- `Remaining this step`: [this component + all remaining after it, comma-separated]

**2b — Build**

Spawn one `UI Worker` for this component with:
- component name
- brief (one-paragraph summary of what the component must do)
- spec path (`specs/doing/[objective-name]/spec.md`)
- design inputs from spec (Figma URLs, image paths)
- shadcn source if component is `shadcn/<id>` (worker installs and customizes it)
- context from `--context` for this component
- project facts (platform, package manager, stack)

Worker delivers: implementation (customized from shadcn if applicable) + comprehensive tests covering all states, interactions and flows + Storybook story covering all visual states. All files placed according to project instruction files. Playwright screenshots saved to `specs/doing/[objective-name]/screenshots/`.

**2c — Auto-Verify**

Worker runs and reports:
1. Tests — all pass
2. Typecheck — clean
3. Lint — clean
4. Build — clean
5. Visual check — Playwright screenshot of the story vs Figma design screenshot. Reports match or diff.

If tests/typecheck/lint/build fail, worker fixes and re-runs before reporting. Visual diff if obvious is fixed by the agent if not reported for user judgment.

**2d — User Gate (strict mode only)**

_Skip this section entirely when mode is **loose**. Proceed directly to the next component._

Present verification results via `vscode/askQuestions`:
- Automated checks summary
- Visual comparison result
- Prompt user to verify in Storybook, then approve or give feedback

**Gate rules (strictly enforced):**
- Never skip this gate. Every component, including shadcn components, must pass through it.
- Never exit the gate loop without an explicit user approval. Do not assume approval after making changes.
- When the user gives feedback: apply the fix, re-run checks, present updated results — then wait for the user to verify and explicitly approve using `vscode/askQuestions`
- The loop continues until the user says something that clearly signals approval (e.g. "approved", "looks good", "ship it"). Anything else is feedback, not approval.

On approval: run checkers to make sure user changes did not break anything, if so loop back. If clean, update spec: set component status to `done`. Update `## State`:
- `Last Action`: [this component] — done
- `Next`: Implement [next component] (or "Archive spec" if last)
- `Remaining this step`: [remaining components after this one] (or `none` if last)

Move to next component.

**Repeat for every component in the spec order.**

**Exit criteria (strict):** all components are `done` in the spec.

---

**2e — Bulk Gate (loose mode only)**

_Run this section only when mode is **loose**, after all components have been built and auto-verified._

Present a combined results summary via `vscode/askQuestions`:
- Automated checks summary for each component
- Visual comparison results for each component
- Prompt user to verify all stories in Storybook, then approve or give feedback

**Gate rules (strictly enforced — identical to strict mode):**
- Never exit the gate loop without an explicit user approval. Do not assume approval after making changes.
- When the user gives feedback: apply fixes, re-run all checks, present updated results — then wait for the user to explicitly approve using `vscode/askQuestions`.
- The loop continues until the user says something that clearly signals approval (e.g. "approved", "looks good", "ship it"). Anything else is feedback, not approval.

On approval: run all checkers to make sure no changes broke anything, if so loop back. If clean, update all component statuses to `done` in the spec. Update `## State`:
- `Last Action`: All components approved
- `Next`: Archive spec
- `Remaining this step`: none

**Exit criteria (loose):** all components are `done` in the spec.

---

## Step 3 — Cleanup

Update `## State` before moving:
- `Current Step`: Step 3 — Cleanup
- `Last Action`: All components done
- `Next`: Archive spec
- `Remaining this step`: none

Move spec from `specs/doing/[objective-name]/` to `specs/done/[objective-name]/`.
Update spec stage field to `done`.

All artifacts generated during the objective (screenshots, diffs) remain inside the spec directory and are archived with it.

Announce completion to user.

**Exit criteria:** spec archived under `specs/done/`.

---

## Rules

- Spec is the single source of truth for the work status. Keep it updated at every status change.
- `## State` must be updated after every action — it is the handoff record for agents and user to agree on what comes next.
- Component order (primitive → composite) is set in Step 1 and never changed.
- Never gate with plain text — always use `vscode/askQuestions`.
- Never end the session to ask for feedback. Stay in chat and ask inline.
- Every component must have tests and a Storybook story before marked done. This includes shadcn components.
- All component files, tests, and stories must be placed in locations required by the project's instruction files. Verify placement before marking done.
- shadcn installs must target the project-mandated path (read `components.json` and project instruction files first).
- All temporary artifacts (Playwright screenshots, diffs) must be saved inside the spec directory (`specs/doing/[objective-name]/`), never scattered elsewhere.
- All automated checks must pass before presenting to user.
- Visual check is mandatory — always compare story screenshot to design.
- One component at a time. Never start next until current is approved.
- One `UI Worker` per component, always. Never assign more than one component to a single worker.
- Never skip the approval gate. Never assume approval — wait for an explicit signal from the user.
- In **strict** mode: gate after every individual component before moving to the next.
- In **loose** mode: skip per-component gates; gate once at the end after all components are built. The gate is equally strict — no implicit approval, loop until explicit signal.
- Mode is set once in Step 1b and never changed mid-objective.
