---
title: Tiered Memory
tags: [agent, memory, context-engineering, harness, self-healing]
created: 2026-04-08
updated: 2026-04-08
sources:
  - title: "Claude Code Source Leak: Three-Layer Memory Architecture"
    url: https://www.mindstudio.ai/blog/claude-code-source-leak-three-layer-memory-architecture
  - title: "Claude Code Architecture Deep Dive"
    url: https://wavespeed.ai/blog/posts/claude-code-architecture-leaked-source-deep-dive/
---

# Tiered Memory

A three-layer memory architecture for LLM agents that balances always-available context with on-demand depth and searchable history, avoiding both context overflow and knowledge loss.

## Overview

Naive agent memory strategies fail at scale in one of two ways: storing everything in the context window (overflow) or offloading everything to a retrieval index (latency, retrieval failures). Tiered memory addresses both by stratifying knowledge by access frequency.

The architecture has three layers:

| Layer | Mechanism | Load Strategy | Analogy |
|-------|-----------|--------------|---------|
| **L1 — Memory Index** | Lightweight index file (each line ≤150 chars, max 200 lines) | **Always loaded** | Working memory |
| **L2 — Topic Files** | Per-topic detail files | **On-demand** when task matches | Notebook on desk |
| **L3 — Session Transcripts** | Full conversation history on disk | **Search-only** retrieval | Library archive |

Claude Code implements this as `MEMORY.md` (L1) + per-topic `.md` files (L2) + session transcript store (L3).

## Self-Healing Memory

Tiered memory systems treat their own cached knowledge as **unreliable by default**. Before acting on a remembered fact, the agent verifies it is still true:

- Remembered file path → check file exists before referencing
- Remembered function name → grep for it before calling it
- Remembered configuration → read the current file, don't assume

Stale memory entries are updated or deleted rather than left to mislead future sessions. This prevents the "confident but wrong" failure mode common in agents with persistent but unvalidated memory.

## Design Principles

- **Index for navigation, not content**: L1 holds pointers and one-line descriptions — enough to decide whether to load L2, not enough to answer questions from L1 alone
- **Semantic partitioning**: L2 files are organized by topic (not chronologically), so a task about memory management loads only the memory file
- **Context budget awareness**: L1's strict size limit (200 lines × 150 chars ≈ 30,000 chars) ensures it never overflows the context window even at minimum LLM sizes
- **Write-on-learn, not write-on-observe**: only information that will be relevant in future sessions is persisted; transient task state is not written to memory

## Application to Scientific Document Agents

For agents processing large volumes of scientific papers, the three-layer mapping is:

| Tier | Content |
|------|---------|
| L1 | Index of processed papers (title, key finding, date, status) |
| L2 | Per-paper extraction results (parameters, tables, figures summary) |
| L3 | Full extracted text, raw tool outputs, conversation logs |

The L1 index lets the orchestrator agent instantly know which papers are processed and what was found, without loading gigabytes of L3 content.

## Backlinks

- [Agentic Harness](agentic-harness.md) — tiered memory is Pattern 1 of the harness
- [derived: Claude Code Leak Architecture Insights](../derived/claude-code-leak-architecture-insights.md)
- [derived: Managed Agents × Material Science 架構設計](../derived/managed-agents-material-science-architecture.md)

## Related Concepts

- [Agentic Harness](agentic-harness.md)
- [Context Engineering](context-engineering.md)
- [Evolving Playbooks](evolving-playbooks.md)

## References

- [Claude Code Source Leak: Three-Layer Memory Architecture](https://www.mindstudio.ai/blog/claude-code-source-leak-three-layer-memory-architecture) — detailed analysis of Claude Code's L1/L2/L3 implementation
- [Claude Code Architecture Deep Dive](https://wavespeed.ai/blog/posts/claude-code-architecture-leaked-source-deep-dive/) — full source analysis
