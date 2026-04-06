# Branch A SDD Agents

This repo now targets the Branch A Figma-to-React-Native workflow defined in
[workflows/sdd-workflow.md](/home/amir/Documents/sdd/workflows/sdd-workflow.md).

The workflow is contract-first and presentational-only:
- Figma target validation and screenshot capture happen before extraction
- raw component extraction is separated from token synthesis
- spec approval is mandatory before any code generation
- UI generation runs from approved specs in DAG-safe batches
- post-sync and wrap-up are part of completion, not optional cleanup

## Agent Set

| Agent | Model | Purpose |
|-------|-------|---------|
| `SpecDriven` | GPT-5.4 | Orchestrator for the full Branch A workflow |
| `SDD Initializer` | GPT-5 mini | INIT, SYNC, and POST-SYNC infrastructure work |
| `SDD Researcher` | GPT-5 mini | Read-only repo research for Step 1.5 |
| `SDD Mapper` | GPT-5 mini | Figma structural tree mapping |
| `SDD Extractor` | GPT-5 mini | Raw component JSON extraction |
| `SDD Token Synthesizer` | GPT-5 mini | Token mapping and token-source updates |
| `SDD Design Guardian` | GPT-5 mini | Diff classification against prior design state |
| `SDD Spec Writer` | GPT-5 mini | Component spec writing and revision |
| `SDD Task Planner` | GPT-5 mini | DAG and tasks generation |
| `SDD UI Worker` | GPT-5 mini | Single-task component, story, and test generation |
| `SDD Reviewer` | GPT-5 mini | Spec, task, and output review |
| `Explore` | GPT-5 mini | Read-only fallback exploration |

## Workflow Routing

The workflow now names the exact agent for each worker step inside
[workflows/sdd-workflow.md](/home/amir/Documents/sdd/workflows/sdd-workflow.md).

High-level flow:
1. Step 0 and Step 1.0 stay in the orchestrator.
2. Step 1.5 uses `SDD Researcher` and `SDD Initializer`.
3. Step 2.0 to Step 3.0 use `SDD Mapper`, `SDD Extractor`, `SDD Token Synthesizer`, and `SDD Design Guardian`.
4. Step 3.1 uses `SDD Spec Writer` and `SDD Reviewer`.
5. Step 4.0 and Step 4.1 use `SDD Task Planner`.
6. Step 4.2 uses parallel `SDD UI Worker` runs plus `SDD Reviewer`.
7. Step 5.0 uses `SDD Initializer` in POST-SYNC mode.

## Installation

```bash
python3 install.py
```

The installer now:
- copies the current agents, references, prompts, and workflow
- updates VS Code settings for agents and prompts
- prunes legacy managed SDD files that no longer exist in this repo so outdated agents and references do not linger after reinstall

Options:
- `--dry-run` or `-n`
- interactive model selection
