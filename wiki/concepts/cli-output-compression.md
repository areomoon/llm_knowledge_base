---
title: CLI Output Compression
tags: [context-compression, agentic-harness, tooling, llm, parsing]
sources: [raw/repos/rtk-token-killer.md]
created: 2026-04-17
updated: 2026-04-17
---

# CLI Output Compression

> **TL;DR**: Shell commands emit output formatted for human eyes — progress bars, colored banners, repeated status lines, multi-line headers. From an LLM's perspective this is almost pure redundancy; command-specific compression routinely removes 70–95% of tokens without losing task-relevant signal.

## Definition

CLI output compression is the technique of transforming a shell command's stdout/stderr into a more token-efficient form **before** it enters an LLM agent's context window. Compression is performed by a proxy (e.g. [RTK Token Killer](rtk-token-killer.md)) that knows the command's semantics and can drop, aggregate, or re-encode output deterministically.

## Why It Works

Human-readable CLI output has very low entropy per token from the agent's standpoint:

- **Progress artifacts** (`Enumerating objects: 100%`, spinner frames, `[##### ]` bars) carry zero task signal after completion.
- **Repeated headers/footers** across sub-commands (`cargo test` printing module headers per file) are redundant given the summary line.
- **Fixed-format noise** (git's "Delta compression using up to N threads") never changes per run.
- **Near-duplicates** (100 lines of "warning: unused variable X" differing only by X) collapse into one templated line plus a count.

The agent only needs the decision-relevant payload: did it succeed, what changed, which errors, where.

## Four Compression Tactics

Standardized by RTK but applicable to any CLI-to-agent pipeline:

| Tactic | Example |
|---|---|
| **Filtering** | Strip ANSI codes, progress lines, legal banners. |
| **Grouping** | `ls` of 200 files → "15 *.py in src/, 8 *.md in docs/, 3 others". |
| **Truncation** | Keep first + last N lines of a log, drop middle. |
| **Deduplication** | 87 identical warnings → `(×87) warning: …`. |

Each is lossy but the loss is command-aware, so task-relevant information is retained.

## Implementation Approaches

### Per-command regex filters (RTK today)

Write a hand-tuned regex filter per command. Fast to ship, broad coverage, but:

- Brittle — CLI format drifts (git, cargo bump their output); a minor version bump can silently strip real signal.
- High maintenance cost per new command.
- Poor composability: a pipe like `git log | grep … | awk …` confuses the filter because the proxy only sees the outer shape.

### Structural parsing (compiler-style)

Treat each command's output as a small language with a grammar:

1. **Lexer** — tokenize into structured events (commit header, diff hunk, test pass/fail).
2. **AST** — build a tree the proxy understands semantically.
3. **Semantic compression** — render the AST back as a minimal token stream, optionally with a schema marker so the LLM can parse it deterministically.

Harder to bootstrap but robust to format changes and reaches closer to the information-theoretic lower bound (see [Information Theory for LLM Context](information-theory-for-llm-context.md)).

## Trade-offs and Failure Modes

- **Debugging drop-outs.** Aggressive filtering can remove a stack frame or warning that was the actual signal the agent needed (documented Playwright case in RTK).
- **Mitigation**: `tee recovery` — persist full raw output; expose a "show me the unfiltered run" fallback tool.
- **LLM re-parse cost.** Maximally compressed encodings can confuse the LLM; adding a few marker/framing tokens is a small tax that makes downstream parsing reliable. RTK-user estimate: ~3 percentage points (95% theoretical → 92% practical).
- **Scope gap.** Proxies that only intercept the Bash surface leave built-in tools (Claude Code's `Read`/`Grep`/`Glob`) uncompressed — a completeness vs. invasiveness trade-off.

## When to Use

- Long agentic sessions that repeatedly run the same dev commands.
- Fixed-budget deployments where context tokens are the bottleneck.
- Any pipeline where you control the tool surface between the agent and the shell.

## Backlinks

- [RTK Token Killer](rtk-token-killer.md)
- [Information Theory for LLM Context](information-theory-for-llm-context.md)
- [Agentic Harness](agentic-harness.md)

## Sources

- [rtk-ai/rtk (GitHub)](https://github.com/rtk-ai/rtk)
- [MadPlay — I Only Compressed CLI Output](https://madplay.github.io/en/post/rtk-reduce-ai-coding-agent-token-usage)
