---
title: Harness Engineering
tags: [harness-engineering, LLM, context-engineering, prompt-engineering, agent, workflow, NTU, hung-yi-lee]
created: 2026-04-13
updated: 2026-04-13
sources:
  - title: "Harness Engineering：有時候語言模型不是不夠聰明，只是沒有人類好好引導"
    url: https://www.youtube.com/watch?v=R6fZR_9kmIw
    author: Hung-yi Lee (李宏毅), NTU
    date: 2026-04-13
---

# Harness Engineering

The discipline of systematically guiding LLMs to their full potential — not by improving the model itself, but by engineering the context, workflow, and feedback loops around it. Coined/popularized by NTU Professor Hung-yi Lee (李宏毅) in 2026.

> 「有時候語言模型不是不夠聰明，只是沒有人類好好引導」  
> ("Sometimes language models are not unintelligent — they just haven't been properly guided by humans")

## Core Thesis

The capability ceiling of modern LLMs is rarely the bottleneck. The bottleneck is how humans and systems *harness* those capabilities. Harness Engineering is the answer to: **given a powerful LLM, how do you extract reliable, high-quality output for a specific task?**

This is distinct from:
- **Prompt Engineering** — single-shot instruction design (narrow scope)
- **Fine-tuning** — changing model weights (expensive, inflexible)
- **Context Engineering** — designing what goes into the context window (a sub-discipline of Harness Engineering)

## What Harness Engineering Encompasses

1. **Context Design** — what information to provide, in what format, and when
2. **Agent Workflow** — how to decompose tasks, sequence steps, and route outputs
3. **Feedback Loops** — how to evaluate outputs and feed results back to improve future runs
4. **Evaluation** — defining what "good output" means and measuring against it
5. **Memory & State** — accumulating knowledge across sessions so the agent improves over time

## Relationship to Other Concepts

### Harness Engineering ⊃ Context Engineering
[Context Engineering](context-engineering.md) focuses on *what goes in the context window*. Harness Engineering is broader — it also includes the workflow orchestration, evaluation mechanisms, and feedback loops that sit outside the context itself.

### Harness Engineering ≈ ACE Framework (in practice)
The [ACE Framework](ace-framework.md) (Agentic Context Engineering) is an instantiation of Harness Engineering for self-improving agents:
- Generator-Reflector-Curator roles = structured harness for task execution + quality feedback
- Evolving Playbook = the accumulated harness strategy for a specific task domain

### Harness Engineering → Hermes Agent
[Hermes Agent Architecture](hermes-agent-architecture.md) implements Harness Engineering as a closed learning loop:
- Skill documents = machine-readable harness strategies for specific task types
- MEMORY.md = the persistent harness state across sessions
- FTS5 transcript search = retroactive harness improvement via past session analysis

### Harness Engineering ⊃ Agentic Self-Improvement
[Agentic Self-Improvement](agentic-self-improvement.md) describes how agents improve task performance from experience. This is the temporal/longitudinal axis of Harness Engineering — how the harness gets better over time without retraining the model.

## The Hierarchy

```
Harness Engineering (broadest — how you guide LLMs)
├── Context Engineering (what's in the window)
│   ├── Prompt Engineering (instruction design)
│   └── Memory & RAG (what to retrieve)
├── Workflow Engineering (how steps are orchestrated)
│   ├── Agent Loops (ReAct, Plan-Act-Observe)
│   └── Multi-Agent Coordination (fan-out, mailbox)
└── Feedback Engineering (how outputs improve future runs)
    ├── Evaluation (what's good)
    └── Evolving Playbooks (delta updates to strategy)
```

## Application to areomoon's Work

For the **Material Science Extraction Agent**, every design decision is a Harness Engineering decision:
- How the paper is chunked and presented = context design
- The Generator → Reflector → Curator pipeline = workflow design
- The evolving extraction schema = feedback loop
- The ACE playbook = accumulated harness strategy

The extraction agent isn't "doing AI" — it's harnessing AI.

## Notes from the Lecture

- **1:25:50**: Anthropic Haiku 3.5 API has been retired; experiments use Open Router
- Lecture is 1:32:21 in length, 3,036 views within first 5 hours of release (2026-04-13)
- Part of a broader NTU 生成式AI 2025 lecture series

## Backlinks

- [ACE Framework](ace-framework.md) — Harness Engineering instantiated as a three-role self-improving loop
- [Context Engineering](context-engineering.md) — the context-window sub-discipline of Harness Engineering
- [Agentic Self-Improvement](agentic-self-improvement.md) — how harnesses improve over time
- [Hermes Agent Architecture](hermes-agent-architecture.md) — open-source closed-learning-loop as Harness Engineering implementation

## Related Concepts

- [ACE for Materials](ace-for-materials.md)
- [Evolving Playbooks](evolving-playbooks.md)
- [Agentic Harness](agentic-harness.md) — infrastructure harness (memory, compression, permissions)
- [Material Science Agents](material-science-agents.md)

## References

- [Harness Engineering lecture (YouTube)](https://www.youtube.com/watch?v=R6fZR_9kmIw) — Hung-yi Lee, NTU, 2026-04-13
- [raw note](../raw/articles/harness-engineering-hungyi-lee.md)
