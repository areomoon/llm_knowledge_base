---
title: Claude Code Token Efficiency Playbook
tags: [claude-code, token-efficiency, bcherny, worktree, hooks, skills, context-engineering]
sources: [raw/articles/bcherny-claude-code-tips.md, https://howborisusesclaudecode.com]
created: 2026-04-17
updated: 2026-04-17
---

# Claude Code Token Efficiency Playbook

> **TL;DR**: Synthesis of Boris Cherny's (creator of Claude Code, @bcherny) 2026 tips on minimizing tokens per useful outcome. The high-leverage knobs: effort level, auto-compact threshold, `/rewind` instead of correction, `PreToolUse` rewrite (RTK), WebFetch markdown trick, worktree parallelism, and CLAUDE.md discipline.

## Definition

A ranked set of Claude Code configuration changes and usage habits that reduce token spend while holding or increasing output quality. All items are sourced from Boris Cherny's tips collection, verified against current Claude Code features as of 2026-04.

## The Token Budget

Tokens are consumed at four surfaces in a Claude Code session:

1. **System prompt + CLAUDE.md** (paid once per cached session)
2. **Tool output** (repeats every call — highest variance)
3. **Agent reasoning output** (scales with effort level)
4. **Dialogue with user** (scales with session length)

The playbook targets each surface independently.

## High-Leverage Controls

### 1. Effort level (reasoning output)

Four tiers: `low` / `medium` / `high` / `max`, with **xhigh** as the new Opus 4.7 default. Boris uses **High by default**; Max "burns through usage limits faster, activate per session." Claude 4.7 thinks longer than 4.6, so equal effort levels yield higher token counts — budget accordingly.

### 2. Auto-compact window (dialogue)

Context quality degrades around **300–400k tokens** on the 1M-context model (context rot). Set:

```bash
export CLAUDE_CODE_AUTO_COMPACT_WINDOW=400000
```

Compaction before the rot zone yields a cleaner summary. Pair with a `PostCompact` hook that re-injects critical instructions (so they survive compaction).

### 3. `/rewind` over corrections (dialogue)

When Claude takes a wrong step, rewinding is cheaper and cleaner than adding "no, do X instead" — the latter keeps the failed attempt in context forever.

### 4. PreToolUse rewrite (tool output)

The single biggest lever on tool-output tokens. The `PreToolUse` hook lets an external process (e.g. [RTK Token Killer](rtk-token-killer.md)) rewrite bash commands so the agent receives compressed results. Typical savings: 60–90% per command.

### 5. WebFetch markdown trick (tool output)

Claude Code's `WebFetch` already sends `Accept: text/markdown, */*`. Docs sites that honour this (Vercel, Next.js, Anthropic docs, MDN via shortcuts) return markdown variants — **~10× smaller** than rendered HTML. No config needed; just prefer sites that serve markdown.

### 6. Worktree parallelism (throughput, indirectly token-efficient)

3–5 parallel Claude sessions on git worktrees finish the same work faster with less cross-contamination. `claude --worktree <name>` is the primary command. Indirect token win: each session has a cleaner scoped context, so less time is spent re-establishing state.

### 7. CLAUDE.md Gotchas section (system prompt amortized)

One line in CLAUDE.md prevents an infinite recurrence of the same mistake. The Gotchas section is cited as "highest-signal content" in the playbook. Update rule: after every observed wrong action.

### 8. Permissions allowlist (latency, tangentially tokens)

Pre-allow safe commands with `/permissions` wildcards (`Bash(git status)`, `Bash(bun run *)`). Prevents permission-prompt round-trips that cost user tokens for approval dialogue.

### 9. Skills for repeated flows (amortization)

Rule: do it more than once a day → make it a skill. Skills are loaded on demand, not every session, so they don't inflate the base context.

### 10. Verification feedback loop (quality per token)

Boris's #1 tip, token-adjacent: a feedback loop (tests, Chrome extension, simulator) yields **2–3× quality**, which reduces re-prompting — the most expensive token category.

## Ranked by ROI

| Rank | Tip | Effort to adopt | Savings surface |
|---|---|---|---|
| 1 | Install RTK (PreToolUse rewrite) | Low (`rtk init -g`) | Tool output, 60–90% |
| 2 | Set auto-compact to 400k | Trivial (env var) | Dialogue, +quality |
| 3 | CLAUDE.md Gotchas discipline | Ongoing | System prompt, per-mistake |
| 4 | Worktree parallelism | Medium | Throughput |
| 5 | `/rewind` habit | Trivial | Dialogue |
| 6 | Permissions allowlist | One-time | Latency + dialogue |
| 7 | WebFetch on markdown sites | Trivial | Tool output (~10× on docs) |
| 8 | Skills for repeated flows | Medium | Amortized |
| 9 | Effort tuning (High default) | Trivial | Reasoning output |
| 10 | Verification loops | Medium | Quality/token |

## Anti-patterns

- **Correcting instead of rewinding** — leaks failed attempts into long-term context.
- **Running at Max effort by default** — exhausts usage limits without quality gain for straightforward tasks.
- **CLAUDE.md as dumping ground** — dilutes signal. Maintain a focused Gotchas section.
- **Monolithic context** — avoid stuffing all docs/examples into CLAUDE.md when a skill or on-demand file would do.

## Relation to Other Concepts

- **[RTK Token Killer](rtk-token-killer.md)** — realizes Tip #4, the biggest single lever.
- **[CLI Output Compression](cli-output-compression.md)** — the general technique underlying RTK and the markdown trick.
- **[Information Theory for LLM Context](information-theory-for-llm-context.md)** — why this works at all (low entropy per token in human-formatted output).
- **[Agentic Harness](agentic-harness.md)** — the broader harness catalogue that Boris's tips operationalize.
- **[Tiered Memory](tiered-memory.md)** — amortization principle behind Tip #9 (skills).

## Backlinks

- [2026-04-17 Boris Cherny Claude Code Tips (derived)](../derived/2026-04-17-bcherny-claude-code-tips.md)
- [RTK Token Killer](rtk-token-killer.md)
- [Local vs Cloud Coding Agents](local-vs-cloud-coding-agents.md) — playbook tips apply only to local-agent deployments

## Sources

- [howborisusesclaudecode.com](https://howborisusesclaudecode.com) — Boris Cherny's full tips collection
- [@bcherny on X](https://x.com/bcherny) — original threads (Jan–Feb 2026, 42 tips)
- [Tweet 2044802544896221484 — Claude 4.7 xhigh & token management](https://x.com/bcherny/status/2044802544896221484)
