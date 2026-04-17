---
title: Subagent Dispatch Economics
tags: [claude-code, subagent, dispatch, token-efficiency, context-engineering, bcherny]
sources: [raw/articles/bcherny-claude-code-tips.md, https://howborisusesclaudecode.com]
created: 2026-04-17
updated: 2026-04-17
---

# Subagent Dispatch Economics

> **TL;DR**: Each subagent dispatch pays for a fresh context window (system prompt + CLAUDE.md + briefing) on top of whatever work it does. Dispatch is worth it when the expected tool-output volume exceeds the dispatch overhead, or when isolation protects the parent context from being polluted. Used wrong — for known-path lookups, unbounded searches, or serial independent queries — it is strictly more expensive than doing the work inline.

## Definition

Subagent dispatch (Claude Code's `Agent`/`Task` tool, called "sub-agents" in Boris Cherny's tips) spawns a nested Claude session with its own tools, briefing, and result. The parent only sees the subagent's final summary; the subagent's intermediate reasoning and tool output stay in its own context. This is the core mechanism that keeps the parent context "clean" — and also where token waste compounds when misused.

## Cost Model

A single dispatch pays at four places:

1. **Subagent boot cost** — system prompt + `CLAUDE.md` + any skill files are re-rendered for the subagent's own context (new cache key).
2. **Parent briefing cost** — the prompt you write is counted in the parent *and* fed to the subagent.
3. **Subagent internal tokens** — reasoning + every tool call's full output, at whatever effort level is active.
4. **Parent ingest of the summary** — the returned message enters the parent context permanently.

Only #3 is invisible to the parent. For a task that returns a one-line answer, #1–#4 can together exceed doing the lookup inline by an order of magnitude.

## When Dispatch Pays Off

- **Tool output would bloat the parent** — exploring a large codebase, scanning many files, reading long logs. The subagent absorbs the noise and returns a summary.
- **Parallelism** — multiple independent queries in one message. Per Boris Cherny, worktree-isolated subagents enable batched migrations (`/batch`) and parallel review (`/simplify`).
- **Isolation is the feature** — side-chaining exploration (`/btw`) without perturbing the active plan.

## Anti-Patterns

- **Dispatching for a known path/symbol**: if the file path or exact grep pattern is already known, `Read`/`Grep` is always cheaper than an `Explore` agent — the subagent still has to reason its way to the same lookup, and pays the boot cost to do so.
- **Unbounded thoroughness**: Claude Code's `Explore` agent accepts `quick` / `medium` / `very thorough`. Default wording ("look into X") tends to produce over-thorough exploration. Bound it explicitly — e.g. *"report in under 200 words"*, *"stop after finding first match"*.
- **Serial dispatch of independent work**: the first subagent's returned summary gets re-ingested before the second is dispatched, so the second subagent sees it too. Fire them in a single message (multiple tool-use blocks) to avoid this cascade.
- **Delegating synthesis**: passing a research finding to a "fix the bug based on your findings" subagent pushes the judgement call to the subagent, which has less context than the parent. The parent should do the synthesis and dispatch only the mechanical piece.

## Mitigations (ranked)

| Rank | Mitigation | Mechanism |
|---|---|---|
| 1 | Inline the lookup when target is known | Avoids subagent boot cost entirely |
| 2 | Parallel dispatch in one message | Each subagent sees clean briefing, no cross-ingest |
| 3 | Bound response length in briefing | Caps subagent-internal and parent-ingest tokens |
| 4 | Pick lowest-sufficient thoroughness | `quick` → `medium` → `very thorough` for Explore |
| 5 | Worktree isolation for independent work | Eliminates cross-contamination (bcherny's top unlock) |
| 6 | RTK / PreToolUse rewrite active | Compresses the subagent's tool output too |

## Authority

- Boris Cherny (@bcherny), Claude Code creator — *"Delegate to keep main context window clean"* is the stated design intent for subagents; see [Boris Cherny's Claude Code Tips (derived)](../derived/2026-04-17-bcherny-claude-code-tips.md) and [howborisusesclaudecode.com](https://howborisusesclaudecode.com).
- Claude Code `Agent` tool documentation — defines the `Explore` / `Plan` / `general-purpose` subagent types and the `quick` / `medium` / `very thorough` thoroughness knob.
- *Cost model and anti-pattern framing are the user's own synthesis*, derived from the above plus observed dispatch patterns.

## Relation to Other Concepts

- **[Claude Code Token Efficiency Playbook](claude-code-token-efficiency-playbook.md)** — subagent dispatch is one axis of that playbook; this article zooms into it.
- **[RTK Token Killer](rtk-token-killer.md)** — `PreToolUse` rewrite applies inside subagents, so RTK compounds with correct dispatch discipline.
- **[Agentic Harness](agentic-harness.md)** — dispatch is the multi-agent orchestration primitive the harness exposes.
- **[Context Engineering](context-engineering.md)** — deciding *what* to dispatch is a context-engineering choice (what belongs in the parent vs. a nested session).

## Backlinks

- [Mobile Dispatch Workflow](mobile-dispatch-workflow.md)

## Sources

- [Boris Cherny's Claude Code Tips (derived)](../derived/2026-04-17-bcherny-claude-code-tips.md)
- [howborisusesclaudecode.com](https://howborisusesclaudecode.com) — "Sub-agents" section
- [@bcherny on X](https://x.com/bcherny)
