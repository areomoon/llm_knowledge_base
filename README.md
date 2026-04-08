# LLM Knowledge Base

基於 [Andrej Karpathy LLM Knowledge Base](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 概念建立的個人 AI/Agent 研究知識庫系統。

> **Browse the wiki**: [`wiki/index.md`](wiki/index.md)

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
│   ├── articles/           # 網頁文章 (.md + .meta.json)
│   ├── papers/             # 論文 (.pdf, .md + .meta.json)
│   ├── repos/              # GitHub repo 學習筆記
│   └── datasets/           # 資料集描述與筆記
├── wiki/                   # Phase 2: LLM 編譯輸出的結構化 wiki
│   ├── index.md            # 總索引（所有概念文章的入口摘要）
│   ├── concepts/           # 概念文章（主力內容，含 backlinks）
│   ├── derived/            # 衍生產出（原始資料摘要）
│   └── queries/            # 查詢結果與 Q&A 記錄存檔
├── scripts/                # 工具腳本
│   ├── ingest.py           # 輸入處理：URL → raw/
│   └── search.py           # 全文搜尋引擎（CLI + Web UI）
├── config/
│   └── settings.yaml       # LLM API 設定、路徑設定
├── CLAUDE.md               # Claude Code Agent 操作指引（compile / lint）
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 模組說明

### `scripts/ingest.py`

- **功能**：從 URL 抓取網頁內容，轉換為 Markdown 格式存入 `raw/articles/`；支援 arXiv PDF 下載、GitHub repo 摘要
- **依賴**：`requests`, `beautifulsoup4`, `markdownify`, `arxiv`, `PyMuPDF`

### `scripts/search.py`

- **功能**：對 `wiki/` 做全文搜尋，支援 CLI 和簡易 Web UI
- **設計**：naive keyword search（仿 Karpathy 的 vibe-coded 風格），不需向量資料庫
- **依賴**：`flask`（Web UI）, `click`（CLI）

### Claude Code Agent（compile / lint）

Compile 和 Lint 任務由 Claude Code Agent 直接執行，操作規範定義於 [`CLAUDE.md`](CLAUDE.md)。

| 任務 | 執行方式 |
|------|---------|
| 編譯所有新的 raw 檔案 | 告訴 Claude Code："compile all new raw files" |
| 編譯單一檔案 | 告訴 Claude Code："compile raw/articles/abc123.md" |
| Wiki 健康檢查 | 告訴 Claude Code："lint the wiki" |

---

## 技術棧

| 類別 | 工具 |
|------|------|
| 程式語言 | Python 3.11+ |
| LLM API | Claude API（Anthropic）/ OpenAI API |
| 知識庫瀏覽 | GitHub（原生 Markdown 渲染） |
| Agent 操作指引 | CLAUDE.md（Claude Code） |
| 文件格式 | GitHub Flavored Markdown（含 YAML frontmatter） |
| 設定管理 | YAML |

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

# 4. 編譯 wiki（透過 Claude Code）
# 在 Claude Code 中執行：compile all new raw files

# 5. 搜尋
python scripts/search.py --query "transformer attention"

# 6. 健康檢查（透過 Claude Code）
# 在 Claude Code 中執行：lint the wiki
```

---

## MCP Server

The knowledge base exposes an MCP server (`mcp_server.py`) that lets Claude Desktop or Claude Code query the wiki directly.

**Tools:**
- `search_wiki(query)` — full-text search across `wiki/concepts/` and `wiki/derived/`
- `read_article(filename)` — read a specific wiki article by filename (e.g. `context-engineering.md`)

**Resources:**
- `wiki://index` — returns `wiki/index.md`

**Run the server:**

```bash
pip install -r requirements.txt
python mcp_server.py
```

**Connect to Claude Desktop** — add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "llm-knowledge-base": {
      "command": "python",
      "args": ["/path/to/llm_knowledge_base/mcp_server.py"]
    }
  }
}
```

**Connect to Claude Code** — run once in your terminal:

```bash
claude mcp add llm-knowledge-base python /path/to/llm_knowledge_base/mcp_server.py
```

---

## 參考來源

- [Andrej Karpathy — LLM Knowledge Base Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [DAIR.AI Academy — LLM Knowledge Bases (Karpathy)](https://academy.dair.ai/blog/llm-knowledge-bases-karpathy)

---

*由 Claude Code 輔助建立 | 2026-04*
