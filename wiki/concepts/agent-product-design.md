---
title: Agent Product Design
tags: [agent, product-design, human-in-the-loop, ux, trust]
sources:
  - title: "Building Effective Agents — Anthropic"
    url: https://www.anthropic.com/research/building-effective-agents
  - title: "How Agents Can Improve LLM Performance — Andrew Ng"
    url: https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/
  - title: "Building AI Agents — Chip Huyen"
    url: https://huyenchip.com/2025/01/07/agents.html
  - title: "What is a Cognitive Architecture — Harrison Chase (LangChain)"
    url: https://blog.langchain.com/what-is-a-cognitive-architecture/
  - title: "AutoGen: Enabling Next-Gen LLM Applications — Microsoft Research"
    url: https://arxiv.org/abs/2308.08155
  - title: "Agent Harness as Operating System — Phil Schmid (Hugging Face)"
    url: https://www.philschmid.de/agent-harness-2026
  - title: "Google Cloud Agents Whitepaper"
    url: https://www.kaggle.com/whitepaper-agents
  - raw/articles/agent-product-case-studies.md
created: 2026-04-09
updated: 2026-04-09
---

# Agent Product Design

> **TL;DR**: Agent 產品的成敗不在 LLM 能力，而在 human-in-the-loop 的位置設計、信任的漸進建立、以及 harness 工程。這不是泛知識——Anthropic、Andrew Ng、Chip Huyen、Google 都從不同角度提出了同樣結論。

## Definition

Agent Product Design 是一套設計原則，指導如何將 autonomous AI agent 包裝成用戶可信賴、可控制、可持續使用的產品。它關注的不是 agent 的推理能力，而是 agent 與人類之間的互動介面和信任機制。

## Core Principles

### 1. Autonomy Spectrum（自主度光譜）

**來源：** Anthropic 的 Erik Schluntz & Barry Zhang 在 [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)（2024.12）中明確定義了從 **workflows**（"LLMs and tools orchestrated through predefined code paths"）到 **agents**（"LLMs dynamically direct their own processes and tool usage"）的光譜。這是目前最清晰的產業界自主度框架。

Harrison Chase（LangChain CEO）在 [What is a Cognitive Architecture](https://blog.langchain.com/what-is-a-cognitive-architecture/)（2024.07）中從框架設計角度補充：LLM 控制流的比例越高，系統越 "agentic"。

| 層級 | Anthropic 分類 | Agent 做什麼 | 人做什麼 | 代表產品 |
|------|---------------|-------------|---------|---------|
| L1 | Augmented LLM | 單步生成 + 工具 | 每步決策 | GitHub Copilot |
| L2 | Workflow（Prompt Chaining / Routing） | 按預定流程執行 | 設計流程 + 審核 | Perplexity Pro Search |
| L3 | Orchestrator-Workers | 動態規劃 + 分發子任務 | 關鍵節點審核 | Claude Code, Cursor Agent |
| L4 | Autonomous Agent | 自主閉環執行 | 例外處理 | Devin, Factory AI |

**Anthropic 的設計哲學：**
> *"Start simple; increase complexity only when demonstrable performance gains justify the added latency and cost."*

### 2. Trust is Earned, Not Assumed（信任漸進建立）

**來源：** Chip Huyen（Stanford 講師、O'Reilly《AI Engineering》作者）在 [Building AI Agents](https://huyenchip.com/2025/01/07/agents.html)（2025.01）中引用 Microsoft 的 **"Crawl-Walk-Run"** 漸進式框架，建議組織 *"clearly define the level of automation an agent can have for each action"*——信任是 per-action 漸進授予，而非全局開關。

Anthropic 的 [Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy)（2023.09）從安全角度提出 AI Safety Levels（ASL-1 → ASL-4+），本質也是相同邏輯：能力越強，safeguard 越嚴格，信任逐層累積。

**產品實踐：**
- Cursor 的演進：tab completion → multi-file edit → agent mode（L1 → L3 的漸進路徑）
- Claude 的 permission gating：allow → prompt → deny 三層權限，用戶可逐步放寬

### 3. Human-in-the-Loop Placement（人類介入點設計）

**來源：** Microsoft Research 的 AutoGen 團隊（Wu, Bansal, Zhang 等）在 [AutoGen paper](https://arxiv.org/abs/2308.08155)（COLM 2024）中將 HITL 實現為一等公民設計參數：`UserProxyAgent` 的 `human_input_mode` 可設為 `ALWAYS`、`TERMINATE`、`NEVER`。這是目前對 HITL 作為**可程式化產品設計決策**最明確的工程實現。

Anthropic 在 Building Effective Agents 中提出 agents 應有 **"human checkpoints"** 和 **"stopping conditions"**——pause-for-approval 的位置決定了產品的 risk/speed tradeoff。

Chip Huyen 建議 **decouple planning from execution**：人類在 plan 階段審核，execution 階段放手，這比每步確認更高效。

**設計決策框架：**

| 介入時機 | 適用場景 | 原因 |
|---------|---------|------|
| 高風險操作前 | 刪除、發佈、支付 | 不可逆操作需人類確認 |
| Agent 低信心時 | LLM 自評不確定的決策 | 避免幻覺造成的錯誤傳播 |
| Domain checkpoint | 法律 memo 簽核、實驗方案確認 | 領域合規要求 |
| Plan 完成後、執行前 | 複雜多步驟任務 | Chip Huyen 推薦的 plan/execute decouple |

### 4. Harness > Loop（基礎設施重於推理循環）

**來源：** Phil Schmid（Hugging Face Technical Lead）在 [Agent Harness](https://www.philschmid.de/agent-harness-2026)（2026.01）中提出經典類比：

> *Model = CPU, Context window = RAM, Agent harness = Operating System, Agent = Application*

他的核心論點：frameworks 提供 agentic loops；harnesses 提供 "prompt presets, opinionated handling for tool calls, lifecycle hooks, planning, filesystem access, sub-agent management"。

Swyx（Latent Space 創辦人）在 [IMPACT framework](https://www.latent.space/p/agent)（2025.03）中區分 **Model Labs**（靠更好的模型）和 **Agent Labs**（靠更好的 harness），指出 Agent Labs *"don't mind rewriting the harness every few months for the gains they bring"*。

**這與 Claude Code 的架構分析吻合**（見 [Agentic Harness](agentic-harness.md)）：核心 agent loop 只有幾十行，harness 有幾十萬行。

### 5. Agent-Computer Interface (ACI)

**來源：** Anthropic 在 Building Effective Agents 中提出 **ACI** 概念——tool design 應像 HCI（Human-Computer Interaction）一樣被認真對待：

> 設計 agent 工具時，要寫 thorough documentation、設計 clear schemas、提供 descriptive error messages。

Google Cloud 的 [Agents Whitepaper](https://www.kaggle.com/whitepaper-agents)（Wiesinger, Marlow & Vuskovic, 2024.09）從三層架構角度補充：
1. **Model layer** — LLM 本身
2. **Orchestration layer** — cognitive architecture（推理 + 規劃）
3. **Tools layer** — extensions, functions, data stores

### 6. Metrics That Matter

**來源：** METR（Model Evaluation & Threat Research，由 Beth Barnes 創辦，顧問含 Yoshua Bengio）提出 **"task-completion time horizon"** 指標——衡量 agent 在多長時間範圍的任務上能達到 50%/80% 可靠性。

結合產業實踐，agent 產品的核心 metrics：

| 指標 | 衡量什麼 | 來源 |
|------|---------|------|
| Task completion rate | agent 成功完成任務的比例 | SWE-bench (Princeton), METR |
| Human intervention rate | 需要人類介入的比例 | Chip Huyen: Crawl-Walk-Run |
| Time-to-value | 任務開始到交付的時間 | METR: task-completion time horizon |
| Cost per task | token / API 成本 | Anthropic: 複雜度必須 justified by performance gains |
| Task horizon at 50% reliability | 能自主處理多複雜的任務 | METR (Beth Barnes) |

## When to Use

設計任何面向用戶的 agent 產品時，都需要考慮這些原則。特別是：
- 從 demo/prototype 過渡到 production 時（Anthropic: "start simple"）
- 面對非技術用戶時（Chip Huyen: Crawl-Walk-Run）
- 在高風險 domain（法律、醫療、科學）中（AutoGen: programmable HITL modes）

## Backlinks

- [Agentic Harness](agentic-harness.md) — harness 是實現這些產品設計原則的工程基礎
- [Agent-Friendly Design](agent-friendly-design.md) — 從工具側看 agent 介面設計（對應 ACI 概念）
- [Agent Evaluation](agent-evaluation.md) — 量化產品設計是否成功
- [derived: Agent Product Case Studies](../derived/2026-04-09-agent-product-case-studies.md)
- [derived: Warmup Gap Analysis](../derived/2026-04-09-warmup-agent-knowledge-gap-analysis.md)

## Related Concepts

- [Agentic Harness](agentic-harness.md)
- [Agent-Friendly Design](agent-friendly-design.md)
- [Superapp Paradigm](superapp-paradigm.md)
- [Agent Evaluation](agent-evaluation.md)
- [Context Engineering](context-engineering.md)

## Sources

- [Building Effective Agents — Anthropic (Schluntz & Zhang, 2024.12)](https://www.anthropic.com/research/building-effective-agents) — 定義 workflow→agent 光譜、ACI 概念、"start simple" 原則
- [How Agents Can Improve LLM Performance — Andrew Ng (2024.03)](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/) — 四大 agentic design patterns（Reflection, Tool Use, Planning, Multi-Agent）
- [Building AI Agents — Chip Huyen (2025.01)](https://huyenchip.com/2025/01/07/agents.html) — Crawl-Walk-Run 漸進信任、plan/execute decouple
- [What is a Cognitive Architecture — Harrison Chase, LangChain (2024.07)](https://blog.langchain.com/what-is-a-cognitive-architecture/) — LLM 控制流比例定義 "agentic" 程度
- [AutoGen: Enabling Next-Gen LLM Applications — Microsoft Research (COLM 2024)](https://arxiv.org/abs/2308.08155) — HITL 作為可程式化設計參數
- [Agent Harness as Operating System — Phil Schmid, Hugging Face (2026.01)](https://www.philschmid.de/agent-harness-2026) — Model=CPU, Harness=OS 類比
- [IMPACT Framework — Swyx, Latent Space (2025.03)](https://www.latent.space/p/agent) — Model Labs vs Agent Labs 區分
- [Google Cloud Agents Whitepaper — Wiesinger, Marlow & Vuskovic (2024.09)](https://www.kaggle.com/whitepaper-agents) — 三層架構（Model / Orchestration / Tools）
- [Anthropic Responsible Scaling Policy (2023.09)](https://www.anthropic.com/responsible-scaling-policy) — AI Safety Levels 漸進信任框架
- [METR — Model Evaluation & Threat Research](https://metr.org/) — task-completion time horizon 指標
