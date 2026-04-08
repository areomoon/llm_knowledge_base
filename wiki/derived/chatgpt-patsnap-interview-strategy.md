---
title: "ChatGPT 諮詢：Patsnap 面試準備與職涯策略全紀錄"
type: session
source_url: ""
raw_path: raw/areomoon_career_llm/ChatGPT_Patsnap_Interview_Strategy.md
created: 2026-04-08
tags: [career, patsnap, interview, rag, agent, salary-negotiation, singapore]
---

# ChatGPT 諮詢：Patsnap 面試準備與職涯策略全紀錄

> **TL;DR**: 完整記錄 Patsnap Algorithm Expert 面試全流程（技術 → PM → HR 談薪），含 System Design 答題框架、薪資談判話術、入職 30 天策略、以及 6-12 個月從 200k 跳到 300k 的職涯路線圖。

## 面試核心答題框架

### RAG System Design（技術面必考）

```
Data Ingestion → Structure-aware Chunking → Hybrid Retrieval → Re-ranking
→ Evidence Aggregation → Context Normalization → Multi-step Agent Reasoning
→ Grounded Generation（附 citation，信心不足則 abstain）
```

關鍵技術點：
- **Hierarchical Indexing**：Parent（section）→ Child（數值/公式），檢索 Child 自動拉 Parent context
- **Evidence Aggregation**：多來源結構化整理為 material/property/condition/value 對照表
- **Context Normalization**：不同實驗條件標準化（溫度區間/濃度分段/方法差異標記）
- **Iterative Bridge Retrieval**：根據初步結果自動發起二次檢索
- **Extraction Pipeline 三層**：Parsing → Information Extraction（明確 schema）→ Validation（unit/range/cross-source）

### PM 面核心題

- **Option A vs B（精做 data vs 快速上線）**：選 B 起手 + A 長期規劃，用 user feedback 指導 data pipeline 優化
- **Metric 設計**：retrieval precision@k + evidence click-through + task completion time
- **Trust 問題**：Evidence + Transparency + Consistency，「讓系統看起來可驗證而非太聰明」

## 薪資談判實戰

| 階段 | 策略 |
|------|------|
| 報價前 | 先讓 HR 報價，不先給數字 |
| Expected salary | 給 range（230-250k），不給死數字 |
| 被壓價 | 「equity → cash 結構變化需要 uplift」|
| 底線被探 | 「I'd focus on what makes the move meaningful」|
| Final offer ~200k | 接受但視為「career accelerator」|

## 職涯戰略路線圖

| 階段 | 時間 | 目標 | 薪資 |
|------|------|------|------|
| 轉賽道 | 0-6 個月 | 拿 RAG/Agent/Product 實戰 | 200k |
| 變現 | 6-12 個月 | 帶作品集跳槽 | 250-300k |
| 穩定 | 12-24 個月 | 選 WLB + 高薪 | 300k+ |

### 入職 30 天策略
- Week 1：畫系統 bottleneck 圖 + 找高價值問題（不要當乖新人）
- Week 2-3：提方案 + 快速 prototype + 量化改善
- Week 4：分享成果 + 建立技術標籤
- 原則：「只做高槓桿工作」，每個 task 問「能不能寫在履歷第一條？」

### 30 天紅旗觀察清單
- team 只講 prompt/demo，不講 data/retrieval/evaluation
- 每個問題都用「換 model 試試」解決
- 沒有 offline eval / benchmark
- 你的 task 只有 API 串接 / prompt 調整

### 3 個月 Checkpoint
1. 有沒有做過一個 RAG pipeline？
2. 有沒有解過一個 hard problem？
3. 有沒有 measurable impact？
→ 都沒有 → 立刻開始找下一份

## 面試 Narrative 設計

**核心定位轉換**：
- ❌ Search/Ranking Engineer
- ✅ AI Agent / RAG System Builder

**關鍵敘事**：
- 「Search 是 retrieval，retrieval 是 RAG 的核心」
- 「不是放棄搜推，是把搜推能力升級到下一個階段」
- 永遠講「complex knowledge system」不講「材料科學」— domain abstraction

**同儕焦慮調整**：
- 差距本質是「賽道差距」不是「能力差距」
- 前同事在 cash cow 賽道（推薦/ads），自己在切換到下一代高價值賽道（LLM/Agent）
- 「大部分高薪的人不是一直領高薪，是在某個時間點對齊了賽道」

## 風險與控制

| 風險 | 控制策略 |
|------|---------|
| 只做 glue code | 入職 1 個月確認有 pipeline ownership |
| Burnout | 只做高槓桿工作 |
| 薪資被錨定 | 賣 impact 不賣 base |
| Domain 太 niche | 講「AI system」不講「材料科學」|

## Concepts Referenced

- [Material Science Agents](../concepts/material-science-agents.md)
- [Context Engineering](../concepts/context-engineering.md)

## Related

- [Gemini 諮詢：Patsnap 職涯決策全紀錄](gemini-career-decision-patsnap.md) — 決策過程與 Offer 細節
- [Career Development Roadmap](career-development-roadmap.md) — 長期職涯規劃

## Notes

- 兩份諮詢（Gemini + ChatGPT）結論一致：接 Patsnap 作為轉賽道跳板
- ChatGPT 更著重面試實戰（mock interview、話術、答題框架）
- Gemini 更著重宏觀決策分析（職涯路徑、風險矩陣）
- 核心共識：「這份工作不是終點，是通往 300k 的門票」
