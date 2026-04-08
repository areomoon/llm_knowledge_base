"""
search.py — 搜尋與查詢模組

提供對 wiki/ 知識庫的語意搜尋（向量索引）與關鍵字搜尋，
並支援自然語言問答（RAG 模式：先檢索相關片段，再由 LLM 生成答案）。

使用方式：
    python scripts/search.py --query "什麼是 RLHF？"
    python scripts/search.py --query "Transformer attention" --mode keyword
    python scripts/search.py --query "比較 LoRA 與全參數微調" --mode rag
    python scripts/search.py --reindex          # 重建向量索引
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

WIKI_DIR = Path(__file__).parent.parent / "wiki"
INDEX_PATH = Path(__file__).parent.parent / ".index"  # 向量索引快取目錄

SEARCH_MODES = ("semantic", "keyword", "rag")


def build_vector_index(force: bool = False) -> Any:
    """
    建立或載入 wiki/ 文件的向量索引。

    Args:
        force: 若為 True，強制重建索引（即使已存在）。

    Returns:
        已載入的向量索引物件（FAISS Index 或 ChromaDB Collection）。

    TODO:
        - 掃描 wiki/concepts/ 與 wiki/derived/ 下所有 .md 檔案
        - 使用 embedding model（如 text-embedding-3-small）對每個文件分塊
        - 建立 FAISS 或 ChromaDB 索引，儲存至 .index/
        - 若 .index/ 已存在且文件未變更，直接載入（快取）
        - 回傳索引物件供後續查詢使用
    """
    logger.info("建立向量索引（force=%s）", force)
    # TODO: implement
    raise NotImplementedError


def semantic_search(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """
    對知識庫進行語意相似度搜尋。

    Args:
        query: 自然語言查詢字串。
        top_k: 回傳最相關的前 k 個結果。

    Returns:
        結果列表，每項包含：score、title、excerpt、source_path。

    TODO:
        - 將 query 轉換為 embedding 向量
        - 在向量索引中執行近鄰搜尋
        - 回傳相關分塊及其來源檔案資訊
        - 格式化輸出供 CLI 顯示或 RAG 使用
    """
    # TODO: implement
    raise NotImplementedError


def keyword_search(query: str, top_k: int = 10) -> list[dict[str, Any]]:
    """
    對知識庫進行全文關鍵字搜尋（BM25 或簡單字串比對）。

    Args:
        query: 搜尋關鍵字（支援多詞）。
        top_k: 回傳最多 k 個結果。

    Returns:
        結果列表，每項包含：title、matched_lines、source_path。

    TODO:
        - 掃描 wiki/ 所有 .md 檔案
        - 實作 BM25 排序（或使用 rank_bm25 套件）
        - 回傳含匹配行上下文的結果
        - 支援大小寫不敏感、繁簡中文搜尋
    """
    # TODO: implement
    raise NotImplementedError


def rag_query(question: str, top_k: int = 5) -> str:
    """
    以 RAG 模式回答問題：先檢索相關知識片段，再由 LLM 生成答案。

    Args:
        question: 使用者的自然語言問題。
        top_k: 檢索的相關片段數量。

    Returns:
        LLM 生成的答案，附帶引用來源。

    TODO:
        - 呼叫 semantic_search() 取得相關知識片段
        - 組裝 context prompt（系統角色 + 知識片段 + 問題）
        - 呼叫 compile.call_llm() 生成答案
        - 在回答末尾附上來源引用（[1] title — path）
        - 將問答記錄至 wiki/queries/<timestamp>.md
    """
    # TODO: implement
    raise NotImplementedError


def format_results(results: list[dict], mode: str) -> str:
    """
    將搜尋結果格式化為可讀的 CLI 輸出。

    Args:
        results: semantic_search() 或 keyword_search() 的回傳值。
        mode: 搜尋模式，影響顯示格式。

    Returns:
        格式化後的字串，供直接印出。

    TODO:
        - 語意搜尋：顯示相似度分數、標題、摘錄
        - 關鍵字搜尋：高亮匹配關鍵字
        - 支援 --json 旗標輸出原始 JSON
    """
    # TODO: implement
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM Knowledge Base — 搜尋與查詢工具")
    parser.add_argument("--query", "-q", required=False, help="搜尋或查詢字串")
    parser.add_argument("--mode", choices=SEARCH_MODES, default="semantic", help="搜尋模式（預設：semantic）")
    parser.add_argument("--top-k", type=int, default=5, help="回傳結果數量（預設：5）")
    parser.add_argument("--reindex", action="store_true", help="重建向量索引")
    parser.add_argument("--json", action="store_true", dest="as_json", help="以 JSON 格式輸出")
    args = parser.parse_args()

    if args.reindex:
        build_vector_index(force=True)
        return

    if not args.query:
        parser.error("請提供 --query 參數或使用 --reindex 重建索引")

    if args.mode == "semantic":
        results = semantic_search(args.query, args.top_k)
        print(format_results(results, "semantic"))
    elif args.mode == "keyword":
        results = keyword_search(args.query, args.top_k)
        print(format_results(results, "keyword"))
    elif args.mode == "rag":
        answer = rag_query(args.query, args.top_k)
        print(answer)


if __name__ == "__main__":
    main()
