---
title: Constrained Decoding
tags: [structured-output, json-schema, tool-use, decoding, extraction, format-correctness]
sources:
  - Outlines (https://github.com/dottxt-ai/outlines)
  - Willard & Louf 2023 — Efficient Guided Generation (https://arxiv.org/abs/2307.09702)
  - Anthropic Tool Use docs (https://docs.anthropic.com/en/docs/agents-and-tools/tool-use)
  - OpenAI Structured Outputs (https://platform.openai.com/docs/guides/structured-outputs)
  - conversation: prompt_engineering_lab walkthrough 2026-04-23
created: 2026-04-23
updated: 2026-04-23
---

# Constrained Decoding

> **TL;DR**: Force the model to emit tokens that conform to a schema (JSON Schema, regex, CFG) at decode time. Solves format correctness, not fact correctness — the output will parse, but it can still be wrong. Complementary to self-consistency, not a replacement.

## Definition

Constrained decoding restricts next-token sampling to only tokens that keep the partial output valid under some formal constraint. Common constraint types:

- **JSON Schema** — the output must parse as JSON matching a given schema.
- **Regex** — the output matches a regular expression.
- **Context-free grammar (CFG)** — output is a valid sentence in a BNF grammar.
- **Tool use** — the output is a valid function call with typed arguments.

The canonical open-source implementation is [Outlines](https://github.com/dottxt-ai/outlines) (Willard & Louf 2023, [arXiv:2307.09702](https://arxiv.org/abs/2307.09702)), which compiles the schema into a finite-state machine over the token vocabulary and masks invalid tokens at each step. Commercial APIs:

- **Anthropic Tool Use** — implicit constrained decoding when `tools=[...]` is set; the model must emit a valid function call.
- **OpenAI Structured Outputs** (`response_format={"type": "json_schema", ...}`) — GPT-4o+ with strict schema adherence.
- **Google Gemini** controlled generation via `responseSchema`.

## How It Works

```python
# Anthropic tool use — schema is the implicit constraint
response = client.messages.create(
    model="claude-haiku-4-5",
    tools=[{
        "name": "extract_patent_params",
        "description": "Extract patent parameters from text",
        "input_schema": {
            "type": "object",
            "properties": {
                "substrate_temp_C": {"type": "number"},
                "oxygen_pressure_mTorr": {"type": "number"},
                "material": {"type": "string"},
            },
            "required": ["material"]
        }
    }],
    messages=[{"role": "user", "content": text}],
)
# response.content[0].input is guaranteed to match schema
```

At the token level, the decoder maintains a state in the schema's FSM. When generating the next token, it computes the logit mask: tokens that would advance to a valid next state get their logits kept; others get `-inf`. Sampling then happens over the valid set.

## Key Properties

- **Format correctness is guaranteed; fact correctness is not.** The model will output `{"substrate_temp_C": 700}` — but whether 700 is the right number is a separate question, solved by [Self-Consistency Implementation](self-consistency-implementation.md), [Verifier Model](verifier-model.md), or [Retrieval-Augmented Verification](retrieval-augmented-verification.md).
- **Eliminates whole categories of bug.** No more "model returned 95% valid JSON but this one broke the downstream parser at 3am". Code that consumes the output can drop defensive try/except blocks.
- **Slight quality trade-off in some cases.** Heavily constrained decoding can under-perform unconstrained-then-parse when the schema conflicts with how the model naturally wants to express information. Measure per task.
- **Ignores required fields that don't exist in source.** If a schema says `substrate_temp_C` is required but the patent doesn't mention it, the model will hallucinate a value to satisfy the schema. Mitigation: make fields optional; allow `null`.

## Industry Applications

- **Anthropic Claude Agent SDK** — all tool calls use constrained decoding internally; the tool_use block is schema-valid by construction.
- **OpenAI GPT-4o Structured Outputs** — widely deployed for JSON-producing endpoints in enterprise apps.
- **Outlines + vLLM** — self-hosted LLMs commonly run Outlines as the decoding layer for production extraction services.
- **LangChain / LlamaIndex output parsers** — wrap constrained decoding where the underlying API supports it, fall back to retry-on-parse-failure where it doesn't.
- **Patsnap-relevant**: every extraction endpoint should use tool-use or structured outputs. Format-related bugs are pure overhead you can eliminate by configuration.

## When to Use

**Always use constrained decoding when:**
- Output feeds a downstream structured system (DB insert, API call, analytics).
- Format errors dominate your debugging time.
- You're building on Anthropic or OpenAI — tool use / structured outputs is free to turn on.

**Consider unconstrained + parse-on-output when:**
- Output is free-form prose with embedded structure (reports, summaries with citations).
- You want reasoning *before* the structured output — use CoT first, then a tool call at the end.
- Self-hosted model doesn't yet support efficient constrained decoding (non-trivial engineering).

## Patsnap-Specific Applications

- **All Claude-based extractors default to tool use, not prompt-parsed JSON.** Removes a class of parse errors from the backlog permanently.
- **Nested schemas for patent claim structure** — tool use supports nested objects natively.
- **Use `anyOf` / nullable fields** for parameters not always present — avoid hallucination-to-satisfy-schema.

## Related Concepts

- [Self-Consistency Implementation](self-consistency-implementation.md) — complementary: format vs fact.
- [Retrieval-Augmented Verification](retrieval-augmented-verification.md) — complementary: hallucination control.
- [Agent-Friendly Design](agent-friendly-design.md) — tool schemas are the agent-facing interface contract.
- [API to SuperAgent Transition](api-to-superagent.md) — tool use is the substrate enabling agent-callable services.

## Backlinks

*(none yet — populated by lint)*

## Sources

- [Efficient Guided Generation for Large Language Models (Willard & Louf 2023)](https://arxiv.org/abs/2307.09702) — Outlines paper.
- [Outlines repository](https://github.com/dottxt-ai/outlines).
- [Anthropic Tool Use documentation](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use).
- [OpenAI Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).
- Conversation: prompt_engineering_lab walkthrough 2026-04-23.
