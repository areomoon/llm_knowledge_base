---
title: RTK 能不能套到 Codex / Devin？本地 vs 雲端 agent 的差異
date: 2026-04-20
tags: [rtk, claude-code, devin, codex, deployment-model, hook-surface]
---

# RTK 能不能套到 Codex / Devin？本地 vs 雲端 agent 的差異

## Context

使用者已看過 [RTK Token Killer](../concepts/rtk-token-killer.md) 的基礎介紹，進一步詢問：
1. RTK 是否只為 Claude Code 設計？
2. 用公司電腦從本地 IDE 連 Devin 算本地還雲端？

由此展開「本地 vs 雲端 agent」的分類討論，產出新概念 [Local vs Cloud Coding Agents](../concepts/local-vs-cloud-coding-agents.md)。

## 關鍵問答

### Q1: RTK 只給 Claude Code 用嗎？

不是。RTK 官方支援 **12 種 agent**（見 [RTK Token Killer § Key Properties](../concepts/rtk-token-killer.md)），但接法有差：

- **硬攔**（有真 hook API）：Claude Code、Copilot、Cursor、Gemini CLI — agent 不知道被攔，100% 生效
- **軟求**（沒有 hook 機制）：Windsurf、Cline、Aider — 靠 prompt 規則請求 agent 自己加 `rtk` 前綴，可能失效

Codex / Devin **完全無法接**（見 Q2）。

### Q2: 公司電腦開 local IDE 跑 Devin 算哪類？

**仍然是雲端 agent**。判定軸是**「shell 指令在哪台機器上執行」**，不是使用者的 UI 在哪裡。

| 使用者操作點 | Devin 實際執行點 |
|---|---|
| 公司電腦網頁 | Cognition 雲端 VM |
| 公司電腦 IDE 外掛 | Cognition 雲端 VM |
| 手機 App | Cognition 雲端 VM |

IDE 只是遙控器。三個判定啟發式：

1. 斷網還能跑嗎？不能 → 雲端
2. `ps` 看得到 agent process 嗎？看不到 → 雲端
3. agent 剛寫的檔案，`cat` 得到嗎？不能 → 雲端

### 為什麼這影響 RTK 能不能用

RTK 需要兩個條件：
1. `rtk` binary 在**執行機器**的 `$PATH`
2. agent 讀得到的 hook / 設定檔

雲端 agent 兩者都不滿足。即使在 prompt 裡寫「請加 `rtk` 前綴」，VM 裡沒有 binary，會直接 `command not found`。

## 衍生結論

1. 本 KB 已有 [RTK Token Killer](../concepts/rtk-token-killer.md)、[Agentic Harness](../concepts/agentic-harness.md)、[Claude Managed Agents](../concepts/claude-managed-agents.md)，但缺「分類 agent 的部署軸」這一層抽象。新建 [Local vs Cloud Coding Agents](../concepts/local-vs-cloud-coding-agents.md) 補上。
2. [Claude Managed Agents](../concepts/claude-managed-agents.md) 是 Anthropic 試圖在雲端側重建「hook surface」的嘗試 — 屬於把本地 harness 能力搬上雲端的特例。
3. GitHub Codespaces + Copilot 是常見的誤判案例：UI 像本地，實際是雲端。

## 行動項目

- [x] 新建 concept `local-vs-cloud-coding-agents.md`
- [x] `rtk-token-killer.md` Limitations 段連到新 concept
- [x] `index.md` 加新 concept 行、加本 query 行
- [ ] （待辦）`mobile-dispatch-workflow.md` 可考慮補引用新 concept，釐清 iPhone + Claude Code 仍算本地（因為 Claude Code 在 Mac 上跑）
