---
title: RTK Token Killer
tags: [agentic-harness, context-compression, claude-code, rust, cli-proxy]
sources: [raw/repos/rtk-token-killer.md, https://github.com/rtk-ai/rtk]
created: 2026-04-17
updated: 2026-04-20
---

# RTK Token Killer

> **TL;DR**: A Rust CLI proxy that installs a `PreToolUse` hook, rewrites shell commands to `rtk <cmd>` transparently, and returns compressed output to the LLM agent — cutting 60–90% of tokens on 100+ dev commands with <10ms overhead.

## Definition

RTK ("Rust Token Killer") is an open-source MIT-licensed tool that sits between an AI coding agent (Claude Code, Cursor, Copilot, Gemini CLI, Codex, Windsurf, Cline, Aider, etc.) and the shell. It intercepts common dev commands — `git`, `ls`, `cat`, `cargo test`, `pytest`, `docker`, `aws`, package managers — and applies command-specific filters that remove boilerplate, group similar lines, truncate redundant sections, and deduplicate repeats. The agent sees only the compressed output.

## How It Works

```mermaid
flowchart LR
  A[Agent plans: "run git push"] --> B[PreToolUse hook]
  B -- rewrites --> C[rtk git push]
  C --> D[real git push]
  D -- 15 lines, ~200 tokens --> E[RTK filter]
  E -- "ok main", ~10 tokens --> F[Agent context]
```

1. `rtk init -g` installs a Bash preprocessing script (`rtk-rewrite.sh`) and registers a `PreToolUse` hook in the agent's config.
2. When the agent emits a bash tool call, the hook rewrites the command to its `rtk`-prefixed equivalent. The rewrite is invisible to the agent.
3. RTK executes the real command, captures stdout/stderr, and applies a **per-command filter** implemented in Rust (heavy regex matching).
4. Filtered output is returned as the tool result. If the command fails, the full unfiltered output is tee'd to disk ("tee recovery mode") so the agent can review it without re-running.

## Key Properties

- **Four compression tactics** — filter / group / truncate / dedup, applied per command.
- **Transparent** — no change to agent prompts or tools; only the Bash surface is affected.
- **100+ commands** — files, git, gh, tests, build/lint, package managers, AWS, docker.
- **12 agent integrations** — Claude Code and Copilot via `PreToolUse` hook; Cursor via `hooks.json`; Gemini via `BeforeTool` hook; Windsurf/Cline via project-scoped rule files; OpenCode/OpenClaw via TS plugins.
- **<10ms overhead** — single Rust binary, zero deps.
- **Observability** — `rtk gain` reports cumulative savings; `rtk discover` flags missed opportunities.

## Measured Savings

From the author's own 30-minute Claude Code benchmark, independently reproduced by MadPlay on a TypeScript/Rust project (78 commands, 80% overall reduction):

| Command | Before | After | Savings |
|---|---|---|---|
| `ls`/`tree` | 2,000 | 400 | -80% |
| `cat`/`read` | 40,000 | 12,000 | -70% |
| `cargo test`/`npm test` | 25,000 | 2,500 | -90% |
| `git add/commit/push` | 1,600 | 120 | -92% |
| Session total | ~118,000 | ~23,900 | -80% |

A Kilo-Org user reported **10M tokens (89%) saved** over extended use.

## Limitations

- **Bash-only hook surface.** Claude Code's built-in `Read`/`Grep`/`Glob` bypass RTK unless the user explicitly calls `rtk`.
- **Local agents only.** RTK needs to install a binary and hook into the execution machine, so it is inapplicable to cloud-hosted agents (Devin, OpenAI Codex, Replit Agent, Codespaces-hosted Copilot) — see [Local vs Cloud Coding Agents](local-vs-cloud-coding-agents.md).
- **Lossy by design.** Aggressive filtering can drop debug-relevant signal (documented Playwright test case).
- **Regex-heavy filter code.** Adding/changing filters is labor-intensive and brittle vs. the structural diversity of real-world CLI output — a reason to prefer a lexer/AST approach (see [CLI Output Compression](cli-output-compression.md)).
- **Restart required** after hook install.
- **Windows** needs WSL for full support.

## When to Use

- Long agent sessions that repeatedly run `git`, tests, builds, or `ls`/`cat` on large trees — the budget quickly dominates context.
- Fixed-budget agent deployments (e.g. Claude Code on a fixed usage tier) where compressing deterministic tool output is nearly free win.
- Not ideal when outputs carry the actual signal (debug traces, uncommon failure modes) — use `tee recovery` or bypass for those commands.

## Relation to Information Theory

RTK's 60–90% compression empirically demonstrates that shell output, as emitted for human readers, carries extremely low entropy per token from the agent's perspective. The user reports (from weeks of hands-on testing) that a more principled encoding could push this to **~95%**, with ~**92%** practically achievable once marker tokens are added to prevent Claude-class misinterpretation. See [Information Theory for LLM Context](information-theory-for-llm-context.md) for the Shannon framing.

## Backlinks

- [CLI Output Compression](cli-output-compression.md)
- [Information Theory for LLM Context](information-theory-for-llm-context.md)
- [Agentic Harness](agentic-harness.md)
- [Local vs Cloud Coding Agents](local-vs-cloud-coding-agents.md)
- [2026-04-17 RTK Token Killer (derived)](../derived/2026-04-17-rtk-token-killer.md)
- [2026-04-20 RTK: local vs cloud agents (query)](../queries/2026-04-20-rtk-local-vs-cloud-agents.md)

## Sources

- [rtk-ai/rtk (GitHub)](https://github.com/rtk-ai/rtk)
- [MadPlay — I Only Compressed CLI Output, Yet Tokens Dropped by 80%?](https://madplay.github.io/en/post/rtk-reduce-ai-coding-agent-token-usage)
- [Kilo-Org/kilocode Discussion #5848](https://github.com/Kilo-Org/kilocode/discussions/5848)
