---
title: Retrieval-Augmented Verification
tags: [hallucination, verification, citation, traceability, patent, extraction, rag]
sources:
  - Gao et al. 2023 — Enabling Large Language Models to Generate Text with Citations (https://arxiv.org/abs/2305.14627)
  - Es et al. 2023 — RAGAS (https://arxiv.org/abs/2309.15217)
  - conversation: prompt_engineering_lab walkthrough 2026-04-23
created: 2026-04-23
updated: 2026-04-23
---

# Retrieval-Augmented Verification

> **TL;DR**: After extracting a value, verify it appears (verbatim or semantically) in the source text. Catches the failure mode self-consistency misses: when all N samples agree on a hallucinated value because the model's prior invented it out of thin air.

## Definition

Retrieval-Augmented Verification (RAV) is the post-extraction check that every extracted value is grounded in a specific span of the source document. Three implementation tiers:

1. **Exact match** — the extracted string appears verbatim in source.
2. **Fuzzy / semantic match** — extracted value's embedding matches a source span within similarity ε.
3. **Citation span** — the LLM is asked to output not just the value but also the source span supporting it; a second pass verifies the span is real and its content matches.

Related literature: citation-generation (Gao et al. 2023, [arXiv:2305.14627](https://arxiv.org/abs/2305.14627)), RAGAS faithfulness metrics (Es et al. 2023, [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)).

## How It Works

```python
# Tier 3: citation-span pattern with verification
extraction = llm.extract(
    patent_text,
    schema_requires="value + supporting_span",
)
for field, v in extraction.items():
    span = v["supporting_span"]
    if span not in patent_text:
        flag(field, "hallucinated span")
    elif not contains_value(span, v["value"]):
        flag(field, "span does not support value")
    else:
        accept(field, v)
```

Why this catches what self-consistency can't: if the model's prior for "oxygen pressure in PLD" is 200 mTorr, all N self-consistency samples may converge on 200 mTorr even when the patent says 350 mTorr or doesn't specify at all. Self-consistency's agreement signal says "high confidence" — but the extraction is wrong. Retrieval verification catches it because the claimed span either doesn't contain 200 or doesn't exist.

## Key Properties

- **Catches shared-prior hallucinations that self-consistency reinforces.** These are the most dangerous failure mode — high confidence + wrong answer.
- **Grants auditability / traceability.** For patent and regulatory work, being able to show "this extracted claim 1 temperature of 700°C corresponds to this exact span in column 3, line 15" is often a hard requirement, not a nice-to-have.
- **Adds cost: one extra LLM call or one embedding lookup per field.** Embedding-based RAV is cheap (~$0.0001/call on voyage-3 or text-embedding-3-small). Exact-match RAV is free.
- **False negatives on paraphrased values.** If source says "seven hundred degrees Celsius" and extraction says "700°C", exact match fails. Normalise both sides before comparison.

## Industry Applications

- **Anthropic Citations API** (introduced 2025) — built-in support for passage-level citations in Claude responses. Use when source traceability is a product requirement.
- **Perplexity AI / You.com** — every answer sentence linked to a source URL; verification is part of the UX contract.
- **Legal tech** (Harvey, Casetext) — extracted legal citations are always verified against actual case text before surfacing to lawyers.
- **Patsnap-relevant**: this is arguably the most important pattern for Patsnap. Patent extraction without source-span traceability is not shippable for IP-law use cases — customers use the extracted data in infringement analysis and patent prosecution, where every claim must be defensible.
- **Medical evidence extraction** (Elicit, Consensus) — verification against the original paper is the core product.

## When to Use

**Mandatory when:**
- Output traceability is a regulatory / legal requirement (patents, medicine, law, finance).
- Downstream users will challenge the output's veracity (analyst reports, expert witness testimony).
- Source documents are long and highly specific (patents average 20–50 pages; memorisation is a real failure mode).

**Optional when:**
- Output is summarisation / paraphrase, not extraction (no exact-value correspondence expected).
- Source is short and was already in-context — hallucination risk is low.

## Implementation Tiers (pick by budget)

| Tier | Cost | Coverage | Best for |
|---|---|---|---|
| Exact-match after normalisation | ~Free | Misses paraphrases | Patent claim values, dates, numerics |
| Embedding similarity on spans | $0.0001/field | Catches paraphrases | Descriptive extractions, material names |
| Second-pass LLM verification | $0.001–$0.01/field | Highest coverage, reasoning-aware | High-stakes legal / medical |

Start at the cheapest tier; escalate only when the tier misses errors that matter.

## Patsnap-Specific Applications

- **Mandatory for Claim 1 extractions.** Legal defensibility requires span traceability.
- **Pair with [Constrained Decoding](constrained-decoding.md)** — schema requires `{value, supporting_span}` pair; decoder enforces both.
- **Store spans in the output record** — becomes the audit trail downstream tools (search, analytics) can link back to.
- **Measure faithfulness as a production KPI**, not just accuracy. Use [RAGAS](https://docs.ragas.io/) or equivalent on a monthly held-out set.

## Related Concepts

- [Self-Consistency Implementation](self-consistency-implementation.md) — what RAV catches that self-consistency misses.
- [Constrained Decoding](constrained-decoding.md) — forces the schema that includes supporting spans.
- [LLM-as-Judge](llm-as-judge.md) — often used for the tier-3 second-pass verification.
- [Memory Stores vs RAG](memory-stores-vs-rag.md) — retrieval as context vs retrieval as verification.
- [Material Science Agents](material-science-agents.md) — where extracted values feed experiment-design logic; grounding is safety-critical.

## Backlinks

- [Self-Consistency Implementation](self-consistency-implementation.md)
- [LLM-as-Judge](llm-as-judge.md)
- [Constrained Decoding](constrained-decoding.md)
- [Self-Refine / Critic Loop](self-refine-critic-loop.md)
- [Model Ensembling](model-ensembling.md)
- [Logprob Uncertainty](logprob-uncertainty.md)
- [Material Science Agents](material-science-agents.md)
- [Memory Stores vs RAG](memory-stores-vs-rag.md)
- [Agent Evaluation](agent-evaluation.md)
- [derived: Extraction Pipeline Composite Strategies](../derived/2026-04-23-extraction-pipeline-composite-strategies.md)

## Sources

- [Enabling Large Language Models to Generate Text with Citations (Gao et al. 2023)](https://arxiv.org/abs/2305.14627) — ALCE benchmark, citation generation methodology.
- [RAGAS: Automated Evaluation of Retrieval Augmented Generation (Es et al. 2023)](https://arxiv.org/abs/2309.15217) — faithfulness metric is RAV at eval time.
- [Anthropic Citations API documentation](https://docs.anthropic.com/en/docs/build-with-claude/citations).
- Conversation: prompt_engineering_lab walkthrough 2026-04-23.
