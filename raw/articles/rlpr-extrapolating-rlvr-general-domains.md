---
title: "RLPR: Extrapolating RLVR to General Domains without Verifiers"
source: https://arxiv.org/abs/2506.18254
github: https://github.com/OpenBMB/RLPR
date: 2025-06-23
tags: [RL, RLVR, LLM-reasoning, general-domain, verifier-free, probability-reward]
---

# RLPR: Reinforcement Learning with Reference Probability Reward

## 核心問題
RLVR (Reinforcement Learning with Verifiable Rewards) 在數學和程式碼領域取得顯著成果，但主要限制是依賴 domain-specific verifier — 在數學可以用符號求解器驗證，在 code 可以跑 unit test，但在自然語言通用領域沒有這種 verifier。

## 核心洞察
LLM 對於生成「正確答案」的內在機率 (intrinsic probability) 本身就是一個 reward signal — 機率越高代表 LLM 自己認為這個推理過程越能導向正確答案。不需要外部 verifier，LLM 自己就是 judge。

## 方法
1. **Reference Probability Reward**: 用 LLM 對 reference answer 的 token probability 當 reward
2. **Prob-to-reward transformation**: 把機率轉換成穩定的 reward signal
3. **Stabilizing methods**: 處理機率 reward 的 high variance 問題

## 對比
| 方法 | Reward 來源 | 適用領域 | 限制 |
|------|-------------|----------|------|
| RLVR | 外部 verifier (math solver, unit test) | 數學、Code | 需要 domain verifier |
| VeriFree | 最大化 reference answer 機率 | 通用 | 需要 reference answer |
| RLPR | LLM intrinsic probability | 通用 | 機率 noise 高 |

## 實驗結果
- 在 Gemma、Llama、Qwen 系列模型上一致提升推理能力
- 跨 4 個通用領域 benchmarks 和 3 個數學 benchmarks
- 超越同期 VeriFree：TheoremQA +7.6, Minerva +7.5
- 超越 verifier-dependent 的 General-Reasoner 平均 +1.6 分
- 7 個 benchmarks 平均領先

## 對材料科學 Agent 的意義
這是最關鍵的連結：
- 材料科學是典型的「沒有客觀 verifier」的領域 — 你無法用 unit test 驗證一篇論文的 extraction 是否正確
- RLPR 的「用 LLM 內在機率當 reward」正好適用於 extraction agent 的訓練
- 結合 ACE Framework 的 Generator-Reflector-Curator，Reflector 可以用 RLPR 的 probability signal 做信心校準
- 可以用在 post-training：用 QLoRA + RLPR 在累積的 extraction cases 上強化 agent

## 參考資源
- Paper: https://arxiv.org/abs/2506.18254
- GitHub: https://github.com/OpenBMB/RLPR
- HuggingFace: https://huggingface.co/papers/2506.18254
