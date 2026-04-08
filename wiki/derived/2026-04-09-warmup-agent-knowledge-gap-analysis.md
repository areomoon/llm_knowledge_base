---
title: Warmup Repo × Knowledge Base 交叉分析：Agent 產品認知缺口
type: article
raw_path: raw/articles/warmup-agent-knowledge-gap-analysis.md
created: 2026-04-09
---

# Warmup × KB 缺口分析

> **TL;DR**: warmup repo 技術實作紮實，但缺少 5 個產品/產業維度：產品設計思維、production engineering、agent evaluation、產業生態認知、stakeholder 溝通框架。

## Key Points

- warmup 7 個模組覆蓋了技術棧（prompt → RAG → agent → ACE → materials → fine-tuning → multimodal），但全是 happy path demo
- **缺口 1 — 產品設計思維**：不知道 agent 的用戶是誰、human-in-the-loop 放哪裡、error recovery UX 怎麼做
- **缺口 2 — Production Patterns**：缺 error handling、context compression、permission gating、observability、cost management
- **缺口 3 — Agent Evaluation**（最關鍵）：只有模型微調的 eval，沒有 agent-level 的 task completion rate、efficiency、safety eval
- **缺口 4 — 產業生態**：知道框架名字但不知道誰在用、解決什麼業務問題、商業模式是什麼
- **缺口 5 — 溝通框架**：需要學會用產品語言而非技術語言講 agent

## 優先行動

| 優先級 | 項目 | 時間 |
|--------|------|------|
| P0 | 深讀 agent 產品案例 + 準備產品語言翻譯範例 | 6hr |
| P1 | 研究 agent evaluation（MADE + SWE-bench） | 4hr |
| P1 | 在 warmup 03 實作 production patterns | 6hr |
| P2 | Agent infra 生態調研 | 3hr |

## 心態轉變

```
ML 工程師 → AI Agent 系統工程師
訓練/部署模型 → 設計 LLM + Harness + Tools + Evaluation 的完整系統
```

## Concepts Referenced

- [Agentic Harness](../concepts/agentic-harness.md)
- [Material Science Agents](../concepts/material-science-agents.md)
- [ACE Framework](../concepts/ace-framework.md)
- [Agent Product Design](../concepts/agent-product-design.md)
- [Agent Evaluation](../concepts/agent-evaluation.md)
