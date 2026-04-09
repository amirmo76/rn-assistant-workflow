# Objective Spec Reference
> Used by **RN Component Spec Writer** at Step 0 (objective mode) and by **RN Planner** at Step 0.
> Defines the required structure and rules for `specs/[queue|doing|done]/[objective-name]/spec.md`.

Reference for `specs/[queue|doing|done]/[objective-name]/spec.md`.

## Required Sections

### 1. Header

```markdown
# Objective Spec: [Objective Name]

**Stage:** queue | doing | done
**Owner component:** [root component or screen]
```

### 2. Objective

One short paragraph describing the UI outcome.

### 3. Inputs

Relevant visuals, files, Figma URLs, or existing code references.

### 4. Approved Architecture

Final architecture from `RN Architect`.

```text
Root: [ComponentName]

Levels:
- ComponentName: page
- ChildA: organism

Graph:
ComponentName -> ChildA, ChildB
ChildA -> LeafA, LeafB
ChildB
LeafA
LeafB
```

### 5. Scope

- **In scope**
- **Out of scope**

### 6. Affected Component Specs

| Component | Spec path | Action | Notes |
|-----------|-----------|--------|-------|

`Action` is `create | update | confirm-no-change`.

### 7. Required Changes

What must be true in the final UI. Group by meaningful work area, not by implementation file.

### 8. Acceptance Criteria

Observable facts that define success for the objective.

### 9. Open Questions

Use `- None.` when there are no open questions.

## Rules

- Finalize the architecture before finalizing the rest of the objective spec.
- Keep the objective spec focused on the objective. Full component contracts belong in component specs.
- The objective spec must be clear enough to plan and execute without follow-up questions.
