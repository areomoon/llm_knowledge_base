---
title: Self-Refine / Critic Loop
tags: [self-refine, critic, iterative-improvement, reasoning, reflexion]
sources:
  - Madaan et al. 2023 — Self-Refine (https://arxiv.org/abs/2303.17651)
  - Shinn et al. 2023 — Reflexion (https://arxiv.org/abs/2303.11366)
  - conversation: prompt_engineering_lab walkthrough 2026-04-23
created: 2026-04-23
updated: 2026-04-23
---

# Self-Refine / Critic Loop

> **TL;DR**: Same model generates, critiques its own output, then revises. Gains come from using the critique prompt to surface errors the initial generation missed. Best for reasoning and generation tasks; marginal for atomic extraction — self-consistency is usually the better tool there.

## Definition

Self-Refine (Madaan et al. 2023, [arXiv:2303.17651](https://arxiv.org/abs/2303.17651)) is a three-step loop with the same model:

1. **Generate** — initial output.
2. **Critique** — feedback on the initial output under explicit rubric.
3. **Refine** — revised output incorporating the critique.

Extended by Reflexion (Shinn et al. 2023, [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)) with verbal reinforcement learning — the critique is stored as persistent memory across trials.

Contrast with [LLM-as-Judge](llm-as-judge.md): judge is a separate (often stronger) model scoring another model's output. Critic loop reuses the same model on itself. Cheaper, but bounded by the model's own blind spots.

## How It Works

```python
output = model.generate(task)
for _ in range(max_iterations):
    critique = model.critique(task, output, rubric)
    if critique.says_acceptable():
        break
    output = model.refine(task, output, critique)
```

Where critic loops win, per Madaan et al.'s experiments:
- Code generation (errors visible on re-read).
- Multi-constraint generation (was every constraint satisfied?).
- Math and multi-step reasoning (did each step follow?).

Where they underperform:
- Atomic extraction — the model's initial prior already determined the answer; critic can't escape it.
- Tasks where the correctness check requires external information the model lacks.

## Key Properties

- **Gains cap at the model's ceiling.** A model that can't solve a problem can't critique its way to a solution. Reflexion experiments show diminishing returns after 2–3 iterations.
- **Cost = (1 + 2k) calls for k refinement rounds.** Similar order to [Self-Consistency Implementation](self-consistency-implementation.md) with N = 2k+1 — but without the confidence signal that self-consistency produces as a by-product.
- **Critique prompt design dominates performance.** Generic "find issues" underperforms task-specific rubric ("check unit conversions", "verify cited spans exist").
- **Works with [Retrieval-Augmented Verification](retrieval-augmented-verification.md) as the critique step.** Use retrieval to ground the critique in source text rather than the model's prior.

## Industry Applications

- **Cursor / Copilot inline code generation** — internal critic loops catch syntax and type errors before surfacing suggestions.
- **Bard / ChatGPT long-form writing** — critic loops polish drafts under user-visible revision requests.
- **Agent harnesses with replanning** — most LangGraph / CrewAI agent setups include a reflection / replanning step after tool execution fails, which is a critic loop variant.
- **Anthropic Claude Code `/review`** — a built-in critic loop over pending diffs, rubric-driven.
- **Patsnap-relevant (marginal)**: for atomic patent parameter extraction, critic loops rarely help — use [Self-Consistency Implementation](self-consistency-implementation.md) or [Retrieval-Augmented Verification](retrieval-augmented-verification.md) instead. Where critic loops *do* help in Patsnap: summary generation, multi-patent trend reports, Claim-interpretation reasoning.

## When to Use

**Pick self-refine / critic loop when:**
- Task is **reasoning or generation**, not atomic extraction.
- Errors are **detectable by re-reading** (syntax, unit mismatches, missing constraints).
- Cost budget covers 3–5× inference without the per-field confidence self-consistency provides.

**Don't use when:**
- Task is atomic extraction — initial prior dominates; no room to refine.
- The critique requires knowledge the model doesn't have — use [Verifier Model](verifier-model.md) or [Retrieval-Augmented Verification](retrieval-augmented-verification.md).
- Latency-bound UI.

## Related Concepts

- [Self-Consistency Implementation](self-consistency-implementation.md) — parallel sampling alternative, better for extraction.
- [LLM-as-Judge](llm-as-judge.md) — cross-model critic, escapes self-blind-spot.
- [Retrieval-Augmented Verification](retrieval-augmented-verification.md) — can serve as the "critique" step when grounded in source.
- [Agentic Self-Improvement](agentic-self-improvement.md) — critic loops are a primitive in self-improving agent architectures.
- [ACE Framework](ace-framework.md) — Reflector role is a critic loop specialised for playbook curation.

## Backlinks

- [Self-Consistency Implementation](self-consistency-implementation.md)
- [LLM-as-Judge](llm-as-judge.md)
- [Verifier Model](verifier-model.md)
- [Retrieval-Augmented Verification](retrieval-augmented-verification.md)
- [ACE Framework](ace-framework.md)
- [Agentic Self-Improvement](agentic-self-improvement.md)
- [derived: Extraction Pipeline Composite Strategies](../derived/2026-04-23-extraction-pipeline-composite-strategies.md)

## Sources

- [Self-Refine: Iterative Refinement with Self-Feedback (Madaan et al. 2023)](https://arxiv.org/abs/2303.17651) — originating paper.
- [Reflexion: Language Agents with Verbal Reinforcement Learning (Shinn et al. 2023)](https://arxiv.org/abs/2303.11366) — memory-persistent variant.
- Conversation: prompt_engineering_lab walkthrough 2026-04-23.
