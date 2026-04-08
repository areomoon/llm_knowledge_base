---
title: "Material Science Agent 入職行動計劃"
source_type: article
source_url: ""
ingested: 2026-04-08
compiled: 2026-04-08
tags: [career, onboarding, material-science, agent, ace-framework, qlora]
---

# Material Science Agent 入職行動計劃

> **TL;DR**: 三階段行動計劃（入職前 → 第1-2月 → 第3-4月），將 ACE Generator/Reflector/Curator 模式實際落地到材料科學 agent 算法工程師角色，從 extraction prompt 設計開始，逐步推進到 QLoRA fine-tuning。

## Key Points

**入職前（2026年4-5月）— 架構理解**
- 重點讀：MARS（19 LLM agents + 16 domain tools，含 Orchestrator/Scientist/Engineer/Executor/Analyst 分工）
- 重點讀：LLMatDesign（arXiv 2406.13163）— iterative propose/evaluate/refine + self-reflection 從歷史決策學習；[GitHub](https://github.com/Fung-Lab/LLMatDesign)
- MatAgent（[GitHub](https://github.com/adibgpt/MatAgent)）— physics-aware multi-agent framework
- 補充：MADE Benchmark（arXiv 2601.20996）— closed-loop materials discovery 標準評估集

**第1-2月 — Generator + Reflector 優先於 fine-tuning**
- 先實作 extraction prompt template（Generator 角色）+ self-consistency check（Reflector 角色）
- 同步收集 extraction cases → 為中期 fine-tuning 累積訓練資料
- 關鍵資源：Andrew Ng Reflection patterns、LangChain Reflection Agents、ACE Playbook 開源實作（[github.com/jmanhype/ace-playbook](https://github.com/jmanhype/ace-playbook)）

**第3-4月 — QLoRA fine-tuning**
- 將初期 extraction cases 整理為 SFT 訓練集
- 推薦模型：Llama 或 Qwen 系列
- 推薦設定：r=16, DoRA, target_modules="all-linear", lr=2e-4, cosine warmup
- 評估：fine-tuned vs base + prompt engineering 的 extraction 品質 A/B 比較
- 關鍵資源：QLoRA 論文（arXiv 2305.14314）、[github.com/artidoro/qlora](https://github.com/artidoro/qlora)

## Extracted Concepts

- [ACE Framework](../concepts/ace-framework.md)
- [ACE for Materials](../concepts/ace-for-materials.md)
- [Material Science Agents](../concepts/material-science-agents.md)
- [Agentic Self-Improvement](../concepts/agentic-self-improvement.md)

## Raw Source

`raw/areomoon_career_llm/Onboarding_Action_Plan.md`
