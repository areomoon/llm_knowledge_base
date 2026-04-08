# CLAUDE.md — LLM Knowledge Base

Claude Code Agent 操作手冊：本文件定義如何驅動 compile 與 lint 流程。

---

## 專案結構速覽

```
raw/          # Phase 1 輸入：網頁文章、論文、筆記
wiki/         # Phase 2 輸出：LLM 編譯的結構化 wiki
scripts/      # 四大工具腳本
config/       # settings.yaml（模型、路徑、批次設定）
.github/      # GitHub Actions 工作流程
```

---

## 核心指令

### Phase 2 — Compile（raw → wiki）

```bash
# 增量編譯所有尚未處理的 raw/ 文件
python scripts/compile.py

# 強制重新編譯（忽略 .compiled_index.json 快取）
python scripts/compile.py --force

# 限制單次批次數量（避免 API 費用失控）
python scripts/compile.py --batch 10

# 只編譯單一檔案
python scripts/compile.py --file raw/articles/some-article.md
```

### Phase 4 — Lint（wiki 健康檢查）

```bash
# 執行完整 lint 報告
python scripts/lint.py

# 自動修復斷裂的 [[internal links]]（fuzzy match）
python scripts/lint.py --fix

# 產出 Markdown 格式報告到 wiki/queries/lint-report.md
python scripts/lint.py --report

# 呼叫 LLM 建議缺失的主題（需設定 ANTHROPIC_API_KEY）
python scripts/lint.py --suggest
```

### Phase 1 — Ingest（可選，手動觸發）

```bash
python scripts/ingest.py --type article --url "https://..."
python scripts/ingest.py --type paper --file path/to/paper.pdf
python scripts/ingest.py --type repo --url "https://github.com/..."
```

### Phase 3 — Search

```bash
python scripts/search.py --query "transformer attention"
python scripts/search.py --query "RLHF" --mode rag
```

---

## Agent 工作流程

### 標準更新週期

1. **檢查 raw/ 有無新檔案**
   ```bash
   ls raw/articles/ raw/papers/ raw/repos/ raw/datasets/ 2>/dev/null
   ```

2. **執行 compile**（增量，不重複處理已知檔案）
   ```bash
   python scripts/compile.py
   ```

3. **執行 lint 確認 wiki 健康**
   ```bash
   python scripts/lint.py --report
   ```

4. **若 lint 發現問題，自動修復後再 lint 一次**
   ```bash
   python scripts/lint.py --fix
   python scripts/lint.py --report
   ```

5. **Commit 結果**
   ```bash
   git add wiki/ .compiled_index.json
   git commit -m "chore: compile & lint wiki [$(date +%Y-%m-%d)]"
   ```

---

## 環境設定

```bash
# 安裝依賴
pip install -r requirements.txt

# 必要環境變數（設於 .env 或系統環境）
export ANTHROPIC_API_KEY="sk-ant-..."
# export OPENAI_API_KEY="sk-..."  # 備用

# 驗證設定讀取正常
python -c "import yaml; print(yaml.safe_load(open('config/settings.yaml'))['llm']['model'])"
```

---

## 設定檔關鍵參數（config/settings.yaml）

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `llm.model` | `claude-opus-4-6` | 主要 LLM 模型 |
| `compile.batch_size` | `5` | 每次 compile 處理的文件數 |
| `compile.max_concepts_per_file` | `15` | 每篇原始文件最多抽取概念數 |
| `lint.fuzzy_match_threshold` | `0.85` | 自動修復連結的相似度門檻 |

---

## 重要規範

- **不要手動編輯 `wiki/concepts/`** — 由 compile.py 全權管理
- **不要刪除 `.compiled_index.json`** — 記錄已處理檔案的雜湊值，刪除會導致重複編譯
- **`raw/` 只進不出** — 原始資料永久保留，wiki 是其「編譯產物」
- **Commit 前必須 lint 通過** — CI（GitHub Actions）會在 PR 時執行 lint 檢查

---

## GitHub Actions 自動化

| Workflow | 觸發條件 | 說明 |
|----------|----------|------|
| `lint.yml` | push / PR to main | 自動執行 lint，失敗則阻擋 merge |
| `compile.yml` | 手動觸發 / 排程（每日 UTC 02:00） | 自動 compile 並 commit wiki 更新 |
