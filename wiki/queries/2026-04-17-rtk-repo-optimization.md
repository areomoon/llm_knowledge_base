---
title: RTK 套用到本 repo + Claude Code 優化路線
date: 2026-04-17
tags: [claude-code, rtk, token-efficiency, repo-optimization]
---

# RTK 套用到本 repo + Claude Code 優化路線

## Context

使用者測試 [RTK](../concepts/rtk-token-killer.md) 數週後，詢問如何套用到本 `llm_knowledge_base` repo 提升 Claude Code token 效率，並延伸問 repo system design 層面的優化建議（Boris Cherny tips 綜合，見 [Claude Code Token Efficiency Playbook](../concepts/claude-code-token-efficiency-playbook.md)）。

## 本 repo 的誠實評估

Claude Code 內建 `Read` / `Grep` / `Glob` **繞過 RTK**。本 repo 是 markdown 為主，多數讀檔走 Read tool，因此 RTK 贏面集中在 Bash surface：

| 動作 | 頻率 | RTK 贏面 |
|---|---|---|
| `git status` / `diff` / `log`（compile/lint 每次多次） | 高 | **-75~92%** |
| `ls wiki/` / `tree` | 中 | **-80%** |
| `python3 scripts/search.py` 輸出 | 中 | 30–50% |
| Bash `cat raw/*.md` | 很低（用 Read） | 不適用 |

**保守估計單 session 節省 5–15%**。結構性改進（拆 skills、subagent 平行、script 化）收益更大。

## 優化路線（依 ROI）

### P0（立即可做，10–15 分鐘）

| 項目 | 內容 | 預期效果 |
|---|---|---|
| **A. Auto-compact window** | `CLAUDE_CODE_AUTO_COMPACT_WINDOW=400000` | 避開 300–400k context rot 區 |
| **D. Allowlist 擴充** | `.claude/settings.local.json` 加 `git diff/log/show`, `ls`, `tree`, `wc`, `rtk`, 本地 `Read/Grep/Glob` 全目錄 | 每 session 少 5–10 次權限彈窗 |
| **E. Gotchas section** | `CLAUDE.md` 新增「Claude 過去犯過的錯」清單 | 防重複錯誤（Boris 稱最高訊號區塊） |

### P1（30 分鐘–1 小時，結構性）

| 項目 | 內容 | 預期效果 |
|---|---|---|
| **A1. 裝 RTK** | `brew install rtk-ai/tap/rtk && rtk init -g`，重啟 CC | -5~15% tool-output |
| **B. CLAUDE.md → skills 拆分** | compile / lint 流程移到 `.claude/skills/`，CLAUDE.md 瘦身到只剩格式規範 + Gotchas | 每 session 省 2–5k tokens |

### P2（1 小時+）

| 項目 | 內容 |
|---|---|
| **C. Subagent 平行 compile** | `raw/` 多檔案改用 `/batch` 或 worktree-isolated subagents |
| **H. Script 化確定流程** | `scripts/compile.py` / `lint.py` 吃掉 hash 計算、index stats 更新等決定性部分；LLM 只做概念抽取 |
| **F. PostCompact hook** | 壓縮後重新注入 wiki 格式規範 |
| **G. Pre-commit lint hook** | 壞連結阻擋 commit |

## 相關概念

- [RTK Token Killer](../concepts/rtk-token-killer.md)
- [Claude Code Token Efficiency Playbook](../concepts/claude-code-token-efficiency-playbook.md)
- [CLI Output Compression](../concepts/cli-output-compression.md)
- [Information Theory for LLM Context](../concepts/information-theory-for-llm-context.md)
- [Agentic Harness](../concepts/agentic-harness.md)

## Sources

- [rtk-ai/rtk (GitHub)](https://github.com/rtk-ai/rtk)
- [howborisusesclaudecode.com](https://howborisusesclaudecode.com)
- [MadPlay — 80% token reduction](https://madplay.github.io/en/post/rtk-reduce-ai-coding-agent-token-usage)
