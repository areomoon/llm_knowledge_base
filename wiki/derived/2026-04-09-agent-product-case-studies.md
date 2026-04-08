---
title: AI Agent 產品案例研究
type: article
raw_path: raw/articles/agent-product-case-studies.md
created: 2026-04-09
---

# AI Agent 產品案例研究：從 API Wrapper 到 Autonomous Agent

> **TL;DR**: 產業界 agent 產品的核心競爭力不在 LLM，而在 harness 工程和產品設計。按自主程度分 4 層：Copilot → Semi-Autonomous → Domain-Specific Autonomous → Platform/Superapp。

## Key Points

- **Tier 1 Copilot**（GitHub Copilot、Cursor、Perplexity）：人類主導，agent 輔助。成功關鍵是低摩擦 UX，不是模型能力
- **Tier 2 Semi-Autonomous**（Claude Code、Devin、Replit Agent）：agent 規劃執行，人類在關鍵節點審核。核心是 harness（context compression、permission gating、self-healing）
- **Tier 3 Domain-Specific**（Harvey AI、ChemCrow、MARS）：在特定領域做到高準確率。與 Patsnap 材料科學場景最直接相關
- **Tier 4 Platform**（OpenAI Superapp、Claude Superapp）：統一 AI 入口，agent 呼叫 N 個服務
- 跨案例共通 pattern：harness > loop、trust 漸進建立、domain-specific > general-purpose、evaluation 是護城河

## 5 個跨案例共通 Pattern

1. **Agent Loop 不是重點，Harness 才是** — 所有成功產品的核心 loop 都是 `reason → act → observe`，差異在 harness
2. **Human-in-the-loop 位置是產品決策** — 從每步確認（copilot）到只在失敗時升級（autonomous）
3. **Trust 漸進建立** — 沒有產品一開始就 fully autonomous
4. **Domain-specific > General-purpose** — 特定領域 90% 準確率比通用 70% 更有商業價值
5. **Evaluation 是最被低估的投資** — Harvey 的法律 benchmark、MARS 的 MADE benchmark 都是護城河

## Concepts Referenced

- [Agentic Harness](../concepts/agentic-harness.md)
- [Superapp Paradigm](../concepts/superapp-paradigm.md)
- [API to SuperAgent Transition](../concepts/api-to-superagent.md)
- [Agent-Friendly Design](../concepts/agent-friendly-design.md)
- [Material Science Agents](../concepts/material-science-agents.md)
- [Agent Product Design](../concepts/agent-product-design.md)
- [Agent Evaluation](../concepts/agent-evaluation.md)

## Notes

- Harvey AI 的法律 agent 與 Patsnap 專利搜索場景高度類比：domain-specific RAG、citation accuracy 是生死線、嵌入既有工作流
- ChemCrow / MARS 是材料科學 agent 的直接參考，特別是實驗數據抽取和 multi-modal 處理
- 所有案例都證明：production agent 的 90% 工程量在 harness，不在 LLM reasoning loop
