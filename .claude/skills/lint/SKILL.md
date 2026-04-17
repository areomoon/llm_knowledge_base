---
name: lint
description: Health-check the wiki — scan `wiki/**/*.md` for broken relative links, orphan pages (no incoming links), and missing `## Backlinks` entries; optionally suggest missing concept topics; output a Wiki Health Report. Trigger on "lint", "check wiki", "find broken links", "health check", or "wiki audit".
---

# Lint Skill — Wiki Health Check

Canonical format rules (link style, Backlinks requirement, index discipline) live in the **Wiki Format Specifications** and **Gotchas** sections of the project `CLAUDE.md`. Read those before lint-fixing.

## Steps

1. **Collect all pages**: build a map of `slug → path` for every `.md` file in `wiki/`.

2. **Check broken links**:
   - Scan all `.md` files for `[text](path.md)` links.
   - Verify each relative link target exists on disk (resolve relative to the source file's directory).
   - Report: `source_file:line_number → broken target`.

3. **Find orphan pages**:
   - Build a reverse-link graph: for each page, which pages link to it?
   - Pages with zero incoming links (excluding `index.md`) are orphans.
   - Report orphans; suggest adding links from related concept articles.

4. **Check missing backlinks**:
   - For each link `A → B`, verify `B`'s `## Backlinks` section lists `A`.
   - Report missing entries; offer to auto-add them.

5. **Suggest missing topics** (optional, requires LLM):
   - Collect all concept titles.
   - Ask: "Given these AI/LLM concepts, what important topics are missing?"
   - Output suggestions as a list.

6. **Produce health report**:
   ```
   === Wiki Health Report ===
   Total pages: N
   Broken links: N  [list]
   Orphan pages: N  [list]
   Missing backlinks: N  [list]
   Suggested topics: [list]  (if requested)
   ```

## Auto-fix Policy

- **Backlinks**: safe to auto-add missing entries to `## Backlinks` sections.
- **Broken links**: only auto-fix if fuzzy-match confidence > 0.90; otherwise flag for human review.
- **Orphans**: never auto-delete; only suggest linking.
- **Index stats drift**: if `wiki/index.md` count disagrees with disk, fix the stats block AND the Concepts table (both — see CLAUDE.md Gotchas).

## Watch-outs (from Gotchas)

- `wiki/index.md` may be modified mid-session by an external linter. If `Edit` fails with "File has been modified since read", re-read and retry.
- Do not write below the `<!-- END AUTO-GENERATED -->` marker in `index.md` — that section is user-authored.
