---
title: "ACE: Agentic Context Engineering — Evolving Contexts for Self-Improving Language Models"
source_type: article
source_url: https://arxiv.org/abs/2510.04618
ingested: 2026-04-08
compiled: 2026-04-08
tags: [agent, context-engineering, stanford, self-improving, playbook]
---

# ACE: Agentic Context Engineering — Evolving Contexts for Self-Improving Language Models

> **TL;DR**: ACE lets LLM agents improve task performance across episodes by evolving a "playbook" of strategies in-context — no fine-tuning required — achieving SOTA on the AppWorld benchmark (+10.6 pp).

## Key Points

- Proposed by Stanford, SambaNova Systems, and UC Berkeley researchers (arXiv 2510.04618, Oct 2025)
- Identifies two failure modes of naive context management: **Brevity Bias** (compression discards insight) and **Context Collapse** (rewrites erode detail)
- Uses a **three-role architecture**: Generator produces reasoning traces → Reflector extracts lessons → Curator merges lessons into the playbook via delta updates
- **Grow-and-Refine algorithm**: new bullets are appended or merged; periodic de-duplication removes redundancy; no full rewrites
- **AppWorld benchmark**: 59.5% accuracy, +10.6 pp over prior SOTA, matching IBM GPT-4.1 agent
- **Financial reasoning** (FNER, Formula): +8.6% average improvement; strongest gains with ground-truth feedback
- Requires no model-specific infrastructure — the playbook is a markdown document in the system prompt

## Extracted Concepts

- [ACE Framework](../concepts/ace-framework.md)
- [Context Engineering](../concepts/context-engineering.md)
- [Evolving Playbooks](../concepts/evolving-playbooks.md)
- [Agentic Self-Improvement](../concepts/agentic-self-improvement.md)

## Raw Source

`raw/articles/ace-agentic-context-engineering.md`
