---
title: Skill Modes Pattern
tags: [agent-design, skill-modes, claude-code, prompt-engineering, agentic-ai]
created: 2026-04-08
updated: 2026-04-08
sources:
  - title: "career-ops: AI Job Search Pipeline"
    url: https://github.com/santifer/career-ops
  - title: Claude Code Skills Documentation
    url: https://docs.anthropic.com/en/docs/claude-code/skills
---

# Skill Modes Pattern

A multi-capability agent architecture where a single slash command dispatches to specialized sub-prompts loaded from separate Markdown files, each handling one domain of behavior.

## Overview

The Skill Modes Pattern addresses the challenge of building agents that need to perform many distinct tasks without bloating a single monolithic system prompt. Instead of encoding all behavior in one place, the agent loads a small, focused "mode" file for each capability — only when that capability is invoked.

In career-ops, `/career-ops oferta` loads `modes/oferta.md` into context alongside a shared base (`modes/_shared.md`). The mode file is pure natural language describing what to do, what to output, and what rules to follow. The AI interprets these instructions directly — no code parsing required.

This pattern originated in Claude Code's skill system (`.claude/skills/<name>/SKILL.md`) and has been generalized into a reusable design for any multi-mode agent built on a coding CLI.

The pattern separates **shared context** (scoring logic, global rules, tools config) from **mode-specific instructions** (output format, step-by-step workflow, decision logic for that mode). This separation keeps each mode file focused and reduces the risk of instruction conflicts.

## Key Ideas

- **Single entry point, multiple modes**: One slash command (`/career-ops`) with mode arguments (`scan`, `batch`, `pdf`, etc.) routes to different behavior without exposing complexity to the user
- **Modes as natural-language prompts**: Each `modes/*.md` file is a self-contained instruction set — no code, no function calls — interpreted directly by the LLM at invocation time
- **Two-layer file architecture**: `_shared.md` holds system-level context (auto-updatable); `_profile.md` holds user customizations (never overwritten). This allows the system to be updated without destroying personalization
- **Localization via mode directories**: `modes/de/` and `modes/fr/` provide full replacements of the modes directory with market-specific vocabulary, activated by config or user request
- **Auto-dispatch**: The agent detects intent from user input (pasted URL → `oferta` mode; "scan portals" → `scan` mode) and selects the appropriate mode without explicit invocation
- **Context economy**: Loading only the relevant mode file keeps the context window focused; `_shared.md` provides cross-cutting rules without repeating them in every mode

## Implementation Structure

```
.claude/skills/career-ops/
  SKILL.md          ← entry point loaded by Claude Code
modes/
  _shared.md        ← scoring logic, archetypes, global rules (system layer)
  _profile.md       ← user archetypes, narrative, negotiation (user layer)
  oferta.md         ← single offer evaluation (A-F blocks)
  batch.md          ← batch processing with sub-agents
  scan.md           ← portal scanner
  pdf.md            ← ATS-optimized CV generation
  de/               ← DACH market localization
  fr/               ← Francophone market localization
```

At invocation, Claude reads `_shared.md` + `_profile.md` + the relevant mode file. The SKILL.md routes the user's intent to the correct mode.

## Design Trade-offs

| Benefit | Trade-off |
|---------|-----------|
| Each mode is independently readable and editable | User must know mode names (or rely on auto-dispatch) |
| System layer can be updated without breaking user data | Two-layer split requires discipline to maintain |
| Modes can be localized or forked per market | Mode proliferation requires governance |
| LLM interprets modes directly — no parser needed | Mode quality depends on prompt-writing skill |

## Related Concepts

- [Evolving Context Accumulation](evolving-context-accumulation.md)
- [Agent-Friendly Design](agent-friendly-design.md)
- [API to SuperAgent Paradigm Shift](api-to-superagent.md)

## References

- [career-ops GitHub Repository](https://github.com/santifer/career-ops) — reference implementation with 14 modes, two-layer data contract, batch processing
- [Claude Code Skills Documentation](https://docs.anthropic.com/en/docs/claude-code/skills) — upstream skill system that inspired the pattern
