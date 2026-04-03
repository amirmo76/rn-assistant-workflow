# Figma-to-React-Native Spec Driven Agentic Workflow (Branch A)

## System Overview

This system implements a Spec-Driven, Component-Driven Development pipeline powered by AI agents. It serves as "Branch A" (Visuals) in a Y-shaped development architecture. Its sole purpose is to translate Figma designs into isolated, strictly presentational React Native components and Storybook files.

By completely separating UI generation from application logic ("Branch B") and enforcing a **Contract-First** workflow, we prevent LLM context bloat, eliminate design hallucination, and produce highly reusable, self-documenting code.

## Core Architectural Principles

### 1. Contarct-First Spec-Driven Development

The system does not write code directly from Figma JSON. Instead, a `spec_writer` agent analyzes the design data and generates a strict Contract (`spec.md`). The coding agents only execute against this approved specification.

### 2. The `.ui-state` Directory (Design State Management)

* **What:** The system saves intermediate JSON extractions (e.g., `home-tree.json`, `Button.json`) to a `.ui-state` folder committed to the repository.
* **How:** The directory structure:

```
.ui-state/
  pages/
  components/
```

### 3. "Dumb" Controlled Components

UI components must not contain internal state logic for interactive elements (e.g., no `useState` for a dropdown or modal). All interactivity must be passed up to the parent via props (e.g., `isOpen`, `onClose`).

### 4. Template-Driven Token Taxonomy

Agents are forbidden from writing raw hardcoded styles (e.g., `#0F172A` or `15px`). All raw values must be mapped to a strict semantic taxonomy (e.g., `colors.slate[900]` or `spacing.md`) and injected into a central `design-system.ts` file.

---

## Agent Definitions

The system utilizes specialized domain agents, strictly separated by read/write capabilities to prevent hallucination and execution drift.

## Workflow

figma_mapper -> figma_extractor -> token_syntesizer -> design_guardian -> spec_writer -> planner -> tasker -> executor