---
title: "職涯執行計畫：入職前 → 入職 → 跳槽 完整時間線"
created: 2026-04-09
tags: [career, patsnap, execution-plan, openai, networking]
---

# 職涯執行計畫：Patsnap → 300k+ Applied AI

> 基於 [Gemini 諮詢](../derived/gemini-career-decision-patsnap.md)、[ChatGPT 諮詢](../derived/chatgpt-patsnap-interview-strategy.md)、[OpenAI 目標分析](../derived/openai-target-role-strategy.md) 三份討論的綜合行動方案。

---

## Phase 0：入職前（現在 ~ 5 月中，約 4-6 週）

### 技術預熱（每天 1-2 小時，低壓）

> 對應 [areomoon_agent_warmup](https://github.com/areomoon/areomoon_agent_warmup) repo 的 6 週 warmup 計畫。
> 以下按 warmup repo 模組排列，標注優先級。

**Week 1 — Prompt Engineering（必做）** → `01_prompt_engineering/`
- [ ] 跑 `chain_of_thought.py`：比較 Zero-shot CoT vs Manual CoT 在科學文本的差異
- [ ] 跑 `react_pattern.py`：理解 ReAct（Reasoning + Acting）基礎
- [ ] 完成 `notebook/prompt_engineering_lab.ipynb`
- [ ] 讀論文：CoT (Wei 2022)、ReAct (Yao 2022)

**Week 2 — RAG Fundamentals（核心）** → `02_rag_fundamentals/`
- [ ] 跑 `basic_rag.py`：LlamaIndex 基礎 pipeline（PDF → chunk → embed → retrieve → generate）
- [ ] 跑 `embedding_search.py`：比較 BGE-M3 vs text-embedding-3-small
- [ ] 完成 `notebook/rag_lab.ipynb`（用真實論文做問答）
- [ ] 額外：掃 LlamaIndex Advanced Retrieval 文件（Parent-Child / Hierarchical Indexing）

**Week 3 — Agent Patterns（關鍵）** → `03_agent_patterns/` + `04_ace_framework/`
- [ ] 跑 `generator_reflector.py`：ACE Generator-Reflector pattern
- [ ] 跑 `reflection_agent.py`：LangGraph reflection agent（自我修正循環）
- [ ] 跑 `multi_agent_basic.py`：Orchestrator + Specialist agents
- [ ] ACE：跑 `playbook_evolution.py` + `curator_pattern.py`
- [ ] 讀論文：Reflexion (Shinn 2023)、ACE (arXiv 2510.04618)

**Week 4 — Multimodal（材料科學需要）** → `07_multimodal/`
- [ ] 跑 `image_analysis.py`：圖表理解（GPT-4.1-mini vision / Claude API）
- [ ] 理解 ColPali / DocLLM 在文件檢索的應用

**Week 5 — Fine-tuning（了解即可）** → `06_finetuning/`
- [ ] 跑 `lora_basics.py`：LoRA 原理
- [ ] 理解 QLoRA 訓練流程（Colab 上跑一次）
- [ ] 理解 SFT vs RAG+prompt 的取捨（Patsnap 團隊已選後者）

**持續 — Material Science Agents** → `05_material_science_agents/`
- [ ] 讀 `mars_architecture_study.md` + `llmatdesign_study.md`
- [ ] 跑 `extraction_agent.py`：材料論文 extraction agent 原型
- [ ] 對照知識庫 [Material Science Agents](../concepts/material-science-agents.md) 概念文章

**其他預熱**
- [ ] 熟悉向量資料庫差異（Milvus vs Qdrant vs Pinecone — 至少知道取捨）
- [ ] 瀏覽 warmup repo 的 `resources/papers.md` 和 `resources/tools.md`

### 人脈啟動
- [ ] 跟 Huwei（hiring manager）聊：前 1-3 月期待、目前最大 bottleneck、建議先看什麼
- [ ] 跟 2-3 位 Grab 前同事各聊一次（聊技術趨勢，不提求職）
- [ ] LinkedIn Profile 更新：標題改為 `Senior ML Engineer | RAG / AI Agent Systems | Search & Retrieval`，About 段落重寫

### 生活準備
- [ ] 台北離職手續 + 搬遷安排
- [ ] 新加坡租房（考慮 75 High Street 通勤 + 攀岩館距離）
- [ ] 婚姻登記相關文件
- [ ] 攀岩：盡情爬，入職後會變少

---

## Phase 1：入職初期（Month 1-3）— 「快速卡位」

### 核心目標
> 讓主管和團隊覺得：「這人不是新手，是可以丟問題的人」

### Month 1：理解系統 + 找問題
**Week 1**
- [ ] 自己畫出完整 pipeline 圖（PDF → parsing → chunking → embedding → retrieval → LLM → answer）
- [ ] 標記每個環節的 bottleneck（慢？不準？hallucination？）
- [ ] 問主管 3 個高價值問題：
  - 目前 extraction 最常錯在哪類資料？
  - Scientist 最不信任的 case 是哪種？
  - Latency bottleneck 是 parsing 還是 retrieval？

**Week 2-3**
- [ ] 選定一個「高價值問題」（extraction precision / retrieval recall / latency）
- [ ] 提出方案：「我觀察到 X 問題，想試方法 Y，預期改善 Z」
- [ ] 快速做 prototype（速度 > 完美）

**Week 4**
- [ ] 做 before/after 量化比較
- [ ] 主動跟團隊分享結果（demo / 簡報）
- [ ] **30 天紅旗檢查**：我的 task 是核心系統問題，還是 API glue / prompt 調整？

### Month 2-3：建立技術標籤
- [ ] 拿下至少一條 pipeline 的 end-to-end ownership
- [ ] 開始建 evaluation system（offline metrics + human feedback loop）
- [ ] 主動跟 scientist / domain expert 互動，理解真實使用場景
- [ ] 記錄 prompt engineering 方法論（什麼有效/失敗/如何 iterate）

### 人脈 & Portfolio
- [ ] 每月跟 1 位 Grab 前同事聊（分享你在做的 AI agent 工作）
- [ ] LinkedIn 開始活躍：每週 2-3 次 comment 或 repost AI 相關內容
- [ ] 參加 1 次 SG AI meetup

### 3 個月 Checkpoint ⚠️
問自己：
1. 有沒有做過一個 RAG pipeline？
2. 有沒有解過一個 hard problem？
3. 有沒有 measurable impact？

→ **都沒有 → 立刻開始低強度找下一份**
→ 都有 → 進入 Phase 2

---

## Phase 2：入職中期（Month 3-9）— 「建立影響力 + 準備彈藥」

### 核心目標
> 累積 2-3 個可以寫進履歷、講進面試的 killer project

### 技術深度
- [ ] 主導一個 Agent feature（multi-step reasoning / evidence aggregation / scientist workflow optimization）
- [ ] 把 evaluation system 做到可量化（precision@k、grounding rate、latency）
- [ ] 如果有機會接觸 SFT / model training — 搶著做

### 產品影響力
- [ ] 綁定 product metrics（query success rate ↑ / research time ↓ / user adoption ↑）
- [ ] 開始 influence PM / domain expert 的 product decision
- [ ] 每個 project 記錄：problem → solution → tradeoff → impact（面試故事素材）

### Portfolio 建設
- [ ] **第 1 篇技術文章**（Month 4）：「從 Search Ranking 到 RAG：5 個設計差異」
- [ ] **第 2 篇技術文章**（Month 6）：「如何建立 RAG Evaluation Pipeline」
- [ ] GitHub 放一個公開的 eval/RAG repo
- [ ] 開始做 1-2 次 internal 或 external 技術分享

### 人脈升級
- [ ] 跟 Grab 前同事分享具體成果，自然詢問：「你們那邊有沒有在看 Applied AI / Agent 方向的人？」
- [ ] LinkedIn 主動觸及 OpenAI SG / Anthropic 的 Applied AI 成員（有價值的 DM，不是隨便加）
- [ ] 持續參加 SG AI meetup，目標：認識 2-3 個 target 公司的人

### 低強度市場測試
- [ ] 每週 1-2 個 recruiter call
- [ ] 每月 1-2 個 screening interview
- [ ] 目的：練 narrative + 探市場價格，不是拼命找工作

---

## Phase 3：準備跳槽（Month 9-12）— 「收割」

### 核心目標
> 帶著 "agent workflow + eval pipeline + domain collaboration" 三件套出去打

### 履歷最終版
```
Senior ML Engineer (LLM / RAG / Agent Systems) — Patsnap
• Designed multi-stage RAG pipeline for scientific literature, improving
  answer reliability and decision-making support for R&D users
• Built evaluation pipeline (offline + human feedback) converting usage
  patterns into systematic benchmarks — reduced hallucination rate by X%
• Improved retrieval precision via hybrid search + re-ranking, ↑ recall X%
• Developed evidence aggregation framework for multi-source scientific
  reasoning, ↑ user trust metrics
• Collaborated with domain experts to translate complex R&D workflows
  into AI-powered agent solutions, ↓ research time from 10hr to Xhr
```

### 面試準備
- [ ] System Design：「怎麼幫一個 startup 設計 AI workflow」（不是設計 infra）
- [ ] Behavioral：「講一次你幫非技術人員解決 AI 問題的經驗」
- [ ] Product Sense：「這個 use case 適合 agent 還是 simple RAG？」
- [ ] **第 3 篇技術文章**（Month 8）：「垂直領域做 Agent：data quality > model」

### 目標公司 & 職位
| 公司 | 職位方向 | 預估薪資 |
|------|---------|---------|
| OpenAI | Applied AI / Solutions Engineer / Developer Experience | 250-350k |
| Anthropic | Solutions Engineer / Applied Research | 250-350k |
| Google DeepMind | Applied ML | 300k+ |
| Meta GenAI | Applied AI / LLM Product | 300-350k |
| AI Startups (SG) | Head of AI / Senior Applied AI | 250-400k |

### 談判策略
- 用 Patsnap 的 agent + eval 經驗作為核心賣點
- 用 competing offers 創造競價
- 永遠講 total comp range，不講 base
- Grab 前同事 referral 作為主要進入管道

---

## 貫穿全程的原則

1. **每個 task 問自己**：「能不能寫在履歷第一條？」— 不能就降低投入
2. **Domain abstraction**：永遠講「complex knowledge system / AI agent」，不講「材料科學」
3. **人脈 = 分發渠道**：先有值得分發的東西（實戰 + 文章），再讓人脈幫你送到對的地方
4. **Evaluation 是差異化武器**：大部分 MLE 不會做 eval system，你有就是碾壓
5. **攀岩 = 心理調節**：每週至少 1-2 次，防 burnout，Funan / Rochor 岩館離辦公室近

---

## 時間分配（每週額外 3-4 小時）

| 活動 | 頻率 | 時間 |
|------|------|------|
| Grab 前同事 coffee chat | 每月 1-2 次 | 30 min/次 |
| LinkedIn 經營 | 每週 2-3 次 | 15 min/次 |
| 技術文章寫作 | 每月 1 篇 | 2-3 hr/篇 |
| SG AI meetup | 每月 1 次 | 2 hr/次 |
| Recruiter call / screening | 每週 1-2 次 | 30 min/次 |
