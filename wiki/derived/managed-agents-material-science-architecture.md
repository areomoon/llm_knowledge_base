---
title: "Managed Agents × Material Science Agent 架構設計"
type: design-doc
source_url: raw/areomoon_career_llm/Managed_Agents_Material_Science_Architecture.md
raw_path: raw/areomoon_career_llm/Managed_Agents_Material_Science_Architecture.md
created: 2026-04-10
---

# Managed Agents × Material Science Agent 架構設計

> **TL;DR**: 以 Claude Managed Agents 取代自建 LangChain/LangGraph harness，透過四個 memory store 實作 ACE 的 GRC 循環，為材料科學文獻 extraction agent 提供 production-grade 的 persistent learning 能力。

## 核心架構決策

本設計文件的中心論點：**材料科學 extraction agent 的核心工程問題不是 reasoning loop，而是 harness 和 persistent memory**。Managed Agents 解決了 harness 問題；four-store memory 解決了 persistent learning 問題。

### 四層 Memory Store

| Store | 類型 | 更新頻率 | 對應角色 |
|-------|------|---------|---------|
| `materials_domain_knowledge` | 唯讀 | 每季度（人工）| 靜態 domain KB |
| `extraction_playbook` | 讀寫 | 每 session（Curator）| ACE 的 evolving playbook |
| `extraction_cases` | 讀寫 | 每次 extraction | lab notebook |
| `user_feedback` | 讀寫 | reviewer 寫入 | RLHF 的 preference signal |

### Custom Tools

- `materials_property_lookup` — 查詢 Materials Project API，用於 Reflector 的 database validation
- `unit_conversion` — 使用 pint 處理材料科學非標準單位（emu/g, ZT, S/cm）
- `structure_visualizer` — 使用 pymatgen 生成晶體/分子結構視覺化
- `citation_tracker` — Semantic Scholar API，用於 cross-document validation

## ACE Framework Mapping

```
GENERATOR  = session 推理循環（extraction plan → JSON draft → confidence scores）
REFLECTOR  = self-consistency 3x check + database validation + cross-doc validation
CURATOR    = memory store write/update（每次 session 後自動觸發）
PLAYBOOK   = extraction_playbook store（版本控制，支援 rollback）
```

## 三階段 Rollout

| Phase | 週次 | 目標 | Exit Criteria |
|-------|------|------|---------------|
| Phase 1 | Week 1-2 | Infrastructure + 第一個 GRC demo | GRC 循環跑通 |
| Phase 2 | Week 3-6 | Playbook seeding，50+ cases | precision ≥ 0.75 |
| Phase 3 | Week 7+ | Automated Curator + RLPR 評估 | precision ≥ 0.85 |

## 與現有系統的關係

本方案定位在 MARS 和 LLMatDesign 之間：

- **MARS**（19 agents）: 適合 closed-loop discovery；對 extraction-first 用途過於複雜
- **LLMatDesign**（strategy library）: 最接近 ACE playbook，但缺乏 multi-modal extraction 能力
- **本方案**: LLMatDesign 的 persistent strategy + MARS 的 multi-modal + Managed Agents 的 harness

## 風險要點

1. **Beta feature risk**: Managed Agents 仍為 beta，需要 adapter layer 隔離 API 變動
2. **Memory pollution**: 三層防護（Curator confidence gate → tentative rule 機制 → benchmark regression）
3. **Cost**: Phase 2 估算 ~$80/month（Opus），切換 Sonnet 可降至 ~$20/month
4. **Compliance**: 含有害元素（Pb/Cd/Hg/U）的 extraction output 自動加警告標記

## Concepts Referenced

- [ACE Framework](../concepts/ace-framework.md) — Generator/Reflector/Curator 三角色；Grow-and-Refine 演化機制
- [ACE for Materials](../concepts/ace-for-materials.md) — GRC roles 在材料科學的具體映射（Extraction Generator、Result Analyzer、Materials Playbook）
- [Material Science Agents](../concepts/material-science-agents.md) — MARS / LLMatDesign / MatAgent 的對比分析
- [Evolving Playbooks](../concepts/evolving-playbooks.md) — extraction_playbook store 的設計基礎
- [Tiered Memory](../concepts/tiered-memory.md) — four-store design 的記憶分層邏輯
- [Agentic Harness](../concepts/agentic-harness.md) — Managed Agents 所解決的 12 個 harness patterns

## Notes

本文件是為入職 Material Science Extraction Agent 算法工程師角色而設計的 technical design doc。其核心假設是：ACE 的理論架構（由 Stanford/SambaNova 於 2025 年提出）可以直接映射到 Anthropic Managed Agents 的 production 實作，且在 <1000 cases 的早期階段，memory store 在迭代速度、可解釋性、和 rollback 能力上全面優於 fine-tuning。

First 30 days 的 action plan 詳見原始文件，涵蓋 Day 1 到 Day 30 的具體任務和交付物。
