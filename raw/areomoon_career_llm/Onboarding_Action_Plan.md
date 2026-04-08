---
title: "Material Science Agent 入職行動計劃"
date: 2026-04-08
tags: [career, onboarding, material-science, agent, ACE]
---

# Material Science Agent 入職行動計劃

基於 ACE (Agentic Context Engineering) 框架和現有材料科學 Agent 研究，為即將到來的 Material Science Agent 算法工程師角色制定的行動計劃。

## 短期（入職前，2026年4月-5月）

**重點：理解 MARS 和 LLMatDesign 的架構，特別是 multi-modal + domain tool 整合**

### 必讀論文
- MARS 系統論文：Knowledge-driven autonomous materials research via collaborative multi-agent and robotic system
  - 重點：19 個 LLM agents 如何分工（Orchestrator, Scientist, Engineer, Executor, Analyst）
  - 重點：16 個 domain-specific tools 的整合模式
  - 新聞報導：https://phys.org/news/2026-01-multi-agent-ai-robots-automate.html

- LLMatDesign 論文：https://arxiv.org/abs/2406.13163
  - GitHub 實作：https://github.com/Fung-Lab/LLMatDesign
  - 重點：LLM 如何進行 iterative propose/evaluate/refine
  - 重點：self-reflection 機制如何從過去的決策中學習

- MatAgent：https://github.com/adibgpt/MatAgent
  - physics-aware multi-agent LLM framework

### 學習資源
- Towards Agentic Intelligence for Materials Science (arxiv 2602.00169)
- Agentic material science: https://www.oaepublish.com/articles/jmi.2025.87
- MADE Benchmark for closed-loop materials discovery: https://arxiv.org/abs/2601.20996

## 入職初期（第1-2個月）

**重點：先做 Generator extraction prompt + Reflector self-consistency，比 fine-tuning 更快見效**

### Generator-Reflector Pattern 學習資源
- Andrew Ng - Agentic Design Patterns Part 2 Reflection: https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/
- LangChain Reflection Agents: https://blog.langchain.com/reflection-agents/
- Reflexion 技術指南: https://www.promptingguide.ai/techniques/reflexion
- ACE Playbook 開源實作 (Generator-Reflector-Curator): https://github.com/jmanhype/ace-playbook
- Reflection Agent Pattern 文檔: https://agent-patterns.readthedocs.io/en/stable/patterns/reflection.html
- LangGraph 自我改進 Agent: https://medium.com/@shuv.sdr/langgraph-build-self-improving-agents-8ffefb52d146

### 實戰步驟
1. 設計 extraction prompt template（Generator 角色）
2. 實作 self-consistency check（Reflector 角色）
3. 建立 extraction case 收集機制（為後續 fine-tuning 累積資料）

## 中期（第3-4個月）

**重點：用累積的 extraction case 建 SFT 訓練集做 QLoRA — 與 Warmup Plan Week 5 對齊**

### QLoRA Fine-tuning 學習資源
- QLoRA 原始論文: https://arxiv.org/abs/2305.14314
- QLoRA GitHub: https://github.com/artidoro/qlora
- 2025 實用指南: https://reintech.io/blog/how-to-fine-tune-llms-with-lora-and-qlora-practical-guide
- 2026 完整教程: https://oneuptime.com/blog/post/2026-01-30-qlora-fine-tuning/view
- 深度指南 (LoRA + QLoRA): https://www.mercity.ai/blog-post/guide-to-fine-tune-llms-with-lora-and-qlora/
- LLM Fine-tuning 完整指南 2025: https://tensorblue.com/blog/llm-fine-tuning-complete-guide-tutorial-2025
- Consumer GPU 實戰: https://letsdatascience.com/blog/fine-tuning-llms-with-lora-and-qlora-complete-guide

### 實戰步驟
1. 從入職初期累積的 extraction cases 中整理 SFT 訓練集
2. 選擇基礎模型（推薦先用 Llama 或 Qwen 系列）
3. QLoRA 設定建議：r=16, DoRA, target_modules="all-linear", lr=2e-4, cosine warmup
4. 評估：比較 fine-tuned model vs base model + prompt engineering 的 extraction 品質

## 參考架構連結
- [ACE Framework](../../wiki/concepts/ace-framework.md)
- [ACE for Materials](../../wiki/concepts/ace-for-materials.md)
- [Material Science Agents](../../wiki/concepts/material-science-agents.md)
- [Agentic Self-Improvement](../../wiki/concepts/agentic-self-improvement.md)
