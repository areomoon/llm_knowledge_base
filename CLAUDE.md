# CLAUDE.md — LLM Knowledge Base Agent Instructions

This file defines how Claude Code Agent handles **compile** (`raw/` → `wiki/`) and **lint** tasks for this knowledge base. Run these tasks directly via Claude Code instead of calling scripts.

---

## Wiki Format Specifications

### Naming Rules

- **Concept files**: `wiki/concepts/<slug>.md` — lowercase, hyphens, English only
  - e.g. `attention-mechanism.md`, `rlhf.md`, `chain-of-thought.md`
- **Derived files**: `wiki/derived/<YYYY-MM-DD>-<slug>.md`
  - e.g. `2026-04-08-attention-is-all-you-need.md`
- **Query files**: `wiki/queries/<YYYY-MM-DD>-<slug>.md`

### Link Format

Use standard GitHub Markdown links — **not** `[[wikilinks]]`:

```markdown
[Attention Mechanism](concepts/attention-mechanism.md)
[RLHF](concepts/rlhf.md)
```

All internal links are relative to `wiki/`. Cross-linking between concept articles is strongly encouraged.

### Concept Article Template

```markdown
---
title: <Concept Name>
tags: [<tag1>, <tag2>]
sources: [<raw file paths or URLs>]
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# <Concept Name>

> **TL;DR**: One sentence that captures the core idea.

## Definition

Clear, precise definition in 2–4 sentences. Avoid jargon where possible; define acronyms on first use.

## How It Works

Explain the mechanism, algorithm, or intuition. Use numbered steps or diagrams (Mermaid) when helpful.

## Key Properties

- Property 1
- Property 2
- Property 3

## Variants & Related Work

| Variant | Description | Paper |
|---------|-------------|-------|
| ...     | ...         | ...   |

## When to Use

Practical guidance on applicability, trade-offs, and failure modes.

## Backlinks

Pages that reference this concept (maintain manually or via lint task):
- [Page Title](path/to/page.md)

## Sources

- [Source Title](URL or raw/path)
```

### Derived Note Template

```markdown
---
title: <Source Title>
type: <article|paper|repo|dataset>
source_url: <URL>
raw_path: <raw/articles/abc123.md>
created: <YYYY-MM-DD>
---

# <Source Title>

> **TL;DR**: One sentence summary.

## Key Points

- Point 1
- Point 2

## Concepts Referenced

- [Concept Name](../concepts/slug.md)

## Notes

Free-form observations, questions, connections to other work.
```

---

## Compile Task (`raw/` → `wiki/`)

**Trigger**: "compile", "process raw files", "update wiki"

### Steps

1. **Scan `raw/`** for unprocessed files:
   - Check each file's corresponding `.meta.json` for `compiled_at` field
   - Files without `compiled_at` or with `hash` mismatch are unprocessed

2. **For each unprocessed file**:
   a. Read the file content and its `.meta.json` (contains `type`, `source`, `hash`)
   b. Generate a **derived note** in `wiki/derived/` using the Derived Note Template above
   c. Extract **concepts** mentioned in the file:
      - Identify AI/LLM terms, model names, techniques, acronyms
      - For each concept, check if `wiki/concepts/<slug>.md` already exists
      - If exists: merge new information into the existing article (add sources, expand sections)
      - If new: create the article using the Concept Article Template above
   d. Update the `.meta.json` with `compiled_at: <ISO datetime>`

3. **Update `wiki/index.md`**:
   - Recount all articles in `wiki/concepts/`, `wiki/derived/`, `wiki/queries/`
   - Update the stats block and article lists (see index format in `wiki/index.md`)
   - Sort concepts alphabetically, derived notes by date descending

4. **Verify cross-links**:
   - Ensure each new concept article links to related concepts
   - Ensure the derived note links to all concepts it mentions

### LLM Guidance for Concept Extraction

When processing a raw file, use this reasoning:
- What are the **named techniques or methods**? (e.g., "LoRA", "Flash Attention")
- What are the **key ideas or claims**? Distill into concept definitions
- What **existing concepts** does this source expand or contradict?
- Aim for **atomic concept articles**: one clear idea per file, ~200–800 words

---

## Lint Task

**Trigger**: "lint", "check wiki", "find broken links", "health check"

### Steps

1. **Collect all pages**: build a map of `slug → path` for every `.md` file in `wiki/`

2. **Check broken links**:
   - Scan all `.md` files for `[text](path.md)` links
   - Verify each relative link target exists on disk
   - Report: `source_file:line_number → broken target`

3. **Find orphan pages**:
   - Build a reverse-link graph: for each page, which pages link to it?
   - Pages with zero incoming links (excluding `index.md`) are orphans
   - Report orphans; suggest adding links from related concept articles

4. **Check missing backlinks**:
   - For each link `A → B`, verify `B`'s `## Backlinks` section lists `A`
   - Report missing entries; offer to auto-add them

5. **Suggest missing topics** (optional, requires LLM):
   - Collect all concept titles
   - Ask: "Given these AI/LLM concepts, what important topics are missing?"
   - Output suggestions as a list

6. **Produce health report**:
   ```
   === Wiki Health Report ===
   Total pages: N
   Broken links: N  [list]
   Orphan pages: N  [list]
   Missing backlinks: N  [list]
   Suggested topics: [list]  (if requested)
   ```

### Auto-fix Policy

- **Backlinks**: safe to auto-add missing entries to `## Backlinks` sections
- **Broken links**: only auto-fix if fuzzy match confidence > 0.90; otherwise flag for human review
- **Orphans**: never auto-delete; only suggest linking

---

## Directory Reference

```
raw/
├── articles/        # Web articles (.md + .meta.json)
├── papers/          # PDFs and paper notes (.pdf, .md + .meta.json)
├── repos/           # GitHub repo summaries
└── datasets/        # Dataset descriptions

wiki/
├── index.md         # Auto-maintained master index
├── concepts/        # Concept articles (one idea per file)
├── derived/         # Source summaries (one per raw file)
└── queries/         # Q&A session logs

scripts/
├── ingest.py        # Fetch URLs → raw/ (run directly)
└── search.py        # Search wiki content (run directly)
```

---

## Quick Reference

| Task | How to run |
|------|-----------|
| Ingest a URL | `python scripts/ingest.py --type article --url <URL>` |
| Compile all new raw files | Ask Claude Code: "compile all new raw files" |
| Compile a single file | Ask Claude Code: "compile raw/articles/abc123.md" |
| Lint the wiki | Ask Claude Code: "lint the wiki" |
| Search | `python scripts/search.py --query "<terms>"` |
