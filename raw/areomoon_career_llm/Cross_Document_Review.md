---
title: "跨文件統整：矛盾修正、缺口補齊、優先執行建議"
date: 2026-04-08
tags: [career, review, synthesis, action-items]
---

# 跨文件統整：矛盾修正、缺口補齊、優先執行建議

本文件交叉審閱 `areomoon_career_llm/` 資料夾內的 4 份文件，找出文件間的矛盾、冗餘、和缺口，給出修正建議和統一的執行優先序。

---

## 一、4 份文件的定位與重疊

| 文件 | 寫作時間點 | 核心定位 | 問題 |
|------|-----------|----------|------|
| **Agentic_Service_Warmup_Plan** | 最早 | 6 週技術學習計畫 | 已被 `areomoon_agent_warmup` repo 取代，內容較舊 |
| **Claude_Code_Leak_Architecture_Insights** | 中期 | Agent 架構模式分析 | 品質好，但「對我們專案的啟示」部分尚未落地 |
| **Career_Development_Roadmap** | 較早版本 | 200K→300K 職涯策略 | 是舊版本（基於 repo audit），不含入職資訊 |
| **Onboarding_Action_Plan** | 最新 | 入職行動計畫 | 最對齊現況，但和 Warmup Plan 有大量重複 |

**核心問題：Warmup Plan 和 Onboarding Plan 有 70% 重疊。** 兩份都講 Generator-Reflector、QLoRA、MARS，但 Warmup Plan 不知道你即將入職，Onboarding Plan 不知道你有 `areomoon_agent_warmup` repo 的完整 code。

---

## 二、文件間的矛盾

### 矛盾 1：時間線不一致

| 文件 | 假設的入職時間 | 計畫長度 |
|------|---------------|----------|
| Warmup Plan | 未提及入職 | 6 週 |
| Onboarding Plan | 2026 年 5 月入職 | 入職前 + 前 4 個月 |
| Career Roadmap | 未提及入職 | 12 個月跳槽策略 |

**修正：** 你的真實時間線是 **2026/5 入職 → 2027/5 前拿到 300K+ offer**。所有計畫應對齊這條線。

### 矛盾 2：Portfolio 策略衝突

Career Roadmap 建議建 3 個公開 repo（`scientific-paper-agent`, `ml-system-design`, `rag-experiments`）。但你實際上已有 `areomoon_agent_warmup` 裡完整的 GRC code，和 `areomoon_agent_plan` 裡的架構分析文件。

**各 repo 實際定位澄清：**
- `areomoon_agent_warmup` — **私有練習 repo**，入職前實作練習用，不適合直接公開當 portfolio
- `llm_knowledge_base` — **私有知識庫**，餵給 Claude agent 做個人諮詢的 assistant，非公開作品
- `areomoon_agent_plan` — 學習文件 + 架構分析（目前公開）

**修正：** Portfolio 需要另建專門的展示用 repo，從練習 code 中萃取精華、加上架構文件和 eval 數據後才公開。結構建議：

```
公開（展示用）：
  areomoon_agent_plan         → 架構分析 + 學習歷程（已公開）
  scientific-paper-agent      → 旗艦 portfolio（新建，從 warmup 萃取精華 + 加 README/架構圖/eval）
  ml-system-design            → 用自己的話重寫 5-7 個 case（從 ML_sysyemdesign clone 改寫）

私有（不公開）：
  areomoon_agent_warmup       → 練習 repo，持續迭代
  llm_knowledge_base          → Claude agent 個人知識庫
  local-rag-llama-demo        → 遷移精華到旗艦 repo 後 archive
  leetcode101/coding_practice → 合併，面試刷題用

設為 archive：
  DL_tensorflow_learning, tensorflow_offline_prac, tryout_chatgpt
```

> **關鍵區分：** 練習 repo 的 code 可以亂、可以有 TODO、可以有半成品。
> Portfolio repo 的每個檔案都要有意義：README 有架構圖和數字、code 可跑、有 eval 結果。
> 從 warmup 練習中挑出最成熟的部分（例如跑通的 extraction_agent + eval 數據），
> 重構到 portfolio repo 裡。

### 矛盾 3：文章主題重複

Career Roadmap 列了 5 篇文章。Onboarding Plan 沒提文章。兩邊都沒考慮到你已經在 `areomoon_agent_plan` 有一份完整的 Claude Code 架構分析，可以直接改寫。

**修正：** 文章策略統一（見下方第四節）。

---

## 三、所有文件都缺少的東西

### 缺口 1：Eval 基準線

4 份文件都提到 evaluation 很重要，但沒有一份定義了 **具體的 eval metric 和 baseline 數字**。

你的 `extraction_agent.py` 有 VO₂ 薄膜的 sample text 和完整 schema，但你還沒有：
- 一個 ground truth dataset（至少 20-30 篇論文的手動標註）
- 一個 baseline 數字（純 GPT-4.1-mini zero-shot extraction 的 accuracy 是多少？）
- 一個 eval script 能自動跑 precision/recall/F1

**行動：** 在入職前，用你的 VO₂ sample + 再找 5-10 篇不同材料的論文（PVD, CVD, sol-gel 各挑幾篇），手動標註 ground truth。跑一次 baseline。這組數據是所有後續工作的基準。

### 缺口 2：「材料科學 AI Agent」作為差異化標籤的市場驗證

Career Roadmap 說你的差異化是「材料科學 + AI Agent」交叉領域。但沒有驗證這個標籤在新加坡市場是否有足夠的 demand。

**行動：** 在 LinkedIn Jobs 搜以下關鍵字，記錄結果：
- "materials science AI" Singapore — 看有多少職位
- "AI agent" Singapore — 看有多少職位
- "scientific data extraction" — 看哪些公司在做
- 看 A*STAR、NUS、SUTD 是否有相關的研究 / industry 合作

如果純材料科學 AI 職位太少，你的 positioning 應該更廣：**「AI Agent 系統架構師，專精科學文獻智能處理」**，這樣可以同時 target 材料科學公司和通用 AI Agent 公司。

### 缺口 3：入職後的 Design Doc 模板

Onboarding Plan 說「第 1-2 個月做 Generator extraction prompt + Reflector self-consistency」，Career Roadmap 說「寫 Design Doc」。但沒有人具體說 Design Doc 該長什麼樣。

你要寫的第一份 Design Doc 結構建議：

```
Title: GRC Extraction Pipeline for [Material Class]

1. Problem Statement
   - 現有 extraction 流程的痛點（手動？準確率？速度？）
   - 量化：科學家目前花多少時間做這件事

2. Proposed Solution
   - GRC (Generator-Reflector-Curator) 架構
   - 架構圖（你 areomoon_agent_warmup 裡已有）
   - 和現有流程的差異

3. Technical Design
   - Generator prompt template（你已有）
   - Reflector validation logic（你已有）
   - Playbook evolution mechanism（你已有）
   - Schema 定義（你的 MATERIALS_EXTRACTION_SCHEMA 已有）

4. Evaluation Plan
   - Dataset：N 篇論文，M 個欄位
   - Metrics：per-field accuracy, recall, F1
   - Baseline：zero-shot GPT-4.1-mini
   - A/B：GRC vs baseline

5. Timeline & Milestones
   - Week 1-2: baseline eval
   - Week 3-6: GRC pipeline
   - Week 7-8: A/B comparison + report

6. Risks & Mitigations
```

你已經有 80% 的素材（schema、code、架構概念）。入職第一週就能開始寫。

### 缺口 4：cross-paper validation

你的 `extraction_agent.py` TODO 裡寫了 "Add cross-paper validation: compare same material across multiple papers"。這是一個所有文件都沒展開的高價值功能。

為什麼重要：科學家最痛的不是「從一篇論文裡抽數據」，而是「比較 10 篇論文裡同一材料在不同合成條件下的性質差異」。如果你的 Agent 能做到這一點，impact 直接翻倍。

這應該是入職 Month 3-4 的主要目標，也是你寫文章的素材。

---

## 四、統一的執行計畫

將 4 份文件的建議去重、排序，對齊「2026/5 入職 → 2027/5 拿到 300K+ offer」的時間線。

### 入職前（2026 年 4 月，剩餘 3 週）

**技術：**
- [ ] 跑通 `extraction_agent.py`，拿到 VO₂ demo 結果
- [ ] 手動標註 5-10 篇論文的 ground truth（不同材料、不同合成方法）
- [ ] 跑 baseline eval（zero-shot GPT-4.1-mini），記錄 accuracy 數字
- [ ] 跑 GRC loop（`generator_reflector.py`），記錄改善幅度

**Portfolio：**
- [ ] 把 TF tutorial repos（`DL_tensorflow_learning`, `tensorflow_offline_prac`, `tryout_chatgpt`）archive
- [ ] 改 LinkedIn headline
- [ ] 規劃 `scientific-paper-agent` portfolio repo 的 README 結構（入職後有 eval 數據再正式建立）

**人脈：**
- [ ] 約 1 位拿 300-400K 的同儕聊 30 分鐘

### 入職 Month 1-3（2026 年 5-7 月）

**在公司內：**
- [ ] 第 1 週對齊 manager 期望，搞清楚團隊現有 pipeline
- [ ] 第 2-3 週交付第一個 quick win
- [ ] 第 4-8 週寫第一份 Design Doc（GRC extraction pipeline）
- [ ] 第 8-12 週跑 A/B eval，產出量化結果

**在公司外：**
- [ ] 發佈文章 1：Claude Code 架構分析（改寫你已有的文件，最快能出）
- [ ] 發佈文章 2：MARS 19-agent 架構拆解（你的研究筆記直接改寫）
- [ ] LinkedIn 每週 1 則短 post
- [ ] 參加 1 次 AI Singapore meetup

### 入職 Month 4-8（2026 年 8-12 月）

**在公司內：**
- [ ] 累積 extraction cases → 做 QLoRA 微調實驗
- [ ] 建立 eval benchmark（和 Onboarding Plan 的 Phase 2 對齊）
- [ ] 實作 cross-paper validation 功能
- [ ] 寫第 2 份 Design Doc（微調 vs prompt engineering trade-off 報告）
- [ ] 在內部 tech talk 分享

**在公司外：**
- [ ] 發佈文章 3：GRC extraction 的 A/B eval 數據
- [ ] 發佈文章 4：Fine-tuning vs Prompt Engineering 真實比較
- [ ] 重寫 5 個 ML system design case（加 GenAI 觀點）
- [ ] 建立 10-15 個業界聯繫人
- [ ] 做 1 次 lightning talk

### 入職 Month 9-14（2027 年 1-5 月）

**拿 offer：**
- [ ] 準備面試素材（12 個月的 Design Doc + eval 數據 + 文章）
- [ ] 聯繫 headhunter
- [ ] 面 3-5 家
- [ ] 拿到 2-3 個 competing offer
- [ ] 談到 300K+ TC

---

## 五、文章發佈的統一排序

| 順序 | 文章 | 素材來源 | 預計時間 | 為什麼這個順序 |
|------|------|----------|----------|---------------|
| 1 | Claude Code 洩漏的 7 個 Agent 設計模式 | `Claude_Code_Leak_Architecture_Insights.md` 改寫 | 入職 Month 1 | 有話題性、素材最完整、最快能出 |
| 2 | MARS 19-Agent 架構：材料科學 AI 的未來 | `mars_architecture_study.md` + 你的入職觀察 | Month 2 | 差異化內容，英文世界幾乎沒人寫 |
| 3 | GRC Extraction：科學論文自動抽取的 A/B 測試 | 入職後的 eval 數據 | Month 4-5 | 有真實數據才有說服力 |
| 4 | Fine-tuning vs Prompt Engineering 在科學文本的比較 | 微調實驗數據 | Month 6-7 | 和文章 3 形成系列 |
| 5 | 算法工程師的 AI Agent 轉型經驗 | 你的完整歷程 | Month 8-9 | 個人品牌，放在面試前發佈效果最好 |

---

## 六、需要從知識庫刪除或更新的內容

| 文件 | 建議 | 原因 |
|------|------|------|
| `Agentic_Service_Warmup_Plan.md` | 標註為 archived | 已被 `areomoon_agent_warmup` repo 完全取代 |
| `Career_Development_Roadmap.md` | 需更新 | 是舊版本，不含入職資訊和 warmup repo 分析。`areomoon_agent_plan` repo 裡已有最新版 |
| `Claude_Code_Leak_Architecture_Insights.md` | 保留，準備改寫成公開文章 | 品質好，且是文章 1 的素材 |
| `Onboarding_Action_Plan.md` | 保留，作為 single source of truth | 最對齊現況的行動計畫 |
