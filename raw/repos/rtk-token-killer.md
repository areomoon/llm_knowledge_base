# RTK (Rust Token Killer) — Repo Summary

- **Source**: https://github.com/rtk-ai/rtk
- **License**: MIT
- **Language**: Rust (single binary, zero dependencies)
- **Purpose**: CLI proxy that compresses shell command output before it reaches an LLM agent's context window, reducing token consumption by 60–90% on common dev commands.

## What it does

RTK installs a `PreToolUse` hook (for Claude Code, Copilot, Cursor, Gemini CLI, Windsurf, Cline, Aider, Codex, OpenCode, OpenClaw — 12 tools total). The hook transparently rewrites `git status` → `rtk git status` etc. before execution; the agent only ever sees the compressed output. Overhead is <10ms per command.

Coverage: 100+ commands across files (`ls`, `tree`, `cat`), git, gh, test runners (`cargo test`, `npm test`, `pytest`), build/lint, package managers, AWS, docker.

## Compression strategies (per-command filters)

1. **Smart filtering** — strip comments, boilerplate, whitespace
2. **Grouping** — aggregate similar items (files by directory, errors by type)
3. **Truncation** — preserve relevant context, cut redundancy
4. **Deduplication** — collapse repeated log lines with occurrence counts

Filters are command-specific, implemented with heavy regex matching. Example: `git push`'s 15-line verbose output ("Enumerating objects... Counting objects... Delta compression...") becomes `ok main` (~200 → ~10 tokens).

## Measured savings (30-min Claude Code session, author benchmark)

| Command | Before | After | Savings |
|---|---|---|---|
| `ls`/`tree` | 2,000 | 400 | -80% |
| `cat`/`read` | 40,000 | 12,000 | -70% |
| `cargo test`/`npm test` | 25,000 | 2,500 | -90% |
| `git add/commit/push` | 1,600 | 120 | -92% |
| **Session total** | ~118,000 | ~23,900 | **-80%** |

Independent reproduction (MadPlay, TypeScript/Rust mid-sized project, 78 commands): ~88,000 saved of 111,000 (80%).

## Tooling

- `rtk init -g` — install global hook
- `rtk gain` — analytics: token savings over time
- `rtk discover` — find missed optimization opportunities
- **Tee recovery mode** — failed commands save full unfiltered output so the agent can review without re-running
- Config: `~/.config/rtk/config.toml`, per-project or global filters
- Telemetry: opt-in only

## Limitations

- Hook only covers Bash tool calls. Claude Code's built-in `Read`, `Grep`, `Glob` bypass RTK (user must call explicit `rtk` commands).
- Aggressive filtering can strip debug-relevant signal (documented Playwright case).
- Requires Claude Code restart after install.
- Windows needs WSL for full functionality.

## Architecture

```
src/           Rust core (filters, command handlers, proxy)
hooks/         Bash preprocessing scripts (rtk-rewrite.sh)
openclaw/      OpenClaw plugin
docs/          User guide, telemetry, architecture
.claude/       Claude Code hook config
```
