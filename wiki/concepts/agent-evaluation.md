---
title: Agent Evaluation
tags: [agent, evaluation, benchmark, metrics, swe-bench, made, metr]
sources:
  - title: "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"
    url: https://arxiv.org/abs/2310.06770
  - title: "METR — Model Evaluation & Threat Research"
    url: https://metr.org/
  - title: "HELM: Holistic Evaluation of Language Models — Stanford CRFM"
    url: https://crfm.stanford.edu/helm/
  - title: "MADE Benchmark"
    url: https://arxiv.org/abs/2601.20996
  - title: "WebArena: A Realistic Web Environment for Building Autonomous Agents"
    url: https://arxiv.org/abs/2307.13854
  - title: "Building Effective Agents — Anthropic"
    url: https://www.anthropic.com/research/building-effective-agents
  - title: "Building AI Agents — Chip Huyen"
    url: https://huyenchip.com/2025/01/07/agents.html
created: 2026-04-09
updated: 2026-04-09
---

# Agent Evaluation

> **TL;DR**: Agent evaluation 不同於 model evaluation — 需要評估多步驟任務的完成率、效率、安全性和 cost，而非單一輸出品質。權威框架來自 Princeton NLP (SWE-bench)、METR (Beth Barnes)、Stanford CRFM (HELM)。

## Definition

Agent Evaluation 是衡量 autonomous AI agent 在真實任務場景中表現的方法論和基準體系。與傳統 LLM evaluation（衡量單次生成品質）不同，agent evaluation 必須考量多步驟推理的完整軌跡、工具使用的正確性、以及任務完成的端到端效果。

## Why It's Hard

1. **Non-deterministic paths**：同一任務可能有多條正確的解法路徑
2. **Intermediate steps matter**：最終結果正確但中間步驟危險/低效，仍然是問題
3. **Environment dependency**：agent 的表現取決於工具可用性、資料品質、context window
4. **Cost-accuracy trade-off**：Anthropic 在 [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) 中明確指出——*增加複雜度必須有 demonstrable performance gains 來 justify*

## Evaluation Dimensions

| 維度 | 衡量什麼 | 指標 | 權威來源 |
|------|---------|------|---------|
| **Correctness** | 任務是否正確完成 | Task completion rate, EM, F1 | SWE-bench (Princeton NLP) |
| **Efficiency** | 花了多少步驟/時間/成本 | Step count, Token usage, Time | METR: task-completion time horizon |
| **Safety** | 有沒有做危險操作 | Unsafe action rate | METR: autonomous capability assessment |
| **Robustness** | 面對 edge case 是否穩定 | Failure recovery rate | HELM 7-metric framework |
| **Holistic** | 多維度綜合評估 | 7 metrics across 16 scenarios | HELM (Stanford CRFM, Percy Liang) |

## Key Benchmarks & Their Authorities

### SWE-bench — Princeton NLP Group

**作者：** Carlos E. Jimenez, John Yang, Alexander Wettig, **Shunyu Yao**, Kexin Pei, Ofir Press, **Karthik Narasimhan**
**機構：** Princeton NLP Group
**發表：** ICLR 2024 Oral
**論文：** [arXiv 2310.06770](https://arxiv.org/abs/2310.06770) | [官網](https://www.swebench.com/)

- 2,294 real GitHub issues from 12 popular Python repos
- Agent 需要定位 bug → 理解 codebase → 寫 fix → 通過測試
- 當前 SOTA：~50% resolve rate（Devin-class agents）
- **為什麼重要：** Shunyu Yao 是 ReAct paper 的作者，SWE-bench 是他從理論到實踐的延伸。這是目前最接近真實軟體工程任務的 agent benchmark，也是 Devin、Claude Code、Cursor 等產品用來宣傳能力的標準。

### METR — Model Evaluation & Threat Research

**創辦人：** Beth Barnes (CEO)；顧問包含 **Yoshua Bengio**（圖靈獎得主）和 **Alec Radford**（GPT 系列核心作者）
**官網：** [metr.org](https://metr.org/) | [Evaluations](https://evaluations.metr.org/)

- 提出 **"task-completion time horizon"** 指標：衡量 agent 在「人類專家需要 X 時間才能完成的任務」上達到 50%/80% 可靠性
- 開源 eval runner：[Vivaria](https://github.com/METR/vivaria)
- **為什麼重要：** METR 是目前 agent 安全評估的最高權威，Anthropic、OpenAI 的 frontier model 評估都參考其框架。Beth Barnes 之前在 Anthropic 建立了第一代 evals 團隊。

### HELM — Stanford Center for Research on Foundation Models

**核心作者：** **Percy Liang**（Stanford CS 教授）、Rishi Bommasani、Tony Lee 等
**官網：** [crfm.stanford.edu/helm](https://crfm.stanford.edu/helm/) | [Paper](https://arxiv.org/abs/2211.09110)

- 7 個評估維度：accuracy, calibration, robustness, fairness, bias, toxicity, efficiency
- 16 core scenarios 的 living benchmark
- **為什麼重要：** 雖然更偏 LLM-general 而非 agent-specific，但 HELM 定義了「全面評估」的標準方法論。Percy Liang 也是 Stanford HAI 的核心成員。

### MADE — Materials Data Extraction Benchmark

**論文：** [arXiv 2601.20996](https://arxiv.org/abs/2601.20996)

- 材料科學論文的結構化數據抽取 benchmark
- 評估：實驗條件抽取、性質數值提取、單位轉換
- **與 Patsnap 的關聯：** 這是你入職後最直接的參考。主動提議建立類似 benchmark 是展現專業度的最佳切入點。

### WebArena — Carnegie Mellon

**論文：** [arXiv 2307.13854](https://arxiv.org/abs/2307.13854)

- Web browsing agent 的 benchmark
- Agent 需要在真實網站上完成任務（搜索、下單、填表）
- 評估 agent 的 UI 理解和多步驟操作能力

## Evaluation Framework

基於上述權威來源，agent evaluation 可分四個層級：

### Level 1: Unit Eval（單步驟）— HELM 風格
```
Input → Agent single action → Compare with expected output
```
- 適用：tool selection accuracy、single extraction accuracy
- 方法：Exact Match, F1, LLM-as-Judge
- 參考：HELM 的 per-scenario evaluation

### Level 2: Trajectory Eval（多步驟）— METR 風格
```
Task → Agent trajectory (N steps) → Evaluate path + outcome
```
- 適用：multi-step reasoning correctness、efficiency
- 方法：Step count analysis, Token cost tracking, Trajectory comparison
- 參考：METR 的 task-completion time horizon

### Level 3: End-to-End Eval（任務完成）— SWE-bench 風格
```
Task description → Agent full run → Binary: success/failure
```
- 適用：overall task completion rate
- 方法：Test suite pass rate, Human evaluation
- 參考：SWE-bench 的 "does the patch pass tests?" 判定

### Level 4: Regression Eval（持續監控）
```
Benchmark suite → Run on every agent update → Track metrics over time
```
- 適用：確保 agent 更新不退步
- 方法：CI/CD integrated benchmark runs
- 參考：METR 的 Vivaria 持續評估框架

## Practical Guide

### 建立你自己的 Eval Benchmark

Chip Huyen 在 [Building AI Agents](https://huyenchip.com/2025/01/07/agents.html) 中建議的漸進式方法：

1. **收集 50-100 個 ground truth cases**（不需要很多，但要有代表性）
2. **定義成功標準**（exact match? F1? human judgment?）
3. **跑 baseline**（pure LLM without agent loop — Andrew Ng 的 zero-shot baseline）
4. **跑 agent version** 並記錄：completion rate, step count, cost
5. **A/B compare** 並決定投資方向

Andrew Ng 的關鍵數據點：GPT-3.5 加上 agentic loop 在 HumanEval 上達到 95.1%，超越 GPT-4 zero-shot 的 67%。這證明了 **harness/workflow 的投資回報可能超過模型升級**。

### Agent Eval 的常見陷阱

- **只看最終結果，忽略路徑**：agent 碰巧得到正確答案但推理路徑錯誤（METR 關注 trajectory，不只 outcome）
- **測試集太小**：50 筆以下容易有統計噪音（HELM 的 approach 是 16 scenarios × 多個 metrics）
- **沒有 cost tracking**：Anthropic 明確警告——複雜度增加必須 justified（"demonstrable performance gains"）
- **沒有 regression test**：agent 更新後變好了一些場景，但破壞了另一些（需要 Vivaria-style 持續監控）

## When to Use

- 在決定「要不要 fine-tune」之前，先建好 eval benchmark（Andrew Ng: 先用 agentic loop 壓榨小模型，再考慮大模型/微調）
- 在向 stakeholder 展示 agent 價值時，用 metrics 而非 demo（METR 的 task-completion time horizon 是最好的溝通工具）
- 在 agent 更新/迭代時，用 regression eval 確保不退步
- 入職 Patsnap 後，主動提議建 MADE-style benchmark 是展現專業度的最佳切入點

## Backlinks

- [Agent Product Design](agent-product-design.md) — evaluation 是驗證產品設計的手段
- [Agentic Harness](agentic-harness.md) — harness 的 Plan→Work→Review cycle 本身就是一種 eval
- [Material Science Agents](material-science-agents.md) — MADE benchmark 出自此領域
- [derived: Agent Product Case Studies](../derived/2026-04-09-agent-product-case-studies.md)
- [derived: Warmup Gap Analysis](../derived/2026-04-09-warmup-agent-knowledge-gap-analysis.md)

## Related Concepts

- [Agent Product Design](agent-product-design.md)
- [Agentic Harness](agentic-harness.md)
- [Material Science Agents](material-science-agents.md)
- [ACE Framework](ace-framework.md)

## Sources

- [SWE-bench — Jimenez, Yang, Wettig, Yao, Pei, Press, Narasimhan (Princeton NLP, ICLR 2024 Oral)](https://arxiv.org/abs/2310.06770) — 真實 GitHub issue 的 coding agent benchmark
- [METR — Beth Barnes et al., advisors: Yoshua Bengio, Alec Radford](https://metr.org/) — task-completion time horizon, autonomous capability assessment
- [HELM — Percy Liang et al. (Stanford CRFM)](https://crfm.stanford.edu/helm/) — 7-metric holistic evaluation framework
- [MADE Benchmark (arXiv 2601.20996)](https://arxiv.org/abs/2601.20996) — 材料科學 agent 結構化數據抽取 benchmark
- [WebArena (CMU, arXiv 2307.13854)](https://arxiv.org/abs/2307.13854) — web browsing agent benchmark
- [Building Effective Agents — Anthropic (Schluntz & Zhang, 2024.12)](https://www.anthropic.com/research/building-effective-agents) — "complexity must be justified by performance gains"
- [How Agents Can Improve LLM Performance — Andrew Ng (2024.03)](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/) — GPT-3.5 + agent loop = 95.1% on HumanEval vs GPT-4 zero-shot 67%
- [Building AI Agents — Chip Huyen (2025.01)](https://huyenchip.com/2025/01/07/agents.html) — 漸進式 eval 建議
- [Vivaria — METR open-source eval runner](https://github.com/METR/vivaria) — 持續 agent 評估框架
