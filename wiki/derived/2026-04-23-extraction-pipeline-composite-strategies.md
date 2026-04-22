---
title: Extraction Pipeline Composite Strategies — Notebook Walkthrough
type: session
source: conversation with Claude Code, prompt_engineering_lab notebook comparison
created: 2026-04-23
---

# Extraction Pipeline Composite Strategies — Notebook Walkthrough

> **TL;DR**: Zero-shot / Few-shot / CoT / Self-Consistency / ReAct are not mutually exclusive. Production pipelines stack them into composite strategies where each method owns a specific failure mode (format, reasoning, confidence, computation). The conversation compiled three canonical stacks and enumerated eight industry alternatives to pure self-consistency.

## Key Points

### Comparison of the five base methods (from notebook)

| Method | Output form | Determinism | Cost / call | Intermediate artefact |
|---|---|---|---|---|
| Zero-shot | JSON | High (T=0) | 1× | None |
| Zero-shot CoT | Reasoning + JSON | High | 1× | Text reasoning |
| Few-shot CoT | Reasoning + JSON | High | 1× (longest prompt) | Domain-shaped reasoning |
| Self-Consistency | N JSONs → vote + per-field confidence | Low (T>0, aggregate) | N× | Agreement distribution |
| ReAct | Thought/Action/Observation + Final Answer | Medium | Multi-round | Tool-call trace |

Key deltas worth remembering:
- **Zero-shot CoT is the highest-CP upgrade** — one sentence, massive gain on numeric/unit tasks (Kojima et al. 2022).
- **Few-shot CoT's cost is prompt-length, not call-count** — but wrong-domain examples *harm* extraction (notebook exercise 4).
- **Only Self-Consistency yields per-field confidence** — which is what production routers actually need, not a "better answer".
- **ReAct in prompt-parsed form is fragile** — today's `StopIteration` at `react_pattern.py:151` is a concrete example. Production systems use native tool use (Anthropic tool API / OpenAI function calling), not regex-on-free-text.

### Three composite strategies (with Patsnap scenarios)

**Strategy 1 — Zero-shot CoT default + selective Self-Consistency fallback.** Applied to patent-spec parameter extraction: 90% of fields parse cleanly on one call; only low-confidence / high-risk fields (Claim 1 core parameters, unit-missing values, out-of-range numerics) fan out to N=5. Net cost ~1.3–1.5× vs 5× for full self-consistency.

**Strategy 2 — Few-shot CoT *reads*; tool use *computes*.** Applied to cross-patent energy-density comparison (Wh/kg vs mAh/g × V): LLM only extracts raw value + raw unit from text; a deterministic Python layer does unit conversion and aggregation. This separation of concerns makes errors attributable (read-error vs compute-error) and the computation layer unit-testable.

**Strategy 3 — Offline Self-Consistency builds the gold set; online uses a cheap method + periodic eval.** Applied when launching a new extractor with no labelled data: Phase 1 offline runs N=10 × strongest model on 500–2000 samples; high-agreement items become silver labels, low-agreement items go to minimal expert review. Phase 2 serves with Haiku + zero-shot CoT, evaluating weekly against the gold set. This is "weak supervision" / "LLM-as-annotator" (Snorkel, Argilla).

### Self-consistency implementation details (core takeaways)

- **Aggregate field-by-field, not whole-JSON.** Whole-JSON diff treats any single-field disagreement as total mismatch.
- **Normalisation is the real work.** `"700°C"` / `"700 C"` / `700` / `"seven hundred celsius"` must canonicalise before voting. Pydantic validators or regex pipelines.
- **Tolerance-band voting for numerics** (e.g. ±1% = same vote). Otherwise float noise dissolves all agreement.
- **Temperature** 0.5–0.9 band; 0.7 as starting point; ablate per task.
- **N** — N=3 captures most gains, N=5 is the sweet spot; N=10 diminishing returns. Batch API compresses 5× cost to ~2.5×.
- **Anthropic caveat** — Opus 4.7 removes `temperature`/`top_p`/`top_k`; use Haiku 4.5 or Sonnet 4.6 for self-consistency.

### System diagram (concept adopted)

```
Input → Dispatcher (fan-out N async) → Sample Store → Normalizer
       → Field-level Aggregator → Router
                                    ├─ conf ≥ 0.8 → auto-accept
                                    ├─ 0.5–0.8  → LLM-as-judge
                                    └─ < 0.5    → human queue
       → Output + Telemetry (per-field confidence timeseries → drift signal)
```

Sample Store is non-optional — raw outputs feed ablation, audit, and future fine-tuning corpora.

### Eight industry alternatives to pure self-consistency

| Method | One-liner | When to pick over self-consistency |
|---|---|---|
| LLM-as-judge | Stronger model scores or picks among candidates | Pairwise preference, style judgement |
| Verifier model | Small classifier trained to accept/reject extractions | High volume, have labelled data |
| Constrained decoding / JSON schema | Force schema-valid output at decode time | Format errors dominate |
| Retrieval-augmented verification | Verify each extracted value appears in source text | Hallucination control, patent auditability |
| Self-refine / critic loop | Same model critiques then revises itself | Multi-step reasoning, not extraction |
| Model ensembling | Vote across Haiku + Sonnet + GPT + Gemini | High-value, low-volume (cost spike acceptable) |
| Logprob-based uncertainty | Read token logprobs as confidence | OpenAI/open-source only; Anthropic hides these |
| Active learning loop | Low-confidence → human label → retrain / few-shot refresh | Long-horizon ops, continuous improvement |

### Patsnap-specific three-month recommendation

1. **Tool use + JSON schema** for format stability and computation/extraction separation.
2. **Retrieval-augmented verification** — extracted values must map back to source spans; patent work demands traceability.
3. **Self-consistency** reserved for critical fields + offline evaluation; online use scales cost linearly with N.
4. **Defer fine-tuning** until it's clear which errors prompt engineering cannot fix. Self-consistency + retrieval verification alone typically reach shippable quality on top of zero-shot CoT.

### One-line takeaway

**Self-consistency's value is not "vote for the answer" — it's "produce per-field confidence so you can route".** The routing capability, not the accuracy bump, is what makes it production-relevant.

## Concepts Referenced

- [Self-Consistency Implementation](../concepts/self-consistency-implementation.md)
- [Cost-Aware Cascade Design](../concepts/cost-aware-cascade-design.md)
- [LLM-as-Judge](../concepts/llm-as-judge.md)
- [Verifier Model](../concepts/verifier-model.md)
- [Constrained Decoding](../concepts/constrained-decoding.md)
- [Retrieval-Augmented Verification](../concepts/retrieval-augmented-verification.md)
- [Self-Refine / Critic Loop](../concepts/self-refine-critic-loop.md)
- [Model Ensembling](../concepts/model-ensembling.md)
- [Logprob Uncertainty](../concepts/logprob-uncertainty.md)
- [Active Learning Loop](../concepts/active-learning-loop.md)
- [Material Science Agents](../concepts/material-science-agents.md)

## Notes

- Fixes a `StopIteration` in `01_prompt_engineering/react_pattern.py:151` by providing a default to `next(...)` when stop-sequence fires immediately. Retained here because the failure mode ("prompt-parsed ReAct is fragile") motivates preferring native tool use in production.
- User is joining Patsnap as algorithm engineer; all three composite strategies map to real Patsnap workloads (patent parameter extraction, cross-patent trend analysis, new-extractor bootstrap).
