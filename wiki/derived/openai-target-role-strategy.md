---
title: "OpenAI 目標職位分析與轉職策略"
type: session
source_url: "https://www.linkedin.com/jobs/view/4388873796/"
raw_path: raw/areomoon_career_llm/OpenAI_Target_Role_Strategy.md
created: 2026-04-09
tags: [career, openai, applied-ai, networking, portfolio, singapore]
---

# OpenAI 目標職位分析與轉職策略

> **TL;DR**: 分析 OpenAI AI Deployment Engineer (Startups, SG) 職位，設計從 Patsnap 出發的 6-12 個月轉職路線，涵蓋技術能力對齊、人脈經營（Grab 前同事 + Applied AI 圈）、Portfolio 建設（LinkedIn + 技術文章 + GitHub）。

## 目標職位本質

不是傳統 MLE，而是 **Solutions Engineer + Applied AI + DevRel 混合體**：
- 跟 startup 客戶一起 prototype agents / prompts / workflows
- 把客戶 usage pattern 翻譯成 evaluation / benchmark
- 回饋給 OpenAI 的 Product & Research team

## 核心能力差距與補齊計畫

| 能力 | 補齊方式（在 Patsnap） |
|------|----------------------|
| Agent workflow design | 把 RAG pipeline 設計成 multi-step，記錄 design decision |
| Evaluation system | 建 offline eval（precision@k、grounding rate）— **差異化武器** |
| Prompt engineering | 記錄 expert context prompt 方法論 |
| 溝通 / 客戶面 | 跟 scientist 互動 + internal demo + 技術 blog |

## 三層人脈策略

1. **Grab 前同事**（ByteDance/Apple/Meta）：0-3 月維持溫度聊技術 → 3-6 月分享成果播種 → 6-12 月收割 referral
2. **Applied AI 圈**（新建）：SG AI meetup + LinkedIn 主動觸及 target 公司 Applied AI 成員
3. **Portfolio 漏斗**：LinkedIn 關鍵字/文章被搜到 → insider 注意 → referral → 面試有實戰佐證 → Offer

## 技術文章計畫

| 篇 | 主題 | 時間 |
|---|---|---|
| 1 | 從 Search Ranking 到 RAG：設計差異 | 入職 2 個月 |
| 2 | 如何建立 RAG Evaluation Pipeline | 入職 4 個月 |
| 3 | 垂直領域做 Agent：data quality > model | 入職 6 個月 |

## 擴大目標公司

OpenAI、Anthropic（SG 擴編）、Google DeepMind、AI Startups (SG)

## 技術準備對齊

OpenAI JD 要求的能力與 [areomoon_agent_warmup](https://github.com/areomoon/areomoon_agent_warmup) 模組對應：

| JD 要求 | Warmup 模組 | 備註 |
|---------|------------|------|
| Prompt prototyping | `01_prompt_engineering/` | CoT、ReAct、Self-consistency |
| AI agents / workflows | `03_agent_patterns/` + `04_ace_framework/` | Generator-Reflector、LangGraph |
| Evaluation systems | 需在 Patsnap 實戰建立 | warmup repo 目前無對應模組，可考慮新增 `08_evaluation/` |
| Model training / RL | `06_finetuning/` | LoRA/QLoRA 基礎 |
| Domain knowledge | `05_material_science_agents/` | MARS、LLMatDesign 架構 |
| Multimodal (scientific docs) | `07_multimodal/` | 圖表理解、PDF parsing |

> **Gap**：warmup repo 缺少 evaluation/benchmark 模組和 portfolio/networking 策略。Knowledge base 的 [Career Execution Plan](../queries/2026-04-09-career-execution-plan.md) 補齊了後者。

## Concepts Referenced

- [Material Science Agents](../concepts/material-science-agents.md) — Patsnap 實戰場景
- [Context Engineering](../concepts/context-engineering.md) — prompt/context 方法論
- [Agentic Harness](../concepts/agentic-harness.md) — agent workflow 設計基礎

## Related

- [Gemini 諮詢：Patsnap 職涯決策全紀錄](gemini-career-decision-patsnap.md)
- [ChatGPT 諮詢：Patsnap 面試準備與職涯策略](chatgpt-patsnap-interview-strategy.md)
- [Career Development Roadmap](career-development-roadmap.md)
