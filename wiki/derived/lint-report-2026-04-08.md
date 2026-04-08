---
title: "Wiki Lint Report — 2026-04-08"
source_type: lint-report
compiled: 2026-04-08
tags: [lint, quality, wiki-health]
---

# Wiki Lint Report — 2026-04-08

> Full compile + lint pass over the entire wiki and raw/ directory.

---

## Compile: Unprocessed Raw Files

### Files Without `compiled_at` (before this pass)

| File | Status |
|------|--------|
| `raw/areomoon_career_llm/Claude_Code_Leak_Architecture_Insights.md` | ✅ Compiled |
| `raw/areomoon_career_llm/Agentic_Service_Warmup_Plan.md` | ✅ Compiled |
| `raw/areomoon_career_llm/Career_Development_Roadmap.md` | ✅ Compiled |

**Actions taken:**
- Created `meta.json` for all three files with `compiled_at: 2026-04-08T00:00:00Z`
- Created `wiki/derived/claude-code-leak-architecture-insights.md`
- Created `wiki/derived/agentic-service-warmup-plan.md`
- Created `wiki/derived/career-development-roadmap.md`

**New concepts extracted from Claude Code Leak:**
- Created `wiki/concepts/agentic-harness.md` — 12-pattern harness design catalog
- Created `wiki/concepts/tiered-memory.md` — L1/L2/L3 tiered memory architecture

---

## Lint: Broken Links

### Found and Fixed

| Location | Broken Link | Fix Applied |
|----------|-------------|-------------|
| `wiki/index.md:25` | `[Concept Name](concepts/slug.md)` — template placeholder | Replaced header with plain text `Concept` column header |
| `wiki/index.md:43` | `[Title](derived/YYYY-MM-DD-slug.md)` — template placeholder | Replaced header with plain text `Title` column header |
| `wiki/concepts/ace-framework.md:30` | `[Generator](ace-framework.md)`, `[Reflector](ace-framework.md)`, `[Curator](ace-framework.md)` — 3 self-referential links | Changed to plain text |

### Not Broken (false positive check)
- `wiki/index.md:58`: `[Query](queries/YYYY-MM-DD-slug.md)` — inside an HTML comment block; not rendered as a link. No action needed.

---

## Lint: Orphan Pages

### Result: No Orphans

All concept articles are linked from `wiki/index.md` and at least one peer concept article. Incoming link counts:

| Article | Incoming Links (from concepts + derived) |
|---------|------------------------------------------|
| `ace-framework.md` | 7 |
| `context-engineering.md` | 5 |
| `evolving-playbooks.md` | 6 |
| `agentic-self-improvement.md` | 6 |
| `superapp-paradigm.md` | 3 |
| `api-to-superagent.md` | 3 |
| `agent-friendly-design.md` | 3 |
| `material-science-agents.md` | 4 |
| `ace-for-materials.md` | 4 |
| `agentic-harness.md` | 3 (new) |
| `tiered-memory.md` | 3 (new) |

---

## Lint: Missing Cross-Links

### Fixed

| Source | Missing Link To | Fix |
|--------|----------------|-----|
| `ace-framework.md` | `ace-for-materials.md` | Added to Related Concepts |
| `evolving-playbooks.md` | `ace-for-materials.md` | Added to Related Concepts |
| `agentic-self-improvement.md` | `material-science-agents.md` | Added to Related Concepts |
| `context-engineering.md` | `tiered-memory.md`, `agentic-harness.md` | Added to Related Concepts |
| `agent-friendly-design.md` | `agentic-harness.md` | Added to Related Concepts |
| `material-science-agents.md` | `agentic-harness.md` | Added to Related Concepts |
| `ace-for-materials.md` | `agentic-harness.md` | Added to Related Concepts |

---

## Lint: Missing Backlinks Sections

### Found and Fixed

All 9 pre-existing concept articles were missing `## Backlinks` sections entirely (compiled with an older template). Two new articles include Backlinks sections from creation.

**Added `## Backlinks` to:**
- `ace-framework.md`
- `context-engineering.md`
- `evolving-playbooks.md`
- `agentic-self-improvement.md`
- `superapp-paradigm.md`
- `api-to-superagent.md`
- `agent-friendly-design.md`
- `material-science-agents.md`
- `ace-for-materials.md`

---

## Lint: Format Consistency

### Missing `## References` Section
All concept articles: ✅ have References section.

### Missing `## Related Concepts` Section
All concept articles: ✅ have Related Concepts section.

### YAML Frontmatter
All concept articles: ✅ have valid frontmatter with `title`, `tags`, `created`, `updated`, `sources`.

### Derived Notes Frontmatter
All derived notes: ✅ have valid frontmatter.

### Naming Convention
All files: ✅ kebab-case filenames. Exception: `raw/areomoon_career_llm/` files use mixed case (original filenames from source repo — intentionally preserved, not wiki files).

---

## Suggested Missing Topics

Based on existing concept coverage, these AI/LLM topics are absent from the knowledge base and would be high-value additions:

- [ ] **RAG (Retrieval-Augmented Generation)** — mentioned repeatedly in derived notes as a technique but has no standalone concept article
- [ ] **LoRA / QLoRA Fine-Tuning** — central technique for domain adaptation in the warmup plan; no wiki article
- [ ] **Multi-Modal LLMs** — critical for scientific document processing; referenced in several articles but not defined
- [ ] **Chain-of-Thought (CoT) Prompting** — foundational prompting technique; referenced but not defined
- [ ] **LLM Evaluation (LLM-as-Judge, benchmarks)** — heavily discussed in warmup plan; evaluation design is a key skill
- [ ] **MCP (Model Context Protocol)** — referenced in multiple articles as foundational; deserves its own concept article
- [ ] **ReAct Pattern** — foundational agent loop pattern mentioned in warmup plan; not in wiki
- [ ] **Scientific Document Intelligence** — the overarching application domain; would tie material science agents, multi-modal, RAG into one concept

---

## Wiki Health Summary (Post-Fix)

```
=== Wiki Health Report — 2026-04-08 ===
Total concept articles : 11  (+2 new: agentic-harness, tiered-memory)
Total derived notes    : 6   (+3 new: claude-code-leak, warmup-plan, career-roadmap)
Total raw files compiled: 6/6 (100%)
Broken links fixed     : 3
Missing backlinks fixed : 9 articles
Missing cross-links fixed: 7
Orphan pages           : 0
Suggested new topics   : 8
```
