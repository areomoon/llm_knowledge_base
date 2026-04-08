# AI Agent 產品案例研究：從 API Wrapper 到 Autonomous Agent

## 為什麼需要研究產品案例

大多數 ML 工程師對 agent 的認知停留在「LLM + function calling」，但產業界真正在賺錢的 agent 產品，其核心競爭力不在模型本身，而在 **harness 工程**（context management、tool orchestration、permission gating、evaluation loop）和 **產品設計**（human-in-the-loop 的位置、信任建立、error recovery UX）。

以下案例按「agent 自主程度」由低到高排列，幫助建立從 copilot → autonomous agent 的完整光譜認知。

---

## Tier 1：Copilot 型（人類主導，agent 輔助）

### GitHub Copilot / Cursor

**產品定位：** IDE 內嵌的 coding assistant
**Agent Loop：** 用戶觸發 → LLM 生成建議 → 用戶 accept/reject
**關鍵設計：**
- Tab completion 的低摩擦 UX 是成功關鍵，不是模型能力
- Cursor 加入 multi-file edit + codebase indexing，從「行級補全」升級為「任務級理解」
- Agent mode (Cursor) 引入 plan → edit → terminal → review loop
**產業啟示：** 最成功的 agent 產品往往從 copilot 起步，逐步提升自主度

### Perplexity

**產品定位：** AI-native search engine
**Agent Loop：** Query → 多輪 web search → 綜合生成 → 附 citation
**關鍵設計：**
- Multi-step retrieval：一個問題可能觸發 3-5 輪搜索，每輪根據前一輪結果調整 query
- Citation-first UX：每句話都標注來源，解決 LLM 幻覺的信任問題
- Pro Search 模式加入 clarifying questions，讓用戶在 loop 中提供 intent refinement
**產業啟示：** Agent 不一定需要調用「工具」，search + synthesis 本身就是一個強大的 agentic pattern

---

## Tier 2：Semi-Autonomous 型（agent 規劃，人類審核）

### Claude Code / Anthropic Claude with Computer Use

**產品定位：** Terminal-native coding agent + 通用 computer agent
**Agent Loop：** 理解任務 → 規劃步驟 → 執行工具呼叫 → 觀察結果 → 自我修正 → 人類審核關鍵決策
**關鍵設計：**
- Agentic Harness 是核心（參見 wiki/concepts/agentic-harness.md）：
  - 3 層 memory（always-loaded index → on-demand files → session transcript）
  - 3 層 permission gating（allow / prompt / deny）
  - Context compression（MicroCompact → AutoCompact → Full Reset）
- Plan → Work → Review cycle（Pattern 6）確保輸出品質
- Progressive tool discovery：不一次暴露所有工具，降低 LLM 選擇錯誤率
**產業啟示：** Production agent 的 90% 工程量在 harness，不在 LLM reasoning loop

### Devin / Factory AI / Cosine Genie

**產品定位：** Autonomous software engineer
**Agent Loop：** 接收 issue → 分析 codebase → 規劃修改 → 寫代碼 → 跑測試 → 提交 PR → 等待 review
**關鍵設計：**
- Sandboxed environment：agent 在隔離的 VM 裡跑，可以自由 install packages、run tests
- Long-horizon planning：一個任務可能跨越數十個步驟，需要 persistent memory
- Self-healing：測試失敗後自動分析 error → 修改 → 重試，不需要人工介入
- Human-in-the-loop 在 PR review 環節，不在 coding 環節
**產業啟示：** Autonomous agent 需要的不只是好 LLM，更需要 sandboxed execution、persistent state、self-correction loop

### Replit Agent

**產品定位：** 從自然語言到部署的 full-stack agent
**Agent Loop：** 描述需求 → 生成代碼 → 部署 → 用戶測試 → 迭代修改
**關鍵設計：**
- 與 Devin 不同，Replit Agent 面向「非工程師」用戶
- 重點在 deployment pipeline 的自動化（build → deploy → preview URL），不只是 code generation
**產業啟示：** Agent 的用戶不一定是技術人員，UX 設計需要考慮非技術用戶的信任建立

---

## Tier 3：Domain-Specific Autonomous Agent

### Harvey AI / Casetext (Thomson Reuters)

**產品定位：** Legal AI agent，律師的研究助手
**Agent Loop：** 法律問題 → 搜索案例法 → 分析 precedent → 生成 memo → 律師審核
**關鍵設計：**
- Domain-specific RAG：法律文獻的 chunking 需要尊重法條結構（section、subsection、clause）
- Citation accuracy 是生死線：法律場景不容許幻覺，每個 claim 必須可溯源
- Workflow integration：嵌入律師已有的工作流（文件管理、案件系統），不是獨立產品
**與 Patsnap 的關聯：** 專利搜索的結構化需求、citation 要求、domain expertise 需求都極為相似

### ChemCrow / Coscientist

**產品定位：** Chemistry research agent，能自主設計實驗
**Agent Loop：** 研究問題 → 搜索文獻 → 設計實驗步驟 → 呼叫計算工具 → 分析結果 → 建議下一步
**關鍵設計：**
- Tool integration 是核心：連接 PubChem、RDKit、計算化學引擎
- Safety guardrails：化學實驗有安全風險，agent 必須有 safety check 機制
- Multi-step reasoning：合成路線規劃需要深度 chain-of-thought
**與 Patsnap 的關聯：** 材料科學 agent 的直接參考，特別是實驗數據抽取和 multi-modal 處理

### MARS (Multi-Agent Research System for Materials Science)

**產品定位：** 19-agent 系統，覆蓋材料科學研究全流程
**Agent Loop：** 研究問題 → 文獻搜索 agent → 數據抽取 agent → 分析 agent → 報告生成 agent
**關鍵設計：**
- Orchestrator + Specialist 架構：每個 agent 專注一個子任務
- Shared memory pool：agents 之間通過共享 memory 傳遞中間結果
- Evaluation benchmark (MADE)：標準化的材料科學 agent 評估基準
**與 Patsnap 的關聯：** 你的目標角色（Algorithm Expert）很可能參與類似系統的建設

---

## Tier 4：Platform / Superapp 型

### OpenAI Superapp (ChatGPT + Codex + Atlas)

**產品定位：** 統一 AI 入口，整合對話、代碼、瀏覽
**關鍵設計：** 參見 wiki/concepts/superapp-paradigm.md
- Persistent agent with shared memory across tools
- Agent-callable tool interface (MCP-like)
- 從「用戶開 N 個 app」到「用戶在一個 app 裡用 agent 呼叫 N 個服務」

### Anthropic Claude (Chat + Code + Cowork)

**產品定位：** 同上，但強調 computer use 和 agentic coding
**關鍵設計：**
- MCP 作為 universal tool protocol
- Tiered memory architecture
- Progressive autonomy：從 copilot 到 autonomous 的漸進式信任

---

## 跨案例的共通 Pattern

### 1. Agent Loop 不是重點，Harness 才是
所有成功的 agent 產品，核心 loop 都是 `while(task_not_done) { reason → act → observe }`。差異化在 harness。

### 2. Human-in-the-loop 的位置是產品決策
- Copilot：每一步都需要人類確認
- Semi-autonomous：關鍵節點人類審核（PR review、法律 memo 簽核）
- Autonomous：只在失敗或高風險時升級給人類

### 3. Trust 是漸進建立的
沒有產品一開始就是 fully autonomous。都從 copilot 起步，逐步提升自主度。

### 4. Domain-specific > General-purpose
在特定領域做到 90% 準確率，比在通用場景做到 70% 準確率更有商業價值。

### 5. Evaluation 是最被低估的投資
沒有好的 eval，就無法證明 agent 真的在改善。Harvey AI 的法律 benchmark、MARS 的 MADE benchmark 都是產品護城河。

---

## 你（areomoon）的行動項目

1. **立即**：深讀 Claude Code 的 harness 設計（你的 wiki 已有），能在對話中引用具體 pattern
2. **本週**：研究 Harvey AI 的產品設計，與 Patsnap 專利場景做類比筆記
3. **入職前**：在 warmup repo 的 03_agent_patterns 或 05_material_science_agents 中實作一個 mini agent，包含 plan→work→review cycle + permission gating
4. **入職後**：主動提議建立 evaluation benchmark（MADE-style），這是最能展現專業度的切入點

---

## 參考資源

- [Lilian Weng: LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
- [Andrew Ng: Agentic Design Patterns](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/)
- [The Landscape of Emerging AI Agent Architectures (arXiv 2404.11584)](https://arxiv.org/abs/2404.11584)
- [ChemCrow: Augmenting LLMs with Chemistry Tools (arXiv 2304.05376)](https://arxiv.org/abs/2304.05376)
- [Coscientist: Autonomous Chemical Research (Nature 2023)](https://www.nature.com/articles/s41586-023-06792-0)
- [MARS: Multi-Agent Research System (arXiv 2602.00169)](https://arxiv.org/abs/2602.00169)
- [MADE Benchmark (arXiv 2601.20996)](https://arxiv.org/abs/2601.20996)
- [12 Agentic Harness Patterns from Claude Code](https://generativeprogrammer.com/p/12-agentic-harness-patterns-from)
- [Harvey AI Blog](https://www.harvey.ai/blog)
- [Devin Technical Report](https://www.cognition.ai/blog/introducing-devin)
