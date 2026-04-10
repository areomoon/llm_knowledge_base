---
title: Three-Tier Memory Systems
tags: [agent, memory, FTS5, SQLite, context-engineering, tiered-memory, hermes, self-improving]
sources:
  - title: "Hermes Agent Memory Docs"
    url: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/
  - title: "Claude Code Source Leak: Three-Layer Memory Architecture"
    url: https://www.mindstudio.ai/blog/claude-code-source-leak-three-layer-memory-architecture
created: 2026-04-10
updated: 2026-04-10
---

# Three-Tier Memory Systems

> **TL;DR**: A structured approach to agent memory that separates in-session compression (Tier 1), cross-session searchable history (Tier 2), and persistent long-term knowledge (Tier 3) — balancing immediacy, recall breadth, and durability.

## Definition

A three-tier memory system stratifies an agent's knowledge by access pattern and persistence horizon. Rather than treating all memory as a single flat store (causing overflow or retrieval failure), each tier handles a distinct temporal scope. The pattern appears across multiple production agent frameworks (Hermes, Claude Code) with slightly different implementations at each tier.

## The Three Tiers

### Tier 1 — In-Session Context Compression

**What it stores**: The live conversation/task context for the current session.

**Mechanism**: As the session grows, older turns are automatically compressed or summarized. Only semantically relevant portions survive into the active window.

**Access pattern**: Always present; updated continuously during execution.

**Analogies**: Working memory, RAM, a whiteboard that gets erased as you run out of space.

**Key design trade-off**: Compression must preserve signal without brevity bias — see [ACE Framework](ace-framework.md) for how this failure mode is addressed via delta updates.

---

### Tier 2 — Cross-Session Full-Text Search

**What it stores**: Complete records of all past sessions, written to a persistent store.

**Mechanism in Hermes**: SQLite with FTS5 (full-text search extension). When the agent needs historical context, it queries by keyword; results are LLM-summarized before injection into the current context window — only the relevant excerpt arrives, not the full session.

**Mechanism in Claude Code**: Session transcript files on disk; loaded on-demand when a task pattern matches.

**Access pattern**: On-demand retrieval, not always loaded.

**Key advantage over RAG**: FTS5 avoids embedding model dependency and is exact-match reliable; trade-off is weaker semantic/fuzzy recall compared to vector search.

**Session lineage**: Hermes tracks parent/child relationships across compressions, and enforces per-platform isolation to prevent context bleed (e.g., Discord messages don't pollute Slack context).

---

### Tier 3 — Persistent Long-Term Knowledge

**What it stores**: Curated facts the agent should remember indefinitely + procedural knowledge (how to do things).

**Mechanism in Hermes**:
- `MEMORY.md` — agent-curated declarative memory with periodic nudges to update; structured as a lightweight index (each entry ≤150 chars)
- **Skill documents** — procedural memory ("when context looks like X, approach Y works"); separate from episodic records by design

**Mechanism in Claude Code**: `MEMORY.md` (L1 index) + per-topic `.md` files (L2 topic files).

**Access pattern**: `MEMORY.md` always loaded; skill/topic files loaded when relevant.

**Key design principle**: Separate *episodic* memory (what happened) from *procedural* memory (how to do it). Hermes uses Tier 2 for episodic, Tier 3 for procedural — preventing skill documents from being buried in session noise.

---

## Comparative Table

| Dimension | Tier 1 | Tier 2 | Tier 3 |
|-----------|--------|--------|--------|
| Scope | Current session | All past sessions | Permanent knowledge |
| Load strategy | Always active | On-demand search | Always loaded (index); on-demand (detail) |
| Hermes implementation | In-context compression | SQLite FTS5 | MEMORY.md + skill docs |
| Claude Code implementation | Active context window | Session transcript search | MEMORY.md + topic files |
| Failure mode if missing | Context overflow | No cross-session recall | Knowledge resets each session |
| Write trigger | Continuous | After each session | After validated learning |

## Comparison with Adjacent Approaches

### vs. Plain RAG

RAG (Retrieval-Augmented Generation) embeds all content in a vector store and retrieves by semantic similarity. Three-tier memory differs in:
- Tier 1 is not retrieved — it is the live context
- Tier 2 uses FTS5 (keyword) or file search, not semantic embeddings — simpler but exact-match dependent
- Tier 3 is *always* loaded (index portion), whereas RAG has no always-present layer

RAG is better for large heterogeneous corpora; three-tier memory is better for agent self-knowledge and session continuity.

### vs. Single MEMORY.md (Karpathy LLM Wiki Style)

A single persistent notes file (Karpathy's approach) is essentially Tier 3 only, maintained manually. Three-tier adds:
- Automatic Tier 1 compression (no manual pruning)
- Tier 2 search across history (no manual recall)
- Agent-curated updates to Tier 3 (instead of human-curated)

Hermes explicitly credits the Karpathy `MEMORY.md` concept as inspiration for Tier 3.

### vs. Traditional Context Window Management

Naive agents load everything into the context window until it overflows, then discard. Three-tier memory avoids this by routing knowledge to the appropriate tier on write, not scrambling at overflow time.

## When to Use

- Any agent that runs across multiple sessions with the same user or domain
- Scientific/research agents where past extraction results must be recallable (e.g., materials science literature agents)
- Multi-platform deployments where per-channel isolation is important
- Self-improving agents: Tier 3 skill docs enable compound gains across sessions

## Backlinks

- [Hermes Agent Architecture](hermes-agent-architecture.md) — Hermes is the primary reference implementation of this pattern
- [Tiered Memory](tiered-memory.md) — Claude Code's L1/L2/L3 is an instance of the three-tier pattern
- [ACE Framework](ace-framework.md) — ACE's evolving playbook maps to Tier 3 procedural memory
- [Agentic Harness](agentic-harness.md) — tiered memory is a core harness pattern
- [Evolving Playbooks](evolving-playbooks.md) — skill documents in Tier 3 implement the evolving playbook concept
- [derived: Hermes Agent Summary](../derived/2026-04-10-hermes-agent-summary.md)

## Sources

- [Hermes Agent Memory Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/)
- [Hermes Agent GitHub](https://github.com/NousResearch/hermes-agent)
- [Claude Code Source Leak: Three-Layer Memory Architecture](https://www.mindstudio.ai/blog/claude-code-source-leak-three-layer-memory-architecture)
