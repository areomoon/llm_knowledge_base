---
title: "Hermes Agent: Self-Improving Open-Source AI Agent Framework by Nous Research"
source: https://github.com/NousResearch/hermes-agent
docs: https://hermes-agent.nousresearch.com/docs/
date: 2026-02-01
updated: 2026-04-03
version: v0.7.0 "The Resilience Release"
tags: [agent, self-improving, open-source, nous-research, memory, skills, FTS5, learning-loop]
---

# Hermes Agent: 會跟你一起成長的 AI Agent

## 背景與熱度
- 由 Nous Research 於 2026 年 2 月發布
- 發布後兩個月內：33,000+ GitHub stars、4,200+ forks、142+ 貢獻者
- 定位：Self-hosted、open-source、self-improving agent framework
- 口號：The agent that grows with you

## 核心理念：Closed Learning Loop
Hermes 的架構圍繞一個「封閉式學習循環」：
1. Agent 執行任務
2. 評估結果（self-evaluation）
3. 如果方法有價值，萃取成 skill document
4. 儲存到 skill library
5. 下次類似任務自動檢索並應用 skill
6. 隨著使用，skills 不斷 refine

## 四大核心組件

### 1. AIAgent Loop (同步編排引擎)
- Reasoning + tool execution
- Skill creation 與 self-evaluation
- 所有操作的中央循環

### 2. Gateway (多平台訊息路由)
- 單一 process 支援多個 messaging 平台
- 支援：Telegram, Discord, Slack, WhatsApp, Signal, CLI
- 訊息統一進入 agent loop

### 3. Tooling Runtime (6 種 terminal backends)
- Local
- Docker
- SSH
- Daytona
- Singularity
- Modal

### 4. Cron Scheduler (定時任務)
- 在 fresh sessions 執行 recurring tasks
- 自動 deliver outputs

## 三層記憶系統 (最關鍵的創新)

這是 Hermes 跟傳統 flat-memory agents 最大的差異：

### Tier 1: Context Compression
- 當前 session 的即時 context
- 自動壓縮舊的 turn，只保留相關部分

### Tier 2: SQLite FTS5 Session Search
- 所有過去 sessions 寫入 SQLite 檔案
- 用 FTS5 做 full-text search
- 當需要歷史 context 時，用關鍵字搜尋而非 load 整個舊 session
- 檢索結果先經過 LLM summarization，只注入相關部分

### Tier 3: Persistent MEMORY.md + Skills
- MEMORY.md: Agent-curated 的長期記憶，有 periodic nudges 提醒更新
- Skills: Procedural memory（怎麼做事情）
- 跟 episodic memory（發生了什麼）刻意分離

### Session lineage
- 每個 session 有 parent/child 追蹤（跨 compression）
- Per-platform isolation（Discord 的訊息不會污染 Slack 的 context）
- Atomic writes with contention handling

## Skill 系統設計

### Skill Document 格式
結構化模板：「when context looks like this, this approach works」

### Skill 生命週期
1. **Creation**: 複雜任務完成後自動萃取
2. **Discovery**: 下次類似情境時自動檢索
3. **Refinement**: 使用中根據結果自動優化
4. **Versioning**: 隨著新的成功案例更新

## Honcho 整合（Optional）
- 跟 Plastic Labs 的 Honcho 整合
- Deeper user preference modeling
- 用 "peer paradigm" 和 reasoning models
- 建立 high-fidelity 的 user identity、values、mental states representation
- Dialectic modeling：同時建模 user 和 agent 的相對關係
- 12 個 identity layers

## v0.7.0 "The Resilience Release" 安全強化（2026-04-03）

5 個主要安全功能：
1. **Credential pool rotation**：least_used 策略 + 自動 401 failover
2. **Secret exfiltration blocking**：掃描 browser URLs 和 LLM responses 避免 base64/URL encoding/prompt injection 形式的 credential 洩漏
3. **Sandbox output redaction**：防止 code execution 洩漏 credentials
4. **Protected directories**：禁止 file tool 存取 .docker/.azure/.config/gh
5. **Path traversal prevention**：profile imports 時檢查路徑

## 模型彈性
支援任何 model provider：
- Nous Portal
- OpenRouter (200+ models)
- z.ai/GLM
- Kimi/Moonshot
- MiniMax
- OpenAI
- 自建 endpoint

## 與現有知識庫概念的關聯

### 跟 ACE Framework 的關係
Hermes 是 ACE 概念的完整開源實作：
- ACE Generator → Hermes AIAgent Loop
- ACE Reflector → Hermes self-evaluation step
- ACE Curator → Hermes skill document creation + refinement
- ACE Evolving Playbook → Hermes skills library + MEMORY.md

### 跟 SkillClaw 的關係
都是「let skills evolve」的實作，但差異：
| 維度 | Hermes | SkillClaw |
|------|--------|-----------|
| Scope | 單用戶 per-instance | 跨用戶集體進化 |
| 架構 | 本地 SQLite + MEMORY.md | 雲端 shared repo |
| Evolver | 同一個 agent 的 self-evaluation | 專門的 Agentic Evolver |
| 對象 | Personal productivity agent | Multi-tenant agent ecosystem |

Hermes 更適合個人/小團隊的 deployment，SkillClaw 更適合平台級 skill sharing。

### 跟 Claude Managed Agents 的對比
| 維度 | Hermes | Managed Agents |
|------|--------|----------------|
| Hosting | Self-hosted | Managed cloud |
| Memory | SQLite FTS5 + MEMORY.md | Memory Store (managed) |
| Skills | MEMORY.md + skill docs | Custom skills / tools |
| Cost | 自己付 API | Anthropic API + infra |
| 控制度 | 完全控制 | Anthropic opinionated |
| Lock-in | 低 | 中等 |

Hermes 是 Managed Agents 的 self-hosted 替代方案，適合重視 data sovereignty 或想用多種模型的人。

### 跟 Karpathy LLM Wiki 的關係
- Karpathy LLM Wiki 的 MEMORY.md 概念直接啟發 Hermes 的 persistent memory
- Hermes 把 Karpathy 的手動維護變成 agent-curated 自動更新

## 對材料科學 Agent 工作的啟發

1. **Closed Learning Loop 範本**：Hermes 提供一個完整可參考的 self-improving 架構，可以直接借鑑到 extraction agent 的設計
2. **FTS5 cross-session recall**：很適合材料科學 agent 記憶過去處理過的論文和 extraction cases
3. **Self-hosted = Data sovereignty**：對藥廠和材料公司很重要（專利、商業機密不能上雲）
4. **6 種 terminal backends**：Singularity 和 Modal 對 HPC 環境特別有用（材料科學常用到 supercomputer）
5. **Honcho user modeling**：reviewer 的偏好可以被建模，讓 agent 越用越符合 team 的 extraction style

## 使用成本
- 可在 $5/月 的 VPS 上運行（如果不算 LLM API 費用）
- LLM 費用依使用的 model 而定

## 參考資源
- GitHub: https://github.com/NousResearch/hermes-agent
- Docs: https://hermes-agent.nousresearch.com/docs/
- Architecture: https://hermes-agent.nousresearch.com/docs/developer-guide/architecture/
- Memory: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/
- Skills Hub: https://hermes-agent.nousresearch.com/docs/skills
