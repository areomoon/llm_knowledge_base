"""
ingest.py — 資料攝取模組

負責將外部資料來源（文章、論文、GitHub repo、資料集）下載並正規化，
存放至 raw/ 對應子目錄，並記錄元資料（來源 URL、時間戳記、雜湊值）。

使用方式：
    python scripts/ingest.py --type article --url <URL>
    python scripts/ingest.py --type paper --file path/to/paper.pdf
    python scripts/ingest.py --type repo --url https://github.com/user/repo
"""

import argparse
import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"

SUPPORTED_TYPES = ("article", "paper", "repo", "dataset")


def compute_hash(content: str | bytes) -> str:
    """計算內容的 SHA-256 雜湊，用於去重識別。"""
    if isinstance(content, str):
        content = content.encode()
    return hashlib.sha256(content).hexdigest()[:16]


def build_metadata(source_type: str, source: str, content_hash: str) -> dict:
    """
    建立標準化的元資料字典。

    Args:
        source_type: 資料類型，如 'article'、'paper'。
        source: 來源 URL 或檔案路徑。
        content_hash: 內容雜湊值，用於去重。

    Returns:
        包含 type、source、hash、ingested_at 的 dict。
    """
    return {
        "type": source_type,
        "source": source,
        "hash": content_hash,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }


def ingest_article(url: str) -> None:
    """
    攝取網頁文章，提取正文並存為 Markdown。

    Args:
        url: 文章的完整 URL。

    TODO:
        - 使用 requests + BeautifulSoup4 抓取 HTML
        - 使用 markdownify 將 HTML 轉換為 Markdown
        - 移除導覽列、廣告等非正文元素（Readability 演算法）
        - 儲存至 raw/articles/<hash>.md
        - 寫入對應的 <hash>.meta.json
        - 若 hash 已存在則跳過（去重）
    """
    logger.info("攝取文章：%s", url)
    # TODO: implement
    raise NotImplementedError


def ingest_paper(file_path: str) -> None:
    """
    攝取 PDF 論文，提取文字層並存為 Markdown。

    Args:
        file_path: 本地 PDF 檔案路徑。

    TODO:
        - 使用 PyMuPDF (fitz) 解析 PDF 文字
        - 識別標題、摘要、章節結構
        - 儲存至 raw/papers/<hash>.md
        - 記錄原始 PDF 路徑於 meta.json
        - 支援 arXiv URL 直接下載
    """
    logger.info("攝取論文：%s", file_path)
    # TODO: implement
    raise NotImplementedError


def ingest_repo(url: str) -> None:
    """
    攝取 GitHub repo，擷取 README、目錄結構、主要語言資訊。

    Args:
        url: GitHub repo 的 HTTPS URL。

    TODO:
        - 使用 GitHub API 取得 repo 基本資訊（stars、language、description）
        - 下載並解析 README.md
        - 列出頂層目錄結構
        - 儲存至 raw/repos/<owner>_<repo>.md
        - 記錄 API 回應快照於 meta.json
    """
    logger.info("攝取 repo：%s", url)
    # TODO: implement
    raise NotImplementedError


def ingest_dataset(url: str) -> None:
    """
    攝取資料集描述，記錄元資料（不下載完整資料集）。

    Args:
        url: HuggingFace Hub、Papers with Code 或其他資料集頁面 URL。

    TODO:
        - 解析資料集名稱、大小、授權、任務類型
        - 支援 HuggingFace Hub API
        - 儲存描述至 raw/datasets/<hash>.md
    """
    logger.info("攝取資料集：%s", url)
    # TODO: implement
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM Knowledge Base — 資料攝取工具")
    parser.add_argument("--type", choices=SUPPORTED_TYPES, required=True, help="資料來源類型")
    parser.add_argument("--url", help="來源 URL")
    parser.add_argument("--file", help="本地檔案路徑（適用 paper 類型）")
    args = parser.parse_args()

    dispatch = {
        "article": lambda: ingest_article(args.url),
        "paper": lambda: ingest_paper(args.file or args.url),
        "repo": lambda: ingest_repo(args.url),
        "dataset": lambda: ingest_dataset(args.url),
    }

    dispatch[args.type]()


if __name__ == "__main__":
    main()
