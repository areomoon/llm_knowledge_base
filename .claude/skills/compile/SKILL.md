---
name: compile
description: Process unprocessed files in `raw/` into the wiki — generate a derived note in `wiki/derived/`, extract/merge concept articles in `wiki/concepts/`, stamp `.meta.json` with `compiled_at`, and update `wiki/index.md`. Trigger on "compile", "process raw files", "update wiki", or when the user points at a specific `raw/**/*.md` file to add to the KB.
---

# Compile Skill — `raw/` → `wiki/`

Canonical templates (Concept Article, Derived Note) and format rules (link style, naming, Backlinks requirement) live in the **Wiki Format Specifications** section of the project `CLAUDE.md`. Always read that first — do not duplicate the templates here.

## Steps

1. **Scan `raw/`** for unprocessed files:
   - Check each file's corresponding `.meta.json` for `compiled_at` field.
   - Files without `compiled_at` or with `hash` mismatch are unprocessed.

2. **For each unprocessed file**:
   a. Read the file content and its `.meta.json` (contains `type`, `source`, `hash`).
   b. Generate a **derived note** in `wiki/derived/` using the Derived Note Template from `CLAUDE.md`.
   c. Extract **concepts** mentioned in the file:
      - Identify AI/LLM terms, model names, techniques, acronyms.
      - For each concept, check if `wiki/concepts/<slug>.md` already exists.
      - If exists: merge new information into the existing article (add sources, expand sections).
      - If new: create the article using the Concept Article Template from `CLAUDE.md`.
   d. Update the `.meta.json` with `compiled_at: <ISO datetime>`.

3. **Update `wiki/index.md`**:
   - Recount all articles in `wiki/concepts/`, `wiki/derived/`, `wiki/queries/`.
   - Update the stats block and article lists.
   - Sort concepts alphabetically, derived notes by date descending.
   - Only edit above the `<!-- END AUTO-GENERATED -->` marker.

4. **Verify cross-links**:
   - Ensure each new concept article links to related existing concepts.
   - Ensure those related concepts list the new page in their `## Backlinks` (bidirectional).
   - Ensure the derived note links to every concept it mentions.

## LLM Guidance for Concept Extraction

When processing a raw file, reason:
- What are the **named techniques or methods**? (e.g., "LoRA", "Flash Attention")
- What are the **key ideas or claims**? Distill into concept definitions.
- What **existing concepts** does this source expand or contradict?
- Aim for **atomic concept articles**: one clear idea per file, ~200–800 words.
- Every claim cites a **named authority** (researcher, paper, specific tool, dated post). No generic "it is well known that…".

## Post-compile checklist

- [ ] `.meta.json` has `compiled_at` (ISO-8601, e.g. `"2026-04-17T00:00:00Z"`).
- [ ] Derived note filename is `<YYYY-MM-DD>-<slug>.md` using **today's date**, not the source publish date.
- [ ] Each new concept file has a `## Backlinks` section (placeholder `*(none yet)*` if empty).
- [ ] `wiki/index.md` Stats block count matches disk reality AND the Concepts table has a new row.
- [ ] All internal links use `[text](relative/path.md)`, never `[[wikilinks]]`.
