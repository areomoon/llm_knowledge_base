# Career-Ops Architecture Analysis

Source: https://github.com/santifer/career-ops
Ingested: 2026-04-08
Type: repository

---

## Overview

Career-ops is an open-source AI job search automation system built on Claude Code. Created by Santiago Ferrer, it was used to evaluate 740+ job offers, generate 100+ tailored CVs, and land a Head of Applied AI role. The system demonstrates several advanced AI agent design patterns worth extracting for the knowledge base.

---

## Core Architecture

```
User pastes job URL or description
        │
        ▼
┌──────────────────┐
│  Archetype       │  Classifies: LLMOps / Agentic / PM / SA / FDE / Transformation
│  Detection       │
└────────┬─────────┘
         │
┌────────▼─────────┐
│  A-F Evaluation  │  Match, gaps, comp research, STAR stories
│  (reads cv.md)   │
└────────┬─────────┘
         │
    ┌────┼────┐
    ▼    ▼    ▼
 Report  PDF  Tracker
  .md   .pdf   .tsv
```

**Stack:** Claude Code (agent layer), Node.js/mjs (scripting), Playwright (PDF + scraping), Go + Bubble Tea (TUI dashboard), YAML (config), Markdown (data layer).

---

## 14 Skill Modes Design Pattern

The system uses a single slash command `/career-ops` with multiple sub-modes loaded from `modes/*.md` files:

| Mode | Trigger | Function |
|------|---------|----------|
| `oferta` | Paste JD or URL | Full A-F evaluation |
| `ofertas` | Compare multiple | Rank and compare offers |
| `contacto` | LinkedIn outreach | Find contacts + draft message |
| `deep` | Company research | Deep due diligence |
| `pdf` | Generate CV | ATS-optimized tailored PDF |
| `training` | Course/cert | Evaluate against career goals |
| `project` | Portfolio idea | Evaluate project fit |
| `tracker` | Status overview | Application pipeline view |
| `apply` | Live application | Form-filling assistant |
| `scan` | Portal scanner | Scrape 45+ company portals |
| `batch` | Mass processing | Parallel sub-agent evaluation |
| `pipeline` | Pending URLs | Process inbox of URLs |

**Key design decisions:**
- `_shared.md` contains scoring logic, archetypes, global rules — auto-updatable system layer
- `_profile.md` contains user customizations — never auto-overwritten
- This two-layer split allows system updates without destroying user data
- Modes are written in natural language (Markdown), not code — the AI interprets them directly

**Language mode support:** `modes/de/` (DACH market) and `modes/fr/` (francophone market) provide full localized replacements of the core modes directory, with market-specific vocabulary (Tarifvertrag, RTT, CDI/CDD, etc.).

---

## Evolving Context Accumulation Mechanism

The system is explicitly designed to **improve with use** — a key differentiator from one-shot tools:

### Files as Persistent Memory

| File | Role |
|------|------|
| `cv.md` | Canonical CV — source of truth for all evaluations |
| `article-digest.md` | Proof points and case studies — grows over time |
| `config/profile.yml` | Candidate identity, targets, narrative |
| `modes/_profile.md` | User archetypes, framing, negotiation scripts |
| `interview-prep/story-bank.md` | Accumulated STAR+R stories across evaluations |
| `data/applications.md` | Full application tracker — deduped, integrity-checked |
| `data/scan-history.tsv` | Scanner dedup history — prevents re-processing |

### Learning Loop

After every evaluation:
1. If the score feels wrong → update scoring weights in `_shared.md`
2. If the user mentions new experience → update `article-digest.md`
3. If archetypes don't fit → user asks Claude to edit `_shared.md`
4. New STAR stories → appended to `interview-prep/story-bank.md`

From CLAUDE.md: *"Think of it as onboarding a new recruiter: the first week they need to learn about you, then they become invaluable."*

### Interview Story Bank — STAR+R Pattern

Block F of every evaluation produces STAR+Reflection stories:
- **S** — Situation
- **T** — Task
- **A** — Action
- **R** — Result
- **Reflection** — What was learned / what would be done differently

The Reflection column is what signals seniority. Stories accumulate in `story-bank.md` and are reused across evaluations — 5-10 master stories that can be adapted to any behavioral question.

---

## Batch Processing + Sub-Agent Architecture

### Two Modes

**Mode A — Conductor with Chrome:**
```
Claude Conductor (claude --chrome --dangerously-skip-permissions)
  │
  │  Chrome: navigates portals (logged-in sessions)
  │
  ├─ Offer 1: reads JD from DOM + URL
  │    └─► claude -p worker → report + PDF + tracker-line
  │
  ├─ Offer 2: click next, reads JD + URL
  │    └─► claude -p worker → report + PDF + tracker-line
  │
  └─ End: merge tracker-additions → applications.md + summary
```

**Mode B — Standalone Script:**
```bash
batch/batch-runner.sh --parallel N --retry-failed
```

### Worker Architecture

Each worker is a `claude -p` child process with:
- Clean 200K token context
- Self-contained `batch-prompt.md` as system prompt
- Independent failure (one worker crash doesn't affect others)
- Output: report `.md` + PDF + TSV tracker line + JSON stdout

### Resumability Pattern

State tracked in `batch/batch-state.tsv`:
- `pending` / `completed` / `failed` status per offer
- Lock file prevents double execution
- Re-run → reads state → skips completed → retries failed

### Pipeline Integrity

```
NEVER edit applications.md directly to ADD entries
  ↓
Write TSV to batch/tracker-additions/{id}.tsv
  ↓
node merge-tracker.mjs → deduped merge into applications.md
```

Integrity scripts: `verify-pipeline.mjs`, `normalize-statuses.mjs`, `dedup-tracker.mjs`

---

## Portal Scanner Architecture

- 45+ companies pre-configured (Anthropic, OpenAI, ElevenLabs, n8n, etc.)
- Job boards: Ashby, Greenhouse, Lever, Wellfound, Workable, RemoteFront
- Playwright navigates with user's logged-in Chrome session
- Dedup via `data/scan-history.tsv` — never re-processes seen offers
- Can be scheduled: `/loop` or `/schedule` skill for recurring scans

### Offer Verification Rule

NEVER use WebSearch/WebFetch to verify offer activeness. Always use Playwright:
1. `browser_navigate` to URL
2. `browser_snapshot` to read content
3. Title + description + Apply button = active; only footer/navbar = closed

Exception: batch workers (`claude -p`) use WebFetch as fallback, mark report as "unconfirmed".

---

## Data Contract Pattern

Two-layer data architecture prevents update collisions:

**System Layer** (auto-updatable, no user data):
- `modes/_shared.md`, `modes/oferta.md`, all other modes
- `CLAUDE.md`, `*.mjs` scripts, `dashboard/*`, `templates/*`, `batch/*`

**User Layer** (never auto-updated, personalization lives here):
- `cv.md`, `config/profile.yml`, `modes/_profile.md`, `article-digest.md`
- `data/*`, `reports/*`, `output/*`, `interview-prep/*`

This pattern allows `node update-system.mjs apply` to update the system layer while preserving all user data.

---

## Implications for AI Agent Design

1. **Slash command + modes/*.md** is a powerful pattern for multi-capability agents — each mode is a standalone prompt loaded on demand, reducing context overhead and improving focus.

2. **Two-layer data contract** (system vs. user) is essential for any agent system that needs to be updateable without destroying user state.

3. **Evolving context** via append-only files (story-bank, article-digest) creates genuine capability accumulation — the agent gets better at its job over time without retraining.

4. **Sub-agent batch processing** with `claude -p` workers demonstrates how to parallelize AI workloads: clean context per task, orchestrator handles state, resumable via state file.

5. **Pipeline integrity** patterns (TSV intermediates, merge scripts, dedup) are critical when multiple agents write to a shared data store.

6. **Human-in-the-loop** as a hard constraint: "NEVER submit without user review" is built into the system prompt, not left to chance.
