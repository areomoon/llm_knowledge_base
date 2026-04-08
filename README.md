# LLM Knowledge Base

基於 [Andrej Karpathy LLM Knowledge Base](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 概念建立的個人 AI/Agent 研究知識庫系統。

---

## 專案概覽

本專案讓 LLM 扮演「編譯器」的角色，將原始資料轉化為結構化知識庫：

> **核心理念**：LLM 讀取原始文件 → 產出結構化 Markdown Wiki → Wiki 本身即知識庫，直接在 GitHub 上瀏覽

原始資料（論文、文章、GitHub notes）進入 `raw/` 暫存區，Claude Code Agent 增量讀取並編譯成約 100 篇、40 萬字的概念文章，自動維護相對路徑連結與交叉引用。每一次查詢都會回存 wiki，讓知識庫持續累積。

---

## 架構：混合方案（Claude Code Agent + 輕量 Python 腳本）

```
Phase 1: Ingest      Phase 2+3+4: Claude Code Agent
  ↓                        ↓
scripts/ingest.py    CLAUDE.md 驅動的 Agent
  ↓                    ├─ Compile: raw/ → wiki/
raw/                  ├─ Lint: 健康檢查
                      └─ Query: 問答 → wiki/queries/
                           ↓
                         wiki/           ← 在 GitHub 上直接瀏覽
```

| 工作 | 執行者 | 說明 |
|------|--------|------|
| **Ingest**（抓取 URL） | `scripts/ingest.py` | 純 IO，不需 LLM |
| **Compile**（編譯 wiki） | Claude Code Agent | 依 CLAUDE.md 規範 |
| **Lint**（健康檢查） | Claude Code Agent + `scripts/lint.py` | Agent 負責語意，腳本負責結構 |
| **Query**（問答） | Claude Code Agent | 回答並存入 `wiki/queries/` |
| **Search**（全文搜尋） | `scripts/search.py` | 本地關鍵字搜尋，不需 LLM |

---

## 快速開始

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 設定 API 金鑰（ingest.py 需要）
cp .env.example .env
# 編輯 .env，填入 ANTHROPIC_API_KEY

# 3. 輸入第一篇文章
python scripts/ingest.py --type article --url "https://example.com/article"

# 4. 讓 Claude Code Agent 編譯（核心操作）
claude "請 compile raw/ 目錄的所有新增內容"

# 5. 搜尋（本地關鍵字）
python scripts/search.py --query "transformer attention"

# 6. 健康檢查（完整版含語意分析）
claude "請對 wiki/ 執行 lint 健康檢查"

# 7. 問答
claude "請問什麼是 RLHF？和 DPO 有什麼差異？"
```

---

## 瀏覽知識庫

**主要入口**：直接在 GitHub 上瀏覽 [`wiki/index.md`](wiki/index.md)

- 所有連結使用相對路徑，在 GitHub 上點擊直接跳轉
- 概念文章在 [`wiki/concepts/`](wiki/concepts/)
- 衍生筆記在 [`wiki/derived/`](wiki/derived/)
- 查詢記錄在 [`wiki/queries/`](wiki/queries/)

---

## 資料夾結構

```
llm_knowledge_base/
├── CLAUDE.md               # Claude Code Agent 系統指令（核心！）
├── raw/                    # Phase 1: 原始資料輸入區（不提交）
│   ├── articles/           # 網頁文章（.md）
│   ├── papers/             # 論文（.pdf, .md）
│   ├── repos/              # GitHub repo 學習筆記
│   └── datasets/           # 資料集描述
├── wiki/                   # Agent 編譯輸出的結構化知識庫
│   ├── index.md            # 總索引（GitHub 主要導航入口）
│   ├── concepts/           # 概念文章（主力內容，含相互連結）
│   ├── derived/            # 衍生筆記（論文摘要、文章摘要）
│   └── queries/            # 查詢記錄（Q&A 存檔）
├── scripts/
│   ├── ingest.py           # URL → raw/（IO 工具，不需 LLM）
│   ├── search.py           # 全文搜尋（本地關鍵字，不需 LLM）
│   ├── compile.py          # 編譯狀態檢視（不直接呼叫 LLM）
│   └── lint.py             # 結構健康檢查（不直接呼叫 LLM）
├── config/
│   └── settings.yaml       # 路徑與搜尋設定
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 模組說明

### `CLAUDE.md`（最重要）

Claude Code Agent 的系統指令，定義：
- wiki 的格式規範與文章模板
- 命名規則與連結格式
- Compile、Lint、Query 的執行步驟
- 品質標準

### `scripts/ingest.py`

從 URL 抓取網頁內容，轉換為 Markdown 格式存入 `raw/`；支援 arXiv PDF 下載、GitHub repo 摘要。這是唯一需要網路 IO 的腳本，不呼叫 LLM。

依賴：`requests`, `beautifulsoup4`, `markdownify`, `arxiv`, `PyMuPDF`

### `scripts/search.py`

對 `wiki/` 做全文關鍵字搜尋（BM25），提供 CLI 介面。不需 LLM，本地執行。

依賴：`rank-bm25`, `click`

### `scripts/compile.py`

輕量包裝器，提供 `--status` 顯示 raw/ 中待處理的檔案清單。實際編譯由 Claude Code Agent 執行。

### `scripts/lint.py`

本地結構檢查（斷裂連結、孤立頁面、frontmatter 格式）。語意層面的 lint（概念不一致、建議新主題）由 Claude Code Agent 執行。

---

## 預期效果

仿照 Karpathy 的規模目標：

- **~100 篇** 結構化概念文章（`wiki/concepts/`）
- **~40 萬字** 的知識庫總量
- 所有文章自動維護 backlinks 和交叉引用
- 直接在 GitHub 上瀏覽，無需額外工具

---

## 技術棧

| 類別 | 工具 |
|------|------|
| 程式語言 | Python 3.11+ |
| LLM Agent | Claude Code（依 CLAUDE.md 驅動） |
| 知識庫瀏覽 | GitHub（Markdown 原生渲染） |
| 文件格式 | GitHub Flavored Markdown（含 YAML frontmatter） |
| 設定管理 | YAML |

---

## 參考來源

- [Andrej Karpathy — LLM Knowledge Base Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [DAIR.AI Academy — LLM Knowledge Bases (Karpathy)](https://academy.dair.ai/blog/llm-knowledge-bases-karpathy)

---

*由 Claude Code 輔助建立 | 2026-04*
