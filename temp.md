# Update the workflow and agents with these requirements

Revise the workflow and the affected agent instructions so they satisfy every requirement below. Do not execute the workflow itself; only update the prompt, workflow, and agent guidance so the behavior is unambiguous.

1. Design-system token inference must use this priority order when mapping a visual value to a token:
    - Exact or close value match has the highest priority.
    - Visual similarity comes next. If the observed value looks like a shade of green, do not select a grey token just because the token name sounds closer.
    - Token name similarity is last.

2. The infrastructure or initializer step must ensure that a .github/copilot-instructions.md file exists.
    - If it is missing, create a minimal React Native version.

3. The infrastructure or initializer step must ensure that a design system file exists and that its path is explicitly declared in .github/copilot-instructions.md.
    - If no design system file can be found, ask the user via askQuestions.
    - In the same question flow, also offer to generate a minimal design system file automatically.
    - If the user provides the design system or accepts the generated fallback, add or reference that file from .github/copilot-instructions.md.

4. Introduce memory-based workflow state so work can resume where it stopped.
    - The session source of truth must be `/memories/session/ui-state.md`.

5. The UI Assistant agent must use `/memories/session/ui-state.md` before taking any workflow action.
    - If the file does not exist, create it.
    - After reading the workflow, the first state read must be `/memories/session/ui-state.md` if it exists.
    - give it `vscode/memory` tool.
    - Before any tool-using action within a workflow step, run this checklist:
      1. What step am I on according to `/memories/session/ui-state.md`?
      2. What does the workflow require at this step?
      3. Am I about to do exactly that?
      4. If not, stop and re-read the workflow section.
    - Before every step transition:
      1. Verify the current step exit criteria are satisfied.
      2. Update `/memories/session/ui-state.md`.
      3. Include next_step_requires in the state.
      4. Re-read the next workflow step before acting.
    - Treat `/memories/session/ui-state.md` as the ground truth for session progress.

6. The workflow itself must contain rules that enforce memory updates and memory reads.
    - It must require updating `/memories/session/ui-state.md` at every step transition with the current step contract.
    - It must require reading `/memories/session/ui-state.md` as one of the first actions in the workflow.

7. The initializer must require memory/constitution.md.
    - If memory/constitution.md is missing and the brief does not provide its content, ask the user for the constitution or create the minimal fallback requested by the brief.

8. The workflow and all related agents, including Planner, Reviewer, UI Component Spec Writer, and any other agent that consumes these instructions, must read and comply with memory/constitution.md.
    - The reviewer must verify outputs against the constitution rules as well.

9. review the overal workflow and agents to make sure everything is consistant and there is no bug.
