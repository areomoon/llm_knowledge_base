# ChatGPT 諮詢：Patsnap 面試準備與職涯策略全紀錄

> 來源：ChatGPT 多輪對話
> 諮詢主題：Patsnap 面試全流程（技術面 → PM 面 → HR 談薪）+ 職涯規劃

---

## 一、Patsnap 公司與團隊分析

### 公司定位
- AI 驅動的研發情報平台（ToB SaaS）
- 核心客戶：科技公司 R&D、製藥/生技、製造業、律師事務所
- 「中國背景 + 新加坡總部」混合體，決策偏快、KPI 導向
- 數十億級專利與技術資料，強調 AI/NLP/LLM

### Formulation 團隊現況
- 專注材料科學「配方（Formulation）」業務，首要聚焦日化行業（P&G、Unilever）
- 目標用戶：RD Scientist / Chemist
- 團隊組成：PM×1、全端×1、後端×1、算法×1（極精簡）
- 四條產品線：General QA、小型搜尋引擎、插件功能、私有化 Agent
- 2026 上半年策略：RAG + 專家 context prompt 取代傳統 SFT，實證效果好
- 核心痛點：長文獻抽取、專家 context 檢索、線上提取速度慢（~5 分鐘）

### 主管（Huwei）的技術觀點
- 「數據是資產，Agent 只是殼」
- Agent 偏工程，資深算法做 Agent 是浪費
- 搜推底層 + RAG 才是壁壘
- 團隊最終目標：材料界的 Alpha（數據 → Agent → RL → 模型訓練）

---

## 二、面試準備與執行

### 技術面（System Design）

**核心題型：設計材料科學 AI Assistant**

回答框架：
1. **Data Ingestion**：PDF parsing → 保留 section/table/figure caption 結構
2. **Structure-aware Chunking**：非純 length-based，保留語義邊界
3. **Hybrid Retrieval**：dense embedding + sparse keyword + re-ranking
4. **Evidence Aggregation**：多來源結構化整理（material/property/condition/value）
5. **Context Normalization**：將不同實驗條件標準化以便比較
6. **Multi-step Agent Reasoning**：iterative retrieval，根據前一步結果動態查詢
7. **Grounded Generation**：所有回答附 citation，信心不足時 abstain

**長文獻跨段落整合方案**：
- Hierarchical Indexing（Parent-Child 關係索引）
- Table-to-Markdown/JSON 轉換
- Multi-Vector Retrieval（文本/數值/化學式各自 embedding）
- Bridge Retrieval（根據初步結果自動發起二次檢索）
- ReAct 框架（判斷資訊是否足夠，不足則追查）

**Data Extraction Pipeline（三層）**：
1. **Parsing**：PDF → 結構化 document object（段落/表格/圖表/標題邊界）
2. **Information Extraction**：明確抽取 material/property/condition/value/source
3. **Validation**：unit normalization、range check、schema check、cross-source consistency
- 策略：先從 high-value use case 開始，precision 優先於 recall

**Trust 問題解決方案**：
- Evidence：所有結果有清楚來源
- Transparency：呈現關鍵 context（條件/方法）
- Consistency：類似問題給出穩定結果
- 結構化呈現（對照表）而非單一結論
- 「避免讓系統看起來太聰明，讓它看起來可驗證」

### PM 面

**核心考點**：Product sense + Tradeoff + MVP 思維

**Option A vs B 題（data pipeline 精做 vs 快速上線）**：
- 選 B 起手但帶 A 的長期規劃
- MVP 先驗證 use case，用 user feedback 指導 data pipeline 優化
- 「不在一開始過度優化 data，讓系統在實際使用中暴露問題」

**Metric 評估**：
- Retrieval 端：precision@k、recall、evidence-level accuracy
- User 端：evidence click-through、follow-up query rate、session depth
- Long-term：task completion time（10hr → 6hr）

**A/B Test 設計**：
- 分流：control (baseline RAG) vs treatment (agent/aggregation)
- Metric：多層次（trust/follow-up/task completion）
- 風險控制：小流量開始，fallback 機制，避免 false positive

### HR 面

**Behaviour Question 準備**：

壓力題萬用模板：
1. 承認壓力（但不抱怨）
2. 結構化拆解（「拆成三個 priority」）
3. 行動（systematic）
4. 結果（metric/process improvement）
5. 學習（升級）

缺點題：
- 「遇到問題時容易太快進入解決模式，在問題還沒定義清楚前就投入」
- 有意識調整：先拆問題、對齊再動手

**Self Intro 定位**：
- 從 "Search Engineer" 轉為 "AI Agent / RAG System Builder"
- 核心敘事：Search → RAG → Agent 是自然延伸，不是轉行

---

## 三、薪資談判策略

### 談判原則
1. 永遠不先給死數字，給 range
2. 用 equity → cash 結構變化合理化加薪要求
3. 強調 scope + risk + impact，不是只談「加薪」
4. 永遠不在第一輪接受數字

### 實際談判過程
- 現薪：~200k SGD（140k cash + 60k equity）
- 開價策略：anchor 230-250k（留談判空間）
- HR 回覆：13.5k × 15 = 202k（全現金）
- 最終結果：~200k，幾乎無法再調

### 關鍵話術
- 「Given the shift from equity to cash, I'd expect a meaningful step up」
- 「It would be difficult for me to move at this level」
- 「If we can get closer to 230+, I'd feel very comfortable moving forward」
- 「I'd prefer to focus on what would make the move meaningful, rather than a minimum」

### Offer 細節
- Base: 13.5k SGD × 15（12月 + 1 AWS + 2 Target Bonus）= ~202k
- Title: Algorithm Expert
- Annual Leave: 14 天（carry forward 半年）
- RTO: 週一至週五，無 WFH
- Probation: 6 個月
- 保險：試用期即生效（GP/SP/牙科/住院）
- 調薪：一年兩次（2 月普調 + 8 月晉升/特殊）
- 無 Sign-on Bonus、無股權

---

## 四、職涯戰略規劃

### 短期（0-6 個月）— Patsnap 作為「轉賽道加速器」
- 核心目標：拿到 RAG + Agent + Product 實戰經驗
- 第一個 Project 方向：「提升 Scientific QA 可信度（trust + evidence）」
- 30 天計畫：
  - Week 1：畫系統 bottleneck 圖 + 找高價值問題
  - Week 2-3：提方案 + 快速做 prototype + 量化改善
  - Week 4：分享成果 + 建立技術標籤
- 只做高槓桿工作，拒絕 low leverage task
- 每個 project 問自己：「能不能寫在履歷第一條？」

### 中期（6-12 個月）— 變現跳槽
- 目標薪資：250-300k SGD
- 目標公司：Meta GenAI、TikTok AI Lab、Binance、AI startup
- 持續低強度面試（每週 1-2 recruiter call，每月 1-2 面試）
- 帶著 2-3 個 killer project story 出去打

### 長期（12-24 個月）— 穩定 + 高薪
- 目標：300k+ SGD、SG、不 burnout
- 選擇：大廠穩定 AI team 或高潛 startup
- 從「做 feature 的人」變成「定義問題的人」

### 路線定位
- 不是「大廠推薦系統 → 大廠推薦系統」（同儕路線）
- 而是「Search → LLM/RAG → Agent」（賽道升級路線）
- 推薦系統是「cash cow 賽道」，LLM/Agent 是「下一代高價值賽道」
- 「用 Patsnap 這一跳，進入 300k 賽道」

### 面試 Narrative（未來版本）
- 「我不是放棄搜推，是把搜推能力升級到下一個階段」
- 「問題從 ranking documents → synthesizing knowledge + supporting decision-making」
- 「我的優勢是結合 search/retrieval + LLM systems」
- 永遠講「AI system」不講「材料科學」— domain abstraction

### 履歷目標（6 個月後）
```
Senior ML Engineer (LLM / RAG / Agent Systems) — Patsnap
• Designed multi-stage RAG pipeline for scientific literature
• Built structured extraction pipeline (PDF → material/property/condition)
• Improved retrieval precision via hybrid search + re-ranking
• Developed evidence aggregation for multi-source reasoning
• Established evaluation pipeline (offline + human-in-the-loop)
• Impact: ↑ answer correctness, ↓ research time, ↑ user trust
```

---

## 五、風險管理

| 風險 | 等級 | 控制策略 |
|------|------|---------|
| 轉賽道失敗（只做 glue code） | 高 | 入職 1 個月內確認有 pipeline ownership |
| Burnout | 中 | 只做高槓桿工作，拒絕雜事 |
| 薪資被錨定在 200k | 中 | 賣 impact 不賣 base；用 competing offer |
| Domain 太 niche | 低 | 永遠講「complex knowledge system」|
| 假 AI 工作（prompt/API glue） | 高 | 30 天紅旗觀察清單 |

### 30 天紅旗觀察清單
- 🚩 team 只講 prompt/demo/showcase，不講 data/retrieval/evaluation
- 🚩 每個問題都用「換 model 試試」解決
- 🚩 沒有 offline eval / benchmark
- 🚩 domain discussion 多、system discussion 少
- 🚩 你的 task 只有 API 串接 / prompt 調整 / UI wrapper

### 3 個月 Checkpoint
問自己：
1. 有沒有做過一個 RAG pipeline？
2. 有沒有解過一個 hard problem？
3. 有沒有 measurable impact？
→ 如果都沒有 → 立刻開始找下一份

---

## 六、人脈策略

### 有效人脈 = 一起打過仗的人
- 不是同公司但不熟，不是 LinkedIn connect
- 是一起做過 production system、扛過 deadline、解過模糊問題

### 在 Patsnap 要鎖定的 3 種人
1. **Hiring Manager**：未來可能跳更好公司，第一個拉你
2. **強工程師/Algo**：未來的 referral 來源
3. **PM / Domain Expert**：未來的 decision maker

### 建立人脈的方式
- 主動接模糊問題（不是明確 ticket）
- 跟主管一起做決策（不是只執行）
- 成為「別人卡住找你」的人
- 做可見度高的成果（demo/分享/explain 設計）

---

## 七、同儕比較焦慮的認知調整

### 事實
- Grab 前同事在 TikTok/Apple/Meta，E5 級，300-350k SGD
- 他們吃到的是：時間紅利 + 賽道 alignment + path dependency

### 真正差距
- 不是能力差距，是「賽道差距」
- 他們一直在高價值賽道累積（ads/feed/infra）
- 你中間切了一次賽道（Grab search → Coupang logistics）

### 調整方式
- 從「比較現在薪資」→「比較未來可達薪資」
- 從「焦慮」→「策略」
- 接受「暫時落後」= 轉賽道必經期
- 「大部分高薪的人不是一直領高薪，是在某個時間點對齊了賽道」
