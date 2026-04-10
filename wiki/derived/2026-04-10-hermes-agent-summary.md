---
title: "Hermes Agent: Self-Improving Open-Source AI Agent Framework (Nous Research)"
type: repo
source_url: https://github.com/NousResearch/hermes-agent
raw_path: raw/articles/hermes-agent-nous-research.md
created: 2026-04-10
---

# Hermes Agent: Self-Improving Open-Source AI Agent Framework (Nous Research)

> **TL;DR**: Nous Research's Feb 2026 open-source agent framework that closes the learning loop — every task execution feeds back into a skill library and memory system, making the agent progressively more capable without model retraining.

## Key Points

- Released Feb 2026; 33K+ GitHub stars within two months; v0.7.0 "The Resilience Release" (Apr 2026) added security hardening
- Core mechanic: **Closed Learning Loop** — execute → self-evaluate → extract skill → store → retrieve on next similar task → refine
- **Three-tier memory**: Tier 1 (in-session compression), Tier 2 (SQLite FTS5 cross-session search with LLM summarization), Tier 3 (persistent `MEMORY.md` + skill documents)
- **Four core components**: AIAgent Loop (orchestration), Gateway (multi-platform routing: Telegram/Discord/Slack/WhatsApp/Signal/CLI), Tooling Runtime (6 backends incl. Singularity + Modal for HPC), Cron Scheduler
- **Model-agnostic**: Nous Portal, OpenRouter (200+ models), OpenAI, Kimi, MiniMax, custom endpoints
- **Self-hosted**: full data sovereignty; runnable on $5/month VPS (excl. LLM API costs)
- Optional **Honcho integration** (Plastic Labs) for high-fidelity user identity + dialectic modeling across 12 identity layers
- v0.7.0 security: credential pool rotation, secret exfiltration blocking, sandbox redaction, protected directory list, path traversal prevention

## Concepts Referenced

- [Hermes Agent Architecture](../concepts/hermes-agent-architecture.md) — full architecture breakdown and ACE mapping
- [Three-Tier Memory Systems](../concepts/three-tier-memory-systems.md) — comparative analysis of the three-tier pattern
- [ACE Framework](../concepts/ace-framework.md) — Hermes is the most complete open-source ACE implementation
- [Agentic Self-Improvement](../concepts/agentic-self-improvement.md) — Hermes as a production reference architecture
- [Evolving Playbooks](../concepts/evolving-playbooks.md) — MEMORY.md + skill library operationalizes this concept
- [Tiered Memory](../concepts/tiered-memory.md) — Hermes extends the L1/L2/L3 pattern with FTS5 at L2

## Notes

**ACE mapping**: Hermes makes the ACE Generator/Reflector/Curator abstraction concrete — the AIAgent Loop is the Generator, the self-evaluation step is the Reflector, and skill document creation/refinement is the Curator. The key production addition is infrastructure: multi-platform routing, 6 terminal backends, and SQLite FTS5 at the memory layer.

**Materials science relevance**: The Singularity and Modal backends directly address HPC deployment (common in computational materials). FTS5 cross-session recall is well-suited to remembering past extraction cases across thousands of papers. Self-hosting satisfies data sovereignty requirements for pharma/materials IP.

**Three-tier vs. Claude Code tiered memory**: Both use MEMORY.md as Tier 3 always-loaded index. Hermes distinguishes itself at Tier 2 by using SQLite FTS5 (vs. file-based session search), enabling richer cross-session queries at scale.
