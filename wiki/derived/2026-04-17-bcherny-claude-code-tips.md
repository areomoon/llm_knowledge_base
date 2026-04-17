---
title: Boris Cherny's Claude Code Tips (Creator's Playbook)
type: article
source_url: https://howborisusesclaudecode.com
raw_path: raw/articles/bcherny-claude-code-tips.md
created: 2026-04-17
---

# Boris Cherny's Claude Code Tips (Creator's Playbook)

> **TL;DR**: 42 tips compiled by Claude Code's creator (@bcherny) across Jan–Feb 2026 threads. Biggest productivity unlock: 3–5 parallel worktrees per session. Biggest token/cost levers: set `CLAUDE_CODE_AUTO_COMPACT_WINDOW=400000` to dodge context rot, use High effort by default, exploit WebFetch's auto-markdown accept header (~10× docs compression), and install a CLAUDE.md "Gotchas" section updated every time Claude screws up.

## Key Points

- **Effort levels**: low / medium / high / max, plus **xhigh** (new default on Opus 4.7). 4.7 reasons longer and uses more tokens than 4.6 — manage with effort, budgets, or "be brief" prompting.
- **Context rot starts at 300–400k tokens** on the 1M model. Set auto-compact to 400k. Prefer `/rewind` to corrections.
- **Worktrees are the biggest unlock**: 3–5 parallel Claude sessions, `claude --worktree <name>`; subagents now also support worktree isolation for batched migrations.
- **CLAUDE.md is a living doc**: updated multiple times a week; add a Gotchas section; use `@.claude` in PR reviews to auto-update it.
- **WebFetch trick**: Claude Code already sends `Accept: text/markdown, */*`. If your docs server serves markdown variants, token usage on doc pages shrinks ~10×.
- **Hooks**: PreToolUse (rewrite — this is where RTK plugs in), PostToolUse (auto-format), SessionStart (dynamic context), PermissionRequest (route to Opus classifier), Stop (nudge), PostCompact (re-inject).
- **Skills**: `/simplify`, `/batch`, `/loop`, `/schedule`, `/btw`. Rule: anything you do >1/day → make it a skill.
- **Permissions**: pre-allow wildcards (`Bash(bun run *)`); Auto mode has a safety classifier; sandboxing available.
- **#1 tip — verification**: "Give Claude a way to verify its work. 2–3× quality."

## Connection to RTK

Boris's tips establish the hook surface RTK exploits: the `PreToolUse` contract is a first-class Claude Code feature. RTK is one realization of that contract, specialized for output compression. Together they form a two-sided cost reduction: Boris's tips reduce **context spent on the agent's own output**; RTK reduces **context spent on tool output**.

## Concepts Referenced

- [Claude Code Token Efficiency Playbook](../concepts/claude-code-token-efficiency-playbook.md)
- [RTK Token Killer](../concepts/rtk-token-killer.md)
- [Agentic Harness](../concepts/agentic-harness.md)
- [Context Engineering](../concepts/context-engineering.md)

## Sources

- [howborisusesclaudecode.com](https://howborisusesclaudecode.com) — complete tips collection
- [Boris Cherny @bcherny on X](https://x.com/bcherny)
- [Tweet: Claude 4.7 xhigh effort level & token management](https://x.com/bcherny/status/2044802544896221484)
- [Original setup thread](https://x.com/bcherny/status/2007179832300581177)
- [Team tips thread](https://x.com/bcherny/status/2017742741636321619)
- [Medium: Tips assembled as a skill](https://alirezarezvani.medium.com/boris-chernys-claude-code-tips-are-now-a-skill-here-is-what-the-complete-collection-reveals-b410a942636b)
