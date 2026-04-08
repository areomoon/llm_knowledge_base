---
title: "Gemini 諮詢：Patsnap 職涯決策全紀錄"
type: session
source_url: "https://gemini.google.com/share/4532248d6002"
raw_path: raw/areomoon_career_llm/Gemini_Career_Decision_Patsnap.md
created: 2026-04-08
tags: [career, patsnap, ai-engineering, rag, sft, salary-negotiation, singapore]
---

# Gemini 諮詢：Patsnap 職涯決策全紀錄

> **TL;DR**: 經多輪諮詢分析後，決定口頭接受 Patsnap 新加坡 Algorithm Expert（202k SGD），放棄 Coupang 台北穩定現狀與大廠搜推高薪路線，選擇以 RAG/SFT/RL 實戰經驗作為 18-24 個月的技術轉型跳板。

## 決策背景

| 選項 | 年薪 (SGD) | 技術方向 | 風險 |
|------|-----------|---------|------|
| Coupang 台北（現職） | ~130k | Pipeline 維護 + 修 bug | 技術停滯、履歷過時 |
| Patsnap 新加坡 | 202k | RAG/Embedding/SFT/RL（材料科學） | 被 Lowball、Niche 陷阱 |
| 大廠搜推（Binance/TikTok） | 300-350k | 電商/短影音推薦 | 面試不確定、技術紅利遞減 |

## 關鍵決策因素

1. **32 歲是技術轉型最後窗口** — 無小孩、有 PR、新婚前最後可高強度衝刺的階段
2. **搜推正被 LLM 重構** — 傳統推薦系統（Wide & Deep 以來）邊際效益遞減，未來面試標配是 RAG + Agent 實戰
3. **垂直領域的壁壘價值** — 材料科學的髒數據/極端精準度需求，是通用 Chatbot 無法觸及的「地獄難度」訓練場
4. **PR 身份 = 流動性** — 不受簽證綁定，隨時可創造競價環境追回薪資差距

## Patsnap Offer 細節

- **職級**: Algorithm Expert（IC 高階，需指導同事）
- **月薪**: 13.5k SGD（Gross，CPF 另計）
- **結構**: 12 個月 Base + 1 個月 AWS + 2 個月 Target Bonus = ~202k
- **保險**: 試用期即生效（GP/SP/牙科/住院）
- **辦公**: RTO 五天，75 High Street，無 WFH
- **調薪**: 一年兩次（2 月普調 + 8 月晉升）
- **試用期**: 6 個月
- **無** Sign-on Bonus、無股權

## 與 Hiring Manager 溝通的技術定位

Huwei 哥（前同事）的核心觀點：
- **Agent 是工程問題**，資深算法做 Agent 是大材小用
- **搜推底層 + RAG 才是壁壘**，不是 LangChain 膠水代碼
- **垂直領域紅利期**（2024-2025），通用大模型紅利已過
- 團隊最終目標：**材料界的 Alpha**（數據 → Agent → RL → 模型訓練）

## 風險與對策

| 風險 | 嚴重度 | 對策 |
|------|--------|------|
| 薪資錨點被鎖在 202k | 高 | Expert 職級對標 Staff；累積量化戰績；PR 創造競價 |
| 材料科學太 Niche | 中 | 使用主流工具（LangGraph/RAGAS/vLLM）；聚焦通用方法論 |
| 公司縮減 AI 投入 | 中 | 前 3 個月觀察 GPU 預算與產品規劃 |
| RTO + 高強度 vs 新婚 | 中 | 辦公室靠近岩館；與伴侶建立「戰略共識」 |

## 規劃時間線

| 階段 | 時間 | 目標 |
|------|------|------|
| 預熱期 | 入職前 1 個月 | 休息 + LangGraph/LlamaIndex/Scientific RAG 論文 |
| 蹲馬步 | 0-6 個月 | 摸透 RAG 系統（Chunking/Embedding/Reranking） |
| 技術爆發 | 6-18 個月 | 攻克跨段落證據整合；建立 AI 專家品牌 |
| 價值回歸 | 18-36 個月 | 帶 Expert 頭銜 + 作品集衝刺大廠 E6/Staff（350-450k） |

## Concepts Referenced

- [Material Science Agents](../concepts/material-science-agents.md) — Patsnap 所在的技術領域
- [Context Engineering](../concepts/context-engineering.md) — 主管認為 Agent 的核心在此
- [ACE Framework](../concepts/ace-framework.md) — 團隊技術願景的理論基礎

## Notes

- 同儕焦慮是驅動力也是陷阱 — 前同事在大廠搜推領 350k，但他們的技術棧可能在 LLM 時代邊緣化
- 「帶薪讀博」心態：202k 是研發補助，不是身價定義
- 核心命題：「解決複雜問題的能力」vs「在穩定平台領高薪」— 選前者
- 面對主管的回答策略：「搜推是優化過去，GenAI 是創造未來」
