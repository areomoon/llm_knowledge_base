---
title: RTK (Rust Token Killer) — CLI Output Compression for LLM Agents
type: repo
source_url: https://github.com/rtk-ai/rtk
raw_path: raw/repos/rtk-token-killer.md
created: 2026-04-17
---

# RTK (Rust Token Killer) — CLI Output Compression for LLM Agents

> **TL;DR**: A Rust CLI proxy that intercepts shell output via a `PreToolUse` hook and compresses it (filter/group/truncate/dedup) before it reaches Claude Code or other coding agents, cutting 60–90% of tokens on 100+ common commands with <10ms overhead.

## Key Points

- **Mechanism**: `PreToolUse` hook transparently rewrites `git status` → `rtk git status`; the agent never sees the rewrite, only the compressed stdout.
- **Four compression tactics**: smart filtering (strip boilerplate), grouping (aggregate similar items), truncation (preserve relevant, cut redundancy), deduplication (collapse repeats with counts).
- **Per-command filters, regex-heavy**: 100+ commands each have a hand-written filter. The codebase is regex-dense — a point of critique for anyone with compiler-building instincts who would rather parse structurally.
- **Measured savings**: `git` 75–92%, tests 90%, `cat`/`read` 70%, session total ~80% in both the author's benchmark and an independent MadPlay reproduction.
- **Tee recovery**: failed commands persist full unfiltered output so the agent can inspect without re-running.
- **Coverage gap**: only Bash tool calls. Claude Code's built-in `Read`/`Grep`/`Glob` bypass it unless the user calls `rtk` explicitly.
- **Multi-agent**: 12 supported tools (Claude Code, Cursor, Gemini CLI, Copilot, Codex, Windsurf, Cline, Aider, OpenCode, OpenClaw, …).

## User's Own Analysis (math-for-money thesis)

After weeks of use, the user reports two original observations not in the upstream docs or third-party reviews:

1. **Theoretical headroom**: by moving from regex-based filtering to a more principled encoding (compiler-style parsing + information-theoretic compression), token output could shrink by ~**95%** — well beyond the project's published 80%.
2. **Practical ceiling**: ~**92%** is achievable in practice once you add marker tokens so Claude-class agents don't misinterpret the compressed form. The remaining 3% is the overhead of "legibility guardrails" for downstream LLMs.

This frames RTK as an applied demonstration of Shannon's information theory — the user plans to turn the rewrite into teaching material under the thesis **「用數學賺錢」**("making money with math," or at minimum, saving money with it).

## Concepts Referenced

- [RTK Token Killer](../concepts/rtk-token-killer.md)
- [CLI Output Compression](../concepts/cli-output-compression.md)
- [Information Theory for LLM Context](../concepts/information-theory-for-llm-context.md)
- [Agentic Harness](../concepts/agentic-harness.md)
- [Context Engineering](../concepts/context-engineering.md)

## Notes

- User is rewriting RTK internals because the regex-heavy approach offends their compiler-engineering background. Structural parsing (lexer → AST → semantic compression) would likely replace the per-command regex filters.
- The 95% vs. 92% gap is itself a useful pedagogical artifact: it quantifies the tax the LLM imposes on its own input format — the cost of not being able to read a maximally-compressed stream.
- Integration-wise, RTK is an instance of the broader [Agentic Harness](../concepts/agentic-harness.md) pattern: compression as a first-class layer around the LLM loop.

## Sources

- [rtk-ai/rtk on GitHub](https://github.com/rtk-ai/rtk)
- [I Only Compressed CLI Output, Yet Tokens Dropped by 80%? — MadPlay](https://madplay.github.io/en/post/rtk-reduce-ai-coding-agent-token-usage)
- [Kilo-Org/kilocode Discussion #5848 — 10M tokens saved (89%)](https://github.com/Kilo-Org/kilocode/discussions/5848)
- [rtk-ai.app](https://www.rtk-ai.app/)
