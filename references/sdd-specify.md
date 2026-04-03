# SDD Specification Reference
> Used by the orchestrator during Step 2 and by the SDD Spec Writer.
> Defines the spec template format, quality rules, and brief format.

## Spec Template

The specification (`spec.md`) uses this exact structure:

### Header
```
# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`
**Created**: [DATE]
**Status**: Draft
**Input**: User description: "[original user input]"
```

### Section 1 — User Scenarios & Testing *(mandatory)*
Priority-ordered user stories with Given/When/Then acceptance scenarios.

### Section 2 — Requirements *(mandatory)*
Functional requirements as `FR-NNN` with MUST/SHOULD/MAY.

### Section 3 — Success Criteria *(mandatory)*
Measurable outcomes as `SC-NNN`.

### Section 4 — Assumptions & Constitution Compliance
BUCKET-B assumptions + constitution principle compliance.

## Quality Rules
- Every user story has ≥1 acceptance scenario with Given/When/Then
- P1 story works as standalone MVP
- No story depends on a later-priority story
- No implementation details (no file paths, class names, frameworks)
- Requirements are testable
- Success criteria are measurable
- Constitution principles evaluated

## Branch Naming
Pattern: `username/type/###-feature-name`
Types: `feat`, `fix`, `doc`, `refactor`, `test`, `chore`, `perf`

## Orchestrator Brief Format for Spec Writer

The orchestrator prepares this brief for the `SDD Spec Writer`:

```
WRITE spec.md to: specs/queue/[###-feature-name]/spec.md
FEATURE: [feature name]
BRANCH: [full branch name]
DATE: [YYYY-MM-DD]
USER_INPUT: "[exact user words]"

USER_STORIES:
Story 1 - [Title] (P1):
  Description: [plain language user journey]
  Why priority: [value explanation]
  Independent test: [how to verify standalone]
  Scenarios:
  - Given [state], When [action], Then [outcome]
  - Given [state], When [action], Then [outcome]

Story 2 - [Title] (P2):
  [same structure]

EDGE_CASES:
- [edge case 1]
- [edge case 2]

REQUIREMENTS:
- FR-001: System MUST [capability]
- FR-002: System SHOULD [capability]

SUCCESS_CRITERIA:
- SC-001: [measurable metric]
- SC-002: [measurable metric]

ASSUMPTIONS:
- [assumption 1]
- [assumption 2]

CONSTITUTION:
- [Principle 1]: [How spec complies]
- [Principle 2]: [How spec complies]
```

## Approval Phrases
"yes", "approved", "go ahead", "do it", "lgtm", "looks good",
"proceed", "ship it", "let's go", "execute", "start", "ok", "confirmed"
