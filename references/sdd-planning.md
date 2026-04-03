# SDD Planning Reference
> Used by the orchestrator during Step 3 and by the SDD Plan Writer.
> Defines the plan template, research format, and brief format.

## Plan Template

```markdown
# Implementation Plan: [FEATURE]

**Branch**: `[branch]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `[spec path]`

## Summary
[One paragraph: primary requirement + chosen technical approach]

## Technical Context
**Language/Version**: [value]
**Primary Dependencies**: [value]
**Storage**: [value]
**Testing**: [value]
**Target Platform**: [value]
**Project Type**: [value]
**Performance Goals**: [value]
**Constraints**: [value]
**Scale/Scope**: [value]

## Constitution Check
[List each principle + ✅ Compliant or ⚠ Violation with justification]

## Project Structure
[Concrete file layout — one chosen approach, no options]

## Research Findings
[Summary linking to research.md]

## Data Model
[Summary linking to data-model.md if applicable]

## API / Interface Contracts
[Summary linking to contracts/ if applicable]
```

## Research.md Format
```markdown
# Research: [FEATURE]

## Finding 1: [Topic]
**Source**: [file path or reasoning]
**Details**: [what was found]

## Finding 2: [Topic]
[same structure]
```

## Data-Model.md Format
```markdown
# Data Model: [FEATURE]

## Entity: [Name]
| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK |
| ... | ... | ... |

**State Machine** (if applicable):
[state] → [event] → [new state]

**Traces to**: FR-001, FR-002
```

## Plan Quality Rules
- Summary is one paragraph, not a fragment
- Technical Context has zero `NEEDS CLARIFICATION`
- Constitution Check present
- Project Structure is concrete — no "Option 1 / Option 2"
- Every entity traces to ≥1 spec requirement

## Orchestrator Brief Format for Plan Writer

```
WRITE artifacts to: specs/queue/[###-feature-name]/
SPEC_PATH: [path to spec.md]

SUMMARY:
[One paragraph approach description]

RESEARCH_FINDINGS:
Finding 1 — [topic]:
  Source: [file path]
  Details: [what was found]
Finding 2 — [topic]:
  [same structure]

TECHNICAL_CONTEXT:
Language/Version: [value]
Primary Dependencies: [value]
Storage: [value]
Testing: [value]
Target Platform: [value]
Project Type: [value]
Performance Goals: [value]
Constraints: [value]
Scale/Scope: [value]

CONSTITUTION_CHECK:
- [Principle 1]: ✅ Compliant — [reason]
- [Principle 2]: ✅ Compliant — [reason]

PROJECT_STRUCTURE:
[file tree with descriptions]
Rationale: [why this layout]

DATA_MODEL (if applicable):
Entity: [name]
  Fields: [list with types and constraints]
  Relationships: [list]
  Traces to: [requirement IDs]

API_CONTRACTS (if applicable):
Endpoint: [METHOD /path]
  Request: [body shape]
  Response: [body shape]
  Errors: [error cases]
```
