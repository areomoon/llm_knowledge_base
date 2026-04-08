---
title: Evolving Context Accumulation
tags: [agent-design, context-management, memory, agentic-ai, rlhf-adjacent]
created: 2026-04-08
updated: 2026-04-08
sources:
  - title: "career-ops: AI Job Search Pipeline"
    url: https://github.com/santifer/career-ops
  - title: "ACE: Adaptive Contextual Enrichment (pattern)"
    url: https://github.com/anthropics/anthropic-cookbook
---

# Evolving Context Accumulation

A design pattern where an AI agent's effective capability improves over time through the systematic accumulation of user-specific context in structured files, without model retraining or fine-tuning.

## Overview

Evolving Context Accumulation solves a fundamental limitation of stateless LLM interactions: each session starts with the same base capability, regardless of prior interactions. The pattern addresses this by maintaining a set of **append-only or incrementally-updated files** that grow richer with each agent invocation.

Unlike fine-tuning (which modifies model weights) or RAG (which retrieves from a fixed corpus), this pattern accumulates context that is:
- **User-specific**: reflects this particular user's experience, preferences, and history
- **Interaction-derived**: grows directly from the agent doing its job
- **Immediately available**: loaded into context at the start of each session
- **Human-readable and editable**: stored as Markdown/YAML, inspectable and correctable by the user

The canonical implementation is career-ops's `interview-prep/story-bank.md` — a file that accumulates STAR+R interview stories across evaluations. After 10 job evaluations, the agent has a rich bank of 5-10 master stories it can adapt to any behavioral question. The agent gets measurably better at interview prep not because it learned anything new, but because the context it operates on has grown more complete.

## Key Ideas

- **Append-only accumulation**: files like `story-bank.md` and `article-digest.md` only grow — each evaluation adds new entries, building a corpus of reusable material that improves future evaluations
- **Progressive personalization**: `config/profile.yml` and `modes/_profile.md` deepen over time as the agent learns the user's preferences, deal-breakers, and narrative framing — early evaluations are generic, later ones are highly calibrated
- **Interaction as training data**: every user correction ("this score is too high", "you missed that I have experience in X") is an opportunity to update the profile files — the agent incorporates feedback immediately
- **Dedup and integrity**: accumulation without discipline creates noise; patterns like `scan-history.tsv` (prevents re-scanning seen offers) and `merge-tracker.mjs` (deduped tracker merges) keep accumulated context clean
- **Session initialization**: at the start of each session, the agent reads all accumulation files — the cognitive overhead of "remembering" is eliminated because memory is externalized into the filesystem
- **The onboarding metaphor**: career-ops explicitly frames this as onboarding a recruiter — *"the first week they need to learn about you, then they become invaluable"* — setting correct user expectations about the accumulation curve

## Accumulation File Taxonomy

| File | Accumulation Type | Grows When |
|------|------------------|------------|
| `interview-prep/story-bank.md` | Append new STAR+R stories | After each evaluation (Block F) |
| `article-digest.md` | Append proof points and case studies | User shares new achievements |
| `config/profile.yml` | Update preferences and narrative | User corrects or deepens profile |
| `modes/_profile.md` | Update archetypes and framing | User requests customization |
| `data/applications.md` | Append tracked applications | After each evaluation (via TSV merge) |
| `data/scan-history.tsv` | Append seen offer URLs | After each portal scan |
| `reports/` | Append evaluation reports | After each evaluation |

## STAR+R as Accumulation Primitive

The STAR+R story format (Situation, Task, Action, Result, Reflection) is particularly effective as an accumulation primitive because:

1. **Structured**: each story has the same schema, making the bank searchable and composable
2. **Reusable**: one master story can answer dozens of different behavioral questions by adjusting framing
3. **Seniority signal**: the Reflection column captures lessons learned, distinguishing senior (extracts principles) from junior (describes events) responses
4. **Cross-context**: a story about a product launch can be adapted for "tell me about a time you managed stakeholders", "tell me about a technical decision", or "tell me about a failure"

## Relationship to Other Memory Patterns

| Pattern | Mechanism | Scope | Persistence |
|---------|-----------|-------|-------------|
| Evolving Context Accumulation | Structured files, session-loaded | User-specific | Cross-session, same repo |
| RAG | Vector retrieval from corpus | General or domain | Cross-session, separate store |
| Fine-tuning | Weight updates | Model-level | Permanent, requires retraining |
| In-context learning | Examples in prompt | Task-specific | Single session only |
| Agent memory (MemGPT-style) | LLM manages its own memory files | Agent-level | Cross-session, managed by LLM |

Evolving Context Accumulation is closest to Agent memory patterns but is simpler: the files are managed by explicit agent actions (append after evaluation) and human edits, not by the LLM autonomously deciding what to remember.

## Related Concepts

- [Skill Modes Pattern](skill-modes-pattern.md)
- [Agent-Friendly Design](agent-friendly-design.md)
- [API to SuperAgent Paradigm Shift](api-to-superagent.md)

## References

- [career-ops GitHub Repository](https://github.com/santifer/career-ops) — reference implementation; see `interview-prep/story-bank.md`, `article-digest.md`, `modes/_profile.md`
- [career-ops case study](https://santifer.io/career-ops-system) — author's account of using accumulation to improve evaluation quality over 740+ offers
