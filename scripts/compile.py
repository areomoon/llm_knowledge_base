"""
compile.py — LLM 編譯模組

讀取 raw/ 目錄下的原始資料，呼叫 LLM API 進行摘要、概念提取與索引生成，
將結果寫入 wiki/ 對應子目錄，並維護 wiki/index.md 總索引。

使用方式：
    python scripts/compile.py --all              # 編譯所有未處理的原始資料
    python scripts/compile.py --file raw/articles/abc123.md
    python scripts/compile.py --type concepts    # 只重新生成概念頁
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"
WIKI_DIR = Path(__file__).parent.parent / "wiki"


def load_settings() -> dict:
    """
    載入 config/settings.yaml 設定檔。

    TODO:
        - 使用 PyYAML 解析設定
        - 驗證必要欄位（api_key、model、max_tokens）
        - 支援環境變數覆蓋（如 LLM_API_KEY）
    """
    # TODO: implement
    return {}


def call_llm(prompt: str, system: str = "", settings: dict | None = None) -> str:
    """
    呼叫 LLM API 並回傳生成文字。

    Args:
        prompt: 使用者輸入的 prompt。
        system: 系統提示詞（角色定義、輸出格式要求）。
        settings: 覆蓋預設設定的參數（model、temperature 等）。

    Returns:
        LLM 回應的純文字內容。

    TODO:
        - 支援 Anthropic Claude API（首選）
        - 支援 OpenAI API（備援）
        - 實作指數退避重試（最多 3 次）
        - 記錄 token 用量至 compile log
    """
    # TODO: implement
    raise NotImplementedError


def summarize(raw_text: str, source_type: str) -> str:
    """
    對原始文字進行摘要，生成結構化的知識卡片。

    Args:
        raw_text: 原始文章或論文文字。
        source_type: 'article'、'paper'、'repo' 或 'dataset'。

    Returns:
        Markdown 格式的摘要，包含：TL;DR、關鍵點、相關概念標籤。

    TODO:
        - 根據 source_type 選擇不同的摘要 prompt 模板
        - 論文額外提取：方法論、實驗結果、侷限性
        - 輸出格式符合 wiki/derived/ 規範
    """
    # TODO: implement
    raise NotImplementedError


def extract_concepts(raw_text: str) -> list[dict[str, Any]]:
    """
    從文字中提取核心 AI/LLM 概念，生成概念條目。

    Args:
        raw_text: 原始或已摘要的文字。

    Returns:
        概念列表，每個概念包含：name、definition、related_concepts、sources。

    TODO:
        - 識別專有名詞（模型名稱、技術術語、縮寫）
        - 與 wiki/concepts/ 現有條目合併（避免重複）
        - 輸出 JSON 格式供後續寫入 wiki/concepts/<concept>.md
    """
    # TODO: implement
    raise NotImplementedError


def update_index(new_entries: list[dict]) -> None:
    """
    將新編譯的條目更新至 wiki/index.md 總索引。

    Args:
        new_entries: 新增條目的列表，每項包含 title、path、tags、date。

    TODO:
        - 讀取現有 index.md
        - 依類型（概念、文章摘要、論文摘要）分節插入
        - 依日期降序排列
        - 生成統計摘要（總條目數、各類型數量）
    """
    index_path = WIKI_DIR / "index.md"
    logger.info("更新索引：%s", index_path)
    # TODO: implement
    raise NotImplementedError


def compile_file(raw_path: Path) -> None:
    """
    編譯單一原始檔案，產出摘要與概念到 wiki/。

    Args:
        raw_path: raw/ 目錄下的原始 Markdown 檔案路徑。

    TODO:
        - 讀取 raw_path 及其對應的 .meta.json
        - 呼叫 summarize() 生成摘要，寫入 wiki/derived/
        - 呼叫 extract_concepts() 更新 wiki/concepts/
        - 在 meta.json 標記 compiled_at 時間戳記
        - 更新 wiki/index.md
    """
    logger.info("編譯：%s", raw_path)
    # TODO: implement
    raise NotImplementedError


def compile_all() -> None:
    """
    掃描 raw/ 目錄，編譯所有尚未處理或已更新的原始資料。

    TODO:
        - 比對 raw/*.meta.json 中的 hash 與 compiled_at
        - 跳過已是最新的條目（增量更新）
        - 並行處理（asyncio 或 ThreadPoolExecutor）
        - 編譯完成後輸出統計報告
    """
    logger.info("開始全量編譯...")
    # TODO: implement
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM Knowledge Base — LLM 編譯工具")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="編譯所有未處理的原始資料")
    group.add_argument("--file", help="指定單一原始檔案路徑")
    group.add_argument("--type", choices=["concepts", "derived", "index"], help="只重新生成特定類型")
    args = parser.parse_args()

    if args.all:
        compile_all()
    elif args.file:
        compile_file(Path(args.file))
    elif args.type:
        logger.info("重新生成類型：%s", args.type)
        # TODO: dispatch to type-specific rebuild functions


if __name__ == "__main__":
    main()
