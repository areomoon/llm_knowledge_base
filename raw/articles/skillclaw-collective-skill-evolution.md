---
title: "SkillClaw: Let Skills Evolve Collectively with Agentic Evolver"
source: https://arxiv.org/abs/2604.08377
github: https://github.com/openclaw/skills
benchmark: https://github.com/InternLM/WildClawBench
date: 2026-04-09
tags: [agent, skill-evolution, agentic-evolver, multi-user, collective-intelligence, openclaw, wildclawbench]
---

# SkillClaw: Collective Skill Evolution

## 核心問題
LLM agents (如 OpenClaw) 依賴可重用的 skills 執行複雜任務，但這些 skills 在部署後幾乎都是**靜態的**。結果就是：
- 相同的 workflows 在不同用戶間被重複「發現」
- 同樣的 tool usage patterns 重複被摸索
- 同樣的 failure modes 在每個用戶端重演一次
- 系統無法從經驗中改善

但不同用戶的互動其實包含互補的訊號 — 有人知道某個 skill 什麼時候 work，有人知道它什麼時候 fail。如果能把這些跨用戶的經驗整合起來，skill 就能持續進化。

## 核心方案：Agentic Evolver

SkillClaw 把「skill 集體進化」視為一個 agent 本身的任務，而不是人工維護：

### 工作流程
1. **持續採集 trajectories** — 用戶日常使用 agents 時產生的執行軌跡（成功和失敗都收）
2. **Autonomous Evolver 處理** — 用一個 agent 去分析這些 trajectories
3. **模式識別** — 找出反覆出現的行為模式、失敗模式、成功套路
4. **Skill 更新** — 把洞察翻譯成對 skill set 的更新：
   - Refine 現有 skill（改 prompt、加 guard rails、補 edge case）
   - Extend 新能力（加新的 skill）
5. **Shared Repository** — 更新的 skills 存在共享倉庫
6. **同步到所有用戶** — 一個人發現的改進全系統都受益

### 關鍵創新
- **零用戶成本** — 用戶不需要手動回報 bug、填表單、寫 review
- **跨用戶知識遷移** — 在 context A 發現的改進自動 apply 到 context B
- **累積式能力增強** — 越多人用、系統越強

## 實驗結果

### Benchmark: WildClawBench
- 真實 OpenClaw 環境裡跑任務
- 每個 task 都有真實的 bash shell、file system、browser、email、calendar 服務
- Agent 要處理未預期的結果和無文件的錯誤（就像真實用戶會遇到的一樣）
- Benchmark github: https://github.com/InternLM/WildClawBench

### 結果
- 在有限的互動和回饋下
- **顯著提升 Qwen3-Max 在真實 agent 場景的表現**
- 證明 collective skill evolution 的有效性

## 與現有概念的關聯

### 和 ACE Framework 的差異
| 維度 | ACE | SkillClaw |
|------|-----|-----------|
| 學習 scope | 單一 agent 的 playbook | 跨用戶的 skill library |
| 更新機制 | Generator-Reflector-Curator 循環 | Autonomous Evolver + trajectory aggregation |
| 知識累積 | Append-only playbook | Skill refinement + extension |
| 傳播模型 | Session-local | System-wide sync |
| 最適用例 | 單用戶的 domain-specific 任務 | Multi-tenant agent ecosystem |

SkillClaw 可以看作 **ACE 的分布式版本** — 把 evolving context 從單一 session 擴展到整個用戶群。

### 和 Karpathy LLM Wiki 的差異
Karpathy 的 wiki 是**個人知識庫**，SkillClaw 是**集體技能庫**。兩者都是 LLM-compiled 的，但：
- Karpathy wiki 從原始文件 compile 成結構化知識
- SkillClaw 從執行 trajectories compile 成可執行 skills

### 和 Claude Managed Agents Memory Store 的差異
Managed Agents 的 memory store 是 **workspace-scoped**，每個組織自己的記憶。SkillClaw 是 **global-scoped**，所有用戶共享一個技能池。

對應的設計選擇：
- Private domain knowledge → Memory Store
- Public/shared best practices → SkillClaw 模式

### 對材料科學 Agent 的意義
1. **團隊級 skill evolution** — 不只是個人的 extraction playbook 進化，整個研究團隊可以共享一個技能庫
2. **跨論文類型的知識遷移** — 在一類材料論文學到的 extraction pattern 自動擴展到其他類型
3. **失敗模式的集體學習** — 某個 reviewer 發現的 extraction 錯誤，自動變成所有未來 extraction 的 guard rail
4. **OpenClaw skills 作為 baseline** — OpenClaw 的 skills 倉庫（5400+ skills）可以當作 bootstrap 的起點

## 潛在風險與限制

1. **Quality pollution** — 一個壞 trajectory 可能污染整個 skill library，需要 evolver 有品質把關機制
2. **Privacy leakage** — 跨用戶的 trajectory 可能洩漏某個用戶的敏感操作，需要匿名化
3. **Skill drift** — 長時間的演化可能讓 skill 偏離原始設計意圖，需要 versioning 和 rollback
4. **Cold start** — 新部署的 agent 沒有 trajectories 可以學，需要 seed skills

## OpenClaw 生態系統

SkillClaw 是 OpenClaw 生態系統的一部分：
- **OpenClaw**: open-source personal AI assistant 環境
- **OpenClaw Skills Registry**: 5400+ 社群維護的 skills（https://github.com/VoltAgent/awesome-openclaw-skills）
- **WildClawBench**: 真實環境的 agent benchmark
- **ClawHub**: 雲端 skill marketplace（https://clawhub.ai）
- **MetaClaw**: SkillClaw 的姊妹專案，支援用戶直接跟 agent 對話來演化 skill（https://github.com/aiming-lab/MetaClaw）

## 參考資源
- Paper: https://arxiv.org/abs/2604.08377
- OpenClaw docs: https://docs.openclaw.ai/tools/skills
- Skills 倉庫: https://github.com/openclaw/skills
- WildClawBench: https://github.com/InternLM/WildClawBench
- Awesome OpenClaw Skills: https://github.com/VoltAgent/awesome-openclaw-skills
- MetaClaw: https://github.com/aiming-lab/MetaClaw
