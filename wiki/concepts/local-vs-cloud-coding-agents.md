---
title: Local vs Cloud Coding Agents
tags: [agent, agentic-harness, deployment-model, devin, codex, claude-code, cursor, hook-surface]
sources: [wiki/queries/2026-04-20-rtk-local-vs-cloud-agents.md]
created: 2026-04-20
updated: 2026-04-20
---

# Local vs Cloud Coding Agents

> **TL;DR**: Coding agents split by **where shell execution happens**, not where the UI lives — local agents (Claude Code, Cursor, Aider) run commands on your machine and can be hooked; cloud agents (Devin by Cognition, OpenAI Codex, Replit Agent) run commands in vendor-controlled VMs and cannot accept user-installed binaries or hooks like [RTK Token Killer](rtk-token-killer.md).

## Definition

The **deployment axis** that matters for [agentic harness](agentic-harness.md) extensibility is the **shell execution locus** — the machine on which the agent's tool calls (bash, file I/O, package installs) actually run. LLM inference is almost always cloud-side (Anthropic / OpenAI GPUs) and does not determine this classification. The correct question is *"whose machine does `git push` run on?"*, not *"whose GPU does the model run on?"*.

## The Classification

| | Local agent | Cloud agent |
|---|---|---|
| **Examples** | Claude Code (Anthropic), Cursor, Aider, GitHub Copilot CLI, Gemini CLI | Devin (Cognition), OpenAI Codex, Replit Agent, v0 (Vercel), GitHub Codespaces-hosted Copilot |
| **Shell execution** | User's machine | Vendor-managed VM / container |
| **Filesystem** | User's working directory | Vendor sandbox, often ephemeral |
| **User can install binaries into the exec env** | Yes | No |
| **User can edit agent settings / hooks** | Yes (`~/.claude/settings.json`, `.cursor/hooks.json`) | No — only prompt-level config |
| **Works offline** | Inference offline: no; shell: yes with cached models | No |
| **`ps` shows the agent process** | Yes | No |

## The "Local IDE → Cloud Agent" Nuance

A common confusion: a user may open **Devin or Codex from a local IDE / web tab on their own machine**, and assume this makes it a local agent. It does not. The IDE is a **remote control**; the agent's shell commands still execute in the vendor VM. Diagnostic heuristics:

1. **Unplug the network — does the agent still run?** If no, cloud.
2. **Does `ps aux | grep <agent>` on your machine show the agent process?** If no, cloud.
3. **Can you `cat` a file the agent just wrote without syncing?** If no, cloud.

GitHub Codespaces + Copilot is the canonical misclassification — the VSCode window feels local but the code lives in a GitHub container, making it **cloud** for hook-extensibility purposes.

## Why This Matters for Harness Extensibility

Any tool that modifies the agent's execution loop — [RTK](rtk-token-killer.md) (PreToolUse hook + Rust binary), MCP servers that shell out, custom bash wrappers, local secret managers — requires **two things** that only local agents provide:

1. A binary or script reachable on the **execution machine's** `$PATH`.
2. A **settings surface** the user controls that the agent respects (hook config, rule file, plugin manifest).

Cloud agents satisfy neither. Even prompt-level instructions like *"prefix bash commands with `rtk`"* fail inside a Devin VM because the binary does not exist there — result: `command not found`. Harness innovations from the local-agent ecosystem (RTK's 60–90% token savings, the [Claude Code Token Efficiency Playbook](claude-code-token-efficiency-playbook.md)) cannot be applied to cloud agents until the vendor exposes equivalent hook surfaces, which [Anthropic's Managed Agents](claude-managed-agents.md) is one attempt to do vendor-side.

## Trade-off Summary

| Dimension | Local | Cloud |
|---|---|---|
| Harness customization | High | Near-zero |
| Privacy (code leaves your machine) | Minimal (inference only) | Full repo upload |
| Environment reproducibility | User-dependent | Clean sandbox every run |
| Long-running tasks while user offline | No | Yes |
| Token-efficiency tooling (RTK, compression) | Applicable | Not applicable |
| Vendor lock-in on harness | Low | High |

## When to Use

- **Local agent** when: harness customization matters, privacy constraints exist, token budget is tight and you want compression hooks, or the work is interactive/collaborative.
- **Cloud agent** when: the task is long-running and fire-and-forget, a clean reproducible sandbox matters (CI-like), or the user deliberately wants the agent to act without local resources (e.g., from a phone). Accept that third-party token-efficiency tooling will not apply.

## Backlinks

- [RTK Token Killer](rtk-token-killer.md)
- [Agentic Harness](agentic-harness.md)
- [Claude Managed Agents](claude-managed-agents.md)
- [Mobile Dispatch Workflow](mobile-dispatch-workflow.md)
- [2026-04-20 RTK: local vs cloud agents (query)](../queries/2026-04-20-rtk-local-vs-cloud-agents.md)

## Sources

- User session 2026-04-20 (synthesis; no external source — marked as user's own synthesis per KB authority-citation rule)
- [rtk-ai/rtk integration matrix](https://github.com/rtk-ai/rtk) — 12 supported agents, all local-execution
- [Cognition — Devin product architecture](https://www.cognition.ai/blog/introducing-devin) — cloud VM per session
- [OpenAI Codex (2025) product page](https://openai.com/codex) — cloud sandbox execution
