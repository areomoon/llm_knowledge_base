---
title: Information Theory for LLM Context
tags: [information-theory, shannon, context-compression, llm, entropy, economics]
sources: [raw/repos/rtk-token-killer.md]
created: 2026-04-17
updated: 2026-04-17
---

# Information Theory for LLM Context

> **TL;DR**: Claude Shannon's 1948 framework tells you the lower bound on how many tokens a message *must* take. Most LLM-facing text (CLI output, logs, boilerplate code) lives far above that bound — which is why per-command compressors like [RTK](rtk-token-killer.md) routinely save 80–90% of tokens, and why "用數學賺錢" (making money with math) is a literal business case in the agent era.

## Definition

**Shannon entropy** H(X) = −Σ p(x) log₂ p(x) is the average information content per symbol of a source X. The source coding theorem (Shannon 1948) proves that no lossless encoding can represent X in fewer than H(X) bits per symbol on average. Lossy coding can go below H(X) but only by paying a distortion cost (rate–distortion theory).

Applied to LLM context:

- **X** = the content the agent actually needs from a tool result (success/failure, changed files, error messages, commit SHA, …).
- **Token stream** = the encoding the agent receives.
- **Gap** = token count of the current encoding ÷ token count of an optimal encoding. This gap is where compression savings live.

## Why LLM-Facing Text Is Wildly Redundant

CLI tools, code comments, log files, HTTP responses, and most human-readable artifacts were designed for a human audience whose channel (eyes) is bandwidth-limited differently from an LLM's. They spend tokens on:

- **Framing** (banners, progress bars, section dividers) that convey zero decision-relevant information once the command is complete.
- **Redundancy for scanability** (re-stating the module name on every failing test line) when the agent can hold the whole output in working memory.
- **Fixed-format metadata** (`Delta compression using up to 8 threads`) that has identical content every run.

From Shannon's view, each of these is a symbol whose probability p(x) ≈ 1 — so its information content −log₂ p(x) ≈ 0. A well-designed encoder drops them entirely.

## The Regex → Structural → Information-Theoretic Ladder

Three rungs of increasing compression, with RTK today on rung 1:

| Rung | Approach | Practical ceiling | Cost |
|---|---|---|---|
| 1. Regex filters | hand-tuned per command | ~80% | brittle to format drift |
| 2. Structural parsing (AST) | lex → parse → semantic re-emit | ~90% | one grammar per tool |
| 3. Entropy-coded encoding | dict-based + variable-length codes, LLM-aware markers | ~95% theoretical, ~92% practical | LLM must parse the scheme reliably |

The ~3 percentage-point gap between rung 3's theoretical 95% and its practical 92% is the **legibility tax**: tokens spent on markers/framing so Claude-class models deterministically parse the compressed stream. Remove those markers and the LLM starts hallucinating structure — a classic rate–distortion trade.

This ladder was the user's own framing after weeks of testing RTK and reading its regex-heavy source; it is the pedagogical core of their planned teaching piece **"用數學賺錢"** — math, specifically Shannon's, as the tool that moves the compression ceiling from 80% to 92%+.

## Why This Matters for Agent Economics

- **Direct cost.** Token-billed agents (Claude, GPT, Gemini) pay linearly per token in and out. 92% compression on tool output ≈ a 12× multiplier on the effective context budget for the same spend.
- **Context window as a scarce resource.** Even for fixed-tier subscriptions, tokens not spent on boilerplate are tokens available for code, reasoning, and memory.
- **Scaling argument.** As agent sessions grow longer (see [Agentic Harness](agentic-harness.md)), the integral of wasted tokens grows linearly; any per-call savings compound.

## Caveats

- **Entropy is content-dependent.** The 80–95% numbers hold for stylized CLI output, not arbitrary text. Source code, natural-language docs, and novel debug traces have higher entropy and lower headroom.
- **Lossy ≠ safe.** Dropping "unnecessary" tokens can silently strip the exact line the agent needed. Preserve raw output out-of-band (see RTK's tee recovery) so the agent can demand the unfiltered stream on failure.
- **LLM parser is the bottleneck, not the math.** The theoretical bound is set by the content's entropy; the practical bound is set by what the downstream model can decode without error.

## When to Use

- Designing any pipeline that funnels tool output, logs, or structured data into an LLM context.
- Estimating the ROI of a custom compression layer: measure current tokens vs. a minimal hand-authored summary of the same decision-relevant facts — the ratio is your headroom.
- Arguing for investment in a compiler-style output encoder over another regex patch.

## Backlinks

- [RTK Token Killer](rtk-token-killer.md)
- [CLI Output Compression](cli-output-compression.md)
- [Agentic Harness](agentic-harness.md)
- [Context Engineering](context-engineering.md)

## Sources

- Shannon, C.E. (1948). *A Mathematical Theory of Communication.* Bell System Technical Journal.
- [rtk-ai/rtk](https://github.com/rtk-ai/rtk) — practical case study
- [MadPlay — I Only Compressed CLI Output](https://madplay.github.io/en/post/rtk-reduce-ai-coding-agent-token-usage) — independent reproduction of 80% savings
