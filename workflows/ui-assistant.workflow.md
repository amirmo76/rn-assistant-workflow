# UI Assistant Workflow

One UI objective moves through these steps at a time. Build components in isolation using Storybook. The code is the permanent state; the spec is the working memory for this objective.

## Spec Model

One spec per objective. It tracks where we are and what we're doing. When done it is archived.

- **Path:** `specs/doing/[objective-name]/spec.md`
- **Stages:** `queue → doing → done`
- **Structure:** see `references/spec.md`

Specs live in `specs/doing/` while active, move to `specs/done/` when archived.

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
   Outputs: direct dependencies. Use to determine primitive → composite ordering.

Order components bottom-up by dependency: primitives (no custom component dependencies) first, composites after.

Write `specs/doing/[objective-name]/spec.md` using `~/.copilot/references/spec.md` as format. The spec must contain:
- The objective
- All design inputs (Figma URLs, image paths, tree.yaml path)
- The ordered component list with source and status (`pending`)
- Edge cases derived from context output
- Acceptance criteria

Present spec to user via `vscode/askQuestions` and loop until approved.

**Exit criteria:** spec approved and saved, component order determined.

---

## Step 2 — Implement Loop

Work through components one at a time in the order recorded in the spec.

### Per Component

**2a — Mark In Progress**

Update spec: set component status to `implementing`.

**2b — Build**

Spawn `UI Worker` with:
- component name
- spec path (`specs/doing/[objective-name]/spec.md`)
- design inputs from spec (Figma URLs, image paths)
- shadcn source if component is `shadcn/<id>`
- context from `--context` for this component
- project facts (platform, package manager, stack)

Worker delivers: implementation + comprehensive tests + Storybook story.

**2c — Auto-Verify**

Worker runs and reports:
1. Tests — all pass
2. Typecheck — clean
3. Lint — clean
4. Build — clean
5. Visual check — Playwright screenshot of the story vs Figma design screenshot. Reports match or diff.

If tests/typecheck/lint/build fail, worker fixes and re-runs before reporting. Visual diff if obvious is fixed by the agent if not reported for user judgment.

**2d — User Gate**

Present verification results via `vscode/askQuestions`:
- Automated checks summary
- Visual comparison result
- Prompt user to verify in Storybook, then approve or give feedback

On approval: run checkers to make sure user changes did not break, if so loop. if not update spec, set component status to `done`. Move to next component.

**Repeat for every component in the spec order.**

**Exit criteria:** all components are `done` in the spec.

---

## Step 3 — Archive

Move spec from `specs/doing/[objective-name]/` to `specs/done/[objective-name]/`.
Update spec stage field to `done`.

Announce completion to user.

**Exit criteria:** spec archived under `specs/done/`.

---

## Rules

- Spec is the single source of truth for the work status. Keep it updated at every status change.
- Component order (primitive → composite) is set in Step 1 and never changed.
- Never gate with plain text — always use `vscode/askQuestions`.
- Never end the session to ask for feedback. Stay in chat and ask inline.
- Every component must have tests and a Storybook story before marked done.
- All automated checks must pass before presenting to user.
- Visual check is mandatory — always compare story screenshot to design.
- One component at a time. Never start next until current is approved.
