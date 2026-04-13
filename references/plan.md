# Objective Plan Reference

> Used by **UI Planner** and by **UI Tasker**.
> Defines the required structure and rules for `specs/doing/[objective-name]/plan.md`.

## Orchestration Architecture

- **Phase** = synchronization barrier. Phases execute strictly sequentially.
  Phase N must fully complete before Phase N+1 begins.
- **Component** = parallel worker task. Every component listed inside a Phase is
  spawned simultaneously. One component = one worker.

There is no other hierarchy. Do not introduce sub-levels.

## Required Sections

### 1. Header

```markdown
# Plan: [Objective Name]

**Spec:** specs/doing/[objective-name]/spec.md
**Status:** draft | ready | in-progress | done
```

### 2. Component Analysis

A table listing every in-scope component, its change type, and its direct in-scope
dependencies. Derived from the objective spec (scope) + each component's changelog.

```markdown
## Component Analysis

| Component   | Status  | Depends On (in scope)  |
|-------------|---------|------------------------|
| ButtonBase  | new     | —                      |
| Icon        | new     | —                      |
| IconButton  | new     | ButtonBase, Icon       |
| Toolbar     | updated | IconButton             |
```

- **Status**: `new` (created from scratch) or `updated` (existing component modified).
- **Depends On**: only list dependencies that are also in scope. External or unchanged
  dependencies do not affect phase ordering and must not appear here.
- This table is the sole source of truth for all phase ordering decisions.

### 3. Delivery Order

Two to four sentences explaining the layer sequence: which components are primitives
(no in-scope deps), which are compositions, and why the order matters.

### 4. Execution Map

The master orchestration view. The orchestrator reads this section alone to know
exactly which components to spawn in parallel per phase and the phase order.
No other section is needed to drive orchestration.

```markdown
## Execution Map
Phases run sequentially. Components within a Phase run in parallel.

Phase 1: Base Primitives
  - ButtonBase  (no in-scope deps)
  - Icon        (no in-scope deps)

Phase 2: Compositions
  - IconButton  (depends on Phase 1: ButtonBase, Icon)
  - TextLabel   (depends on Phase 1: Icon)

Phase 3: Complex Assemblies
  - Toolbar     (depends on Phase 2: IconButton, TextLabel)
```

Rules for building the Execution Map:
- Layer 0 components (zero in-scope deps) must all be in Phase 1.
- A component may only appear in Phase N if every component it depends on is in
  Phase N-1 or earlier.
- Every component listed in the same Phase is guaranteed safe to run in parallel.
- When the dependency relationship between two components is ambiguous, place the
  potentially-dependent component in the next Phase. Safety over speed.
- Keep phase count as small as possible while correctly expressing all real
  dependency boundaries. Do not manufacture phases where none are needed.

### 5. Phases

One block per phase, in execution order, matching the Execution Map exactly.

```markdown
### Phase [N] — [Short Name]

**Depends on:** — | Phase [X]

**Components**
- ComponentName — new | updated: [one-line summary of what changed, sourced from changelog]

**Work**
- Concrete implementation tasks. List per-component when tasks differ.

**Coverage**
- Tests to add or update.
- Stories to add or update.

**Exit Criteria**
- Verifiable conditions that confirm every component in this phase is complete.
```

### 6. Risks / Assumptions

Use `- None.` when there are none.

## Rules

- **Completeness**: every in-scope component must appear in the Component Analysis
  table and in exactly one Phase.
- **Map first**: the Execution Map must be fully correct and self-contained before
  writing any Phase detail block. If the map is wrong, the plan is wrong.
- **Architecture is fixed**: Phases are sequential barriers. Components inside a
  Phase are parallel workers. There are no other levels. Do not invent sub-phases
  or groupings.
- **Layer 0 in Phase 1**: all primitives (zero in-scope deps) must be in Phase 1.
- **No invented sequence**: components with no dependency on each other must not be
  placed in separate sequential Phases.
- **No unsafe parallel**: when dependency direction is ambiguous, put the component
  in the next Phase. Safety over speed.
- **Coverage mandatory**: every component change includes tests and story coverage.
- **Single delivery path**: one plan, not disconnected per-component micro-plans.
