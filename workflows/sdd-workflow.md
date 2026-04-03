# SDD Workflow

Source of truth for the Spec-Driven Development orchestration flow.
The orchestrator owns reasoning, sequencing, and state. Workers execute one
focused task at a time.

## Core Rules

1. Orchestrator owns all multi-step logic. Workers do focused execution only.
2. All spawned workers are GPT-5 mini. Keep briefs small, explicit, and pre-digested.
3. User interaction must go through `vscode/askQuestions`.
4. Step order is fixed: `1 -> 1.5 -> 2 -> 3 -> 4 -> 5 -> 5.5 -> 5.7 -> 6`.
5. Update `/memories/session/sdd-state.md` at every step transition with the current step contract.
6. Spawn workers in parallel whenever tasks are independent.
7. The orchestrator must not create `spec.md`, `plan.md`, `tasks.md`, or source code directly.
Only orchestrator-owned tracking files may be edited inline: `/memories/session/*`, `specs/queue/checkpoint.md`, and task checkboxes in `tasks.md`.
8. Revisions always edit existing artifacts in place.
9. Nested subagents are optional. If unavailable, fall back to the original single-hop path.
10. When a code worker returns `STATUS: DONE`, mark that task complete in `tasks.md` immediately.
11. Step 5 is not the end. Always continue through `5.5 -> 5.7 -> 6`.
12. Bug fixes use the full workflow, not an abbreviated path.

## Step 0 - State Check

Process:
1. Read `/memories/session/sdd-state.md`.
2. If missing, create initial state for Step 1.
3. Classify the user message as `QUESTION`, `APPROVAL`, `NEW TASK`, `FEEDBACK`, or `CHECKPOINT CONTINUE`.

## Step 1 - Entry Detection

Goal: determine whether to start fresh, resume, or split the request into multiple independent items.

Process:
1. Run item decomposition before anything else.
2. Split aggressively by type, scope, layer, or user story when that produces smaller coherent work items.
3. If multiple items remain, confirm decomposition with `vscode/askQuestions`.
4. If approved as multi-item work, write `specs/queue/checkpoint.md`, process one item at a time, stop after each committed item, and wait for `continue` before starting the next.
5. Scan `specs/queue/`, `specs/doing/`, and `specs/done/` for an existing resume path.
6. Update state.

Step Contract:
- requires: user request or existing artifacts to resume
- must_do: decompose items, detect resume state, choose fresh vs resume routing
- exit_criteria: items confirmed, route selected, state written
- next_step: Step 1.5 INIT or the appropriate resume step
- next_step_requires: active feature description or resumed artifact path

## Step 1.5 - Initialize

Goal: ensure git, constitution, and Copilot instructions are ready.

Process:
1. Check for `.github/copilot-instructions.md` and `memory/constitution.md`.
2. If both exist, use `SDD Initializer` in SYNC mode.
3. Otherwise run two parallel `SDD Researcher` tasks for stack and structure, analyze the findings, and spawn `SDD Initializer` in INIT mode with a complete brief.
4. Verify success and capture `git_username`.
5. Update state to Step 2.

Step Contract:
- requires: feature description from Step 1
- must_do: verify infrastructure, run init research when needed, spawn initializer
- exit_criteria: git ready, constitution exists, instructions exist, git_username captured
- next_step: Step 2 SPECIFY
- next_step_requires: initialized project and active feature description

## Step 2 - Specify

Goal: produce an approved `spec.md`.

Process:
1. Read `memory/constitution.md`.
2. Spawn 2-3 parallel `SDD Researcher` tasks for domain, structure, and existing context when needed.
3. Analyze findings, resolve what can be resolved directly, bucket remaining ambiguities, and ask only the unresolved user questions.
4. Create the feature branch.
5. Spawn `SDD Spec Writer` with a complete brief.
6. Spawn `SDD Reviewer` on the written spec.
7. If review fails, craft targeted fixes and re-run `SDD Spec Writer` in REVISE mode, then re-review. Maximum two revision rounds.
8. Show the full spec, ask for approval, and stay on this step until approved.
9. Update state to Step 3.

Step Contract:
- requires: initialized project and feature description
- must_do: research, clarify, branch, write spec, review, get approval
- exit_criteria: `spec.md` exists, branch exists, reviewer pass or user-approved artifact exists
- next_step: Step 3 PLAN
- next_step_requires: approved `spec.md`

## Step 3 - Plan

Goal: produce an approved `plan.md` and supporting planning artifacts.

Process:
1. Read the approved spec.
2. Spawn three parallel `SDD Researcher` tasks for architecture, integration, and testing/data patterns.
3. Analyze and choose the concrete technical approach, file structure, data model, interfaces, and constitution compliance.
4. Ask only unresolved clarification questions.
5. Spawn `SDD Plan Writer` with the complete brief.
6. Spawn `SDD Reviewer` on the plan artifacts.
7. If review fails, re-run the writer in REVISE mode with targeted fixes, then re-review. Maximum two revision rounds.
8. Show the complete plan, ask for approval, and stay on this step until approved.
9. Update state to Step 4.

Step Contract:
- requires: approved `spec.md`
- must_do: research, decide approach, clarify, write plan artifacts, review, get approval
- exit_criteria: `plan.md` and required supporting artifacts exist, reviewer pass or user-approved artifact exists
- next_step: Step 4 TASKS
- next_step_requires: approved `spec.md`, `plan.md`, and supporting artifacts

## Step 4 - Tasks

Goal: produce an approved `tasks.md` with dependencies, checkpoints, and coverage.

Process:
1. Read `spec.md`, `plan.md`, and supporting planning artifacts.
2. Build the dependency graph yourself: setup, foundation, per-story phases, and polish.
3. Map every acceptance scenario to at least one task and identify all parallel-safe tasks.
4. Spawn `SDD Task Writer` with a complete brief.
5. Spawn `SDD Reviewer` on `tasks.md`.
6. If review fails, re-run `SDD Task Writer` in REVISE mode with targeted fixes, then re-review. Maximum two revision rounds.
7. Show the complete task list, ask whether execution should begin, and stay on this step until approved.
8. Update state to Step 5.

Step Contract:
- requires: approved `spec.md` and `plan.md`
- must_do: build dependency graph, write tasks, review, get approval
- exit_criteria: `tasks.md` exists, scenarios are mapped, reviewer pass or user-approved artifact exists
- next_step: Step 5 EXECUTE
- next_step_requires: approved `tasks.md` and all supporting artifacts

## Step 5 - Execute

Goal: complete all tasks with verified implementation.

Process:
1. Move the feature directory from `specs/queue/` to `specs/doing/` and commit the move.
2. Detect the build and test commands from the project root.
3. For each phase in `tasks.md`, scan the entire phase first and split work into parallel and sequential sets.
4. For parallel-safe work, spawn up to five `SDD Code Worker` tasks at a time with minimal complete briefs.
5. After each batch returns, mark all completed tasks in `tasks.md` before any build check.
6. Handle non-DONE statuses:
   - `BLOCKED`: analyze, split further, and re-spawn
   - `DEVIATION`: ask the user whether to revise plan, continue, or abort
   - `BUILD_FAIL`: diagnose, create a targeted fix task, and spawn a fix worker
7. For sequential tasks, run one worker at a time and mark completion immediately after each `DONE` result.
8. Run build and test at each phase checkpoint.
9. If a task is too large for GPT-5 mini, split it into sub-tasks, save a checkpoint in `/memories/session/`, and continue from the checkpoint.
10. After all phases, verify every task is checked off, run the final build and test, and verify the acceptance scenarios from the spec.
11. After three failed fix attempts on the same problem, stop and ask the user how to proceed.

Step Contract:
- requires: approved `tasks.md` and detected build system
- must_do: execute all task phases, mark progress on disk, verify build/test checkpoints
- exit_criteria: all tasks complete, final build and test pass, acceptance scenarios verified
- next_step: Step 5.5 POST_SYNC
- next_step_requires: completed implementation and any new technology notes

## Step 5.5 - Post-Execute Sync

Goal: reconcile project instructions with what was built.

Process:
1. Summarize implementation changes, new technologies, and user corrections.
2. Spawn `SDD Initializer` in POST-EXECUTE mode.
3. Update state to Step 5.7.

Step Contract:
- requires: completed execution
- must_do: run post-execution initializer sync
- exit_criteria: instruction sync completed
- next_step: Step 5.7 WRAP_UP
- next_step_requires: synced instructions

## Step 5.7 - Wrap-Up and Commit

Goal: finalize the implemented feature before retrospective.

Process:
1. Ask whether anything else should change before commit.
2. If yes, run targeted code-worker fixes and loop, up to three rounds.
3. If no, or the loop limit is reached:
   - `git add -A`
   - generate a conventional commit message
   - confirm the message with the user
   - `git commit -m "[message]"`
   - move the feature from `specs/doing/` to `specs/done/`
   - commit that move
4. Update state either to Step 6 or to the next unchecked multi-item entry.

Step Contract:
- requires: completed execution and synced instructions
- must_do: ask for final adjustments, commit work, move feature to `specs/done/`
- exit_criteria: feature committed and moved to done
- next_step: Step 6 RETROSPECTIVE or next multi-item entry
- next_step_requires: committed feature

## Step 6 - Retrospective

Goal: close the workflow with lessons and a final summary.

Process:
1. Review assumptions, plan changes, failures, user corrections, and worker issues.
2. Format candidate lessons.
3. Ask which lessons to keep.
4. Save confirmed lessons to `/memories/session/lessons.md`.
5. Present the final summary with spec, plan, tasks, branch, worker count, and batch count.

Step Contract:
- requires: committed feature
- must_do: review the session, save chosen lessons, present final summary
- exit_criteria: lessons saved or declined and final summary shown
- next_step: none
- next_step_requires: n/a