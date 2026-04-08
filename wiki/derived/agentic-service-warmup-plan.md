---
title: "Agentic Service Development Warmup Plan"
source_type: article
source_url: ""
ingested: 2026-04-08
compiled: 2026-04-08
tags: [agent, scientific-paper-agent, rag, fine-tuning, lora, multi-modal, evaluation]
---

# Agentic Service Development Warmup Plan

> **TL;DR**: A 6-week structured ramp-up plan for an algorithm engineer (returning ML practitioner) onboarding to a material science AI agent service — covering LLM fundamentals, RAG, agent frameworks, multi-modal processing, QLoRA fine-tuning, and end-to-end scientific paper agent demo.

## Key Points

- **Target role**: algorithm engineer (model fine-tuning + algorithm design) for a scientific document intelligence service; core task is extracting structured experimental data from long-context, multi-modal sources
- **Week 1–2**: LLM basics refresh + RAG prototype — zero-shot/few-shot/CoT comparison on scientific text; LlamaIndex RAG over PDF with structured JSON output
- **Week 3**: Agent architecture — LangGraph ReAct agent reading papers → extracting parameters → comparing results; MCP for standardizing tool connections (PDF parser, Vector DB, compute engine)
- **Week 4**: Multi-modal + long context — handling tables, figures, spectra, formulas in scientific papers; Gemini 2.5 Pro (1M context) vs. chunked RAG vs. map-reduce tradeoffs
- **Week 5**: QLoRA fine-tuning + evaluation — SFT on (paper section → structured JSON) pairs using Qwen2.5-7B; benchmark: exact match rate + F1 + LLM-as-Judge; A/B: base vs. fine-tuned vs. prompt-engineered
- **Week 6**: End-to-end Scientific Paper Agent demo — multi-agent: Extractor / Analyzer / Advisor agents with shared memory/RAG; validation checklist: ingest PDF → extract conditions → cross-paper comparison → CoT explanation → eval report
- **Key insight**: Evaluation before training — without a ground-truth benchmark, fine-tuning has no measurable value; build the eval set first
- **Hardware constraint**: Mac (Apple Silicon) — all large model training via Colab/Kaggle or cloud GPU; MLX for local fine-tuning experiments

## Extracted Concepts

- [Material Science Agents](../concepts/material-science-agents.md)
- [ACE for Materials](../concepts/ace-for-materials.md)
- [Agentic Harness](../concepts/agentic-harness.md)
- [Tiered Memory](../concepts/tiered-memory.md)

## Raw Source

`raw/areomoon_career_llm/Agentic_Service_Warmup_Plan.md`
