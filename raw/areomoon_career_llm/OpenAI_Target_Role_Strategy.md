# OpenAI 目標職位分析與 6-12 個月轉職策略

> 來源：Claude Code 對話 (2026-04-09)
> 主題：OpenAI AI Deployment Engineer (Startups, Singapore) 職位分析 + 從 Patsnap 到 OpenAI/Anthropic 的規劃

---

## 一、目標職位：OpenAI AI Deployment Engineer, Startups

### JD 摘要
- **地點**：Singapore（Hybrid，每週 3 天進辦公室）
- **本質**：Solutions Engineer + Applied AI + Developer Relations 混合體
- **核心工作**：跟 startup 客戶合作 prototype agents/prompts/workflows，回饋 evaluation/benchmark 給 Product & Research
- **非傳統 MLE**：不是坐在後面寫 model，是跟客戶一起 prototype、debug、design workflow

### 核心要求
- SWE/ML/DS 背景 + production 經驗
- AI agent / evaluation 實作經驗
- 能把客戶 usage pattern 翻譯成 evaluation/benchmark
- 強溝通力（技術 + 非技術受眾）
- High agency + product sense
- 加分：中文/韓文/日文

### 目前 Match 程度

| JD 要求 | 現在 | 6 個月後（Patsnap） |
|---------|------|-------------------|
| Production systems | ✅ | ✅ |
| AI agents / workflows | ⚠️ 理論有實戰少 | ✅ RAG + Agent pipeline |
| Evaluation systems | ❌ | ✅ 若建了 eval pipeline |
| Prompt prototyping | ⚠️ | ✅ expert context prompt |
| Model training / RL | ⚠️ | 🟡 看 Patsnap 有沒有做 SFT |
| 溝通 / 面對客戶 | ⚠️ 偏 IC | 🟡 需刻意練 |
| Mandarin | ✅ 母語 | ✅ |

---

## 二、Patsnap → OpenAI/Anthropic 行動規劃

### Phase 1：Patsnap 刻意累積（0-6 個月）

對齊 JD 的 4 個核心能力：

1. **Agent / Workflow Design**：把 RAG pipeline 設計成 multi-step workflow，能講完整 design decision + tradeoff
2. **Evaluation System（差異化武器）**：建 offline eval pipeline（precision@k、evidence grounding rate）— 大部分候選人沒有這個
3. **Prompt / Context Engineering**：記錄 prompt 方法論（什麼有效/失敗/如何 iterate）
4. **溝通 + 客戶面**：主動跟 scientist/domain expert 互動，做 internal demo/presentation

### Phase 2：市場準備（4-6 個月開始）

履歷敘事直接對齊 OpenAI JD：
- 「Designed and deployed RAG-based agent workflows for scientific research, prototyping prompt strategies and evaluation frameworks」
- 「Built evaluation pipeline to convert usage patterns into systematic benchmarks」
- 「Collaborated with domain experts to translate complex workflows into AI-powered solutions」

### Phase 3：投遞 + 擴大目標（6-12 個月）

目標公司：
- OpenAI — Applied AI / Solutions Engineer / Developer Experience
- Anthropic — Solutions Engineer / Applied Research（SG 擴編中）
- Google DeepMind — Applied ML
- AI Startups（SG）— Head of AI / Senior Applied AI

---

## 三、人脈策略

### Grab 前同事（最高價值資產）

現在在 ByteDance / Apple / Meta 做算法，是未來 referral 的核心來源。

**Phase 1（0-3 個月）：維持溫度，不求事**
- 每 1-2 個月聊一次
- 聊技術（「你們 team 在用什麼 RAG/Agent 方案？」）不聊求職
- 目的：讓他們持續知道你在做 AI agent

**Phase 2（3-6 個月）：播種**
- 有了具體成果後主動分享
- 自然地問：「你們那邊有沒有在看 Applied AI / Agent 方向的人？」
- 他們會主動想到你

**Phase 3（6-12 個月）：收割 referral**
- 他們腦中的你已經是「做過 agent + RAG 的人」
- 直接問 refer 很自然

### 需要新建立的人脈（Applied AI 圈）

Grab 同事在大廠做推薦/MLOps，但 OpenAI/Anthropic 需要的是另一群人：

1. **SG AI Meetup**
   - AI Singapore 活動
   - LLM / GenAI meetup
   - OpenAI / Anthropic developer event
   - 目標：認識 1-2 個 target 公司的 Applied AI 人

2. **LinkedIn 主動出擊**
   - 找 OpenAI SG / Anthropic 的 Applied AI / Solutions 團隊成員
   - 留有價值的 comment 或 DM，不是加了就算
   - 目標：3-6 個月跟 2-3 個 target 公司的人有過真實對話

---

## 四、Portfolio 策略

### LinkedIn Profile 重塑
- 標題改為：`Senior ML Engineer | RAG / AI Agent Systems | Search & Retrieval`
- About 段落寫 search → RAG → agent 的轉型故事
- 關鍵字：RAG, LLM, Agent, Evaluation, Retrieval, NLP（recruiter 搜人用這些）

### 技術文章計畫（6 個月內 2-3 篇）

| 篇 | 主題 | 何時 | 對齊 JD |
|---|---|---|---|
| 1 | 從 Search Ranking 到 RAG：5 個設計差異 | 入職 2 個月 | workflow design |
| 2 | 如何建立 RAG Evaluation Pipeline | 入職 4 個月 | evaluation（核心武器）|
| 3 | 垂直領域做 Agent：data quality > model | 入職 6 個月 | domain collaboration |

### GitHub
- 公開一個 RAG evaluation framework（toy 版本也行）
- `llm_knowledge_base` 本身就是 portfolio（structured knowledge + agent workflow）

### 「被發現」漏斗

```
LinkedIn 關鍵字 / 技術文章被看到
        ↓
Recruiter 或 insider 注意到你
        ↓
前同事 referral
        ↓
面試時有實戰 + 文章 + eval pipeline
        ↓
Offer
```

---

## 五、每週時間分配

| 活動 | 頻率 | 時間 |
|------|------|------|
| 跟 Grab 前同事聊 | 每月 1-2 次 | 30 min/次 |
| LinkedIn 經營（comment/post） | 每週 2-3 次 | 15 min/次 |
| 寫技術文章 | 每月 1 篇 | 2-3 hr/篇 |
| 參加 SG AI meetup | 每月 1 次 | 2 hr/次 |

---

## 六、OpenAI 缺 vs 大廠 MLE 路線比較

| 維度 | 大廠 MLE（Meta/TikTok） | OpenAI Deployment Eng |
|------|------------------------|----------------------|
| 薪資 | 300-350k | 250-350k（估計）|
| 技術深度 | 深但窄（ranking/ads） | 廣但偏應用（agent/eval/workflow）|
| 職涯天花板 | Staff MLE | Applied AI Lead → Product |
| 入門難度 | 高（競爭激烈） | 中高（但 profile 更 match）|

關鍵洞察：OpenAI 這類缺更適合「轉賽道」路線，不要求 ranking expert，要的是能用 AI 解決實際問題 + 建 evaluation 的人。
