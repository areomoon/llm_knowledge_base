---
title: Logprob Uncertainty
tags: [uncertainty, logprobs, calibration, confidence, extraction, openai]
sources:
  - Jiang et al. 2021 — How Can We Know When Language Models Know (https://arxiv.org/abs/2012.00955)
  - Kadavath et al. 2022 — Language Models (Mostly) Know What They Know (https://arxiv.org/abs/2207.05221)
  - conversation: prompt_engineering_lab walkthrough 2026-04-23
created: 2026-04-23
updated: 2026-04-23
---

# Logprob Uncertainty

> **TL;DR**: Read per-token log-probabilities as a cheap confidence signal — a single forward pass produces both the output and an uncertainty estimate. Excellent when available, but Anthropic's Claude API does not expose logprobs, so this path is closed for Claude-based extractors. OpenAI and open-source models do expose them.

## Definition

During autoregressive decoding, every generated token has a log-probability conditional on the prefix. Aggregating these into a sequence- or span-level confidence score gives you **uncertainty for free** — no N-sampling, no judge model, no verifier training.

Foundational work: Jiang et al. 2021 ([arXiv:2012.00955](https://arxiv.org/abs/2012.00955)) on calibration; Kadavath et al. 2022 ([arXiv:2207.05221](https://arxiv.org/abs/2207.05221)) showed LLMs are reasonably well-calibrated on factual QA when probed via logprobs or self-evaluation.

Available today:
- **OpenAI Chat Completions**: `logprobs=True, top_logprobs=5`.
- **Self-hosted (vLLM, TGI, Ollama, etc.)**: full distribution available.
- **Anthropic Claude**: ❌ not exposed. This is a product decision — confirmed as of late 2025 docs.
- **Google Gemini**: limited (`avgLogprobs` in some API paths).

## How It Works

```python
# OpenAI — simplest form: per-token logprobs
resp = openai.chat.completions.create(
    model="gpt-5",
    messages=[...],
    logprobs=True,
    top_logprobs=5,
)
tokens = resp.choices[0].logprobs.content
# Aggregate: min, mean, sum-of-log, or per-span
confidence_score = sum(t.logprob for t in tokens) / len(tokens)

# More useful: per-field confidence on structured output
field_spans = locate_field_spans(extracted_json, tokens)
per_field_conf = {
    field: exp(mean(t.logprob for t in span))
    for field, span in field_spans.items()
}
```

Compared to self-consistency's cost:

| | Logprob Uncertainty | Self-Consistency N=5 |
|---|---|---|
| Calls | 1 | 5 |
| Confidence signal | Token probabilities | Sample agreement |
| Granularity | Per-token, per-field | Per-field (after aggregation) |
| Works on Claude? | ❌ No | ✅ Yes |
| Calibration quality | Model-dependent, often miscalibrated at extremes | Non-probabilistic, vote-share |

## Key Properties

- **"Free" in cost terms — a single forward pass gives both output and uncertainty.** Orders of magnitude cheaper than any sampling-based approach.
- **Miscalibration is the main failure mode.** Models are often overconfident on wrong answers, especially after RLHF. Logprobs need to be calibrated against a held-out eval set (temperature scaling, isotonic regression) before use as a routing threshold.
- **Does not catch prior-driven hallucinations.** If the model confidently invented a value from its prior, logprobs for that value will be high. Pair with [Retrieval-Augmented Verification](retrieval-augmented-verification.md).
- **Per-field aggregation is the practical art.** Raw logprob of every token is noisy; aggregating over schema-field spans (using JSON parsing + token alignment) is the usable signal.

## Industry Applications

- **OpenAI's own evaluation pipelines** — logprobs widely used internally for calibration studies.
- **Self-hosted extraction stacks** — vLLM + custom aggregation is the most cost-efficient confidence pipeline for open-source models.
- **Hugging Face evaluate / lm-eval-harness** — logprob-based metrics for benchmarks like ARC, MMLU.
- **Observability tools** (Arize, Langfuse) that connect to OpenAI-compatible APIs display per-token logprobs as a debug aid.
- **Patsnap-relevant (blocked)**: if the company is Claude-only, this approach is unavailable. If Patsnap adopts OpenAI / self-hosted for any extractor, enable logprobs from day one — it's the cheapest confidence signal in existence.

## When to Use

**Pick logprob uncertainty when:**
- API exposes logprobs (OpenAI, self-hosted, partial Gemini).
- Volume is high — every 1× call beats 5× self-consistency at scale.
- Calibration investment is affordable (one-time evaluation per model version).

**Don't use / cannot use when:**
- Claude-only stack — switch to [Self-Consistency Implementation](self-consistency-implementation.md) for model-derived confidence.
- Failure mode is prior-driven hallucination — logprobs will be confidently wrong; use [Retrieval-Augmented Verification](retrieval-augmented-verification.md).
- No eval set for calibration — uncalibrated logprobs are misleading as a router threshold.

## Patsnap-Specific Note

If the production stack is pinned to Claude, this entire avenue is unavailable. Self-consistency + retrieval verification + LLM-as-Judge must fill the confidence-signal role. If OpenAI or a self-hosted model is in scope, revisit — logprobs unlock 10× cost reductions vs self-consistency at equivalent quality once calibrated.

## Related Concepts

- [Self-Consistency Implementation](self-consistency-implementation.md) — the workaround when logprobs aren't exposed.
- [Retrieval-Augmented Verification](retrieval-augmented-verification.md) — complementary; catches what logprobs miss.
- [Verifier Model](verifier-model.md) — trained alternative when more accurate confidence is needed.
- [Cost-Aware Cascade Design](cost-aware-cascade-design.md) — logprob is often the "cheap signal" tier.
- [RLPR (Reference Probability Reward)](rlpr-reference-probability-reward.md) — logprob-based reward signal for RL post-training.

## Backlinks

- [Self-Consistency Implementation](self-consistency-implementation.md)
- [Verifier Model](verifier-model.md)
- [Retrieval-Augmented Verification](retrieval-augmented-verification.md)
- [Active Learning Loop](active-learning-loop.md)
- [RLPR (Reference Probability Reward)](rlpr-reference-probability-reward.md)
- [Cost-Aware Cascade Design](cost-aware-cascade-design.md)
- [derived: Extraction Pipeline Composite Strategies](../derived/2026-04-23-extraction-pipeline-composite-strategies.md)

## Sources

- [How Can We Know When Language Models Know? (Jiang et al. 2021)](https://arxiv.org/abs/2012.00955) — calibration foundations.
- [Language Models (Mostly) Know What They Know (Kadavath et al. 2022)](https://arxiv.org/abs/2207.05221) — logprob-based self-evaluation.
- [OpenAI logprobs API parameter](https://platform.openai.com/docs/api-reference/chat/create#chat-create-logprobs).
- Conversation: prompt_engineering_lab walkthrough 2026-04-23.
