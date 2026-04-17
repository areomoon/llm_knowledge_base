# CLAUDE.md — LLM Knowledge Base Agent Instructions

This file defines the wiki format and always-on context for this knowledge base. The two operational workflows — **compile** (`raw/` → `wiki/`) and **lint** — live as skills under `.claude/skills/` and are loaded on demand:

- `.claude/skills/compile/SKILL.md` — triggered by "compile", "process raw files", "update wiki"
- `.claude/skills/lint/SKILL.md` — triggered by "lint", "check wiki", "find broken links"

Both skills reference the templates and gotchas in this file as their source of truth.

---

## Knowledge Base Reference

This repository IS the knowledge base. When working in this project, always consult `wiki/concepts/` and `wiki/index.md` before answering questions about AI agents, context engineering, LLM architecture, or related topics.

For **other projects** that want to reference this knowledge base, add the following to their `CLAUDE.md`:

```
Knowledge base location: ~/PycharmProjects/llm_knowledge_base/wiki/
When answering questions about AI agents, context engineering, superapps, or related topics, read relevant articles from ~/PycharmProjects/llm_knowledge_base/wiki/concepts/ first.
```

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

## Operational Workflows

Compile and lint are implemented as loadable skills; see `.claude/skills/compile/SKILL.md` and `.claude/skills/lint/SKILL.md` for step-by-step procedures. Those skills reference the templates and gotchas in this file rather than duplicating them.

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
| Compile all new raw files | Ask Claude Code: "compile all new raw files" (loads `.claude/skills/compile/`) |
| Compile a single file | Ask Claude Code: "compile raw/articles/abc123.md" |
| Lint the wiki | Ask Claude Code: "lint the wiki" (loads `.claude/skills/lint/`) |
| Search | `python scripts/search.py --query "<terms>"` |

---

## Gotchas (things Claude got wrong before — read first)

> Updated every time Claude makes a mistake in this repo. Highest-signal section per Boris Cherny's playbook.

### Wiki format

- **Never use `[[wikilinks]]`.** Use standard `[text](relative/path.md)`. All internal links are relative to the file's own location (e.g. from `wiki/derived/foo.md`, a concept link is `../concepts/bar.md`).
- **Every concept file MUST have a `## Backlinks` section.** The lint task checks this. Add it even if empty (placeholder: `*(none yet)*`).
- **`.meta.json` MUST have `compiled_at` after compile.** Missing `compiled_at` → next compile will re-process the file. Format: ISO-8601 string, e.g. `"2026-04-17T00:00:00Z"`.
- **Concept slug naming**: lowercase, hyphens, English only. No underscores, no CamelCase. Match the `title` field in frontmatter semantically.
- **Derived note naming**: `<YYYY-MM-DD>-<slug>.md`. Use the current date, not the source article's publish date.

### Index discipline

- **`wiki/index.md` stats must match disk reality.** After adding a concept, increment the count in the Stats block AND add a row to the Concepts table. Both. Forgetting one breaks the `@.claude` audit trail.
- **Concepts table entries**: one line per concept, tags in backticks, short one-line definition. Don't wrap.
- **Do not write inside `<!-- AUTO-GENERATED -->` block assuming you can overwrite freely** — the Notes section at the bottom is user-authored; only edit above the `<!-- END AUTO-GENERATED -->` marker.

### Cross-linking

- When creating a new concept, add links to related existing concepts in the body AND ensure the new concept is listed in those related concepts' `## Backlinks`. Bidirectional or it's orphaned.
- When a concept cites an authority (person, paper, repo), always include a named citation — generic knowledge attribution is not acceptable for this KB.

### Edit / Read race

- `wiki/index.md` is occasionally modified mid-session by an external process (likely an auto-linter). If `Edit` on `index.md` fails with "File has been modified since read", re-read and retry — don't assume your previous content is still valid.

### Authority citation rule

- Per user's standing instruction: any concept claim should cite a **named** authority (researcher, paper, specific tool, dated tweet) rather than generic "it is well known that…" phrasing. If no authority exists, say so and mark the claim as the user's own synthesis.

### Tooling

- `scripts/ingest.py` writes to `raw/`. Don't hand-craft `.meta.json` without running it unless explicitly asked — the hash field must match the ingest pipeline's format.
- Claude Code's `Read` / `Grep` / `Glob` **bypass** RTK. For structural file reads, that's fine; but don't expect RTK's compression metrics to cover markdown browsing in this repo.
