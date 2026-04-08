# Claude Code 源碼洩漏事件：Agent 架構設計啟示

> **事件背景：** 2026 年 3 月 31 日，Anthropic 在發布 `@anthropic-ai/claude-code` v2.1.88 時，
> 意外將 59.8 MB 的 source map 檔案（`cli.js.map`）包含在 npm 套件中。
> 短短數小時內，約 **512,000 行 TypeScript** 原始碼被完整還原並公開分析。
> 原因：Bun 建構工具預設產生 source map，團隊未在 `.npmignore` 中排除 `*.map` 檔案。

**本文目的：** 從洩漏的架構設計中萃取可學習的 Agent 設計模式，結合我們的 Scientific Paper Agent 專案需求進行反饋。

---

## 一、Claude Code 整體架構概覽

### 1.1 規模與結構

| 目錄 | 行數 | 職責 |
|------|------|------|
| `utils/` | ~180K 行 | 權限系統、bash 安全檢查、模型管理、session 存儲等核心邏輯 |
| `components/` | ~81K 行 | 140+ 個 Ink 終端 UI 組件（React 渲染） |
| `services/` | ~53K 行 | 外部服務封裝：Anthropic API、MCP 客戶端、OAuth、上下文壓縮、記憶提取 |
| `tools/` | ~50K 行 | 40+ 個 Agent 工具實作 |
| Query Engine | ~46K 行 | 核心推理引擎 |
| Base Tool Def | ~29K 行 | 工具基礎定義 |

**關鍵發現：** 512,000 行程式碼中，真正的「Agent 邏輯」（agentic loop）極為簡潔 — 本質上是一個 **while-loop over tool calls**。複雜度全部在 **harness（外殼/框架）** 裡：上下文管理、權限系統、工具 schema、錯誤恢復、記憶、壓縮。

### 1.2 核心設計哲學

```
Agent = 簡單的推理迴圈
Harness = 讓 Agent 在生產環境穩定運作的一切
```

> **啟示：** 建構 Agent 的真正挑戰不是 LLM 呼叫本身，而是圍繞它的工程基礎設施。

---

## 二、12 個 Agentic Harness 設計模式

洩漏的原始碼揭示了 4 大類、12 個核心設計模式：

### 2.1 Memory & Context（記憶與上下文）

#### Pattern 1：Tiered Memory（分層記憶）

Claude Code 採用**三層記憶架構**，放棄傳統「全部存起來再檢索」的做法：

| 層級 | 機制 | 載入策略 | 類比 |
|------|------|----------|------|
| **L1：MEMORY.md** | 輕量索引檔（每行 ~150 字元，上限 200 行） | **永遠載入** context | 大腦的工作記憶 |
| **L2：Topic Files** | 按主題分的詳細記憶檔案 | **按需載入**（任務匹配時） | 書架上的筆記本 |
| **L3：Session Transcripts** | 完整對話歷史，存在磁碟 | **搜尋時才讀取** | 圖書館檔案室 |

**Self-Healing Memory：** 系統將自己的記憶視為「不可靠的」— 每次使用記憶前都會驗證其是否仍然正確（例如檢查檔案是否存在、函式是否還在），過時記憶會被自動更新或刪除。

```
📌 對我們專案的啟示：
Scientific Paper Agent 需要處理大量論文資料，應採用類似的分層策略：
- L1：當前任務的論文摘要 + 已抽取的關鍵參數（始終在 context 中）
- L2：每篇論文的詳細抽取結果（按需載入）
- L3：歷史論文的完整抽取記錄（存入 Vector DB，搜尋時才檢索）
```

#### Pattern 2：Scoped Rules（作用域規則）

`CLAUDE.md` 按目錄層級載入規則，每個子目錄可以有自己的規則檔，子目錄規則覆蓋父目錄。

```
📌 對我們專案的啟示：
不同科學領域（化學、生物、物理）的論文抽取規則不同。
可以按領域建立 scoped config，而非一套通用規則。
```

#### Pattern 3：Context Compression（上下文壓縮）

三階段壓縮策略，確保長時間運作不會爆 context window：

| 階段 | 名稱 | 觸發條件 | 機制 |
|------|------|----------|------|
| 1 | **MicroCompact** | 持續進行 | 本地裁剪舊的 tool output，零 API 呼叫 |
| 2 | **AutoCompact** | 接近 context window 上限 | 保留 13,000 token buffer，生成最多 20,000 token 的結構化摘要 |
| 3 | **Full Reset** | 極端情況 | 完全重建 context，僅保留記憶索引和當前任務 |

```
📌 對我們專案的啟示：
處理 10-50 頁的科學論文時，不可能全部塞入 context。
應實作類似的漸進式壓縮：先嘗試全文 → 超過限制時自動切換到摘要模式 → 最終 fallback 到 RAG。
```

### 2.2 Workflow & Orchestration（工作流與編排）

#### Pattern 4：Parallel Fan-Out（平行展開）

當任務可分解為**互不依賴**的子任務時，平行執行多個 Agent。

**權衡點：** 平行分支觸碰重疊檔案時，合併衝突比循序執行更難處理。

```
📌 對我們專案的啟示：
論文分析可以平行化：
- Agent A：抽取實驗條件
- Agent B：解析圖表數據
- Agent C：分析引用關係
三者獨立作業，最後由 Orchestrator 合併結果。
```

#### Pattern 5：Mailbox Pattern（信箱模式）

Multi-agent 系統中，worker agent 執行高風險操作時不能自行批准。
它必須將請求送到 coordinator 的「信箱」等待批核，coordinator 評估後批准或拒絕。

```
📌 對我們專案的啟示：
當 Extractor Agent 對抽取結果不確定時（如數值異常），
不應直接輸出，而是送到 Analyzer Agent 的信箱進行二次確認。
這避免了錯誤數據直接進入最終報告。
```

#### Pattern 6：Plan → Work → Review Cycle

自律式開發循環：先規劃 → 執行 → 自我審查 → 修正。

```
📌 對我們專案的啟示：
論文抽取 pipeline 應加入 Review 步驟：
1. Plan：識別論文結構，決定抽取策略
2. Work：執行抽取
3. Review：用另一個 LLM call 檢查結果合理性（如溫度是否在物理範圍內）
4. Fix：修正不合理的抽取結果
```

### 2.3 Tools & Permissions（工具與權限）

#### Pattern 7：Progressive Tool Discovery（漸進式工具發現）

Claude Code 預設只暴露 **< 20 個工具**，其餘 40+ 個按需啟用。

> 同時暴露 60 個工具會造成「選擇問題」— 模型花更多時間決定用哪個，且更容易選錯。

```
📌 對我們專案的啟示：
Scientific Paper Agent 不需要一次載入所有工具。
- 初始：PDF reader + 基本文字抽取
- 偵測到表格時：啟用 table extraction tool
- 偵測到圖表時：啟用 multi-modal vision tool
- 需要跨論文比較時：啟用 compare engine
```

#### Pattern 8：Three-Tier Permission Gating（三層權限門控）

權限不是 UI 裝飾，而是**嵌入工具執行路徑**的強制檢查：

| 層級 | 行為 | 說明 |
|------|------|------|
| **Allow** | 直接執行 | 低風險操作（讀取檔案） |
| **Prompt** | 暫停並要求確認 | 中風險操作（修改檔案） |
| **Deny** | 完全阻止 | 高風險操作（刪除、網路存取） |

通過 `PermissionPolicy` 結構管理，支援 per-tool override 和 path-specific 沙箱。

```
📌 對我們專案的啟示：
科學論文 Agent 若連接外部 API（如 PubMed、CrossRef），
應實作權限門控：
- Allow：讀取本地已下載的論文
- Prompt：查詢外部 API（需確認費用/頻率限制）
- Deny：修改或刪除原始論文檔案
```

#### Pattern 9：Hook System（生命週期鉤子）

`PreToolUse` hook 在工具執行前攔截，類似「深度封包檢測」— 檢查的是原始工具輸入，而非最終結果。

```
PreToolUse → 檢查輸入合法性 → 執行工具 → PostToolUse → 檢查輸出
```

```
📌 對我們專案的啟示：
可以在 tool 執行前加入 validation hook：
- PreExtract：檢查 PDF 是否有效、是否為科學論文格式
- PostExtract：檢查抽取結果是否符合 schema（如 pH 值 0-14）
```

### 2.4 Automation & Infrastructure（自動化與基礎設施）

#### Pattern 10：MCP as Universal Tool Protocol

Claude Code 的工具架構**本身就是 MCP**：Agent 透過 `tools/list` 發現工具、`tools/call` 呼叫、接收結構化結果。

```
📌 對我們專案的啟示：
將論文處理工具統一用 MCP 協議封裝：
- PDF Parser MCP Server
- Table Extractor MCP Server
- Chart Analyzer MCP Server
- Vector DB MCP Server
這樣任何 Agent 框架（LangGraph / CrewAI / Claude Agent SDK）都能直接連接。
```

#### Pattern 11：Dynamic System Prompt Assembly（動態系統提示組裝）

系統提示不是靜態字串，而是**動態組裝**的：

```
System Prompt = [
    全域快取指令（所有用戶共享）  ← prompt cache 邊界
    ---
    CLAUDE.md 規則（專案特定）
    Git 狀態
    當前日期
    可用工具列表（條件式載入）
    記憶索引
]
```

約 50 個工具的描述根據條件判斷是否載入 prompt。快取邊界之前的內容全組織共享，之後的是 session-specific。

```
📌 對我們專案的啟示：
論文 Agent 的 system prompt 也應動態組裝：
- 基礎指令（永遠載入）
- 領域特定規則（根據論文領域動態載入）
- 當前已抽取的參數摘要（隨任務更新）
- 可用工具列表（根據論文內容動態啟用）
```

#### Pattern 12：Feature Flags（功能旗標）

44 個 feature flags 控制未上線功能。這些不是概念驗證，而是**已編譯的完整程式碼**，只是 flag 設為 `false`。

```
📌 對我們專案的啟示：
用 feature flags 管理實驗性功能：
- 新的抽取演算法
- 不同的 LLM provider（Gemini vs Claude vs GPT）
- 實驗性的 multi-modal pipeline
可以在不修改主程式碼的情況下切換。
```

---

## 三、系統安全設計啟示

### 3.1 Git 安全協議

Claude Code 對 git 操作有嚴格的安全規範：
- 永遠不執行破壞性操作（`--force`, `--hard`）除非明確要求
- 優先可逆操作
- 新建 commit 而非 amend（避免覆蓋歷史）
- 絕不跳過 hooks（`--no-verify`）

### 3.2 Bash 安全沙箱

Bash 工具雖然功能最強，但有多層防護：
- 指令白名單/黑名單
- 路徑限制（沙箱化）
- 危險操作需確認
- 輸出長度限制

### 3.3 信任邊界

```
用戶輸入（可信）
    ↓
System Prompt（可信）
    ↓
工具輸出（半可信 — 可能含 prompt injection）
    ↓
外部 API 回應（不可信）
```

```
📌 對我們專案的啟示：
論文抽取結果來自 LLM 解析（半可信），
外部 API（PubMed、CrossRef）回應也是不可信的。
必須在每個信任邊界加入 validation。
```

---

## 四、隱藏功能與未來方向

洩漏中發現的未上線功能，透露了 Agentic AI 的發展方向：

| 功能 | 說明 | 對 Agent 設計的啟示 |
|------|------|---------------------|
| **KAIROS** | 持續背景運行的 daemon，從「對話時運作」變為「持續自主代理」 | Agent 不再是一問一答，而是持續監控和主動行動 |
| **Proactive Mode** | AI 不需明確指令即可主動行動 | Agent 可以主動發現新論文、主動提醒實驗條件衝突 |
| **BUDDY** | AI 寵物系統（18 種物種） | 使用者體驗設計 — 讓 Agent 更有人性化互動 |

---

## 五、對 Scientific Paper Agent 專案的整體建議

### 5.1 建議採用的架構模式（優先順序）

| 優先度 | 模式 | 原因 |
|--------|------|------|
| **P0** | Tiered Memory | 論文數量會持續增長，必須分層管理 |
| **P0** | Context Compression | 長論文必須有壓縮策略 |
| **P0** | Permission Gating | 涉及外部 API 和檔案操作 |
| **P1** | Progressive Tool Discovery | 避免工具過多導致 LLM 選擇困難 |
| **P1** | Plan → Work → Review | 確保抽取結果可靠 |
| **P1** | MCP Tool Protocol | 工具標準化，方便擴展 |
| **P2** | Parallel Fan-Out | 加速多論文處理 |
| **P2** | Dynamic Prompt Assembly | 支援多領域論文 |
| **P2** | Feature Flags | 管理實驗性功能 |

### 5.2 建議的系統架構

```
┌──────────────────────────────────────────────────┐
│              Dynamic System Prompt               │
│  [基礎指令] + [領域規則] + [記憶索引] + [工具列表] │
├──────────────────────────────────────────────────┤
│                                                  │
│    ┌─────────── Agentic Loop ───────────┐        │
│    │  while (task not complete):        │        │
│    │    reason → select tool → execute  │        │
│    │    observe → compress if needed    │        │
│    └────────────────────────────────────┘        │
│                                                  │
├──────────┬──────────┬──────────┬─────────────────┤
│ Extractor│ Analyzer │ Advisor  │   Orchestrator  │
│  Agent   │  Agent   │ Agent    │  (LangGraph)    │
│          │          │          │                 │
│  ┌─────┐ │ ┌──────┐ │ ┌──────┐ │  ┌───────────┐  │
│  │Plan │ │ │Plan  │ │ │Plan  │ │  │ Mailbox   │  │
│  │Work │ │ │Work  │ │ │Work  │ │  │ Pattern   │  │
│  │Review│ │ │Review│ │ │Review│ │  │ (審核門控) │  │
│  └─────┘ │ └──────┘ │ └──────┘ │  └───────────┘  │
├──────────┴──────────┴──────────┴─────────────────┤
│            Permission Gating Layer               │
│     [Allow: 讀取] [Prompt: API] [Deny: 刪除]     │
├──────────────────────────────────────────────────┤
│              MCP Tool Servers                    │
│  ┌────────┐ ┌──────────┐ ┌────────┐ ┌─────────┐ │
│  │PDF     │ │Table     │ │Chart   │ │Vector   │ │
│  │Parser  │ │Extractor │ │Analyzer│ │DB       │ │
│  └────────┘ └──────────┘ └────────┘ └─────────┘ │
├──────────────────────────────────────────────────┤
│           Three-Layer Memory                     │
│  L1: 記憶索引（始終在 context）                    │
│  L2: 論文抽取結果（按需載入）                      │
│  L3: 歷史記錄（Vector DB 搜尋）                   │
└──────────────────────────────────────────────────┘
```

### 5.3 關鍵 Takeaways

1. **Agent 本身很簡單，Harness 才是核心** — 不要花太多時間在 Agent loop 上，把精力放在記憶管理、上下文壓縮、權限控制
2. **記憶要分層且自我修復** — 永遠不要信任快取的資訊，每次使用前驗證
3. **工具要按需載入** — 不要一次暴露所有工具給 LLM
4. **壓縮是長時間運作的關鍵** — 沒有壓縮策略的 Agent 很快就會爆 context window
5. **MCP 是工具標準化的未來** — 早點採用，後續擴展成本低
6. **權限不是事後補丁** — 從第一天就嵌入執行路徑
7. **Plan → Work → Review 是可靠性的基礎** — 單純的 ReAct loop 不夠，需要自我審查機制

---

## 參考資源

- [12 Agentic Harness Patterns from Claude Code](https://generativeprogrammer.com/p/12-agentic-harness-patterns-from) — 12 個設計模式完整解析
- [Claude Code Source Leak: 7 Agent Architecture Lessons](https://particula.tech/blog/claude-code-source-leak-agent-architecture-lessons) — 7 個架構啟示
- [Claude Code Source Leak: Three-Layer Memory Architecture](https://www.mindstudio.ai/blog/claude-code-source-leak-three-layer-memory-architecture) — 三層記憶架構詳解
- [Claude Code Architecture Deep Dive](https://wavespeed.ai/blog/posts/claude-code-architecture-leaked-source-deep-dive/) — 架構深度分析
- [Comprehensive Analysis of Claude Code Source Leak](https://www.sabrina.dev/p/claude-code-source-leak-analysis) — 綜合分析
- [What Claude Code's Leaked Architecture Reveals About Building Production MCP Servers](https://dev.to/shekharp1536/what-claude-codes-leaked-architecture-reveals-about-building-production-mcp-servers-2026-10on) — MCP Server 設計啟示
- [The Claude Code Leak: What the Harness Actually Looks Like](https://paddo.dev/blog/claude-code-leak-harness-exposed/) — Harness 架構拆解
- [Claude Code 源碼深度解析（知乎）](https://zhuanlan.zhihu.com/p/2022442135182406883) — 中文深度解析
- [Claude Code 原始碼外洩拆解](https://ai-coding.wiselychen.com/claude-code-source-leak-memory-architecture-lessons/) — 中文架構分析
- [VentureBeat: Claude Code's source code appears to have leaked](https://venturebeat.com/technology/claude-codes-source-code-appears-to-have-leaked-heres-what-we-know) — 事件報導
