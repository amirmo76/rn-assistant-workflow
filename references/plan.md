# Objective Plan Reference

> Used by **RN Planner** at Step 0 and by **RN Tasker** at Step 0.
> Defines the required structure and rules for `specs/doing/[objective-name]/plan.md`.

Reference for `specs/doing/[objective-name]/plan.md`.

## Required Sections

### 1. Header

```markdown
# Plan: [Objective Name]

**Spec:** specs/doing/[objective-name]/spec.md
**Status:** draft | ready | in-progress | done
```

### 2. Delivery Order

Short explanation of the bottom-to-top dependency order.

### 3. Phases

Use numbered phases in execution order.

```markdown
### Phase [N] — [Short Name]

**Depends on:** — | Phase [X], Phase [Y]
**Execution:** sequential | parallel

**Scope**
- What this phase covers.

**Work**
- Meaningful execution units only.

**Coverage**
- Tests to add or update.
- Stories to add or update.

**Exit Criteria**
- Verifiable conditions for phase completion.
```

### 4. Parallel Notes

Call out only justified parallel work and the dependency that makes it safe.

### 5. Risks / Assumptions

Use `- None.` when there are none.

## Rules

- Plan the objective as one delivery path, not as disconnected per-component micro-plans.
- Follow dependency order from lower-level prerequisites upward when it matters.
- Read the objective spec and every in-scope component changelog before planning.
- Mark work as parallel only when the dependency boundary is clear.
- Batch unrelated or dependency-independent component work together when they sit at the same layer.
- Any component change includes tests and story coverage.
