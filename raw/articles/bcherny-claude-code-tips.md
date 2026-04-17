# Boris Cherny — How I Use Claude Code (tips collection)

Source: https://howborisusesclaudecode.com (Boris Cherny, Claude Code creator, @bcherny)
Related tweet (4.7 effort levels, token mgmt): https://x.com/bcherny/status/2044802544896221484
Collection writeup: https://alirezarezvani.medium.com/boris-chernys-claude-code-tips-are-now-a-skill-here-is-what-the-complete-collection-reveals-b410a942636b

## Token Efficiency & Effort

- Four effort levels: low / medium / high / max; **xhigh** introduced with Opus 4.7 as default — reasons longer before acting.
- Boris personally uses **High for everything**; Max "burns through usage limits faster, activate per session."
- **Claude 4.7 thinks more**, so token use runs higher than 4.6. Manage with: effort level, task budgets, or prompting for brevity.
- WebFetch automatically sends `Accept: text/markdown, */*` — docs sites that serve markdown shrink token usage by **~10×**.

## Context Rot & Auto-Compact

- Context degrades around **300–400k tokens** on the 1M-context model.
- Recommended: `CLAUDE_CODE_AUTO_COMPACT_WINDOW=400000` — compact before entering the rot zone.
- Prefer `/rewind` over corrections: corrections pollute context with failed attempts.
- `PostCompact` hook can re-inject critical instructions post-compression.

## Worktrees (top productivity unlock)

- Run **3–5 git worktrees simultaneously**, each with its own Claude session.
- `claude --worktree <name>` isolates a session.
- Desktop app supports worktrees natively. Non-git VCS (Mercurial/Perforce/SVN) via `WorktreeCreate` hook.
- Subagents now support worktree isolation for batched migrations.

## CLAUDE.md Discipline

- Shared, checked in, updated **multiple times a week**.
- Rule: "Anytime we see Claude do something incorrectly, we add it to CLAUDE.md."
- Build a **Gotchas section** — the highest-signal content.
- `@.claude` in PR review auto-updates CLAUDE.md as part of review.

## Hooks

- **PreToolUse**: validate/rewrite inputs (RTK uses this).
- **PostToolUse**: auto-format after codegen — prevents CI failures.
- **SessionStart**: dynamically load context.
- **PermissionRequest**: route approvals to external channels or an Opus 4.7 classifier.
- **Stop**: nudge Claude to continue.
- **PostCompact**: re-inject critical instructions after compaction.

## Skills & Commands

- `/simplify` — parallel agents review code for reuse, quality, efficiency.
- `/batch` — fan out to dozens of agents in isolated worktrees (migrations).
- `/loop` — schedule tasks locally, up to 3 days.
- `/schedule` — cloud recurring jobs, runs when laptop closed.
- `/btw` — side-chain queries without stopping active work.
- Rule of thumb: if you do something more than once a day, **turn it into a skill or command**.

## Permissions & Safety

- Pre-allow safe commands via `/permissions` with wildcards (e.g. `"Bash(bun run *)"`).
- **Auto mode**: safety classifier auto-approves safe ops, flags risky ones.
- **Sandboxing**: on-machine with file/network isolation.

## Verification (Boris's #1 tip)

- "Give Claude a way to verify its work. If Claude has that feedback loop, it will **2–3× the quality** of the final result."
- Verification surfaces: test suites, Chrome extension for browser testing, simulators, domain checks.

## Memory & Learning

- **Auto-memory**: saves preferences automatically.
- **Auto-dream**: periodic consolidation ("REM sleep"): keep what matters, remove what doesn't.

## Sub-agents

- Delegate to keep main context window clean.
- Route permission requests to Opus 4.7 via hook to scan attacks and auto-approve safe calls.
