---
title: Agentic Harness
tags: [agent, harness, production-ai, context-compression, permission-gating, plan-work-review]
created: 2026-04-08
updated: 2026-04-08
sources:
  - title: "12 Agentic Harness Patterns from Claude Code"
    url: https://generativeprogrammer.com/p/12-agentic-harness-patterns-from
  - title: "Claude Code Source Leak: 7 Agent Architecture Lessons"
    url: https://particula.tech/blog/claude-code-source-leak-agent-architecture-lessons
  - title: "Claude Code Architecture Deep Dive"
    url: https://wavespeed.ai/blog/posts/claude-code-architecture-leaked-source-deep-dive/
---

# Agentic Harness

The infrastructure surrounding a simple LLM reasoning loop that makes it reliable in production — encompassing memory management, context compression, permission gating, tool orchestration, and workflow patterns.

## Overview

Analysis of Claude Code's leaked source (~512,000 lines of TypeScript) revealed a counterintuitive architectural truth: the core agent loop — the "agentic reasoning" — is trivially simple. It is a `while` loop over tool calls: reason → select tool → execute → observe → repeat. The complexity lies entirely in the **harness**: the infrastructure that makes that loop safe, efficient, and useful over extended sessions.

```
Agent = simple reasoning loop (dozens of lines)
Harness = everything else (hundreds of thousands of lines)
```

The harness has four responsibility areas:

1. **Memory & Context** — tiered storage, compression, scoped rules
2. **Workflow & Orchestration** — parallel execution, coordination patterns, quality cycles
3. **Tools & Permissions** — progressive discovery, gating, lifecycle hooks
4. **Infrastructure** — dynamic prompt assembly, feature flags, protocol standards

## 12 Harness Design Patterns

### Memory & Context

**Pattern 1 — Tiered Memory** (see [Tiered Memory](tiered-memory.md))
Three layers: always-loaded index (L1) → on-demand topic files (L2) → searchable session transcripts (L3). Self-healing: memory is verified before use, stale entries are auto-updated.

**Pattern 2 — Scoped Rules**
`CLAUDE.md` files are loaded hierarchically by directory. Each subdirectory overrides its parent. Enables domain-specific configurations without a monolithic config file.

**Pattern 3 — Context Compression**
Three-stage compression strategy to prevent context window exhaustion during long sessions:
- *MicroCompact*: continuous, local trimming of old tool output — zero API calls
- *AutoCompact*: triggered near context limit; preserves a 13,000-token buffer; generates up to 20,000-token structured summary
- *Full Reset*: extreme fallback; retains only the memory index and current task

### Workflow & Orchestration

**Pattern 4 — Parallel Fan-Out**
Independent sub-tasks are dispatched to concurrent agent instances. Risk: parallel branches writing to overlapping resources require merge conflict handling.

**Pattern 5 — Mailbox Pattern**
Worker agents cannot self-approve high-risk actions. Requests are queued to a coordinator's mailbox; the coordinator evaluates and approves or rejects. Prevents low-confidence outputs from propagating.

**Pattern 6 — Plan → Work → Review Cycle**
Self-contained quality loop: plan the approach → execute → review output for consistency and correctness → fix errors. More reliable than a bare ReAct loop for tasks requiring precision (e.g., scientific data extraction).

### Tools & Permissions

**Pattern 7 — Progressive Tool Discovery**
Default exposure: fewer than 20 tools. Additional tools are activated conditionally. Exposing 60+ tools simultaneously increases decision latency and selection errors.

**Pattern 8 — Three-Tier Permission Gating**
Permissions are embedded in the execution path, not layered as a UI overlay:
- *Allow*: execute silently (low-risk reads)
- *Prompt*: pause and request human confirmation (medium-risk writes, external API calls)
- *Deny*: block unconditionally (destructive operations)
Managed via `PermissionPolicy` with per-tool and path-specific overrides.

**Pattern 9 — PreToolUse / PostToolUse Hooks**
Lifecycle hooks intercept tool execution before and after the call. PreToolUse validates raw inputs (schema, safety); PostToolUse validates outputs (schema compliance, domain constraints). Acts as "deep packet inspection" for tool calls.

### Infrastructure

**Pattern 10 — MCP as Universal Tool Protocol**
The harness communicates with all tools via MCP: `tools/list` for discovery, `tools/call` for invocation, structured JSON for results. Enables any agent framework to connect to any tool without bespoke adapters.

**Pattern 11 — Dynamic System Prompt Assembly**
System prompts are assembled at runtime from parts:
1. Cached global instructions (shared across sessions)
2. CLAUDE.md rules (project-specific)
3. Current state (git status, date, task summary)
4. Conditionally loaded tools and memory index

Prompt cache boundary is placed after the static global section to maximize cache hit rate.

**Pattern 12 — Feature Flags**
Unreleased functionality is compiled into the binary but gated behind flags. Enables safe experimentation and gradual rollout without code branches.

## Key Takeaway

Building an agent is not the bottleneck. The harness that makes the agent production-grade — handling context overflow, permission enforcement, memory hygiene, and multi-agent coordination — is where the real engineering investment goes.

## Backlinks

- [Tiered Memory](tiered-memory.md) — detailed treatment of Pattern 1
- [derived: Claude Code Leak Architecture Insights](../derived/claude-code-leak-architecture-insights.md)

## Related Concepts

- [Tiered Memory](tiered-memory.md)
- [Context Engineering](context-engineering.md)
- [Agentic Self-Improvement](agentic-self-improvement.md)
- [ACE Framework](ace-framework.md)
- [Material Science Agents](material-science-agents.md)

## References

- [12 Agentic Harness Patterns from Claude Code](https://generativeprogrammer.com/p/12-agentic-harness-patterns-from) — full pattern catalog from source analysis
- [Claude Code Source Leak: 7 Agent Architecture Lessons](https://particula.tech/blog/claude-code-source-leak-agent-architecture-lessons)
- [Claude Code Architecture Deep Dive](https://wavespeed.ai/blog/posts/claude-code-architecture-leaked-source-deep-dive/)
- [Claude Code Three-Layer Memory Architecture](https://www.mindstudio.ai/blog/claude-code-source-leak-three-layer-memory-architecture)
