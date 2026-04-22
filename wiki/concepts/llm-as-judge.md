---
title: LLM-as-Judge
tags: [evaluation, judge, pairwise, mt-bench, scoring, extraction, confidence]
sources:
  - Zheng et al. 2023 — MT-Bench / Chatbot Arena (https://arxiv.org/abs/2306.05685)
  - conversation: prompt_engineering_lab walkthrough 2026-04-23
created: 2026-04-23
updated: 2026-04-23
---

# LLM-as-Judge

> **TL;DR**: Use a (usually stronger) LLM to score, rank, or arbitrate other LLMs' outputs. Cheaper than self-consistency (1 call vs. N), but introduces judge bias — position bias, verbosity bias, self-preference — that must be controlled for before trusting the signal.

## Definition

LLM-as-Judge (Zheng et al. 2023, MT-Bench / Chatbot Arena, [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)) is the pattern of using one LLM to evaluate another's output. Three common shapes:

1. **Pointwise scoring** — judge outputs a 1–10 quality score.
2. **Pairwise preference** — judge picks between candidate A and B.
3. **Rubric-based ruling** — judge evaluates against explicit criteria (e.g. "is the extracted temperature supported by the source text?").

For extraction pipelines, the rubric form is most useful: judge verifies that each field's value is consistent with the source, flagging hallucinations or unit mistakes.

## How It Works

```python
# Pattern: extract with cheap model, judge with strong model
extraction = haiku.extract(patent_text)
judge_prompt = f"""
Source: {patent_text}
Extracted: {extraction}
For each field, rate: is the value supported by the source? (yes/no/partial)
Return JSON with per-field ruling and one-sentence justification.
"""
rulings = sonnet.judge(judge_prompt)
```

Compared to [Self-Consistency Implementation](self-consistency-implementation.md) the cost model flips:

| | Self-Consistency | LLM-as-Judge |
|---|---|---|
| Calls per input | N (typically 5) | 1 (judge) + 1 (extract) |
| Confidence origin | Sample agreement | Judge's explicit rating |
| Bias risk | Model's own systematic errors reinforced N times | Judge's biases (see below) |
| Best at | Ambiguous reasoning | Source-consistency checks, pairwise comparisons |

## Key Properties — The Three Biases

Documented by Zheng et al. 2023 and the [Chatbot Arena leaderboard](https://chat.lmsys.org/) team:

1. **Position bias** — judges prefer whichever candidate appears first (or second, depending on model). Mitigation: evaluate A-vs-B and B-vs-A, only declare a winner if both orderings agree.
2. **Verbosity bias** — longer answers rated higher even when content is equivalent. Mitigation: include explicit length-normalisation in the rubric or truncate candidates to equal length.
3. **Self-preference** — models prefer outputs from their own family (GPT-4 prefers GPT-4, Claude prefers Claude). Mitigation: use a different-family judge, or ensemble judges across families.

Additional risks:
- **Judge calibration drift** when the underlying judge model is updated (Sonnet 4.5 → 4.6). Treat judge model version as a pinned dependency; re-validate rubrics when it changes.
- **Judge fails silently on domain it doesn't know.** A general Sonnet may not know that 200 mTorr is reasonable for PLD — it will call correct values "unsupported". Domain-specific rubrics + few-shot demonstrations mitigate.

## Industry Applications

- **Anthropic / OpenAI evaluation pipelines** — most commercial LLM leaderboards use LLM-as-Judge because it's the only way to evaluate open-ended generation at scale.
- **RAG answer scoring** — [Ragas](https://docs.ragas.io/) and similar frameworks use LLM-as-Judge for faithfulness, answer relevance, context precision metrics.
- **RLAIF (Reinforcement Learning from AI Feedback)** — Anthropic's Constitutional AI uses LLM-as-Judge for preference labels at training time.
- **Automated PR review bots** — rubric-based LLM-as-Judge ratings scale code review beyond what human reviewers can cover.
- **Patsnap-style extraction QA**: use judge to verify that each extracted patent parameter has a supporting span in the source text.

## When to Use

**Pick LLM-as-Judge over self-consistency when:**
- You need **pairwise preference** (A vs B), not a majority vote among same-model samples.
- Cost of N× inference is prohibitive but you can afford 1× strong-model judge.
- The judgement task is **source-consistency / rubric-compliance**, where a strong model checking a weaker model's work is naturally easier than generation.

**Don't use LLM-as-Judge when:**
- You don't have a model materially stronger than the generator (self-preference + weak discrimination).
- The rubric requires **domain expertise** the judge lacks — use [Verifier Model](verifier-model.md) trained on labelled data instead.
- Regulatory / auditability requires a human decision trail.

## Related Concepts

- [Self-Consistency Implementation](self-consistency-implementation.md) — LLM-as-Judge often occupies the middle-confidence bucket in the self-consistency router.
- [Verifier Model](verifier-model.md) — the "trained classifier" alternative when you have labelled data.
- [Agent Evaluation](agent-evaluation.md) — broader evaluation frame.
- [RLPR (Reference Probability Reward)](rlpr-reference-probability-reward.md) — a verifier-free RL pattern that shares DNA with LLM-as-Judge.

## Backlinks

- [Self-Consistency Implementation](self-consistency-implementation.md)
- [Verifier Model](verifier-model.md)
- [Retrieval-Augmented Verification](retrieval-augmented-verification.md)
- [Self-Refine / Critic Loop](self-refine-critic-loop.md)
- [Model Ensembling](model-ensembling.md)
- [Cost-Aware Cascade Design](cost-aware-cascade-design.md)
- [Agent Evaluation](agent-evaluation.md)
- [RLPR (Reference Probability Reward)](rlpr-reference-probability-reward.md)
- [derived: Extraction Pipeline Composite Strategies](../derived/2026-04-23-extraction-pipeline-composite-strategies.md)

## Sources

- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al. 2023)](https://arxiv.org/abs/2306.05685) — founding paper on the evaluation pattern and its biases.
- [Ragas: Evaluation framework for RAG pipelines](https://docs.ragas.io/) — LLM-as-Judge applied to retrieval-augmented generation.
- Conversation: prompt_engineering_lab walkthrough 2026-04-23.
