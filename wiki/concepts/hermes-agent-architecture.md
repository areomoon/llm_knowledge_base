---
title: Hermes Agent Architecture
tags: [agent, self-improving, open-source, nous-research, memory, skills, closed-loop, FTS5]
sources:
  - title: "Hermes Agent GitHub"
    url: https://github.com/NousResearch/hermes-agent
  - title: "Hermes Agent Docs"
    url: https://hermes-agent.nousresearch.com/docs/
created: 2026-04-10
updated: 2026-04-10
---

# Hermes Agent Architecture

> **TL;DR**: Nous Research's open-source, self-hosted agent framework (Feb 2026) that implements a closed learning loop — executing tasks, evaluating results, extracting skills, and automatically applying them next time.

## Definition

Hermes Agent is a self-improving, self-hosted AI agent framework released by Nous Research in February 2026 (v0.7.0 as of April 2026). It embodies the principle that an agent should *grow with the user*: every task completed feeds into a skill library and memory system that makes the agent more capable on the next invocation. Crucially, it achieves this without model retraining — all adaptation lives in context and stored skill documents.

## How It Works

Hermes operates around a **Closed Learning Loop**:

```
Execute task
    ↓
Self-evaluate result
    ↓
Extract skill document (if valuable)
    ↓
Store in skill library (SQLite + MEMORY.md)
    ↓
Next similar task → retrieve & apply skill
    ↓
Refine skill based on new outcome
```

### Four Core Components

| Component | Role |
|-----------|------|
| **AIAgent Loop** | Synchronous orchestration engine: reasoning, tool execution, skill creation, self-evaluation |
| **Gateway** | Multi-platform message routing (Telegram, Discord, Slack, WhatsApp, Signal, CLI) into a single agent loop |
| **Tooling Runtime** | Six terminal backends: Local, Docker, SSH, Daytona, Singularity, Modal |
| **Cron Scheduler** | Runs recurring tasks in fresh sessions and delivers outputs automatically |

### Three-Tier Memory Architecture

Hermes implements a structured memory hierarchy — see [Three-Tier Memory Systems](three-tier-memory-systems.md) for full comparative analysis:

| Tier | Mechanism | Purpose |
|------|-----------|---------|
| **Tier 1** | In-session context compression | Keep current conversation relevant without overflow |
| **Tier 2** | SQLite FTS5 cross-session search | Full-text search over all past sessions; LLM-summarized before injection |
| **Tier 3** | Persistent `MEMORY.md` + skill documents | Long-term declarative memory + procedural knowledge |

Session lineage is tracked (parent/child across compressions), and per-platform isolation prevents context bleed between channels.

### Skill System

Skill documents follow a structured template: *"when context looks like this, this approach works."* Their lifecycle:

1. **Creation** — extracted automatically after complex task completion
2. **Discovery** — retrieved on next similar context via semantic/keyword match
3. **Refinement** — updated based on subsequent outcomes
4. **Versioning** — new successes produce updated skill versions

## Key Properties

- **No weight updates** — all adaptation is in context/skill files; deployable without retraining infrastructure
- **Model-agnostic** — supports Nous Portal, OpenRouter (200+ models), OpenAI, Kimi/Moonshot, MiniMax, z.ai/GLM, or any custom endpoint
- **Data sovereignty** — fully self-hosted; sensitive data never leaves user infrastructure
- **Low cost floor** — runnable on a $5/month VPS (excluding LLM API costs)
- **Security hardened** (v0.7.0): credential pool rotation, secret exfiltration blocking, sandbox output redaction, protected directories, path traversal prevention

## Relationship to ACE Framework

Hermes is the most complete open-source implementation of [ACE Framework](ace-framework.md) concepts:

| ACE Role | Hermes Equivalent |
|----------|-------------------|
| Generator | AIAgent Loop (task execution + reasoning trace) |
| Reflector | Self-evaluation step |
| Curator | Skill document creation + refinement |
| Evolving Playbook | Skills library + MEMORY.md |

The key difference: ACE is a *research framework* validated on benchmarks; Hermes is a *deployable system* with multi-platform routing, security hardening, and production infrastructure.

## Comparison with Managed Cloud Agents

| Dimension | Hermes | Managed Agents (e.g., Anthropic) |
|-----------|--------|----------------------------------|
| Hosting | Self-hosted | Managed cloud |
| Memory | SQLite FTS5 + MEMORY.md | Managed Memory Store |
| Model choice | Any provider | Provider-specific |
| Data control | Full | Provider-governed |
| Lock-in | Low | Medium |

Hermes is the self-hosted alternative for teams requiring data sovereignty or multi-model flexibility.

## When to Use

- Personal or small-team deployments where accumulated expertise should persist across sessions
- Environments with data sovereignty requirements (pharmaceuticals, materials R&D, legal)
- HPC/supercomputer workflows via Singularity or Modal backends
- Multi-platform teams needing a single agent loop across Slack, Discord, Telegram, etc.
- When you want the ACE self-improvement pattern without building the infrastructure yourself

## Backlinks

- [ACE Framework](ace-framework.md) — Hermes is the most complete open-source implementation of ACE concepts
- [Agentic Self-Improvement](agentic-self-improvement.md) — Hermes is a reference production architecture for context-based self-improvement
- [Three-Tier Memory Systems](three-tier-memory-systems.md) — Hermes implements the three-tier pattern with FTS5 at Tier 2
- [Evolving Playbooks](evolving-playbooks.md) — Hermes MEMORY.md + skill library operationalizes the evolving-playbook concept
- [Tiered Memory](tiered-memory.md) — Hermes extends the L1/L2/L3 pattern with SQLite FTS5 at L2
- [Harness Engineering](harness-engineering.md) — Hermes's closed learning loop is a concrete implementation of Harness Engineering
- [derived: Hermes Agent Summary](../derived/2026-04-10-hermes-agent-summary.md)

## Sources

- [Hermes Agent GitHub (NousResearch)](https://github.com/NousResearch/hermes-agent)
- [Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs/)
- [Architecture Guide](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture/)
- [Memory System Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/)
- [Skills Hub](https://hermes-agent.nousresearch.com/docs/skills)
