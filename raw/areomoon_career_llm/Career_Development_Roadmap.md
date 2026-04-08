# 從 200K 到 300–400K：基於你現有資產的執行計畫

---

## 你手上到底有什麼

我翻了你所有的 repo，你的狀況比你自己想的好，但呈現方式有嚴重問題。

**實際能力：**
- ML System Design 有完整的 9-step framework + 21 個 case study（推薦、搜尋、廣告排序、多模態），這是 Staff level 面試的核心素材
- LeetCode 刷了 38+ 題含 Hard（Burst Balloons, Trapping Rain Water, N-Queens），有完整的 BFS/DFS/DP/Binary Search 教學筆記
- 已經有一個結構不錯的 RAG 系統（local-rag-llama-demo）：LangChain + ChromaDB + HuggingFace embeddings + unit test
- LinkedIn 自動化求職工具展示了端到端的工程能力：scraping + 評分 + Notion sync + scheduler
- 正在建構的 Scientific Paper Agent 是 GenAI/Agent 方向的旗艦專案

**問題在哪：**
- 這些東西散落在 7-8 個私有 repo 裡，外人完全看不到
- 沒有一個 repo 有像樣的 README（架構圖、demo、量化結果）
- ML System Design 筆記是 clone 別人的 repo，不是你自己的產出
- TensorFlow 學習筆記是官方 tutorial 的複製，不加分
- 沒有任何公開的技術文章
- GitHub profile 上幾乎沒有任何能讓 hiring manager 停下來看的東西

> **結論：你的技術底子夠跳 300K+，但你的「包裝」完全不匹配你的 level。**
> 你同儕拿 300-400K，不只因為他們做推薦系統，而是他們的 impact 被看見了。

---

## 200K 和 400K 之間的真正差距

不是技術。你已有 ML system design 的知識庫，刷過 Hard 題，做過 RAG 系統。問題是：

| | 你現在 | 你同儕 300-400K |
|--|--------|-----------------|
| **影響範圍** | 做分配到的任務 | 自己定義要解什麼問題 |
| **可見度** | 團隊內部知道你做了什麼 | manager 的 manager 知道、業界有人知道 |
| **商業語言** | 「我建了 X 系統」| 「X 系統讓 CTR 提升 3%，對應年化 revenue +$2M」|
| **作品集** | 私有 repo + 沒有 README | 公開 repo + 架構文件 + 技術文章 |

你要做的不是「學更多技術」，而是 **把你已有的東西重新包裝 + 補齊 GenAI 實戰 + 讓對的人看到你**。

---

## Phase 1：重組你的武器庫（Month 1–2）

### 1.1 整併 GitHub Portfolio

你現在的 repo 結構是散的。目標是讓任何人點進你的 GitHub，7 秒內知道「這個人是做 AI Agent + ML System 的 Staff-level 工程師」。

**具體動作：**

**Repo 1 — `scientific-paper-agent`（旗艦，從 agentic_services 演化）**

你現在的 agentic_services 只有 doc/，沒有 code。這個 repo 要變成你最核心的展示品。

```
README.md 第一屏必須有：
1. 一句話：「Multi-agent system that extracts structured experimental data
   from scientific papers using LLM + multi-modal + RAG」
2. 一張架構圖（你 Claude Code Leak 文件裡已經有了）
3. 三個數字：處理速度、準確率、支援格式數
4. 一個 demo GIF（用 asciinema 或螢幕錄影）
```

這個 repo 的 code 來源：
- Agent 框架（LangGraph）→ 新寫
- RAG 部分 → 從你的 `local-rag-llama-demo` 遷移 + 升級（把 Ollama 換成 Gemini API，加 evaluation）
- 記憶系統 → 實作 Claude Code 揭示的三層記憶
- 工具 → MCP server 封裝

**Repo 2 — `ml-system-design`（展示 ML 深度）**

你的 `ML_sysyemdesign` 是 clone 別人的。這沒有價值。你要的是 **你自己的版本**。

```
做法：把你 clone 的 21 個 case study 裡面，挑 5-7 個你最熟的，
用你自己的話重寫，加入你在工作中的實際經驗和觀點。

每篇格式：
1. Problem Definition（2-3 句，用商業語言）
2. 架構圖（手繪 → draw.io 都行）
3. 你的設計 + 你會怎麼做不一樣（這是面試官想聽的）
4. Trade-off 分析
5. 延伸：如果加入 LLM/Agent 會怎麼改這個系統？
```

這「延伸」段是你的殺手鐧 — 把傳統 ML system design 和 GenAI 結合起來的人很少。面試時你說「推薦系統的 reranking 階段可以用 LLM 做 reasoning-based reranking」，直接拉開差距。

**Repo 3 — `rag-experiments`（從 local-rag-llama-demo 升級）**

你現有的 RAG demo 結構不錯（有 test、有 module 分離），但是：
- 用的是 Ollama local（你 Mac 會卡死）
- 只支援中文故事生成，太 niche
- 沒有 eval 結果

升級方向：
- 換成 Gemini/OpenAI API
- 加入英文科學論文支援（對齊你的 Agent 專案）
- 加入 naive RAG vs advanced RAG 的 A/B evaluation
- 結果用數字呈現在 README 裡

**其他 repo 處理：**
- `leetcode101`, `coding_practice`, `coding` → 合併成一個 `leetcode` repo，保持私有就好，面試用
- `DL_tensorflow_learning`, `tensorflow_offline_prac` → 刪除或存檔，這些是 tutorial copy，放在 GitHub 上是扣分的
- `tryout_chatgpt` → 刪除，2023 年的過期 code
- `littlehome_account` → 與技術無關，保持私有
- `linkedin_proj` → 保持私有，不公開（含 API key 風險）

### 1.2 補齊 GenAI 實戰（和 Warmup Plan 同步）

你已經有 Warmup Plan，但要加速。你不是從零開始 — 你有 RAG 經驗、有 ML system design 底子。

**前 4 週集中在：**
1. 把 `local-rag-llama-demo` 升級成 Gemini API 版 + 加 eval（你已經會 LangChain + ChromaDB）
2. 用 LangGraph 建 Scientific Paper Agent 的 MVP（不用完美，有 working demo 就好）
3. 把 Agent 的設計決策寫成一篇文章（這篇文章的價值 > 10 小時的 coding）

**後 4 週集中在：**
1. QLoRA 微調一次（Colab 上做，不要用 Mac）
2. 建 eval benchmark + 跑 A/B 比較
3. 把結果寫成第二篇文章

---

## Phase 2：讓對的人看到你（Month 2–5）

### 2.1 技術文章策略

> **你寫一篇有深度的技術文章，效果 = 投 50 封履歷。**
> Headhunter 搜 LinkedIn 找人是用關鍵字的。你的文章就是 SEO。

**不要寫「入門教學」。** 你的目標讀者是 hiring manager 和 Staff engineer，不是初學者。

**5 篇文章計畫（3 個月內完成）：**

**文章 1：「推薦系統 × LLM：我如何用 Agent 重新設計 reranking pipeline」**
- 結合你的 ML system design 知識 + GenAI 新技能
- 用你真實的推薦系統設計筆記當素材
- 加入 LLM reranking 的實驗數據
- 這篇直接打到推薦系統同儕的領域，展示你有 cross-domain 視野

**文章 2：「從 Claude Code 洩漏學到的 7 個生產級 Agent 設計模式」**
- 你已經有完整的分析文件，改寫成公開文章
- 加入你在 Scientific Paper Agent 中的實際應用
- 這題材有話題性（Claude Code 洩漏），自帶流量

**文章 3：「RAG 不是萬能的：我在科學論文抽取中的 A/B 測試數據」**
- 基於你的 RAG 升級實驗
- 用數據說話：naive RAG vs advanced RAG vs fine-tuning vs long context
- 有 eval 數據的文章遠比理論分析有價值

**文章 4：「設計一個 Multi-Agent 科學論文分析系統：架構、記憶、壓縮」**
- 展示系統設計能力（Staff 面試核心）
- 引用 Claude Code 三層記憶 + 你的實作
- 畫出完整架構圖 + 設計決策

**文章 5：「算法工程師的 GenAI 轉型：我做對和做錯的事」**
- 個人經驗分享，容易引起共鳴
- 展示學習能力和自我反思（Staff behavioral 加分）
- 這種文章在 LinkedIn 上的互動率最高

**發佈平台優先順序：**
1. **LinkedIn 文章** — 你的 target hiring manager 都在這裡，直接觸達
2. **Medium（英文）** — 國際可見度，Google 搜尋排名好
3. **知乎 / vocus（中文）** — 中文圈影響力

### 2.2 LinkedIn 經營

你現在的 LinkedIn 大概只有基本資料。這要變成你的「店面」。

**Profile 改造：**

```
Headline（最重要的一行）：
❌ "Algorithm Engineer at [Company]"
✅ "AI/ML Engineer | Building Agentic AI Systems | RAG + LLM Fine-tuning + Multi-modal"

About（前 3 行決定別人是否往下看）：
「I design and build production AI agent systems that extract structured data
from complex multi-modal sources. Currently focused on scientific document
intelligence — combining LLM reasoning, RAG retrieval, and multi-modal
understanding to automate what used to take researchers hours.

Previously worked on [你之前做過的 ML 系統，用商業語言描述 impact]...」
```

**每週動作：**
- 週一或週三發一則短 post（3-5 句 + 一個洞察），例如：
  - 你在建 Agent 過程中學到的一個 trade-off
  - 一個 RAG 的 debugging 經驗
  - 對 AI 產業趨勢的看法
- 每月發一篇長文（上面 5 篇之一）
- 主動在別人的 GenAI 相關 post 下留有深度的 comment（比自己發 post 更快建人脈）

### 2.3 建立人脈

**不是「加好友」，是讓特定的人知道你在做什麼。**

**你需要認識的 5 種人：**

| 角色 | 為什麼 | 怎麼接觸 |
|------|--------|----------|
| **Target 公司的 AI/ML hiring manager** | 他們決定你的 level 和 offer | LinkedIn 搜 "AI ML hiring manager Singapore"，看到他們的 post 就留 comment，3-5 次互動後再私訊 |
| **Target 公司的 Staff/Principal engineer** | 他們是你面試的 bar raiser + 內推來源 | 同上，或去他們的 tech talk / meetup 後直接對話 |
| **AI 領域的 headhunter（新加坡）** | 他們有你看不到的職位 + 薪資情報 | 直接 LinkedIn 私訊：「Hi, I'm a senior ML engineer exploring staff-level AI/ML roles in SG. Would love to connect.」 |
| **你的同儕（那些拿 300-400K 的）** | 他們知道怎麼進去的、面試考什麼、誰在 hire | 直接問。大部分人願意分享，尤其你們本來就認識 |
| **AI Singapore / IMDA 社群的人** | 本地 AI 生態的 connector | 參加 AI Singapore 的 meetup 或 workshop |

**具體 networking 動作（每週 2-3 小時）：**

Month 2-3：
- [ ] 找到 5 個 target 公司的 AI/ML 人，開始在他們 post 下互動
- [ ] 聯繫 3 個 headhunter，告訴他們你的 target level 和 TC
- [ ] 找你拿 300-400K 的同儕聊一次（問：你面試準備了什麼？你覺得什麼最關鍵？）
- [ ] 參加 1 次 AI Singapore 或 PyCon SG 的 meetup

Month 4-5：
- [ ] 從 headhunter 拿到 2-3 個 target 公司的 JD + 面試流程
- [ ] 透過人脈拿到 1-2 個 internal referral
- [ ] 在 meetup 做一次 5-10 分鐘的 lightning talk（就講你的 Agent 專案）
- [ ] 你的 LinkedIn post 應該開始有 hiring manager 主動 connect 你了

**Lightning talk 比正式演講好開始。** 大部分 meetup 都接受 5 分鐘的分享，門檻低、準備少、效果好。內容就講：「我如何用 Claude Code 洩漏的設計模式建了一個科學論文 Agent」— 這個題目有話題性，會被記住。

---

## Phase 3：拿 Offer + 談判（Month 5–8）

### 3.1 面試準備

你已經有 ML system design 的 21 個 case study 和 38+ LeetCode 題。不需要從零開始。

**你要補的是 GenAI 相關的面試題：**

| 題目 | 準備素材 |
|------|----------|
| 「設計一個 RAG 系統」 | 你的 local-rag-llama-demo + 升級版 |
| 「設計一個 AI Agent 平台」 | 你的 Scientific Paper Agent + Claude Code 架構分析 |
| 「RAG vs fine-tuning vs long context，怎麼選？」 | 你的 A/B eval 數據 |
| 「怎麼評估 LLM 輸出品質？」 | 你的 eval benchmark |
| 「描述一個你從零到一設計的系統」 | Scientific Paper Agent 的完整故事 |

**傳統 ML system design 你已有基礎，要做的是加上 GenAI 觀點：**
- 推薦系統的 reranking → 加入 LLM reasoning reranking
- 搜尋系統 → 加入 semantic search + RAG
- 內容理解 → 加入 multi-modal LLM

這個「傳統 ML + GenAI 結合」的角度，是你在面試中的差異化武器。純做推薦的人不懂 Agent，純做 Agent 的人不懂推薦系統的 infra。你兩邊都懂。

### 3.2 Offer 策略

- 同時面 3-5 家，控制 timeline 讓 offer 時間重疊
- 有 competing offer 才有談判籌碼
- 談判時重點爭 **level**（Staff vs Senior），不只是 TC 數字。Staff 的年度 refresher stock 在第 2-3 年帶來的收入遠超 sign-on bonus

---

## Phase 4：長期護城河（Month 9–12）

到這個階段你應該已經拿到 300K+ 的 offer 了。接下來是確保你 **留在這個 level 而不是曇花一現**。

- 每月 1 篇技術文章（持續）
- 每季 1 次 meetup/conference 分享
- 在新公司的前 90 天找到一個高可見度的 GenAI 項目
- 開始 mentor 1-2 個 junior（這是 Staff level 的 multiplier 行為）

---

## 時間線

```
Month 1-2：重組武器庫
  ├── 整併 GitHub（3 個公開 repo + 清理垃圾）
  ├── 完成 Scientific Paper Agent MVP
  ├── 發佈第 1 篇文章
  └── LinkedIn profile 改造

Month 2-5：讓對的人看到你
  ├── 累計 3-5 篇技術文章
  ├── 建立 5-10 個 target 人脈
  ├── 聯繫 headhunter + 拿到 JD
  ├── 做 1 次 lightning talk
  └── 拿到 1-2 個 internal referral

Month 5-8：面試 + 拿 offer
  ├── 面 3-5 家 target 公司
  ├── 拿到 2-3 個 competing offer
  ├── 談判到 300K+ TC
  └── Accept offer 或用 offer 談 counter

Month 9-12：鞏固
  ├── 新角色前 90 天建立影響力
  ├── 持續發文 + networking
  └── 為下一次跳槽（400K+）鋪路
```

---

## 本週就能做的 3 件事

1. **把 `DL_tensorflow_learning`、`tensorflow_offline_prac`、`tryout_chatgpt` 設為 private 或 archive** — 這些放在公開 GitHub 上是扣分的
2. **改 LinkedIn headline** — 花 5 分鐘，把 "Algorithm Engineer" 改成包含 AI Agent / RAG / LLM 的版本
3. **約你拿 300-400K 的同儕喝一杯** — 問三個問題：你面試準備了什麼？你覺得什麼最讓面試官印象深刻？你的 headhunter 是誰？
