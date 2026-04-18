# Spec Reference

> Used by **UI Assistant** to write `specs/doing/[objective-name]/spec.md`.

The spec is the working memory for one objective. It is created in Step 1, updated throughout implementation, and archived to `specs/done/` when complete. The `## State` section is the live handoff record — any agent or user can read it to know exactly where work stands and what comes next.

---

## Format

```markdown
# [Objective Name]

**Stage:** doing
**Started:** YYYY-MM-DD

## State

- **Current Step:** Step 2 — Implement Loop
- **Last Action:** Spec created and approved
- **Next:** Implement Button
- **Remaining this step:** Button, Card, CardList
- **Mode:** strict

## Objective

One short paragraph describing the UI outcome.

## Project

- **Platform:** web | react-native
- **Stack:** next | vite | cra | remix | gatsby | astro | react | expo | react-native-cli
- **Package manager:** npm | yarn | pnpm | bun
- **TypeScript:** true | false

## Design Inputs

- Figma: [url or "none"]
- Visuals: [relative path or "none"]
- Tree: [path to tree.yaml or "none"]

## Components

Ordered primitive → composite. Only `new` and `update` components are implemented; `unchanged` are listed for completeness but skipped.

- **Classification:** `new` | `update` | `unchanged`
- **Status:** `pending` | `implementing` | `done` (always `done` for `unchanged`)

| Order | Component   | Source        | Classification | Status        |
|-------|-------------|---------------|----------------|---------------|
| 1     | Button      | shadcn/button | new            | done          |
| 2     | Card        | none          | update         | implementing  |
| 3     | CardList    | none          | new            | pending       |
| —     | Icon        | none          | unchanged      | done          |

## Edge Cases

- [Edge case derived from context output, or "None."]

## Acceptance Criteria

- [Observable fact that defines success]

## Implementation Notes

Notes added during implementation. One section per component as needed.

### [ComponentName]
- [Decision or note]

## Open Questions

- None.
```

---

## Rules

- Keep the `Stage` field accurate: `doing` while active, `done` after archive.
- **Update `## State` after every action and at every step transition.** It is the primary handoff record.
- `Current Step` — the active workflow step name and number (e.g. `Step 2 — Implement Loop`).
- `Last Action` — one-line summary of the last completed action (e.g. `Button — done`, `Spec approved`).
- `Next` — the immediate next action (e.g. `Implement Card`, `Archive spec`).
- `Remaining this step` — comma-separated list of what is left in the current step. Write `none` when the step is finished.
- `Mode` — `strict` or `loose`, set once in Step 1b and never changed.
- On resume (Step 0), an agent reads `## State` first to determine exactly where to pick up.
- Update component `Status` at every transition (`pending` → `implementing` → `done`).
- `Classification` is set once in Step 1 and does not change. `unchanged` components are not implemented and keep `Status: done` from the start.
- Do not remove components from the table. Status is the record.
- Implementation notes are additive. Add; never rewrite history.
- Acceptance criteria must be observable facts, not implementation details.
- Open questions must be resolved before implementation of the affected component.
