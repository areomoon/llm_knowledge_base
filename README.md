# LLM Knowledge Base

[![Wiki Lint](https://github.com/areomoon/llm_knowledge_base/actions/workflows/lint.yml/badge.svg)](https://github.com/areomoon/llm_knowledge_base/actions/workflows/lint.yml)
[![Wiki Compile](https://github.com/areomoon/llm_knowledge_base/actions/workflows/compile.yml/badge.svg)](https://github.com/areomoon/llm_knowledge_base/actions/workflows/compile.yml)

基於 [Andrej Karpathy LLM Knowledge Base](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 概念建立的個人 AI/Agent 研究知識庫系統。

---

## 專案概覽

本專案不採用傳統的 RAG（Retrieval-Augmented Generation）或向量資料庫方案，而是讓 LLM 扮演「編譯器」的角色：

> **核心理念**：LLM 讀取原始文件 → 產出結構化 Markdown Wiki → Wiki 本身即知識庫

原始資料（論文、文章、GitHub notes）進入 `raw/` 暫存區，LLM 增量讀取並編譯成約 100 篇、40 萬字的概念文章，自動維護 backlinks 與交叉引用。每一次查詢都會回存 wiki，讓知識庫持續累積。

---

## 四大階段架構

```
Phase 1: Ingest  →  Phase 2: Compile  →  Phase 3: Query  →  Phase 4: Lint
   ↑                                                               |
   └───────────────────────────────────────────────────────────────┘
```

| 階段 | 說明 |
|------|------|
| **Phase 1 Ingest** | 收集網頁文章、arXiv 論文、GitHub repos、資料集，存入 `raw/` |
| **Phase 2 Compile** | LLM 讀取 `raw/`，產出結構化 wiki（index + 概念文章 + 衍生內容） |
| **Phase 3 Query** | 透過搜尋引擎、Q&A Agent 探索 wiki，結果回存累積 |
| **Phase 4 Lint** | LLM 健康檢查：找出不一致、缺失資訊、斷裂連結，觸發下一輪編譯 |

---

## 用途

- **個人 AI/Agent 研究**：整理 LLM、Agent、強化學習、多模態等領域最新進展
- **論文閱讀管理**：arXiv 論文自動摘要、關鍵概念抽取、與既有知識的關聯建立
- **知識長期累積**：每次閱讀都讓 wiki 更完整，無需手動撰寫

---

## 預期效果

仿照 Karpathy 的規模目標：

- **~100 篇** 結構化概念文章（`wiki/concepts/`）
- **~40 萬字** 的知識庫總量
- 所有文章自動維護 backlinks 和交叉引用
- 無需手動撰寫，LLM 全程輔助生成與維護

---

## 資料夾結構

```
llm_knowledge_base/
├── raw/                    # Phase 1: 原始資料輸入區
│   ├── articles/           # 網頁文章 (.md)，由 ingest.py 抓取或手動貼入
│   ├── papers/             # 論文 (.pdf, .md)，主要來自 arXiv
│   ├── repos/              # GitHub repo 學習筆記
│   └── datasets/           # 資料集描述與筆記
├── wiki/                   # Phase 2: LLM 編譯輸出的結構化 wiki
│   ├── index.md            # 總索引（所有概念文章的入口摘要）
│   ├── concepts/           # 概念文章（主力內容，含 backlinks）
│   ├── derived/            # 衍生產出（Marp 投影片、matplotlib 圖表）
│   └── queries/            # 查詢結果與 Q&A 記錄存檔
├── scripts/                # 工具腳本
│   ├── ingest.py           # 輸入處理：URL → Markdown
│   ├── compile.py          # LLM 編譯：raw/ → wiki/
│   ├── search.py           # 全文搜尋引擎（CLI + Web UI）
│   └── lint.py             # Wiki 健康檢查
├── config/
│   └── settings.yaml       # LLM API 設定、路徑設定
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 模組說明

### `scripts/ingest.py`
- **功能**：從 URL 抓取網頁內容，轉換為 Markdown 格式存入 `raw/articles/`；支援 arXiv PDF 下載、GitHub repo 摘要
- **依賴**：`requests`, `beautifulsoup4`, `markdownify`, `arxiv`, `PyMuPDF`

### `scripts/compile.py`
- **功能**：增量讀取 `raw/` 新增文件，呼叫 LLM API 產出 wiki 文章
  - 更新 `wiki/index.md` 總索引
  - 建立或更新 `wiki/concepts/` 概念文章（含 backlinks）
  - 維護概念間的連結圖，自動追蹤哪些原始檔案已處理
- **依賴**：`anthropic`, `pyyaml`, `pathlib`

### `scripts/search.py`
- **功能**：對 `wiki/` 做全文搜尋，支援 CLI 和簡易 Web UI
- **設計**：naive keyword search（仿 Karpathy 的 vibe-coded 風格），不需向量資料庫
- **依賴**：`flask`（Web UI）, `click`（CLI）

### `scripts/lint.py`
- **功能**：掃描 wiki，檢查斷裂的 `[[internal links]]`、概念文章間的不一致描述、缺失 backlinks、孤立文章（無任何連結指向）；產出健康報告與 LLM 建議的新文章主題
- **依賴**：`re`, `pathlib`, `anthropic`

---

## 技術棧

| 類別 | 工具 |
|------|------|
| 程式語言 | Python 3.11+ |
| LLM API | Claude API（Anthropic）/ OpenAI API |
| 知識庫瀏覽 | GitHub（原生 Markdown 渲染，Actions 自動 compile/lint） |
| 文件格式 | Markdown（含 YAML frontmatter） |
| 設定管理 | YAML |
| 投影片 | Marp（Markdown → 簡報） |
| 圖表 | matplotlib |

---

## 快速開始

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 設定 API 金鑰
cp .env.example .env
# 編輯 .env，填入 ANTHROPIC_API_KEY

# 3. 輸入第一篇文章
python scripts/ingest.py --type article --url "https://example.com/article"

# 4. 編譯 wiki
python scripts/compile.py

# 5. 搜尋
python scripts/search.py --query "transformer attention"

# 6. 健康檢查
python scripts/lint.py
```

---

## GitHub 作為知識庫介面

本專案以 **GitHub** 取代 Obsidian 作為主要瀏覽與協作介面：

| 功能 | 說明 |
|------|------|
| **Markdown 瀏覽** | GitHub 原生渲染 `wiki/` 所有文章 |
| **自動 Compile** | `compile.yml` 每日排程或手動觸發，自動將 `raw/` 編譯為 wiki |
| **自動 Lint** | `lint.yml` 在每次 push/PR 時執行 wiki 健康檢查 |
| **版本歷史** | git log 追蹤每篇文章的演化 |
| **Issues** | 用 GitHub Issues 記錄待研究的主題 |

> 若需要 backlinks 圖形視覺化，可自行選擇用 Obsidian 開啟 `wiki/` 目錄。

---

## 參考來源

- [Andrej Karpathy — LLM Knowledge Base Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [DAIR.AI Academy — LLM Knowledge Bases (Karpathy)](https://academy.dair.ai/blog/llm-knowledge-bases-karpathy)

---

*由 Claude Code 輔助建立 | 2026-04*
