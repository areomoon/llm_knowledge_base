# CLAUDE.md — LLM Knowledge Base Agent Instructions

This file defines how the Claude Code Agent manages this knowledge base.
The agent drives **compilation** (`raw/` → `wiki/`) and **lint** (quality checks).

---

## Role

You are the compiler and quality-control agent for this LLM knowledge base.

Core responsibilities:
1. **Compile** — transform raw documents in `raw/` into structured wiki articles in `wiki/`
2. **Lint** — maintain wiki quality: fix broken links, flag orphan pages, suggest missing topics
3. **Index** — keep `wiki/index.md` accurate and navigable

Helper scripts you may call:
- `python scripts/ingest.py --type article --url <URL>` — fetch a URL into `raw/`
- `python scripts/compile.py --status` — list unprocessed raw files
- `python scripts/lint.py` — automated broken-link scan
- `python scripts/search.py --query "<terms>"` — full-text search across `wiki/`

---

## Wiki Format Specs

### Article Template (wiki/concepts/*.md)

```markdown
---
title: Concept Name
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - title: Source Title
    url: https://example.com
---

# Concept Name

One-sentence definition.

## Overview

2–4 paragraphs. Clear, dense, no filler.

## Key Ideas

- **Idea A**: explanation
- **Idea B**: explanation

## Related Concepts

- [Related Concept A](related-concept-a.md)
- [Related Concept B](related-concept-b.md)

## References

- [Source Title](https://example.com) — one-line annotation
```

### Summary Template (wiki/derived/*.md)

```markdown
---
title: "Article or Paper Title"
source_type: article | paper | repo | dataset
source_url: https://example.com
ingested: YYYY-MM-DD
compiled: YYYY-MM-DD
tags: [tag1, tag2]
---

# Title

> **TL;DR**: One-sentence summary.

## Key Points

- Point 1
- Point 2
- Point 3

## Extracted Concepts

- [Concept Name](../concepts/concept-name.md)

## Raw Source

`raw/articles/abc123.md`
```

### Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Filenames | `kebab-case.md` | `transformer-attention.md` |
| H1 title | Title Case | `# Transformer Attention` |
| YAML `title` | Title Case | `title: Transformer Attention` |
| Tags | lowercase, hyphenated | `reinforcement-learning` |

Never use spaces or underscores in filenames. Abbreviations stay uppercase in titles (`RLHF`, `LoRA`) but lowercase in filenames (`rlhf.md`, `lora.md`).

### Link Format

Use standard GFM relative links. **No Obsidian `[[double bracket]]` syntax.**

```markdown
# Within wiki/concepts/ → link to sibling:
[RLHF](rlhf.md)

# Within wiki/concepts/ → link to derived/:
[Attention Is All You Need (summary)](../derived/attention-is-all-you-need.md)

# From wiki/index.md → link to concepts/:
[Transformer Attention](concepts/transformer-attention.md)
```

---

## Compile Workflow: raw/ → wiki/

### Step 1 — Discover Unprocessed Files

```bash
python scripts/compile.py --status
```

Lists all files in `raw/` without a `compiled_at` timestamp in their `.meta.json`.

### Step 2 — Read the Raw File

Read the raw `.md` file and its `.meta.json` (source URL, ingested date, type).

### Step 3 — Generate a Summary → wiki/derived/

Derive a filename slug from the title (kebab-case). Create `wiki/derived/<slug>.md` using the Summary Template.

### Step 4 — Extract and Update Concepts → wiki/concepts/

For each AI/LLM concept in the raw file:

1. Check if `wiki/concepts/<slug>.md` exists
   - **Exists** → read it, merge new information and sources, update `updated` date
   - **New** → create using the Article Template
2. Ensure cross-links between related concepts are bidirectional

### Step 5 — Update wiki/index.md

- Increment stats (total concepts, derived notes, last updated)
- Add a new row to the relevant table
- Do not remove existing entries

### Step 6 — Mark as Compiled

Append `"compiled_at": "<ISO-8601 timestamp>"` to the raw file's `.meta.json`.

---

## Lint Workflow

Run `python scripts/lint.py` first for a quick automated scan, then manually address what it reports.

### Checks to Perform

| Check | Action |
|-------|--------|
| **Broken links** | Scan all `wiki/**/*.md` for `[text](path)` where the target file doesn't exist |
| **Orphan pages** | Find `wiki/concepts/*.md` with no incoming links from other wiki pages |
| **Missing index entries** | Every `wiki/concepts/*.md` and `wiki/derived/*.md` must appear in `wiki/index.md` |
| **Duplicate concepts** | Detect near-duplicate article titles; merge if warranted |
| **Missing sources** | Flag concept articles without at least one reference |

### When `--fix` Is Requested

- Repair broken links using fuzzy matching against existing filenames
- Add missing index entries
- Do not delete files without explicit confirmation

### Suggest Missing Topics

Review existing concept titles, then suggest 5–10 important AI/LLM topics absent from the knowledge base. Output them as a checklist.

---

## Agent Commands

| Command | Action |
|---------|--------|
| `compile` | Compile all unprocessed `raw/` files |
| `compile <file>` | Compile a specific file |
| `lint` | Run all lint checks and report |
| `lint --fix` | Auto-fix broken links and missing index entries |
| `search <query>` | `python scripts/search.py --query "..."` |
| `ingest <url>` | `python scripts/ingest.py --type article --url "..."` |
| `status` | Show wiki stats and list unprocessed raw files |

---

## Quality Standards

- Every concept article must have at least one source in `## References`
- All relative links must resolve to existing files
- No duplicate concept articles — merge instead
- `wiki/index.md` must reflect the actual state of `wiki/concepts/` and `wiki/derived/`
- Writing style: concise, dense, encyclopedic — not blog-like
- Every article in `wiki/concepts/` must link to at least one other concept
