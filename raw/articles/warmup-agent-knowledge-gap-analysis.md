# Warmup Repo × Knowledge Base 交叉分析：Agent 產品認知缺口

## 背景

areomoon 即將加入 Patsnap 擔任 Algorithm Expert，核心工作是材料科學 AI Agent。與未來主管 huwei 對話後，發現自身對 **AI agent 在產業界的產品應用** 認知不足，仍停留在傳統 API / 對用戶型服務的功能開發思維。

本文交叉比對 `areomoon_agent_warmup` repo（技術 warmup）和 `llm_knowledge_base` wiki（概念知識庫），找出需要補齊的認知缺口。

---

## Warmup Repo 現有模組 vs 產品認知需求

### ✅ 已覆蓋（技術層面紮實）

| Warmup 模組 | Wiki 概念 | 覆蓋程度 |
|-------------|-----------|---------|
| 01_prompt_engineering | — | 技術完整，但缺少「產品中如何管理 prompt 版本」的觀點 |
| 02_rag_fundamentals | context-engineering.md | 技術完整，但缺少「RAG 在生產環境的 failure mode」分析 |
| 03_agent_patterns | agentic-harness.md, ace-framework.md | 有 Generator-Reflector + LangGraph，但偏學術範例 |
| 04_ace_framework | ace-framework.md, ace-for-materials.md | 理論完整 |
| 05_material_science_agents | material-science-agents.md | MARS + LLMatDesign 架構已研究 |
| 06_finetuning | — | 技術流程完整 |
| 07_multimodal | — | 基礎覆蓋 |

### ❌ 缺口一：Agent 產品設計思維

**問題：** warmup repo 的練習全是「技術實作」，沒有任何模組教你思考：
- 這個 agent 的用戶是誰？科學家？專利律師？研發主管？
- Human-in-the-loop 放在哪個環節？
- Agent 出錯時的 UX fallback 是什麼？
- 如何用 metrics 證明 agent 比人工更好？

**補齊方式：**
- 新增 wiki concept：`agent-product-design.md`（agent 產品設計原則）
- 在 warmup 03_agent_patterns 加入一個「產品設計 checklist」練習
- 研究 Harvey AI 的法律 agent 如何設計 human-in-the-loop

### ❌ 缺口二：Production Agent Engineering

**問題：** warmup repo 的代碼都是 happy path demo，缺少：
- Error handling & retry strategy
- Context window management（長對話怎麼壓縮）
- Permission gating（agent 什麼時候該暫停問人）
- Observability（怎麼 debug 一個 20 步的 agent trace）
- Cost management（每次 agent run 花多少錢、怎麼控制）

**補齊方式：**
- wiki 已有 `agentic-harness.md` 12 個 pattern，但 warmup repo 沒有對應練習
- 建議在 warmup 03 新增 `production_patterns.py`：實作 context compression + permission gating
- 追蹤 LangSmith / Langfuse 等 agent observability 工具

### ❌ 缺口三：Agent Evaluation（最關鍵）

**問題：** warmup 06_finetuning 有 eval 概念，但只針對模型微調。Agent-level evaluation 完全空白：
- 怎麼 eval 一個 multi-step agent 的「任務完成率」？
- 怎麼 eval agent 的「效率」（步數、cost、time）？
- 怎麼 eval agent 的「安全性」（有沒有做危險操作）？
- 怎麼建 regression test 確保 agent 不會退步？

**補齊方式：**
- 新增 wiki concept：`agent-evaluation.md`
- 研究 MADE benchmark（材料科學 agent eval）、SWE-bench（coding agent eval）
- 在 warmup 新增 `08_evaluation/` 模組（README 已提到這是缺口）

### ❌ 缺口四：Agent 產業生態認知

**問題：** 你知道 LangGraph 和 CrewAI，但不清楚：
- 哪些公司在用 agent 做產品？解決什麼業務問題？
- Agent infra 層有哪些玩家？（LangSmith、Langfuse、Braintrust、Humanloop）
- MCP 生態現在發展到什麼程度？誰在用？
- Agent 產品的商業模式是什麼？按 seat？按 run？按 outcome？

**補齊方式：**
- 新增 raw article：`agent-product-case-studies.md`（已建立）
- 新增 wiki concept：`agent-infra-landscape.md`
- 追蹤 a16z AI agent landscape report

### ❌ 缺口五：與主管 / stakeholder 的溝通框架

**問題：** 技術能力 ≠ 專業度感知。在 huwei 哥和同事面前，需要：
- 用 **產品語言** 而非 **技術語言** 討論 agent（「這能減少科學家 X 小時的工作」而非「這用了 ReAct pattern」）
- 能做 **trade-off 分析**（「用 RAG 夠了還是需要 fine-tune？成本差 Y 倍，準確率差 Z%」）
- 能提出 **evaluation 方案**（「我建議先建 50 筆 ground truth，跑 baseline，再決定投資方向」）
- 能講出 **業界對標**（「Harvey AI 在法律領域用類似方法，他們的 pipeline 是...」）

**補齊方式：** 不需要新模組，需要練習「技術翻譯」— 把每個 warmup 練習的結果用一句話解釋給非技術人員

---

## 優先級排序

| 優先級 | 缺口 | 行動 | 預估時間 |
|--------|------|------|---------|
| P0 | Agent 產品案例認知 | 讀 agent-product-case-studies.md，深入研究 2-3 個案例 | 4hr |
| P0 | 溝通框架 | 準備 3 個「技術 → 產品語言」的翻譯範例 | 2hr |
| P1 | Agent Evaluation | 研究 MADE + SWE-bench，寫 agent-evaluation.md concept | 4hr |
| P1 | Production Patterns | 在 warmup 03 實作 context compression + permission gating | 6hr |
| P2 | Agent Infra 生態 | 調研 LangSmith/Langfuse/Braintrust，寫 agent-infra-landscape.md | 3hr |
| P2 | 產品設計思維 | Harvey AI / Patsnap 類比分析 | 3hr |

---

## Warmup Repo 建議新增模組

```
areomoon_agent_warmup/
├── ... (existing modules)
├── 08_evaluation/              # Agent-level evaluation
│   ├── task_completion_eval.py  # Multi-step task completion rate
│   ├── cost_efficiency_eval.py  # Token cost / step count tracking
│   └── notebook/
│       └── eval_lab.ipynb
└── 09_production_patterns/     # Production agent engineering
    ├── context_compression.py   # Implement tiered compression
    ├── permission_gating.py     # 3-tier permission model
    ├── observability.py         # LangSmith / Langfuse integration
    └── notebook/
        └── production_lab.ipynb
```

---

## 關鍵心態轉變

```
舊思維：我是 ML 工程師，我的工作是訓練/部署模型
    ↓
新思維：我是 AI Agent 系統工程師，我的工作是設計「LLM + Harness + Tools + Evaluation」
        的完整系統，讓 domain expert（科學家）能信任並依賴這個系統
```

這個轉變不是技術問題，是 **identity 問題**。你已經有技術基礎，缺的是「用系統思維看 agent 產品」的視角。
