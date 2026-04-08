---
title: "Claude Code Leak Architecture Insights"
source_type: article
source_url: https://generativeprogrammer.com/p/12-agentic-harness-patterns-from
ingested: 2026-04-08
compiled: 2026-04-08
tags: [agent, harness, memory, context-compression, mcp, permission-gating]
---

# Claude Code Leak Architecture Insights

> **TL;DR**: The March 2026 accidental leak of Claude Code's 512,000-line TypeScript source revealed that production agent complexity lives in the *harness* — memory management, context compression, permissions, and tool orchestration — not in the LLM loop itself, which is a trivial while-loop.

## Key Points

- Claude Code's agent loop is ~dozens of lines; the surrounding harness is 512K lines across utils/, services/, components/, tools/ — complexity ratio is ~100:1 harness to agent
- **12 harness patterns** in 4 categories: Memory & Context (Tiered Memory, Scoped Rules, Context Compression); Workflow (Parallel Fan-Out, Mailbox Pattern, Plan→Work→Review); Tools & Permissions (Progressive Tool Discovery, Three-Tier Permission Gating, PreToolUse/PostToolUse Hooks); Infrastructure (MCP Universal Protocol, Dynamic System Prompt Assembly, Feature Flags)
- **Tiered memory (L1/L2/L3)**: MEMORY.md index always loaded; topic files on-demand; session transcripts only on search — with self-healing validation before use
- **Three-stage context compression**: MicroCompact (continuous, local trim) → AutoCompact (near-limit, structured 20K-token summary) → Full Reset (extreme fallback)
- **Three-tier permission gating**: Allow / Prompt / Deny — embedded in execution path, not a UI overlay; managed via PermissionPolicy with per-tool and path-specific overrides
- **Progressive tool discovery**: fewer than 20 tools exposed by default; 40+ additional tools loaded conditionally — large tool sets increase selection errors
- **Dynamic system prompt**: assembled from cached global instructions + scoped CLAUDE.md rules + runtime state + conditional tool list; cache boundary maximizes token reuse
- **Hidden features found**: KAIROS (persistent background daemon), Proactive Mode (agent acts without explicit instruction), BUDDY (AI companion system) — reveal the direction toward always-on autonomous agents

## Extracted Concepts

- [Agentic Harness](../concepts/agentic-harness.md)
- [Tiered Memory](../concepts/tiered-memory.md)
- [Context Engineering](../concepts/context-engineering.md)
- [ACE Framework](../concepts/ace-framework.md)

## Raw Source

`raw/areomoon_career_llm/Claude_Code_Leak_Architecture_Insights.md`
