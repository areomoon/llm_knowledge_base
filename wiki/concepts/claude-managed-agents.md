---
title: Claude Managed Agents
tags: [agent, infrastructure, harness, memory-store, anthropic, beta, cloud]
sources:
  - title: "Claude Managed Agents Overview (Anthropic Docs)"
    url: https://platform.claude.com/docs/en/managed-agents/overview
  - title: "Claude Managed Agents Memory (Anthropic Docs)"
    url: https://platform.claude.com/docs/en/managed-agents/memory
created: 2026-04-10
updated: 2026-04-10
---

# Claude Managed Agents

> **TL;DR**: Anthropic's managed cloud service that packages the agent harness (session orchestration, tool execution, memory stores) so developers define the agent, not the infrastructure.

## Definition

Claude Managed Agents (beta header: `managed-agents-2026-04-01`) is Anthropic's cloud service that turns Claude Code's agent harness into a managed API product. Instead of building agent loops, sandboxes, and tool execution yourself (as with the raw Messages API), you define the agent's configuration and the platform handles orchestration, long-running execution, and memory persistence.

It is the first Anthropic product that makes [Evolving Playbooks](evolving-playbooks.md) and tiered agent memory first-class cloud primitives — not just patterns to implement yourself.

## Core Architecture

Four primitive concepts:

| Concept | Description |
|---------|-------------|
| **Agent** | Model + system prompt + tools + MCP servers + skills — the "what" |
| **Environment** | Cloud container template with pre-installed packages, network rules, mounted files — the "where" |
| **Session** | A running instance of an Agent in an Environment executing a specific task — the "when" |
| **Events** | SSE messages between the application and the session (user turns, tool results, status updates) — the "how" |

## Session Lifecycle

```
1. Create Agent    →  Define model, system prompt, tools, MCP servers
2. Create Environment → Configure container (packages, network, files)
3. Start Session   →  Instantiate Agent in Environment for a task
4. Send Events     →  Stream user turns; receive tool calls and responses via SSE
5. Steer/Interrupt →  Mid-session guidance or cancellation
6. Session end     →  Agent writes learned lessons to Memory Store
```

## Built-in Tools

The platform provides standard tool implementations out of the box:

- `bash` — shell command execution
- `read`, `write`, `edit` — file operations
- `glob`, `grep` — filesystem search
- `web_fetch`, `web_search` — web access
- MCP servers — external service connectors
- Custom tools — user-defined via tool definitions

## Memory Store (Research Preview)

Memory Store is the highest-leverage feature: a workspace-scoped collection of versioned text documents that the agent automatically reads before task start and writes to on task completion.

**Key properties:**
- Maximum 100KB per memory file (~25K tokens)
- Immutable versioning — all writes create new versions (full audit trail, rollback support)
- Read-only and read-write modes per file
- Maximum 8 memory stores per session
- Redaction support for compliance use cases
- Scoping: per-workspace, per-user, per-team, or per-project

**Memory tools** available to the agent:
`memory_list`, `memory_search`, `memory_read`, `memory_write`, `memory_edit`, `memory_delete`

**Recommended file structure:**
Multiple small topic files rather than a few large files — mirrors the [Tiered Memory](tiered-memory.md) pattern and prevents single-file context overload.

## Relationship to ACE Framework

Managed Agents is a managed product implementation of the [ACE Framework](ace-framework.md)'s theoretical architecture:

| ACE Concept | Managed Agents Equivalent |
|------------|--------------------------|
| Generator | Session execution (reasoning + tool calls) |
| Reflector | End-of-session self-check before memory write |
| Curator | `memory_write` / `memory_edit` operations |
| Evolving Playbook | Memory Store (versioned, persistent, multi-file) |
| Grow-and-Refine | Memory versioning + append-only write pattern |

The implication: a team that has been hand-implementing ACE's Curator with custom code can migrate to Memory Store as a managed backend with versioning and multi-session access built in.

## Comparison with Messages API

| Dimension | Messages API | Managed Agents |
|-----------|-------------|----------------|
| Control level | Full (build your own loop) | Partial (configure the harness) |
| Suitable for | Custom agent loops, fine-grained control | Long-running tasks, async execution |
| What you build | Agent loop, sandbox, tool execution | Agent definition + environment |
| Memory | Manual (implement RAG or context injection) | Built-in Memory Store |
| Multi-session learning | Manual | Automatic via Memory Store |

## Relationship to Karpathy LLM Knowledge Base Pattern

Andrej Karpathy's `raw/ + wiki/` knowledge base architecture (as implemented in this repository) maps onto Managed Agents:

| KB Pattern | Managed Agents Equivalent |
|-----------|--------------------------|
| `raw/` files | Incoming task inputs per session |
| `wiki/` compiled articles | Memory Store files |
| `scripts/ingest.py` | Session tool execution |
| LLM-as-compiler (compile task) | Agent auto-reads/writes memory |
| Lint + cross-link | End-of-session memory update + dedup |

Key difference: Managed Agents runs in the cloud and is API-first; the KB pattern runs locally and is file-first.

## Current Limitations (Beta)

- Beta header required: `managed-agents-2026-04-01`
- Memory, multi-agent orchestration, and outcomes features are in Research Preview
- Rate limits: create 60 sessions/min, read 600/min
- No public SLA for Research Preview features

## Implications for Material Science Agent Architecture

For a Patsnap-style extraction service:

1. **Infrastructure replacement**: Managed Agents replaces a custom LangChain/LangGraph harness with a managed service — lower operational burden, faster prototype-to-production
2. **Evolving extraction playbook**: Memory Store natively implements the ACE Curator's playbook without custom code — use memory files for extraction heuristics, per-material-class rules, and confidence calibration data
3. **QLoRA timing shift**: memory-based learning is available from day 1; QLoRA fine-tuning (currently planned for Months 3–4) may be deferred until memory-based improvements plateau
4. **Architecture differentiation**: proposing Managed Agents as the extraction service backbone is a concrete technical vision that differentiates from teams using generic orchestration frameworks

See also: [Memory Stores vs RAG](memory-stores-vs-rag.md) for how Memory Store compares to retrieval-augmented approaches.

## Backlinks

- [ACE Framework](ace-framework.md) — Managed Agents is the managed product realization of ACE's theoretical GRC architecture
- [Agentic Harness](agentic-harness.md) — Managed Agents is a cloud-hosted agentic harness
- [Evolving Playbooks](evolving-playbooks.md) — Memory Store implements evolving playbooks as a managed cloud primitive
- [Tiered Memory](tiered-memory.md) — Memory Store multi-file pattern maps to tiered memory architecture
- [ACE for Materials](ace-for-materials.md) — Managed Agents + Memory Store can host the materials extraction service
- [Memory Stores vs RAG](memory-stores-vs-rag.md) — comparative analysis of memory approaches
- [RLPR (Reference Probability Reward)](rlpr-reference-probability-reward.md) — fine-tuned models can run within Managed Agent sessions
- [derived: Managed Agents Career Impact](../derived/managed-agents-career-impact.md)

## Sources

- [Claude Managed Agents Overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [Claude Managed Agents Memory](https://platform.claude.com/docs/en/managed-agents/memory)
- [Claude Managed Agents Tools](https://platform.claude.com/docs/en/managed-agents/tools)
