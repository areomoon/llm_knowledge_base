---
title: "Claude Managed Agents: Anthropic 官方 Agent Harness 服務"
source: https://platform.claude.com/docs/en/managed-agents/overview
date: 2026-04-01
tags: [claude, managed-agents, agent-harness, memory-store, beta, infrastructure]
---

# Claude Managed Agents

## 概覽
Anthropic 2026 年 4 月發布的新產品，beta header `managed-agents-2026-04-01`。
核心概念：把 Claude Code 的 agent harness 變成 managed cloud service。

## 跟 Messages API 的對比
| | Messages API | Managed Agents |
|---|---|---|
| 定位 | 直接呼叫模型 | Pre-built agent harness + 基礎設施 |
| 適用 | 自訂 agent loop, fine-grained control | Long-running tasks, async work |
| 你要建的 | 整個 agent loop, sandbox, tool execution | 只要 define agent + environment |

## 四個核心概念
1. **Agent**: model + system prompt + tools + MCP servers + skills
2. **Environment**: 雲端容器範本 (pre-installed packages, network rules, mounted files)
3. **Session**: Agent 實例跑在 environment 裡執行特定任務
4. **Events**: 應用與 agent 間的訊息交換 (user turns, tool results, status updates)

## 內建工具
- `bash` - 執行 shell 命令
- `read` / `write` / `edit` - 檔案操作
- `glob` / `grep` - 檔案搜尋
- `web_fetch` / `web_search` - Web 工具
- MCP servers - 外部工具 providers
- Custom tools - 自定義工具

## Memory Store (Research Preview, 最重要的功能)
- Workspace-scoped 文字文件集合
- Agent 在 task 開始前自動檢查，結束時自動寫入學到的東西
- 每個 memory 最大 100KB (~25K tokens)
- 建議拆成多個小檔案而不是幾個大檔案
- 所有變更 immutable versioned (audit + rollback)
- Read-only / read-write 混合支援
- 每個 session 最多掛 8 個 memory stores
- 支援 redact 做 compliance

### Memory Tools
- memory_list, memory_search, memory_read
- memory_write, memory_edit, memory_delete

### 常見使用模式
- Shared reference material (read-only 標準、規範、domain knowledge)
- Per-user / per-team / per-project scoping
- 不同 lifecycle 的記憶分開存

## 使用流程
1. Create an agent - 定義 model, prompt, tools, skills
2. Create an environment - 設定容器
3. Start a session - 啟動一個跑 agent 的 session
4. Send events, stream responses - 透過 SSE 即時接收結果
5. Steer or interrupt - 可中途引導或中斷

## 與 ACE Framework 的對應
這是最關鍵的連結：
- ACE Generator → Managed Agents Session (跑推理和 tool calls)
- ACE Reflector → Session 結束前的自我檢查
- ACE Curator → Memory Store 的 write/update 操作
- ACE Evolving Playbook → Memory Store 本身
- ACE Grow-and-Refine → Memory versioning + append-only writes

Anthropic 基本上把 ACE 理論變成了 managed product。

## 與 Karpathy LLM Wiki 的對應
- Karpathy 的 raw/ + wiki/ 架構 → Memory Store 的多檔案結構
- Karpathy 的 LLM-as-compiler → Agent 自動讀寫 memory
- 主要差異：Managed Agents 跑在雲端 + API first

## 對 Material Science Agent 的實質影響
1. **Extraction service 基礎設施**: 不用自己搭 agent harness
2. **Evolving extraction playbook**: Memory store 直接取代 ACE Curator 的自建實作
3. **QLoRA fine-tuning 可能被延後**: Memory-based learning 成本更低更快
4. **Architecture differentiation**: 入職初期就能提出用 managed agents 替代 LangChain/LangGraph 的 technical vision

## 關鍵限制
- 目前 beta (managed-agents-2026-04-01 header)
- Memory, multi-agent, outcomes 都還在 research preview
- Rate limits: create 60/min, read 600/min

## 參考資源
- Overview: https://platform.claude.com/docs/en/managed-agents/overview
- Memory: https://platform.claude.com/docs/en/managed-agents/memory
- Tools: https://platform.claude.com/docs/en/managed-agents/tools
- Beta access form: https://claude.com/form/claude-managed-agents
