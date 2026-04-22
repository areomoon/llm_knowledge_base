---
title: Memory Stores vs RAG
tags: [memory, rag, context-engineering, agent, knowledge-management, comparison]
sources:
  - title: "ACE: Agentic Context Engineering (arXiv 2510.04618)"
    url: https://arxiv.org/abs/2510.04618
  - title: "Claude Managed Agents Memory (Anthropic Docs)"
    url: https://platform.claude.com/docs/en/managed-agents/memory
created: 2026-04-10
updated: 2026-04-10
---

# Memory Stores vs RAG

> **TL;DR**: Memory stores persist curated, structured knowledge across sessions as editable documents; RAG retrieves relevant chunks from a static index at query time. Both solve knowledge access, but for fundamentally different problems.

## Definition

Three dominant approaches to giving LLM agents access to knowledge beyond their context window:

1. **RAG (Retrieval-Augmented Generation)**: at query time, retrieve relevant chunks from a vector index and inject them into context
2. **Memory Store** (as in [Claude Managed Agents](claude-managed-agents.md)): a workspace-scoped collection of persistent text files that agents read before tasks and write to after — evolving across sessions
3. **Fine-tuning**: bake knowledge into model weights through supervised or RL training

This article focuses on the RAG vs. Memory Store distinction, with fine-tuning as a third reference point.

## Core Distinction

The fundamental difference is **when knowledge is created and how it changes**:

| Dimension | RAG | Memory Store | Fine-tuning |
|-----------|-----|-------------|-------------|
| Knowledge creation | At index build time | At session end (agent writes) | At training time |
| Knowledge update | Re-index (batch) | Append/edit (per session) | Retrain (expensive) |
| Update frequency | Low (periodic) | High (per task) | Very low |
| Format | Chunked embeddings | Human-readable documents | Weight deltas |
| Inspectable? | No (latent space) | Yes (markdown) | No |
| Evolves via agent? | No | Yes | Only via RL |
| Retrieval mechanism | Semantic similarity search | Explicit read or search by name | Always-on (weights) |
| Scope | Corpus-wide | Workspace / per-user / per-project | Model-wide |

## Three Converging Architectures

Three independent projects have converged on the Memory Store pattern from different starting points:

### 1. ACE Framework (Stanford / SambaNova, 2025)

The [ACE Framework](ace-framework.md)'s [Evolving Playbooks](evolving-playbooks.md) is a Memory Store avant la lettre:
- The Curator writes to the playbook after each task (like `memory_write`)
- The Generator reads the playbook before reasoning (like `memory_read` at session start)
- Grow-and-Refine = versioned append + periodic deduplication

ACE proved the concept works without any cloud infrastructure — just a markdown file in the system prompt.

### 2. Karpathy LLM Knowledge Base Pattern (2025)

Andrej Karpathy proposed the `raw/ + wiki/` pattern as an LLM-maintained knowledge base:
- `raw/` files are ingested sources (like RAG's corpus)
- `wiki/` files are the LLM-compiled, human-readable articles (like Memory Store files)
- The LLM acts as compiler: reads raw → synthesizes wiki
- The result is inspectable, editable, and accumulates over time

Key insight: the LLM shouldn't just retrieve from a static index — it should maintain a living document that it continuously improves. This repository implements this pattern.

### 3. Claude Managed Agents Memory Store (Anthropic, 2026)

Anthropic's Memory Store productizes ACE's playbook and Karpathy's wiki pattern into a managed cloud service:
- Versioned storage with full audit trail
- API-accessible by multiple agents and sessions
- Per-workspace, per-user, per-project scoping
- Automatic agent read at session start, write at session end
- Compliance-ready (redaction, access control)

The convergence: three teams arrived at "persistent, editable, agent-maintained documents" independently, suggesting this is the natural architecture for long-lived agent knowledge.

## When to Use Each

### Use RAG when:
- Knowledge corpus is large (millions of documents) and too big for context
- Knowledge is static or updated infrequently (academic literature, product catalogs)
- You need broad coverage over a fixed corpus
- The retrieval task is well-defined (find similar passages)

### Use Memory Store when:
- Knowledge is accumulated from agent experience over many sessions
- Knowledge needs to be inspectable and editable by humans (debugging, compliance)
- Multiple agents or users share the same evolving knowledge base
- You want the agent to contribute to the knowledge it reads (co-evolution)

### Use Fine-tuning when:
- The task distribution is stable and large-scale
- Inference cost is critical (baked-in knowledge is zero retrieval overhead)
- You want the model to improve at a specific skill (not just knowledge access)
- You have labeled training data at scale

### Hybrid architectures:
In practice, the most capable agents combine all three:
- **Fine-tuned base** for domain fluency (extraction skill, reasoning patterns)
- **RAG** for broad literature coverage (retrieve papers, experimental data)
- **Memory Store** for accumulated operational knowledge (extraction heuristics, playbook rules)

## Application to Material Science Extraction

For a Patsnap-style extraction service, the appropriate architecture:

```
Memory Store (evolving playbook)
├── extraction-heuristics.md    ← RLPR-reinforced rules from past sessions
├── per-material-class/
│   ├── oxides.md               ← domain-specific extraction patterns
│   ├── alloys.md
│   └── 2d-materials.md
└── confidence-calibration.md   ← when to flag for human review

RAG index
└── Literature corpus (Materials Project, Springer Materials, arXiv)

Fine-tuned model
└── QLoRA on (paper section → JSON) pairs
```

The Memory Store replaces a hand-coded extraction ruleset with one that the agent improves autonomously. The RAG index provides broad coverage. Fine-tuning provides extraction skill that doesn't need to be re-prompted each session.

## Failure Modes

**RAG failure modes:**
- **Retrieval miss**: relevant knowledge not retrieved (embedding space mismatch)
- **Chunk boundary loss**: key information split across chunks, neither retrieved
- **Stale index**: knowledge updated in source but not re-indexed

**Memory Store failure modes:**
- **Knowledge accumulation error**: if the agent writes incorrect lessons, they persist (requires audit)
- **Context overload**: too many memory files, agent reads selectively — important files may be skipped
- **Version explosion**: high-frequency writes with poor deduplication → many similar versions

**Fine-tuning failure modes:**
- **Distribution shift**: model fine-tuned on training distribution underperforms on new domains
- **Catastrophic forgetting**: fine-tuning on new task degrades base capability
- **Data quality sensitivity**: low-quality training data baked into weights permanently

## Backlinks

- [ACE Framework](ace-framework.md) — Evolving Playbooks are the ACE-specific Memory Store implementation
- [Evolving Playbooks](evolving-playbooks.md) — the delta-update mechanism Memory Stores build on
- [Context Engineering](context-engineering.md) — Memory Store is a context engineering strategy
- [Claude Managed Agents](claude-managed-agents.md) — Memory Store as a managed cloud primitive
- [Retrieval-Augmented Verification](retrieval-augmented-verification.md) — retrieval as verification rather than context
- [Tiered Memory](tiered-memory.md) — tiered memory is a complementary access pattern
- [ACE for Materials](ace-for-materials.md) — four-layer materials playbook as domain Memory Store
- [Agentic Self-Improvement](agentic-self-improvement.md) — Memory Store enables context-based self-improvement
- [RLPR (Reference Probability Reward)](rlpr-reference-probability-reward.md) — RLPR can generate signals used to update Memory Store content

## Sources

- [ACE: Agentic Context Engineering (arXiv 2510.04618)](https://arxiv.org/abs/2510.04618) — Evolving Playbooks as the original memory store pattern
- [Claude Managed Agents Memory](https://platform.claude.com/docs/en/managed-agents/memory) — production implementation with versioning and scoping
