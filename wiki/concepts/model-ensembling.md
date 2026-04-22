---
title: Model Ensembling
tags: [ensembling, robustness, cross-model, high-stakes, extraction, voting]
sources:
  - Jiang et al. 2023 — LLM-Blender (https://arxiv.org/abs/2306.02561)
  - conversation: prompt_engineering_lab walkthrough 2026-04-23
created: 2026-04-23
updated: 2026-04-23
---

# Model Ensembling

> **TL;DR**: Vote across different model families (Claude + GPT + Gemini) rather than N samples from one model. Escapes the systematic-bias trap self-consistency hits when all N samples inherit the same prior. Cost and engineering complexity are both much higher — reserve for high-value low-volume tasks.

## Definition

Model ensembling runs the same input through multiple *different* models (different families, different providers, different training data) and aggregates the outputs. Distinct from [Self-Consistency Implementation](self-consistency-implementation.md), which samples N times from one model.

LLM-Blender (Jiang et al. 2023, [arXiv:2306.02561](https://arxiv.org/abs/2306.02561)) formalised the approach with pairwise ranker + generative fuser components, but most industry use is simpler: run 3 models, take majority vote (or LLM-as-Judge arbitration).

## How It Works

```python
results = await asyncio.gather(
    anthropic.extract(text),    # Claude Sonnet 4.6
    openai.extract(text),       # GPT-5
    google.extract(text),       # Gemini 2.5 Pro
)
# Field-level aggregation — same mechanics as self-consistency,
# but votes come from different model families
aggregated = field_level_vote(results)
```

Compared to self-consistency's cost profile:

| | Self-Consistency N=5 | 3-model Ensemble |
|---|---|---|
| Call count | 5 | 3 |
| $ per input | 5× single-model | ~3× (higher avg, diff pricing) |
| Diversity source | Temperature noise | Training distribution differences |
| Captures shared-prior errors? | No (all 5 share the prior) | Yes (different priors) |
| Engineering complexity | Low (one SDK) | High (3 SDKs, auth, retries, schemas) |

## Key Properties

- **Escapes shared-prior hallucination.** If Claude, GPT, and Gemini all *independently* arrive at "200 mTorr", that's genuinely strong evidence — in a way that 5 Claude samples saying "200 mTorr" is not.
- **Engineering complexity is the dominant cost, not API spend.** Schema differences, rate limits, billing reconciliation, failure-mode drift across providers — each is a team-month of infrastructure work.
- **Calibration across models is non-trivial.** GPT's "confident" and Claude's "confident" don't map directly. Vote-share interpretation is fine; per-model confidence comparison is not.
- **Vendor risk hedge.** If one provider has an outage or major regression, others absorb the load. For regulated industries this is sometimes a procurement requirement, not an optimisation.
- **Legal exposure.** Patent and legal data may have per-provider terms-of-service constraints; verify before routing customer data through three vendors.

## Industry Applications

- **NotDiamond / Martian LLM routers** — productise cross-provider routing and fallback as SaaS.
- **Financial analysis stacks** (e.g. Bloomberg GPT co-pilots) — often ensemble a finance-tuned model with a general frontier model for robustness.
- **High-stakes legal analysis** — some firms run GPT-4 + Claude-3-Opus + a domain-tuned model on key contract clauses as a procurement requirement.
- **Anthropic Constitutional AI training** — though not production ensemble, uses a multi-model preference corpus to train the final model.
- **Patsnap-relevant**: reserve for highest-value extractions (Claim 1 core parameters for flagship customers) or for red-teaming new extractor deployments — not for bulk patent processing where the cost/complexity can't amortise.

## When to Use

**Pick model ensembling when:**
- Errors have **asymmetric high downstream cost** (customer refund > $1k, legal liability, safety-critical).
- You can tolerate **3× engineering complexity** (multi-provider infrastructure).
- The task hits **shared-prior hallucinations** that self-consistency reinforces rather than catches.
- Regulatory or procurement **requires cross-vendor redundancy**.

**Don't use model ensembling when:**
- Volume is high and per-unit value is low — the engineering doesn't amortise.
- You haven't first tried [Self-Consistency Implementation](self-consistency-implementation.md) + [Retrieval-Augmented Verification](retrieval-augmented-verification.md). That combination solves most cases at lower complexity.
- Team has no infrastructure for multi-provider secret management, retry, observability.

## Related Concepts

- [Self-Consistency Implementation](self-consistency-implementation.md) — single-model version; first line of defence.
- [LLM-as-Judge](llm-as-judge.md) — often used as the arbitration step when the 3 models disagree.
- [Retrieval-Augmented Verification](retrieval-augmented-verification.md) — often catches what model ensembling can't (when all 3 models share training-data biases).
- [Cost-Aware Cascade Design](cost-aware-cascade-design.md) — ensemble is the expensive top tier; cheap tiers route most traffic.
- [Local vs Cloud Coding Agents](local-vs-cloud-coding-agents.md) — provider locality affects ensemble feasibility.

## Backlinks

- [Self-Consistency Implementation](self-consistency-implementation.md)
- [LLM-as-Judge](llm-as-judge.md)
- [Retrieval-Augmented Verification](retrieval-augmented-verification.md)
- [Active Learning Loop](active-learning-loop.md)
- [Cost-Aware Cascade Design](cost-aware-cascade-design.md)
- [Local vs Cloud Coding Agents](local-vs-cloud-coding-agents.md)
- [derived: Extraction Pipeline Composite Strategies](../derived/2026-04-23-extraction-pipeline-composite-strategies.md)

## Sources

- [LLM-Blender: Ensembling Large Language Models with Pairwise Ranking and Generative Fusion (Jiang et al. 2023)](https://arxiv.org/abs/2306.02561).
- [NotDiamond model router](https://www.notdiamond.ai/).
- Conversation: prompt_engineering_lab walkthrough 2026-04-23.
