---
title: Verifier Model
tags: [verifier, evaluation, classifier, process-reward-model, openai, extraction, cost-efficiency]
sources:
  - Cobbe et al. 2021 — Training Verifiers to Solve Math Word Problems (https://arxiv.org/abs/2110.14168)
  - Lightman et al. 2023 — Let's Verify Step by Step (https://arxiv.org/abs/2305.20050)
  - conversation: prompt_engineering_lab walkthrough 2026-04-23
created: 2026-04-23
updated: 2026-04-23
---

# Verifier Model

> **TL;DR**: A small classifier trained to predict "is this LLM output correct?" — once you have labelled data, it replaces LLM-as-Judge at orders-of-magnitude lower inference cost. The dominant pattern inside OpenAI's reasoning-model training (process reward models).

## Definition

A **verifier model** is a supervised classifier (often a BERT-family encoder or a small decoder fine-tuned for binary classification) that takes `(input, LLM output)` and predicts a correctness score. Unlike [LLM-as-Judge](llm-as-judge.md), it requires labelled training data — but at inference it costs 1–2 orders of magnitude less than running a large judge.

Two common sub-types:

- **Outcome Reward Model (ORM)** — scores the final answer only (Cobbe et al. 2021, [arXiv:2110.14168](https://arxiv.org/abs/2110.14168)).
- **Process Reward Model (PRM)** — scores each reasoning step, enabling step-level correction (Lightman et al. 2023, [arXiv:2305.20050](https://arxiv.org/abs/2305.20050)).

## How It Works

### Training loop

1. Collect `(input, LLM output, is_correct)` triples. Source: human annotators, self-consistency majority vote, or ground-truth execution (e.g. running generated code).
2. Fine-tune a small encoder (e.g. DeBERTa-v3-base, ModernBERT) as a binary classifier.
3. Calibrate on a held-out set — verifier confidence vs. empirical correctness.

### Inference

```python
candidates = [llm.generate(input, seed=s) for s in range(K)]
scored = [(c, verifier.score(input, c)) for c in candidates]
best = max(scored, key=lambda x: x[1])
```

This is **Best-of-N sampling with a verifier**, the mechanism behind most reasoning leaderboard submissions since 2023.

### Comparison to alternatives

| | Verifier Model | LLM-as-Judge | Self-Consistency |
|---|---|---|---|
| Needs labelled data? | Yes | No | No |
| Inference cost | ~$0.0001/call (small encoder) | ~$0.01/call (strong LLM) | ~$0.005 × N |
| Bias profile | Distribution shift from train | Position, verbosity, self-preference | Systematic model error reinforced |
| Volume regime | High-volume production | Mid-volume eval | Low-volume high-stakes |

## Industry Applications

- **OpenAI o-series reasoning models** — PRMs used at training and inference time to select among thousands of sampled reasoning chains.
- **DeepMind AlphaCode 2** — verifier filters billions of candidate programs down to top submissions.
- **Anthropic Constitutional AI / RLAIF** — verifier-like preference models trained from AI feedback.
- **Patsnap-relevant**: once you have 10k+ human-corrected extractions accumulated, training a DeBERTa-base verifier on `(patent_text, extracted_field_value, is_correct)` gives a cheap online quality gate. Replaces expensive self-consistency for production traffic while retaining confidence signal.
- **LangSmith / Arize evaluator components** — productise a lighter-weight verifier layer for general LLM app evaluation.

## When to Use

**Pick Verifier Model over LLM-as-Judge / Self-Consistency when:**
- You have accumulated **≥5k labelled examples** (self-consistency gold set counts, see Strategy 3 in [Extraction Pipeline Composite Strategies](../derived/2026-04-23-extraction-pipeline-composite-strategies.md)).
- Inference volume is **>10k calls/day** — the training cost amortises quickly.
- You need **consistent, version-controlled** quality signals (verifier weights are a git artefact; LLM judges drift with API updates).

**Don't use Verifier Model when:**
- No labelled data yet — bootstrap with [Self-Consistency Implementation](self-consistency-implementation.md) first.
- Domain shifts rapidly (new patent technology areas monthly) — retraining cadence outpaces value.
- Low-volume traffic — the training ops overhead isn't amortised.

## Key Properties

- **Distribution shift is the #1 failure mode.** Verifier trained on 2024 patents will silently miscalibrate on 2026 patents. Mitigation: periodic retraining with an [Active Learning Loop](active-learning-loop.md) feeding fresh low-confidence samples.
- **Calibration ≠ accuracy.** A verifier with 90% accuracy on held-out may still be miscalibrated (confidence 0.9 ≠ 90% correct). Produce a reliability diagram before trusting verifier confidence as a router threshold.
- **Process > Outcome for complex extraction.** For multi-field patent extraction, step-level (field-level) scoring beats a single "is the whole JSON right?" signal.

## Related Concepts

- [Self-Consistency Implementation](self-consistency-implementation.md) — bootstrapper for the verifier's training set.
- [LLM-as-Judge](llm-as-judge.md) — the zero-labelled-data alternative.
- [Active Learning Loop](active-learning-loop.md) — closes the retraining loop on verifier drift.
- [Cost-Aware Cascade Design](cost-aware-cascade-design.md) — a verifier is the cheap signal in a cascade.
- [RLPR (Reference Probability Reward)](rlpr-reference-probability-reward.md) — verifier-free alternative for RL post-training.
- [Agent Evaluation](agent-evaluation.md) — where verifier fits in broader eval stack.

## Backlinks

*(none yet — populated by lint)*

## Sources

- [Training Verifiers to Solve Math Word Problems (Cobbe et al. 2021)](https://arxiv.org/abs/2110.14168) — GSM8K + outcome verifier.
- [Let's Verify Step by Step (Lightman et al. 2023)](https://arxiv.org/abs/2305.20050) — process reward models.
- Conversation: prompt_engineering_lab walkthrough 2026-04-23.
