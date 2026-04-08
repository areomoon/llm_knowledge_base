---
title: Context Engineering
tags: [context-engineering, prompt-engineering, agent, llm]
created: 2026-04-08
updated: 2026-04-08
sources:
  - title: "ACE: Agentic Context Engineering (arXiv)"
    url: https://arxiv.org/abs/2510.04618
---

# Context Engineering

The practice of systematically designing, managing, and evolving the context provided to an LLM to control and improve its behavior — extending prompt engineering from a one-time craft into a continuous, structured process.

## Overview

Prompt engineering treats context as a static artifact: a developer writes a prompt, tests it, and ships it. Context engineering recognizes that the optimal context for a task is neither known upfront nor stable; it must be discovered and refined through experience.

Context engineering encompasses:

1. **Structure** — organizing context (instructions, examples, memory, tools) to maximize signal and minimize noise
2. **Compression** — summarizing prior interactions without losing critical insight
3. **Evolution** — updating context based on observed outcomes, accumulating strategy over time

The discipline gained prominence as LLM systems moved from single-shot queries toward long-horizon agentic tasks, where context grows in size and the cost of naive management (truncation, naive summarization) becomes measurable.

## Key Ideas

- **Context as the primary lever**: without fine-tuning access, context is the only writable surface for improving a deployed model's behavior
- **Brevity Bias risk**: naive compression (e.g., "summarize to 500 tokens") discards domain-specific insights that were expensive to discover
- **Context Collapse risk**: full rewrites of context destroy accumulated detail; prefer delta updates
- **Separation of concerns**: good context engineering distinguishes system instructions, task-specific playbooks, episodic memory, and retrieved knowledge

## Relationship to Adjacent Concepts

| Concept | Distinction |
|---------|------------|
| Prompt Engineering | Context engineering is the ongoing, systematic extension; prompt engineering is typically one-time |
| RAG | RAG retrieves relevant context at query time; context engineering maintains and evolves persistent context |
| Fine-tuning | Fine-tuning bakes knowledge into weights; context engineering keeps knowledge in the context window |
| [Evolving Playbooks](evolving-playbooks.md) | The specific mechanism ACE uses to implement context evolution |

## Backlinks

- [ACE Framework](ace-framework.md) — implements context engineering via evolving playbooks
- [Evolving Playbooks](evolving-playbooks.md) — the specific mechanism for context evolution
- [Agentic Self-Improvement](agentic-self-improvement.md) — self-improvement requires context engineering
- [Tiered Memory](tiered-memory.md) — tiered memory is a context engineering pattern
- [Agentic Harness](agentic-harness.md) — harness implements context management at scale
- [derived: ACE Agentic Context Engineering](../derived/ace-agentic-context-engineering.md)
- [derived: Claude Code Leak Architecture Insights](../derived/claude-code-leak-architecture-insights.md)
- [derived: Gemini 諮詢：Patsnap 職涯決策全紀錄](../derived/gemini-career-decision-patsnap.md)
- [derived: ChatGPT 諮詢：Patsnap 面試準備與職涯策略](../derived/chatgpt-patsnap-interview-strategy.md)

## Related Concepts

- [ACE Framework](ace-framework.md)
- [Evolving Playbooks](evolving-playbooks.md)
- [Agentic Self-Improvement](agentic-self-improvement.md)
- [Tiered Memory](tiered-memory.md)
- [Agentic Harness](agentic-harness.md)

## References

- [ACE: Agentic Context Engineering (arXiv 2510.04618)](https://arxiv.org/abs/2510.04618) — formalizes context engineering in the agentic setting and identifies brevity bias and context collapse as failure modes
