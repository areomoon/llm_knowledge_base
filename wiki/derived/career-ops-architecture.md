---
title: "Career-Ops: AI Job Search Pipeline Architecture"
source_type: repo
source_url: https://github.com/santifer/career-ops
ingested: 2026-04-08
compiled: 2026-04-08
tags: [agent-design, skill-modes, evolving-context, batch-processing, claude-code, pipeline, agentic-ai]
---

# Career-Ops: AI Job Search Pipeline Architecture

> **TL;DR**: An open-source Claude Code agent system for job search automation, notable for its slash-command + modes/*.md skill architecture, two-layer data contract, evolving context accumulation via append-only files, and resumable sub-agent batch processing.

## Key Points

- **14 skill modes** loaded from `modes/*.md` files — each a standalone natural-language prompt invoked via `/career-ops <mode>`; shared context in `_shared.md`, user customizations in `_profile.md` (never overwritten by updates)
- **Evolving context**: `interview-prep/story-bank.md` accumulates STAR+R stories across evaluations; `article-digest.md` grows proof points; `config/profile.yml` deepens candidate understanding — the system improves with each use without retraining
- **Sub-agent batch processing**: conductor Claude orchestrates `claude -p` workers with clean 200K contexts; state tracked in `batch-state.tsv` for full resumability; TSV intermediates written to `batch/tracker-additions/` and merged by `merge-tracker.mjs` to maintain pipeline integrity
- **Portal scanner**: Playwright navigates 45+ pre-configured company portals (Greenhouse, Ashby, Lever) with logged-in Chrome sessions; dedup via `scan-history.tsv`; offer verification requires Playwright DOM snapshot, never WebSearch
- **Two-layer data contract**: system layer (modes, scripts, templates) is auto-updatable; user layer (cv.md, _profile.md, data/) is never touched by system updates
- **STAR+R evaluation**: Block F of every evaluation adds Situation/Task/Action/Result/Reflection stories to a reusable bank — Reflection signals seniority by extracting lessons, not just describing events
- Used to evaluate 740+ offers, generate 100+ tailored CVs, and land a Head of Applied AI role

## Extracted Concepts

- [Skill Modes Pattern](../concepts/skill-modes-pattern.md)
- [Evolving Context Accumulation](../concepts/evolving-context-accumulation.md)
- [Agent-Friendly Design](../concepts/agent-friendly-design.md)

## Raw Source

`raw/articles/career-ops-architecture.md`
