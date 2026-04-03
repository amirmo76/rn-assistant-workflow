# Figma-to-React-Native Spec Driven Agentic Workflow (Branch A)

Source of truth for the Branch A (Visuals) Figma-to-React-Native orchestration flow.

## System Overview

This system is a spec-driven, component-driven pipeline for Branch A (Visuals) in a Y-shaped architecture. Its job is to turn Figma designs into isolated, strictly presentational React Native components and Storybook files.

By separating UI generation from application logic ("Branch B") and enforcing a **Contract-First** flow, it reduces context bloat, design hallucination, and reuse drift.

The orchestrator owns routing, state, gates, and verification. Workers produce bounded artifacts. Reviewers validate only against explicit contracts and diagnostics.

## Core Rules

1. **Strict Role Separation**: The Orchestrator owns all multi-step logic, entry detection, and DAG planning. Specialized domain agents are strictly separated by read/write capabilities to prevent hallucination and execution drift.
2. **"Dumb" Components Only**: UI components must remain strictly presentational. No internal state logic (e.g., `useState`) is permitted for interactive elements; all interactivity must be passed up to the parent via props.
3. **Absolute Token Taxonomy**: Agents must not write raw hardcoded styles (e.g., `#0F172A`, `15px`). All raw values must map to semantic tokens and be added to the token source of truth.
4. **No AI in the Data Pipe**: Phase 2 is mechanical. No AI logic review is allowed during mapping and extraction.
5. **Mandatory System Pause**: Execution must halt at Step 3.2. No code generation begins until a human explicitly inputs `APPROVE` or `REJECT_WITH_FEEDBACK` on the generated specs.
6. **State Preservation**: `.ui-state/` is the source of truth for design state. Initializers and post-sync agents must preserve existing manifests.
7. **DAG-Driven Parallelism**: UI workers run in parallel only within DAG-safe batches.
8. **Fixed Phase Order**: Execution flows strictly through `Phase 1 (Init) -> Phase 2 (Extraction) -> Phase 3 (Contract/Pause) -> Phase 4 (Execution) -> Phase 5 (Teardown)`.
9. **Bounded Fix Loops**: Reviewer failures go back to the same worker. Maximum 3 retries.
10. **Worker Model & Briefs**: All spawned workers are GPT-5 mini. Briefs must stay small and explicit.
11. **User Interaction Channel**: User interaction must go through `vscode/askQuestions`.
12. **Session State Updates**: Update `/memories/session/sdd-state.md` at every step transition.
13. **Parallelism Policy**: Run workers in parallel whenever tasks are independent.
14. **Orchestrator Editing Restrictions**: The orchestrator must not create `spec.md`, `plan.md`, `tasks.md`, or source code directly. It may edit only orchestrator-owned tracking files: `/memories/session/*`, `specs/queue/checkpoint.md`, and task checkboxes in `tasks.md`.
15. **In-Place Revisions**: Revisions always edit existing artifacts in place.
16. **Subagent Fallback**: Nested subagents are optional. If unavailable, use a single-hop fallback.
17. **Task Completion Marking**: When a code worker returns `STATUS: DONE`, mark that task complete in `tasks.md` immediately.
18. **Canonical Artifacts**: Every run uses stable artifact locations. Session state lives in `/memories/session/sdd-state.md`. Contracts live under `specs/queue/`, active execution under `specs/doing/`, completed tracking under `specs/done/`, and design-state artifacts under `.ui-state/`.
19. **Explicit Routing Before Execution**: The orchestrator must route `QUESTION`, `APPROVAL`, `FEEDBACK`, and `CHECKPOINT CONTINUE` requests before attempting Step 1.0. Only `NEW TASK` requests start a fresh end-to-end build flow.
20. **Visual Grounding**: Agents that require a visual reference (SDD Spec Writer, SDD UI Worker, SDD Reviewer) must call `figma/get_screenshot` directly using the `figma_file_key` and `figma_node_id` provided in their brief. Screenshots are fetched on demand — they are not saved as file artifacts.
21. **One Source of Truth Per Phase**: Each phase must declare what it reads and what it may create or mutate. Missing required inputs must not be inferred.
22. **Fail Closed**: If a required artifact, tool capability, validation result, or approval token is missing, halt and record the blocker in `/memories/session/sdd-state.md`.

## Operating Definitions

- **Execution Context Object**: A persisted object in `/memories/session/sdd-state.md` containing at minimum `session_id`, `request_type`, `figma_file_key`, `figma_node_id`, `target_name`, `node_type`, `resume_mode`, `repo_root`, and `current_step`.
- **Structural Container**: A Figma node that is valid as a page or component root for extraction, typically `FRAME`, `COMPONENT`, `COMPONENT_SET`, or a clearly isolated section explicitly approved by the user.
- **Reference Screenshot**: A screenshot obtained by calling `figma/get_screenshot` with the validated `figma_file_key` and `figma_node_id`. It is fetched on demand by agents that need visual grounding and is never saved as a file artifact. It is a visual guide, not a style source of truth.
- **Diff Array**: The normalized list of components to create or revise, with at minimum `component`, `status`, `source_json`, `target_paths`, and `spec_path`.
- **Approved Spec**: A `spec.md` artifact that has passed reviewer checks and has an explicit user approval token recorded in session state.
- **Execution Batch**: The smallest DAG-safe set of component tasks that may run in parallel without dependency conflicts.

## Artifact Conventions

- `specs/queue/[component]/spec.md`: proposed contract awaiting approval
- `specs/queue/[component]/review.md`: spec completeness review
- `specs/queue/[component]/plan.json`: dependency and execution metadata when needed
- `specs/doing/[component]/`: active execution artifacts for a component
- `specs/done/[component]/`: finalized tracking artifacts after completion
- `.ui-state/pages/[target-name]-mcp-raw.html`: full Figma MCP response (HTML/code) saved by the orchestrator at Step 1.0; the only Figma data source for downstream workers
- `.ui-state/pages/[target-name]-tree.json`: normalized structure tree for the target
- `.ui-state/components/[ComponentName].json`: tokenized component extraction payload

If the repository already uses a compatible naming scheme, the initializer must map these logical artifact types to existing paths and record that mapping in session state before continuing.

## Agent Routing Table

Use these exact agent names when the workflow says to spawn a worker:

| Step | Agent | Responsibility |
|---|---|---|
| 1.5 research | `SDD Researcher` | Read-only repo research for package manager, Storybook, tests, token source, and project shape |
| 1.5 initialize | `SDD Initializer` | INIT or SYNC infrastructure work |
| 2.0 | `SDD Mapper` | Create `.ui-state/pages/[target-name]-tree.json` |
| 2.1 | `SDD Extractor` | Create raw `.ui-state/components/[ComponentName].json` artifacts |
| 2.2 | `SDD Token Synthesizer` | Tokenize component JSONs and update the token source of truth |
| 3.0 | `SDD Design Guardian` | Produce the Diff Array and conflict classification |
| 3.1 write | `SDD Spec Writer` | Write or revise `spec.md` |
| 3.1 review | `SDD Reviewer` | Review spec completeness and policy compliance |
| 4.0 | `SDD Task Planner` | Write DAG topology metadata |
| 4.1 | `SDD Task Planner` | Write or revise `tasks.md` |
| 4.2 execute | `SDD UI Worker` | Generate one presentational component task |
| 4.2 review | `SDD Reviewer` | Review generated task output and diagnostics |
| 5.0 | `SDD Initializer` | POST-SYNC cleanup and manifest reconciliation |

## Step 0 - State Check

**Goal:** Determine session state and classify the request.

**Process:**

1. Read `/memories/session/sdd-state.md`.
2. If missing, create initial state for Step 1.0.
3. Classify the user message as `QUESTION`, `APPROVAL`, `NEW TASK`, `FEEDBACK`, or `CHECKPOINT CONTINUE`.
4. If the request is not `NEW TASK`, route it to the active checkpoint instead of restarting:
   - `QUESTION`: answer from current state only; do not advance steps.
   - `APPROVAL`: only valid when current step is Step 3.2 or commit confirmation in Step 5.1.
   - `FEEDBACK`: only valid when revising an existing artifact in place.
   - `CHECKPOINT CONTINUE`: resume from the recorded `current_step` and required artifacts.
5. Record the request classification, active checkpoint, and any blocker in session state.

**Step Contract:**

- requires: user message
- must_do: read or create state, classify input, route non-build requests safely
- exit_criteria: state exists, message is classified, route decision is recorded
- next_step: Step 1.0 Entry Detection for `NEW TASK`; otherwise remain at current checkpoint or halt pending user input
- next_step_requires: classified request and recorded route decision

## Step 1.0 - Entry Detection & Context Assembly

**Goal:** Assemble and validate execution context from the user request and Figma.

**Process:**

1. Parse the Figma URL, target name, and user prompt.
2. Normalize the Figma identifiers into `file_key` and `node_id` using these exact rules:
   - `file_key`: the path segment immediately after `/design/` in the URL, before the next `/`
     (e.g. `https://www.figma.com/design/Rm9u0p7hbN87OQDkSCAACc/...` → `Rm9u0p7hbN87OQDkSCAACc`)
   - `node_id`: the `node-id` query parameter value with every `-` converted to `:`
     (e.g. `?node-id=15-36` → `15:36`)
   - Reject and halt on malformed URLs or missing target identifiers.
3. Call the Figma MCP tool `figma/get_design_context` with the extracted `fileKey` and `nodeId`.
   IMPORTANT: Only the orchestrator (SpecDriven) may call this tool. Worker subagents (Mapper, Extractor, etc.) run in environments where the MCP is unavailable — they must never attempt to call it. Never use the `web` tool to fetch Figma URLs — the web tool cannot access Figma designs.
   The MCP returns generated React/HTML code and a reference screenshot. If raw node JSON is present, use it directly. Otherwise parse the returned code for `data-node-id` attributes and element hierarchy to recover node structure deterministically.
4. Save the full MCP response HTML/code as `.ui-state/pages/[target-name]-mcp-raw.html`. This file is the single source of Figma data for all downstream workers — they read from it instead of calling the MCP.
5. Resolve whether the request is a fresh target, a resume, or a revision against previously generated components.
6. Scan `specs/queue/`, `specs/doing/`, and `specs/done/` for a resume path.
7. If a resume path exists, confirm whether the user intends resume or restart. A restart must preserve prior artifacts until explicitly superseded.
8. If data is invalid or missing, clarify via `vscode/askQuestions` and halt.
9. Construct the Validated Execution Context Object (Session ID, File Key, Node ID, Node Type, Target Name, Resume Mode, Repo Root).
10. Record the artifact path mapping for this run.
11. Update `/memories/session/sdd-state.md` to Step 1.5.

**Step Contract:**

- requires: classified user request containing Figma target
- must_do: normalize Figma identifiers, validate target, save MCP response as `-mcp-raw.html`, determine resume mode, assemble context object, map artifact paths
- exit_criteria: Validated Execution Context Object exists, `.ui-state/pages/[target-name]-mcp-raw.html` exists, and all required paths are known
- next_step: Step 1.5 Initialize
- next_step_requires: Validated Execution Context Object and `.ui-state/pages/[target-name]-mcp-raw.html`

## Step 1.5 - Initialize

**Goal:** Scaffold the working environment, preserve design state, and prepare source control.

**Process:**

1. Read the Validated Execution Context Object.
2. Detect repository guidance needed for safe execution, including agent instructions, constitution, package manager, and React Native project shape.
3. If sufficient guidance already exists, use the initializer in SYNC mode.
4. Otherwise run focused research for stack and structure, then spawn the initializer in INIT mode with a complete brief.
   - Use `SDD Researcher` for the focused repo research.
   - Use `SDD Initializer` for INIT or SYNC execution.
5. Verify success and capture `git_username` and the active package manager.
6. Create or switch to a local Git feature branch. If the worktree is dirty, record it and continue without discarding unrelated changes.
7. Verify or create the `.ui-state/` directory structure (`.ui-state/pages/` and `.ui-state/components/`).
8. Ensure initialization is idempotent: preserve any existing `.ui-state` manifests.
9. Resolve the design token source of truth:
   - If a compatible `design-system.ts` exists, record its path.
   - If a different token source exists, map it explicitly and record the mapping.
   - If no token source exists, create a blocking decision for the user or scaffold one only if the workflow is explicitly allowed to do so.
10. Verify Storybook and testing environments:
   - Detect Storybook configuration (e.g. `.storybook/`, `storybook/`, or `package.json` scripts). If missing, scaffold a minimal Storybook setup appropriate to the project stack (web or React Native) including a basic config, a sample story, and a `storybook` script.
   - Detect test runner and framework (e.g. `jest`, `vitest`, `@testing-library/react` / `@testing-library/react-native`). If missing, scaffold a minimal testing setup: add a test script, a base test configuration, and a sample smoke test.
   - Run smoke checks using the detected package manager and record exact commands and results in `/memories/session/sdd-state.md`.
11. Record any blockers that still allow extraction but would block later execution.
12. Update `/memories/session/sdd-state.md` to Step 2.0.

**Step Contract:**

- requires: Validated Execution Context Object
- must_do: verify infrastructure, branch git safely, scaffold `.ui-state/` idempotently, resolve token source of truth, detect or scaffold Storybook, detect or scaffold test runner, run smoke checks, record results
- exit_criteria: Git branch active, `.ui-state/` directories validated/created, token source of truth recorded, Storybook config and a sample story present OR scaffolding performed, test runner configured and a sample test exists, smoke checks passed or failing items recorded
- next_step: Step 2.0 Map Component Tree
- next_step_requires: Initialized `.ui-state/` environment

## Step 2.0 - Map Component Tree

**Goal:** Extract the structural hierarchy of the target node without processing stylistic data.

**Process:**

1. Read the Validated Execution Context Object and initialized environment.
2. Spawn a mapper worker with read access to `.ui-state/pages/[target-name]-mcp-raw.html` and write access only to the tree artifact.
   - Use `SDD Mapper`.
   - The brief MUST include the path to `.ui-state/pages/[target-name]-mcp-raw.html` as the Figma data source.
   - The worker reads that file to get the Figma HTML/code. It must not call `figma/get_design_context` or any web tool.
3. Traverse the target node structure from the HTML (using `data-node-id` attributes and element hierarchy) to map parent/child relationships and identify structural boundaries (Atoms, Molecules, Organisms) without generating implementation advice.
4. Normalize node names, stable identifiers, sibling order, and parent references so the tree can be replayed deterministically.
5. Save the structural map to `.ui-state/pages/[target-name]-tree.json`.
6. Update `/memories/session/sdd-state.md` to Step 2.1.

**Step Contract:**

- requires: Initialized `.ui-state/` environment, Validated Execution Context Object, and `.ui-state/pages/[target-name]-mcp-raw.html`
- must_do: map structural hierarchy from the saved MCP HTML, enforce the no-AI-logic rule, normalize identifiers, save tree state
- exit_criteria: `.ui-state/pages/[target-name]-tree.json` exists and is deterministic
- next_step: Step 2.1 Extract JSONs
- next_step_requires: `.ui-state/pages/[target-name]-tree.json` and `.ui-state/pages/[target-name]-mcp-raw.html`

## Step 2.1 - Extract JSONs

**Goal:** Extract raw property data for each component in the mapped tree.

**Process:**

1. Read `.ui-state/pages/[target-name]-tree.json` and `.ui-state/pages/[target-name]-mcp-raw.html`.
2. Spawn an extractor worker with read access to those two files and write access only to `.ui-state/components/`.
   - Use `SDD Extractor`.
   - The brief MUST include paths to both `.ui-state/pages/[target-name]-tree.json` and `.ui-state/pages/[target-name]-mcp-raw.html`.
   - The worker reads the HTML file to recover raw visual, layout, and text properties. It must not call `figma/get_design_context` or any web tool.
3. Extract raw visual, layout, and text properties for each mapped component node from the saved HTML.
4. Preserve source provenance in every JSON file, including the originating `node_id` (from `data-node-id` attributes), target tree path, and extraction timestamp.
5. Save the extracted data as individual, raw `.ui-state/components/[ComponentName].json` files.
6. Update `/memories/session/sdd-state.md` to Step 2.2.

**Step Contract:**

- requires: `.ui-state/pages/[target-name]-tree.json` and `.ui-state/pages/[target-name]-mcp-raw.html`
- must_do: extract raw properties from saved HTML, preserve provenance, generate component JSON files
- exit_criteria: Raw `.ui-state/components/[ComponentName].json` files exist
- next_step: Step 2.2 Synthesize Tokens
- next_step_requires: Raw component JSON files

## Step 2.2 - Synthesize Tokens & Update Design System

**Goal:** Enforce the token taxonomy by scrubbing hardcoded design values.

**Process:**

1. Read raw `.ui-state/components/[ComponentName].json` files and the recorded token source of truth.
2. Spawn a token synthesizer worker with write access only to token artifacts and extracted component JSONs.
   - Use `SDD Token Synthesizer`.
3. Scrub all absolute pixels, hex codes, and raw styling values from the JSON files.
4. Map raw values to semantic tokens (e.g., `theme.colors.primary`, `spacing.md`) and update the token source of truth.
5. If a raw value cannot be mapped confidently, halt and surface a token decision instead of inventing one.
6. Overwrite the raw JSONs with final, tokenized `.ui-state/components/[ComponentName].json` files.
7. Update `/memories/session/sdd-state.md` to Step 3.0.

**Step Contract:**

- requires: raw component JSON files and a recorded token source of truth
- must_do: scrub hardcoded values, synthesize tokens, update token source of truth, rewrite JSONs, fail closed on unmappable values
- exit_criteria: tokenized `.ui-state/components/[ComponentName].json` files and updated token source of truth exist
- next_step: Step 3.0 Guard the Design
- next_step_requires: tokenized component JSONs and updated token source of truth

## Step 3.0 - Guard the Design

**Goal:** Prevent duplicate components and preserve design-system integrity.

**Process:**

1. Read the tokenized `.ui-state/components/[ComponentName].json` files and previous `.ui-state` manifests.
2. Spawn a design guardian worker with read access to current and historical design-state artifacts.
   - Use `SDD Design Guardian`.
3. Compare incoming components against existing design state to identify duplicates, variants, or new components.
4. Generate a Diff Array (e.g., `[{ component: "Button", status: "MODIFIED_BASE" }, { component: "Hero", status: "NEW" }]`).
5. For each diff item, record whether it is `NEW`, `NEW_VARIANT`, `MODIFIED_BASE`, `UNCHANGED`, or `CONFLICT`.
6. Do not generate specs for `UNCHANGED` items; halt on unresolved `CONFLICT` items.
7. Update `/memories/session/sdd-state.md` to Step 3.1.

**Step Contract:**

- requires: Tokenized component JSONs and `.ui-state` history
- must_do: compare current extraction against existing state, classify diff status, exclude unchanged items, stop on unresolved conflicts
- exit_criteria: Diff Array generated and contains only actionable or explicitly blocked items
- next_step: Step 3.1 Specify
- next_step_requires: Diff Array and Tokenized JSONs

## Step 3.1 - Specify

**Goal:** Produce a complete, logically sound component contract (`spec.md`).

**Process:**

1. Read the Diff Array and Tokenized JSONs.
2. Spawn the `SDD Spec Writer` agent.
3. Define the TypeScript `Props` interface, supported visual variants, permitted interaction states, accessibility requirements, and explicit non-goals for each actionable component in the Diff Array.
4. Each spec must include target file paths, required imports or dependencies, expected Storybook coverage, required tests, and the `figma_file_key` and `figma_node_id` for on-demand visual reference via `figma/get_screenshot`.
5. Output the proposed `spec.md` contract under `specs/queue/[component]/spec.md`.
6. Spawn the `SDD Reviewer` agent to ensure the spec is complete: no missing states, no illegal internal state, no token leaks, correct prop typing, and no hidden dependencies.
7. If the review fails, craft targeted fixes and re-run `SDD Spec Writer` in REVISE mode. Maximum two revision rounds.
8. Update `/memories/session/sdd-state.md` to Step 3.2.

**Step Contract:**

- requires: Diff Array and Tokenized JSONs
- must_do: write interface contracts, include output expectations and screenshot reference, review for completeness, handle revisions
- exit_criteria: unapproved `spec.md` files exist for all actionable diff items
- next_step: Step 3.2 System Pause
- next_step_requires: Proposed `spec.md` files

## Step 3.2 - System Pause (Human-in-the-Loop)

**Goal:** Halt for explicit human approval before any code is generated.

**Process:**

1. The Orchestrator halts the execution thread.
2. Present the proposed `spec.md` files and Diff Array to the user. Optionally call `figma/get_screenshot` to display the visual reference inline.
3. Ask for an explicit decision through `vscode/askQuestions`. Freeform approval text is insufficient unless it contains an exact recorded approval token.
4. Wait for `APPROVE` or `REJECT_WITH_FEEDBACK`.
5. If `REJECT_WITH_FEEDBACK`, record the feedback in session state, pass it to the `Spec Writer`, loop back to Step 3.1, and regenerate the spec in place.
6. If `APPROVE`, record the approver decision, timestamp, and approved spec paths in session state, then lock the `spec.md` files as the absolute source of truth.
7. Update `/memories/session/sdd-state.md` to Step 4.0.

**Step Contract:**

- requires: Proposed `spec.md` files
- must_do: halt system, prompt through the approved interaction channel, handle feedback loop or approval, record approval metadata
- exit_criteria: explicit user approval received and recorded for all specs
- next_step: Step 4.0 Plan DAG
- next_step_requires: Approved `spec.md` files

## Step 4.0 - Plan DAG

**Goal:** Map component dependencies to avoid race conditions during generation.

**Process:**

1. Read the approved `spec.md` files.
2. Spawn the `SDD Task Planner` agent in DAG mode.
3. Analyze nested dependencies (e.g., `Icon` before `Button`).
4. Validate that the dependency graph is acyclic. If a cycle exists, halt and route back to Step 3.1 for spec correction.
5. Output a DAG topology map with build order and batch boundaries.
6. Update `/memories/session/sdd-state.md` to Step 4.1.

**Step Contract:**

- requires: Approved `spec.md` files
- must_do: analyze component dependencies, validate acyclicity, generate topological order and batch boundaries
- exit_criteria: DAG topology map exists and contains no cycles
- next_step: Step 4.1 Generate Tasks
- next_step_requires: DAG topology map

## Step 4.1 - Generate Tasks

**Goal:** Translate the DAG into a prioritized queue of execution jobs.

**Process:**

1. Read the DAG topology map.
2. Spawn the `SDD Task Planner` agent in TASKS mode.
3. Generate a task list in `tasks.md`, grouped by execution batch.
4. Map every generation job to its approved spec and target output paths.
5. For each task, include status, owning worker role, retry count, verification commands, and promotion rules from `queue` to `doing` to `done`.
6. Update `/memories/session/sdd-state.md` to Step 4.2.

**Step Contract:**

- requires: DAG topology map
- must_do: create prioritized execution queue, group tasks by batch, embed verification metadata
- exit_criteria: `tasks.md` exists, is populated, and can be executed without inferred information
- next_step: Step 4.2 Execute
- next_step_requires: `tasks.md` and approved `spec.md` files

## Step 4.2 - Execute

**Goal:** Generate strictly presentational components and Storybook files.

**Process:**

1. Read `tasks.md`, approved `spec.md` files, and the recorded token source of truth.
2. Promote only the current execution batch to `specs/doing/`; future batches remain queued.
3. Spawn `SDD UI Worker` agents in parallel, strictly adhering to DAG batches. Pass one approved `spec.md` per worker. Include `figma_file_key` and `figma_node_id` in each brief so the worker can call `figma/get_screenshot` for visual grounding.
4. Workers generate `Component.tsx`, `Component.stories.tsx`, and any required test file. They may call `figma/get_screenshot` for visual grounding, but JSON artifacts and tokens remain the source of truth. No internal state logic (`useState`) is permitted unless the approved spec explicitly allows controlled wrappers that still remain externally driven.
5. After a worker finishes, spawn the `SDD Reviewer` agent to run the task-specific lint, type-check, and test commands declared in `tasks.md`.
6. If the reviewer fails the code, send the error log back to the same `SDD UI Worker` for a fix loop. Hard cap: 3 retries per task. On the third failure, halt the workflow, preserve artifacts in `specs/doing/`, and alert the user with the blocking diagnostics.
7. Upon successful review, mark the task as `STATUS: DONE` in `tasks.md` immediately and promote its tracking artifacts when the whole batch is complete.
8. After each batch completes, run an aggregate verification pass to catch cross-component type or import regressions before releasing the next batch.
9. Update `/memories/session/sdd-state.md` to Step 5.0 once all tasks in `tasks.md` are marked DONE and the final aggregate verification passes.

**Step Contract:**

- requires: `tasks.md`, approved `spec.md` files, and recorded token source of truth
- must_do: spawn parallel workers per DAG batch, provide `figma_file_key`/`figma_node_id` in briefs, generate UI/Stories/tests as specified, use screenshot only as visual guidance, enforce dumb-component rule, run review/fix loops, run aggregate batch verification, mark progress
- exit_criteria: all tasks in `tasks.md` are DONE, required generated files exist, task-level checks pass, and aggregate verification passes
- next_step: Step 5.0 Post-Sync
- next_step_requires: Final generated code

## Step 5.0 - Post-Sync

**Goal:** Clean up temporary files and reconcile design state with the final generated code.

**Process:**

1. Read the final generated code.
2. Spawn `SDD Initializer` in POST-SYNC mode.
3. Clear temporary files from execution, but never delete approved specs, reviews, or session state.
4. Update the `.ui-state` manifests and ensure `[target-name]-tree.json` accurately reflects the finalized generated UI.
5. Reconcile generated file paths back into the Diff Array and manifests so future resume or revision flows know what is authoritative.
6. Update `/memories/session/sdd-state.md` to Step 5.1.

**Step Contract:**

- requires: Final generated code
- must_do: clean temp files safely, synchronize `.ui-state` manifests, reconcile generated outputs into manifests
- exit_criteria: `.ui-state` matches generated codebase and resume metadata is accurate
- next_step: Step 5.1 & 6.0 Wrap-Up & Retrospective
- next_step_requires: Synchronized `.ui-state`

## Step 5.1 & 6.0 - Wrap-Up & Retrospective

**Goal:** Commit the finished work, generate documentation, and capture session lessons.

**Process:**

1. Spawn the Orchestrator.
2. Generate a `.md` summary outlining the semantic tokens added, components built or revised, verification commands run, and any residual limitations.
3. Review assumptions, user corrections, and fix loops to format candidate lessons. Ask the user which lessons to keep and save accepted lessons to `/memories/session/lessons.md`.
4. Stage changes (`git add -A`), generate a conventional commit message, confirm with the user through the approved interaction channel, and execute the commit only after explicit approval.
5. Move the tracked feature artifacts from `specs/doing/` to `specs/done/`.
6. Update `/memories/session/sdd-state.md` to `SESSION_COMPLETE`, including commit SHA and summary path.

**Step Contract:**

- requires: Synchronized `.ui-state` and completed codebase
- must_do: summarize output, capture lessons, confirm and commit to git, move tracking files, close state cleanly
- exit_criteria: git commit completed, `.md` summary generated, lessons saved, state marked complete with commit metadata
- next_step: none
- next_step_requires: n/a
