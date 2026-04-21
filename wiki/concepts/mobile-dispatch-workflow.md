---
title: Mobile Dispatch Workflow
tags: [claude-code, mobile, iphone, remote-development, dispatch, workflow, bcherny]
sources: [raw/articles/bcherny-claude-code-tips.md, https://howborisusesclaudecode.com]
created: 2026-04-17
updated: 2026-04-17
---

# Mobile Dispatch Workflow

> **TL;DR**: iPhone / mobile Claude Code use is a distinct operating regime from desktop — no worktrees, no local hooks (RTK does not run unless you SSH into a machine that has it), typing cost is high, screen is narrow. The right pattern is: long tasks launched on the Mac, mobile as a check-in / side-chain surface via `/loop`, `/schedule`, `/btw`. Dispatch discipline (parallel, bounded, terse) matters more on mobile because correction cycles are disproportionately painful.

## Definition

A set of operating rules for using Claude Code (and related Claude surfaces) from a mobile device — typically iPhone via claude.ai web, the iOS app, or an SSH client connecting to a desktop host. It is a specialisation of [Subagent Dispatch Economics](subagent-dispatch-economics.md) plus a deployment-model choice (what runs where).

## Why mobile is a different regime

Three structural differences from desktop Claude Code:

1. **No native worktrees**. Boris Cherny's biggest productivity unlock — `3–5 parallel worktrees per session` — is desktop-only. On mobile, every session is single-track.
2. **No local hooks**. `PreToolUse` (RTK), `PostToolUse` (auto-format), `SessionStart`, `PostCompact` all require a host running Claude Code. claude.ai web / iOS app have none of these. SSH sessions inherit the host's hooks.
3. **Input cost is high, screen is narrow**. Each corrective round-trip wastes proportionally more time and context than on desktop, and long agent summaries are painful to scroll.

## Deployment Modes

Pick the mode before deciding how to dispatch:

| Situation | Best surface |
|---|---|
| Q&A, review a PR | claude.ai web or iOS app — no Claude Code needed |
| Read-only repo context | claude.ai + GitHub connector; prefer docs sites that serve markdown variants (WebFetch ~10× compression per bcherny) |
| Edit + execute code | SSH into your Mac running `claude` (Blink Shell / Termius / Tailscale SSH) |
| Long / batch tasks | Launch on Mac via `/loop` or `/schedule`; mobile used only for check-in |

## Dispatch Discipline (mobile-specific)

These are tightenings of the general [Subagent Dispatch Economics](subagent-dispatch-economics.md) rules — stricter because mobile correction is expensive:

- **Pre-compose briefings off-device.** Use iOS dictation → Notes → paste. A long briefing typed live on the keyboard is where most mobile context pollution comes from.
- **Parallel in one message, never serial.** On mobile it is tempting to fire one subagent, wait, then fire the next — but the first subagent's returned summary gets re-ingested before the second dispatch, so subagent #2 sees it. Explicitly instruct: "dispatch N subagents in parallel for A / B / C".
- **Always cap response length**: add *"report in under 200 words"* to every dispatch briefing. Long summaries are painful to read and expensive to ingest.
- **Default `Explore` to `quick` thoroughness.** Mobile sessions often run unattended while the user switches apps. A `very thorough` explore can silently push context into the 300–400k rot zone before you notice.

## Long Tasks: Mac-launched, Mobile-checked

The canonical bcherny pattern for mobile involvement:

- `/loop <interval> <cmd>` — local recurring task, up to 3 days; mobile receives a notification on status change.
- `/schedule` — cloud cron; runs even with the laptop closed. Right fit for "check the deploy every hour".
- `/btw` — side-chain query without stopping the active agent. On mobile this is the most-used skill: you think of a question, ask it, the main session is undisturbed.

## SSH-to-Mac Setup

If the mobile surface is a terminal app talking to a desktop Claude Code:

- Wrap the `claude` session in **tmux** — connection drops do not kill the session.
- Use **Tailscale SSH** rather than exposing port 22 publicly (key-based, private-network, zero config for reconnect).
- Narrow screens reward terseness: add a line to `CLAUDE.md` Gotchas like *"responses over 40 lines are painful on mobile — default to terse, skip summaries"*. This is itself a bcherny-style gotcha entry (update every time Claude outputs something mobile-hostile).
- RTK runs here because it is a Mac-side hook — tool-output compression of 60–90% is disproportionately valuable on a narrow screen.

## Anti-Patterns on Mobile

- **Batch migrations (`/batch` with many worktree subagents)**: failure triage on a phone is masochism. Launch from desktop.
- **Tasks requiring visual UI verification**: bcherny's #1 tip is "give Claude a feedback loop"; mobile cannot drive a browser simulator or inspect renders.
- **Running 3–5 parallel desktop worktree sessions from mobile**: context-switching between sessions on a phone is slow enough that the parallelism benefit inverts.
- **Typing a 10-line correction instead of `/rewind`**: on desktop a correction is cheap. On mobile it is 3× more expensive and the correction still pollutes context permanently (only `/rewind` truly removes it).

## Authority

- Boris Cherny (@bcherny), Claude Code creator — source of `/loop`, `/schedule`, `/btw`, the worktree parallelism claim, the WebFetch markdown compression behaviour, and the `CLAUDE.md` Gotchas discipline. See [Boris Cherny's Claude Code Tips (derived)](../derived/2026-04-17-bcherny-claude-code-tips.md) and [howborisusesclaudecode.com](https://howborisusesclaudecode.com).
- Tailscale SSH, Blink Shell, Termius, tmux — standard remote-dev tooling; named-tool choice is deployment-model commodity, not a research claim.
- *Mode selection table, mobile dispatch tightenings, and the SSH-setup assembly are the user's own synthesis* — bcherny's tips do not explicitly address iPhone operation; this article composes them with observed mobile friction points.

## Relation to Other Concepts

- **[Subagent Dispatch Economics](subagent-dispatch-economics.md)** — mobile discipline here is a strict subset / tightening of that cost model.
- **[Claude Code Token Efficiency Playbook](claude-code-token-efficiency-playbook.md)** — `/loop`, `/schedule`, `/btw`, Gotchas all come from the broader playbook; this article selects the mobile-relevant entries.
- **[RTK Token Killer](rtk-token-killer.md)** — relevant only when the mobile device is SSH'd into a Mac running RTK; irrelevant for pure claude.ai / iOS-app use.
- **[Agentic Harness](agentic-harness.md)** — mobile is a degraded harness surface (fewer hooks, no worktrees); this article documents what survives the degradation.

## Backlinks

- [Local vs Cloud Coding Agents](local-vs-cloud-coding-agents.md) — iPhone + Mac-launched Claude Code is still a *local agent* scenario (execution on Mac), not cloud

## Sources

- [Boris Cherny's Claude Code Tips (derived)](../derived/2026-04-17-bcherny-claude-code-tips.md)
- [howborisusesclaudecode.com](https://howborisusesclaudecode.com)
- [@bcherny on X](https://x.com/bcherny)
