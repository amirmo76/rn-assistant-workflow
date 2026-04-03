# SDD Agent — Micro-Worker Architecture

> Spec-Driven Development with a smart orchestrator, GPT-5 mini micro-workers,
> and optional nested subagent delegation.

## Architecture

```
┌──────────────────────────────────────────────────────┐
│              Orchestrator (GPT-5.4)                   │
│  Owns: reasoning, decomposition, sequencing, state    │
│  Handles: user interaction, task splitting, merging    │
└────────┬─────────┬──────────┬─────────┬──────────────┘
         │         │          │         │
    ┌────▼───┐ ┌───▼────┐ ┌──▼───┐ ┌───▼─────┐
    │Research│ │ Spec   │ │Plan  │ │ Code    │   ← All GPT-5 mini
    │Worker  │ │ Writer │ │Writer│ │ Worker  │
    └────────┘ └────────┘ └──────┘ └─────────┘
    (parallel)  (focused)  (focused) (parallel)
```

### Design Principles

1. **Orchestrator thinks, workers execute** — All analysis, decision-making, and
   multi-step reasoning stays in the orchestrator (smart model). Workers get
   pre-digested, unambiguous instructions.

2. **Small tasks for small models** — Every worker task is designed to be
   achievable by GPT-5 mini in a single focused session. If something is too
   complex, the orchestrator splits it.

3. **Parallel by default** — Researchers run in parallel batches (2-4),
   code workers run in parallel batches (up to 5). The orchestrator merges results.

4. **Checkpoint-driven execution** — State is saved after every micro-step.
   Tasks can be split mid-execution. Context is never lost.

5. **Nested delegation is controlled** — When VS Code setting
   `chat.subagents.allowInvocationsFromSubagents` is enabled, v2 can use
   shallow nested delegation for broad research and blocked code lookups.
   The parent agent still owns synthesis and accountability.

## Workflow

The orchestrator drives all reasoning between spawns:

```
Step 1   → Entry detection (orchestrator)
Step 1.5 → Initialize (researchers → initializer)
Step 2   → Specify (researchers → orchestrator analysis → spec writer → reviewer)
Step 3   → Plan (researchers → orchestrator analysis → plan writer → reviewer)
Step 4   → Tasks (orchestrator analysis → task writer → reviewer)
Step 5   → Execute (orchestrator → parallel code workers → fix workers if needed)
Step 5.5 → Post-sync (initializer)
Step 5.7 → Wrap-up & commit (orchestrator)
Step 6   → Retrospective (orchestrator)
```

Nested delegation, when enabled, is intentionally limited:
- `SDD Researcher` may recursively split broad research questions
- `SDD Code Worker` may spawn one `SDD Researcher` for a blocked lookup
- Writers and reviewers remain single-hop for determinism

## Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `SpecDriven` | GPT-5.4 | Orchestrator — all reasoning and coordination |
| `SDD Initializer` | GPT-5 mini | Git, constitution, instruction files |
| `SDD Researcher` | GPT-5 mini | Read-only codebase exploration |
| `SDD Spec Writer` | GPT-5 mini | Writes spec.md from detailed brief |
| `SDD Plan Writer` | GPT-5 mini | Writes plan artifacts from detailed brief |
| `SDD Task Writer` | GPT-5 mini | Writes tasks.md from detailed brief |
| `SDD Code Worker` | GPT-5 mini | Executes single code task |
| `SDD Reviewer` | GPT-5 mini | Validates artifact quality |

## Installation

```bash
python3 install.py
```

To allow subagents to invoke further subagents in VS Code, enable:

```json
"chat.subagents.allowInvocationsFromSubagents": true
```

If this setting is off, v2 falls back to the original single-hop behavior.

Options:
- `--dry-run` / `-n` — preview without writing files
- Interactive model selection on first run

## Configuration

The install script offers presets:
1. **Premium orchestrator** — GPT-5.4 orchestrator, GPT-5 mini workers (recommended)
2. **Claude orchestrator** — Claude Sonnet 4.6 orchestrator, GPT-5 mini workers
3. **Budget** — All GPT-5 mini (not recommended for orchestrator)
4. **Default** — Keep current per-agent defaults
5. **Custom** — Choose per agent

## Usage

Invoke `@SpecDriven` in VS Code Copilot Chat with a feature description.

```
@SpecDriven Add user authentication with email/password
```

The orchestrator will guide you through: Specify → Plan → Tasks → Execute.
