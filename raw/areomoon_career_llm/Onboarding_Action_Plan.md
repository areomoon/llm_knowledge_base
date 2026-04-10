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

---

## 追加：Managed Agents 和 RLPR (2026-04-10 更新)

兩個 2026 年 4 月的新發展，大幅改變入職策略。

### 背景

**Claude Managed Agents** (Anthropic, 2026-04-01 beta)：
- Anthropic 把 ACE Framework 的理論架構變成了 managed cloud service
- Memory Store = managed evolving playbook：agent 在 task 開始前自動讀，結束後自動寫
- 可以替代自己搭 LangChain/LangGraph + ACE Curator 的計劃
- 進入 beta 申請：https://claude.com/form/claude-managed-agents

**RLPR** (OpenBMB, arXiv 2506.18254, 2025-06-23)：
- Reference Probability Reward：用 LLM 對 reference answer 的 token probability 當 reward
- 不需要 domain verifier → 完全適合材料科學 extraction（無法用 unit test 驗證）
- Materials Project / Springer Materials 的結構化資料可以直接當 reference answer → 不需要專家標注就能開始
- 超越需要 verifier 的 General-Reasoner (+1.6 avg)、超越 VeriFree (+7.6 TheoremQA)

### 修訂後的行動計劃

#### 入職前（2026年4月-5月）— 不變
繼續原計劃：讀 MARS, LLMatDesign, MatAgent 論文。
新增：申請 Managed Agents beta + 讀 RLPR 論文。

#### 入職初期（第1-2個月）— 重大更新

**舊計劃**：自己建 Generator extraction prompt + Reflector self-consistency（LangChain/LangGraph）

**新計劃**：
1. 用 **Managed Agents** 搭原型 extraction agent（claude-sonnet-4-6 + bash + web tools）
2. 定義初始 Memory Store 架構：`extraction-heuristics.md`、`per-material-class/oxides.md` 等
3. 跑 20–30 篇論文的 extraction；讓 agent 把規則累積進 Memory Store
4. 比較：有 Memory Store vs 沒有 Memory Store 的 extraction F1

**關鍵提案**：在第一週的架構討論中提出「用 Managed Agents 替代 LangChain/LangGraph」。

#### 中期（第3-4個月）— 更新

**新優先序**（依 ROI 排序）：
1. **Memory Store 調優**（優先）：優化 Memory Store 結構（粒度、deduplication 頻率）
2. **RLPR 基線**（其次）：用 Materials Project 結構化資料當 reference answer；在 Qwen-7B 跑 GRPO + RLPR
   - 設定：r=16, DoRA, cosine warmup, probability reward
3. **SFT 混合**（最後，若 RLPR 到瓶頸）：加入專家標注的 SFT 訓練集

**核心主張**：「RLPR 讓我們不需要專家標注就能開始 RL 訓練。用現有資料庫就能做 reward。」

### 實戰步驟（追加）

入職前：
- [ ] 申請 Claude Managed Agents beta access
- [ ] 讀 RLPR 論文 (arXiv 2506.18254)，重點：prob-to-reward transformation

入職第1-2週：
- [ ] 評估：Patsnap 現有系統用什麼 agent 框架？
- [ ] 在第一次架構討論提出 Managed Agents 方案
- [ ] 定義 Memory Store schema for materials extraction

入職第2個月：
- [ ] 量化 Memory Store 收益：有/沒有 memory 的 extraction 品質對比（50 篇論文）
- [ ] 呈現結果：「Memory Store 不需要標注，提升 X% extraction 品質」

入職第3個月：
- [ ] 建立 RLPR 訓練環境（OpenBMB/RLPR GitHub）
- [ ] 收集 500–1000 個 (paper section, reference answer) pair from Materials Project
- [ ] 跑 RLPR baseline on Qwen-7B

### 技術差異化陳述（面試或架構審查用）

> 「我計劃用 Claude Managed Agents 作為 extraction service 的基礎設施，Memory Store 實作按材料類別分層的 evolving extraction playbook。這讓我們不需要自己寫 ACE Curator 的程式碼就能做到跨 session 的自我改進。在 post-training 方面，RLPR 讓我們可以用現有結構化資料庫的條目當 reward signal 做 RL fine-tuning — 前兩個月不需要專家標注。這個做法降低了基礎設施複雜度，同時加速了改進循環。」

### 參考連結（新增）
- [Claude Managed Agents](../../wiki/concepts/claude-managed-agents.md)
- [RLPR (Reference Probability Reward)](../../wiki/concepts/rlpr-reference-probability-reward.md)
- [Memory Stores vs RAG](../../wiki/concepts/memory-stores-vs-rag.md)
- [Managed Agents Career Impact (Derived Note)](../../wiki/derived/managed-agents-career-impact.md)
