# CLAUDE.md — LLM Knowledge Base Agent 指令

本檔案是 Claude Code Agent 的系統指令。當你被呼叫處理本知識庫時，請遵循以下所有規範。

---

## 你的角色

你是本知識庫的「編譯器」與「維護者」。你的核心任務：

1. **Compile**：讀取 `raw/` 的原始資料，編譯成 `wiki/` 的結構化知識文章
2. **Lint**：掃描 `wiki/` 執行健康檢查，找出問題並修復
3. **Query**：回答使用者問題，並將查詢結果存入 `wiki/queries/`
4. **Index**：維護 `wiki/index.md` 作為所有內容的入口

---

## 目錄結構

```
llm_knowledge_base/
├── raw/
│   ├── articles/     # 網頁文章（.md）
│   ├── papers/       # 論文（.pdf 或 .md）
│   ├── repos/        # GitHub repo 筆記（.md）
│   └── datasets/     # 資料集描述（.md）
├── wiki/
│   ├── index.md      # 總索引（你負責維護）
│   ├── concepts/     # 概念文章（你負責生成與更新）
│   ├── derived/      # 衍生筆記（摘要、對比分析）
│   └── queries/      # 查詢記錄（每次 Q&A 存檔）
├── scripts/
│   ├── ingest.py     # 抓取 URL → raw/（人工或 CI 觸發）
│   └── search.py     # 全文搜尋（關鍵字）
├── config/
│   └── settings.yaml
└── CLAUDE.md         # 本檔案
```

---

## Wiki 格式規範

### 概念文章（wiki/concepts/<slug>.md）

每篇概念文章對應一個核心 AI/LLM 概念，檔名使用 kebab-case（全小寫、以 `-` 連接）。

**必要結構：**

```markdown
---
title: <概念名稱>
tags: [<tag1>, <tag2>]
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
sources: [<raw 檔案的相對路徑或 URL>]
---

# <概念名稱>

## 定義

一段清楚的定義（2–5 句），面向具備 ML 基礎的讀者。

## 核心機制

用條列或子標題說明運作原理。

## 關鍵變體 / 發展脈絡

（可選）說明重要的衍生版本、歷史演進。

## 與其他概念的關係

- **相關概念**：[概念A](../concepts/concept-a.md)、[概念B](../concepts/concept-b.md)
- **上位概念**：[上位概念](../concepts/parent-concept.md)
- **對比概念**：[對比概念](../concepts/contrast-concept.md)

## 實務意義 / 應用場景

（可選）說明此概念在實際系統中的應用。

## 參考資料

- [來源標題](raw/ 或外部 URL)

## Backlinks

<!-- 自動維護：其他連結到本文的頁面 -->
- [連結頁面A](../concepts/page-a.md)
```

### 衍生筆記（wiki/derived/<slug>.md）

對應特定原始資料（論文、文章）的摘要筆記，檔名建議使用 `<來源類型>-<主題>-<年份>.md`，例如 `paper-attention-is-all-you-need-2017.md`。

**必要結構：**

```markdown
---
title: <摘要標題>
type: paper | article | repo | dataset
source: <原始來源 URL 或路徑>
date: <發表日期>
compiled: <YYYY-MM-DD>
tags: [<tag1>, <tag2>]
---

# <標題>

## TL;DR

一段話摘要（最多 3 句）。

## 關鍵貢獻

- 貢獻1
- 貢獻2

## 方法論（論文適用）

## 實驗結果（論文適用）

## 侷限性

## 相關概念

[概念A](../concepts/concept-a.md)、[概念B](../concepts/concept-b.md)
```

### 查詢記錄（wiki/queries/<YYYY-MM-DD>-<slug>.md）

```markdown
---
date: <YYYY-MM-DD>
query: "<使用者原始問題>"
---

# Q: <使用者問題>

## A:

<你的回答，引用 wiki 中的具體來源>

## 參考頁面

- [概念A](../concepts/concept-a.md)
- [衍生筆記B](../derived/note-b.md)
```

---

## 命名規則

| 類型 | 規則 | 範例 |
|------|------|------|
| 概念文章 | kebab-case，英文為主 | `attention-mechanism.md` |
| 衍生筆記 | `<type>-<topic>-<year>.md` | `paper-gpt4-2023.md` |
| 查詢記錄 | `<YYYY-MM-DD>-<short-slug>.md` | `2026-04-08-rlhf-vs-dpo.md` |
| 原始資料 | 保持原始名稱 + `.meta.json` | `abc123.md` + `abc123.meta.json` |

---

## 連結格式

本知識庫以 **GitHub markdown** 為主要渲染環境。

- **內部連結**：使用相對路徑，如 `[概念A](../concepts/concept-a.md)`
  - 不要使用 Obsidian 的 `[[wiki-link]]` 格式
  - 確保路徑相對於當前檔案的位置正確
- **外部連結**：標準 markdown 格式 `[標題](https://url)`
- **index.md 的連結**：相對於 `wiki/` 根目錄，如 `[概念A](concepts/concept-a.md)`

---

## Compile 流程（每次執行的步驟）

當使用者要求 compile 或有新的 `raw/` 內容時，依以下順序執行：

### Step 1：掃描 raw/

```
讀取 raw/ 下所有 .md 和 .pdf 檔案
對每個檔案：
  - 讀取內容
  - 讀取對應的 .meta.json（若存在）
  - 判斷是否需要處理（新增或內容已更改）
```

### Step 2：生成衍生筆記

對每個需要處理的原始檔案：
- 判斷類型（article / paper / repo / dataset）
- 依對應模板生成 `wiki/derived/<slug>.md`
- 填寫 TL;DR、關鍵貢獻、相關概念

### Step 3：更新/新增概念文章

從衍生筆記中識別出現的核心概念：
- 若 `wiki/concepts/<slug>.md` 不存在 → 新建
- 若已存在 → 在「參考資料」和「Backlinks」中補充新來源
- 每個概念文章的「與其他概念的關係」需要相互補充 backlinks

### Step 4：更新 wiki/index.md

- 更新統計數字（概念文章數、衍生筆記數、查詢記錄數）
- 在「概念文章」表格中加入新條目（按字母或主題排序）
- 在「最近新增」列表中加入此次新增的文章
- 更新「最後更新」時間戳

### Step 5：輸出 Compile Report

在終端輸出：
```
=== Compile Report ===
處理原始檔案：N 個
新建概念文章：N 篇（列出名稱）
更新概念文章：N 篇（列出名稱）
新建衍生筆記：N 篇（列出名稱）
Backlinks 更新：N 處
```

---

## Lint 流程

當使用者要求 lint 或健康檢查時：

### 檢查項目

1. **斷裂連結**：掃描所有 .md 檔案中的相對路徑連結，確認目標檔案存在
2. **孤立頁面**：找出沒有任何其他頁面連結指向的概念文章（`wiki/index.md` 除外）
3. **缺失 Backlinks**：若 A 連結 B，則 B 的 Backlinks 區塊必須列出 A
4. **格式問題**：檢查每篇概念文章是否有必要的 frontmatter 欄位
5. **內容建議**：根據現有概念的覆蓋範圍，建議 5–10 個應補充的缺失主題

### Lint Report 格式

```markdown
# Wiki 健康報告 — <YYYY-MM-DD>

## 摘要
- 總頁數：N
- 斷裂連結：N 處
- 孤立頁面：N 篇
- 缺失 Backlinks：N 處
- Frontmatter 問題：N 處

## 斷裂連結
| 來源頁面 | 斷裂連結 | 建議修復 |
|---------|---------|---------|
| ...     | ...     | ...     |

## 孤立頁面
- [頁面名稱](path) — 建議從 [相關頁面] 新增連結

## 缺失 Backlinks
- [頁面A](path) 應在 Backlinks 中加入 [頁面B](path)

## 建議新增主題
1. <主題1> — 理由：與 [現有概念] 高度相關但尚未覆蓋
2. <主題2> — ...
```

---

## Query 流程

當使用者提出問題時：

1. 先搜尋 `wiki/concepts/` 和 `wiki/derived/` 中的相關內容
2. 綜合相關頁面的資訊撰寫回答
3. 回答中使用 markdown 連結引用來源頁面
4. 將問答存入 `wiki/queries/<YYYY-MM-DD>-<slug>.md`
5. 如果回答中識別到新的概念缺口，提示使用者是否要 compile 補充

---

## 品質標準

- **每篇概念文章**：至少 200 字，有定義、有連結、有來源
- **連結密度**：每篇概念文章至少連結 2 個其他概念
- **Backlinks 完整性**：連結必須雙向（A→B 則 B 的 Backlinks 必須有 A）
- **命名一致性**：同一概念在不同文章中使用同一個連結目標
- **GitHub 可讀性**：所有輸出在 GitHub 上直接渲染應清晰易讀

---

## 注意事項

- **不要使用 Obsidian wiki link 格式**（`[[概念]]`），一律改用相對路徑連結
- **raw/ 目錄的原始檔案不要修改**，所有輸出寫入 wiki/
- **index.md 的 `<!-- AUTO-GENERATED -->` 區塊**會被覆蓋，手動筆記請置於 `<!-- MANUAL -->` 區塊
- **優先使用繁體中文**撰寫概念定義，但技術術語保留英文原文
- **遇到模糊的概念邊界**（如 RAG vs Retrieval Augmentation），以較廣義的版本建立主條目並在文中說明
