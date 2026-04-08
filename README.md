# LLM Knowledge Base

個人 AI/Agent 研究知識庫，基於 [Andrej Karpathy 的 LLM Knowledge Base 概念](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)建立。

> **核心理念**：LLM 扮演「編譯器」而非傳統 RAG 的角色 — 讀取原始文件 → 產出結構化 Markdown Wiki → Wiki 本身即知識庫

---

## 工作流程

```
raw/          →    Claude Code Agent    →    wiki/
(原始文件)          (compile + lint)         (結構化知識庫)
     ↑                                            |
     └──── ingest.py (抓 URL) ──── search.py ─────┘
```

| 階段 | 工具 | 說明 |
|------|------|------|
| **Ingest** | `scripts/ingest.py` | 從 URL 抓取文章/論文，存入 `raw/` |
| **Compile** | Claude Code Agent | 讀取 `raw/`，產出 `wiki/concepts/` 和 `wiki/derived/` |
| **Search** | `scripts/search.py` | 對 `wiki/` 進行全文關鍵字搜尋 |
| **Lint** | Claude Code Agent | 健康檢查：斷裂連結、孤立頁面、缺失主題建議 |

Compile 和 Lint 由 Claude Code Agent 直接執行，規則定義在 [`CLAUDE.md`](CLAUDE.md)。

---

## 目錄結構

```
llm_knowledge_base/
├── CLAUDE.md               # Agent 系統指令（wiki 格式規範、compile/lint 步驟）
├── README.md
├── requirements.txt
├── config/
│   └── settings.yaml       # LLM API 設定、路徑設定
├── raw/                    # 原始資料輸入區（不進 git）
│   ├── articles/           # 網頁文章 (.md)
│   ├── papers/             # 論文 (.pdf, .md)
│   ├── repos/              # GitHub repo 學習筆記
│   └── datasets/           # 資料集描述
├── wiki/                   # 結構化知識庫（GitHub 上可直接瀏覽）
│   ├── index.md            # 知識庫導航頁
│   ├── concepts/           # 概念文章（主力內容）
│   ├── derived/            # 文章與論文摘要
│   └── queries/            # Q&A 查詢記錄
└── scripts/
    ├── ingest.py           # 從 URL 抓取原始資料
    ├── compile.py          # 輔助工具：列出待編譯檔案
    ├── search.py           # 全文關鍵字搜尋
    └── lint.py             # 輔助工具：掃描斷裂連結
```

---

## 快速開始

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 設定 API 金鑰
export ANTHROPIC_API_KEY=your_key_here

# 3. 抓取一篇文章
python scripts/ingest.py --type article --url "https://example.com/article"

# 4. 讓 Agent 編譯（在 Claude Code 中執行）
# > compile

# 5. 搜尋
python scripts/search.py --query "transformer attention"

# 6. 健康檢查（在 Claude Code 中執行）
# > lint
```

---

## 瀏覽知識庫

知識庫 Markdown 針對 **GitHub Flavored Markdown** 優化，可直接在 GitHub 上瀏覽：

- **導航頁**：[`wiki/index.md`](wiki/index.md)
- **概念文章**：[`wiki/concepts/`](wiki/concepts/)
- **論文與文章摘要**：[`wiki/derived/`](wiki/derived/)
- **查詢記錄**：[`wiki/queries/`](wiki/queries/)

---

## 技術棧

| 類別 | 工具 |
|------|------|
| 語言 | Python 3.11+ |
| LLM API | Claude API (Anthropic) |
| 知識庫格式 | Markdown (GFM + YAML frontmatter) |
| 主要介面 | GitHub |
| 搜尋 | BM25 (`rank-bm25`) |
| 文件解析 | `beautifulsoup4`, `markdownify`, `PyMuPDF` |

---

## 參考來源

- [Andrej Karpathy — LLM Knowledge Base Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [DAIR.AI Academy — LLM Knowledge Bases](https://academy.dair.ai/blog/llm-knowledge-bases-karpathy)

---

*由 Claude Code 輔助建立與維護 | 2026-04*
