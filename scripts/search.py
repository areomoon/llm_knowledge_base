"""
search.py — Wiki 全文關鍵字搜尋

對 wiki/ 目錄下所有 Markdown 文件進行全文搜尋。
使用 BM25 排序（rank-bm25），支援 CLI 操作。

使用方式：
    python scripts/search.py --query "transformer attention"
    python scripts/search.py --query "RLHF" --top-k 10
    python scripts/search.py --query "fine-tuning" --json
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

WIKI_DIR = Path(__file__).parent.parent / "wiki"
CONTEXT_LINES = 2  # 匹配行前後各顯示幾行


def load_wiki_docs() -> list[dict[str, Any]]:
    """載入 wiki/ 中所有 .md 文件，回傳文件列表。"""
    if not WIKI_DIR.exists():
        logger.error("wiki/ 目錄不存在：%s", WIKI_DIR)
        return []

    docs = []
    for md_path in sorted(WIKI_DIR.rglob("*.md")):
        content = md_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        # 取第一個 H1 作為標題，否則用檔名
        title = md_path.stem
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break
        docs.append({
            "path": md_path,
            "rel_path": str(md_path.relative_to(WIKI_DIR.parent)),
            "title": title,
            "content": content,
            "lines": lines,
        })
    return docs


def tokenize(text: str) -> list[str]:
    """簡單的 tokenizer：轉小寫、取英數字詞彙。"""
    return re.findall(r"[a-z0-9\u4e00-\u9fff]+", text.lower())


def keyword_search(query: str, top_k: int = 10) -> list[dict[str, Any]]:
    """
    對 wiki/ 進行 BM25 全文關鍵字搜尋。

    若 rank_bm25 未安裝，退回簡單的 TF 計數排序。
    """
    docs = load_wiki_docs()
    if not docs:
        return []

    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    # 嘗試使用 BM25
    try:
        from rank_bm25 import BM25Okapi
        corpus = [tokenize(doc["content"]) for doc in docs]
        bm25 = BM25Okapi(corpus)
        scores = bm25.get_scores(query_tokens)
    except ImportError:
        logger.warning("rank_bm25 未安裝，退回簡單 TF 計數。pip install rank-bm25")
        scores = []
        for doc in docs:
            tokens = tokenize(doc["content"])
            score = sum(tokens.count(t) for t in query_tokens)
            scores.append(score)

    # 取得排序後的前 top_k 個結果（過濾分數為 0 的）
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    ranked = [(i, s) for i, s in ranked if s > 0][:top_k]

    results = []
    query_pattern = re.compile(
        "|".join(re.escape(t) for t in query_tokens), re.IGNORECASE
    )

    for idx, score in ranked:
        doc = docs[idx]
        matched_lines = find_matched_lines(doc["lines"], query_pattern)
        results.append({
            "score": round(float(score), 4),
            "title": doc["title"],
            "rel_path": doc["rel_path"],
            "matched_lines": matched_lines,
        })

    return results


def find_matched_lines(
    lines: list[str], pattern: re.Pattern, max_matches: int = 3
) -> list[dict[str, Any]]:
    """找出包含匹配關鍵字的行及其上下文。"""
    matches = []
    seen_lines: set[int] = set()

    for i, line in enumerate(lines):
        if pattern.search(line) and i not in seen_lines:
            start = max(0, i - CONTEXT_LINES)
            end = min(len(lines) - 1, i + CONTEXT_LINES)
            context = lines[start : end + 1]
            # 標記匹配行在 context 中的位置
            highlight_idx = i - start
            matches.append({
                "line_no": i + 1,
                "context": context,
                "highlight": highlight_idx,
            })
            # 將已包含在 context 中的行標記為已見
            seen_lines.update(range(start, end + 1))

            if len(matches) >= max_matches:
                break

    return matches


def format_results(results: list[dict[str, Any]], query: str) -> str:
    """將搜尋結果格式化為可讀的 CLI 輸出。"""
    if not results:
        return f'找不到符合「{query}」的結果。'

    query_pattern = re.compile(
        "|".join(re.escape(t) for t in tokenize(query)), re.IGNORECASE
    )
    output_lines = [f'搜尋「{query}」— 找到 {len(results)} 個結果\n{"=" * 50}']

    for i, result in enumerate(results, 1):
        output_lines.append(
            f"\n[{i}] {result['title']}\n    {result['rel_path']}  (score: {result['score']})"
        )
        for match in result["matched_lines"]:
            output_lines.append(f"    ── 第 {match['line_no']} 行 ──")
            for j, ctx_line in enumerate(match["context"]):
                prefix = "  > " if j == match["highlight"] else "    "
                # 簡單高亮（終端機粗體）
                highlighted = query_pattern.sub(lambda m: f"\033[1m{m.group()}\033[0m", ctx_line)
                output_lines.append(f"    {prefix}{highlighted}")

    return "\n".join(output_lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM Knowledge Base — Wiki 全文搜尋")
    parser.add_argument("--query", "-q", required=True, help="搜尋關鍵字")
    parser.add_argument("--top-k", type=int, default=5, help="回傳結果數量（預設：5）")
    parser.add_argument("--json", action="store_true", dest="as_json", help="以 JSON 格式輸出")
    args = parser.parse_args()

    results = keyword_search(args.query, args.top_k)

    if args.as_json:
        # JSON 輸出時移除 matched_lines 中的 context（避免過長）
        output = [
            {k: v for k, v in r.items() if k != "matched_lines"} for r in results
        ]
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(format_results(results, args.query))

    sys.exit(0 if results else 1)


if __name__ == "__main__":
    main()
