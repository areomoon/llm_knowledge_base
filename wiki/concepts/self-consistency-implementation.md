---
title: Self-Consistency Implementation
tags: [self-consistency, extraction, confidence, aggregation, implementation, patsnap, algorithm-engineer]
sources:
  - Wang et al. 2022 (https://arxiv.org/abs/2203.11171)
  - conversation: prompt_engineering_lab walkthrough 2026-04-23
created: 2026-04-23
updated: 2026-04-23
---

# Self-Consistency Implementation

> **TL;DR**: Self-consistency's production value is not "vote for the best answer" — it's "produce per-field confidence so the pipeline can route". Implementation hinges on field-level aggregation, normalisation before voting, and numeric tolerance bands; none of which are in the original paper.

## Definition

Self-consistency (Wang et al. 2022, [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)) samples N independent reasoning paths with `temperature > 0`, then aggregates their outputs. For structured extraction (the Patsnap use case), the aggregation is **per-field majority vote with a confidence score = vote share**, not whole-output matching.

This concept covers the implementation details — the paper describes the algorithm on arithmetic QA benchmarks; shipping it in a production extraction pipeline requires several additions the paper never discusses.

## How It Works

### Core recipe

```python
# 1. Fan-out N independent samples
samples = []
for _ in range(N):
    resp = client.messages.create(
        model="claude-haiku-4-5",   # Opus 4.7 drops temperature/top_p/top_k
        temperature=0.7,
        messages=[...],
    )
    samples.append(parse_json(resp))

# 2. Field-level aggregation — NOT whole-JSON comparison
aggregated = {}
for field in SCHEMA:
    values = [s.get(field) for s in samples if field in s]
    normalized = [normalize(field, v) for v in values]
    counter = Counter(normalized)
    top_value, top_count = counter.most_common(1)[0]
    aggregated[field] = {
        "value": top_value,
        "confidence": top_count / len(samples),
        "all_votes": dict(counter),
    }
```

### Six pitfalls (the part the paper skips)

1. **Field-level aggregation is non-negotiable.** Whole-JSON diffing classifies any single-field disagreement as total mismatch, so you'd get near-zero agreement on long schemas. Aggregate field by field.

2. **Normalisation is the real work.** `"700°C"` / `"700 C"` / `700` / `"seven hundred celsius"` must map to the same canonical form before `Counter`. Use Pydantic validators, unit-aware regex, or a lightweight normalisation DSL per field type.

3. **Numeric fields need tolerance-band voting.** Without it, `0.0012` and `0.00120` vote separately. Conventions: bucket numerics to K significant figures, or cluster with ε-nearest-neighbour (ε = 1–5% of the magnitude).

4. **Temperature selection is task-specific.** 0.5–0.9 is the live band. Below 0.3, samples collapse to one answer and self-consistency has nothing to measure; above 1.0, the model starts inventing values not in the source. Ablate per task on a labelled eval set — do not default blindly to 0.7.

5. **N = 3 → 5 → 10 is diminishing-returns.** N=3 already captures most of the gain; N=5 is a typical sweet spot; N=10 rarely earns its cost. Use [Anthropic's Batch API](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) to compress the 5× wall-cost into ~2.5× spend, and `asyncio.gather` to keep wall-latency at ~1× instead of 5×.

6. **Model-family caveat.** Claude Opus 4.7 removes `temperature`, `top_p`, `top_k` as tunable parameters — self-consistency across Opus samples will collapse into the same output. Use Haiku 4.5 or Sonnet 4.6. See [Claude Managed Agents](claude-managed-agents.md) for the broader Anthropic API context.

### Reference system diagram

```
[Input]
   ↓
[Dispatcher] ── fan-out N async calls → [LLM]
   ↓                                     ↓
[Sample Store] ← N raw JSONs ────────────┘
   ↓
[Normalizer]  (unit canonicalisation, numeric binning, enum mapping)
   ↓
[Aggregator]  (field-level majority vote + confidence)
   ↓
[Router]      ├── conf ≥ 0.8  → auto-accept
              ├── 0.5–0.8     → LLM-as-judge secondary ruling
              └── conf < 0.5  → human review queue
   ↓
[Output + Telemetry]  (per-field confidence timeseries → drift signal)
```

Non-obvious design notes:
- **Sample Store is mandatory, not optional.** N raw JSONs per input are the feedstock for ablations, audits, and future fine-tuning corpora. Dropping them to save storage is the kind of short-term optimisation that kills the next quarter's initiative.
- **Three-bucket router** (not the naive "≥0.8 = ship / else = reject"). The middle band is where [LLM-as-Judge](llm-as-judge.md) earns its keep.
- **Telemetry is the drift canary.** When per-field confidence timeseries start sliding downward on new inputs, a new vocabulary / technology area / document style has arrived — see [Active Learning Loop](active-learning-loop.md).

## Key Properties

- **Per-field confidence is the actual product** — the vote-winning value is a by-product. Every downstream decision (auto-accept, escalate, reject) runs off the confidence, not the value.
- **Agreement ≠ calibrated probability.** 0.8 agreement doesn't mean 80% chance of being correct. Before customer-facing claims, produce a reliability diagram on a held-out eval set — see [Agent Evaluation](agent-evaluation.md).
- **Cost scales linearly in N but super-linearly in prompt length.** Long patent specs with N=5 can push $/document into territory where [Model Ensembling](model-ensembling.md) across model families becomes comparable in cost and higher in robustness.
- **Wins on ambiguous numerics, tables, long methods sections** — i.e. exactly the patent / scientific-paper surface Patsnap works on. Loses on format-error failure modes where [Constrained Decoding](constrained-decoding.md) is the correct fix.

## When to Use

Pick self-consistency when all of these hold:

- Extraction or classification tasks with a **structured schema** (fields you can vote on).
- **Cost budget tolerates N× inference** (or you batch-API the 5× into ~2.5×).
- You want **per-field confidence** as an engineered signal, not just a better answer.
- Failure mode is **ambiguity / reasoning noise**, not schema violations (for those, use [Constrained Decoding](constrained-decoding.md)) or hallucination from nothing (for those, use [Retrieval-Augmented Verification](retrieval-augmented-verification.md)).

Skip it when:

- **Latency-bound UI** (<300 ms response) — N=5 latency is unacceptable even with parallel dispatch.
- **Opus 4.7 locked** — no temperature means no diversity.
- You have **labelled data and high volume** — a trained [Verifier Model](verifier-model.md) is cheaper at scale.
- The dominant error is **format not fact** — fix with schema-constrained decoding first.

## Patsnap-Specific Applications

- **Claim-1 parameter extraction**: always N=5 — errors here propagate into product analytics that customers quote in investor decks.
- **Example-section table parsing**: N=3 with numeric tolerance-band voting; tables are the per-field confidence signal's strongest use case.
- **Offline gold-set construction**: N=10 × Sonnet 4.6 on 500–2000 representative samples, high-agreement entries become silver labels — see Strategy 3 in [Extraction Pipeline Composite Strategies](../derived/2026-04-23-extraction-pipeline-composite-strategies.md).

## Related Concepts

- [Cost-Aware Cascade Design](cost-aware-cascade-design.md) — how the confidence signal becomes a cost-minimising threshold.
- [LLM-as-Judge](llm-as-judge.md) — the middle-bucket router's second-pass rule.
- [Constrained Decoding](constrained-decoding.md) — complementary: format correctness vs. fact correctness.
- [Retrieval-Augmented Verification](retrieval-augmented-verification.md) — complementary: catches hallucinations that self-consistency cannot.
- [Verifier Model](verifier-model.md) — successor when labelled data accumulates and N× inference cost bites.
- [Active Learning Loop](active-learning-loop.md) — where low-confidence items go next.

## Backlinks

- [LLM-as-Judge](llm-as-judge.md)
- [Verifier Model](verifier-model.md)
- [Constrained Decoding](constrained-decoding.md)
- [Retrieval-Augmented Verification](retrieval-augmented-verification.md)
- [Self-Refine / Critic Loop](self-refine-critic-loop.md)
- [Model Ensembling](model-ensembling.md)
- [Logprob Uncertainty](logprob-uncertainty.md)
- [Active Learning Loop](active-learning-loop.md)
- [Cost-Aware Cascade Design](cost-aware-cascade-design.md)
- [Material Science Agents](material-science-agents.md)
- [Agent Evaluation](agent-evaluation.md)
- [derived: Extraction Pipeline Composite Strategies](../derived/2026-04-23-extraction-pipeline-composite-strategies.md)

## Sources

- [Self-Consistency Improves Chain of Thought Reasoning (Wang et al. 2022)](https://arxiv.org/abs/2203.11171) — original paper.
- Conversation: prompt_engineering_lab notebook walkthrough, 2026-04-23 — derived Patsnap-specific implementation notes.
- [Anthropic Messages API — batch + temperature](https://docs.anthropic.com/en/api/messages).
