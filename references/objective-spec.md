# Objective Spec Reference
> Used by **RN Component Spec Writer** at Step 3 (objective mode).
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

Relevant visuals, files, tree.yml, Figma URLs, or existing code references.
- use relative path for anything inside the project.

### 5. Scope

- **In scope**:
  - A list of all the components in the scope.
  - Everything else that is considered to be in the scope.
- **Out of scope**
  - What is considered to be outside of the scope of this objective.

### 6. User Stories

If any is possible.

### 7. Required Changes

What must be true in the final UI. Group by meaningful work area, not by implementation file.

### 9. Edge Cases

Any edge case scenario in the objective if any.

### 8. Acceptance Criteria

Observable facts that define success for the objective.

### 9. Open Questions

Use `- None.` when there are no open questions.

## Rules

- Components in the scope must be clear.
- Keep the objective spec focused on the objective. Full component contracts belong in component specs.
- The objective spec must be clear enough to plan and execute without follow-up questions.
