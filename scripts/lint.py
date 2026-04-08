"""
lint.py — Wiki 品質檢查模組

掃描 wiki/ 目錄，偵測知識庫中的常見問題並產出健康報告：
- 斷裂的 [[internal links]]
- 孤立文章（無任何其他頁面連結至此）
- 概念文章間矛盾或不一致的描述
- 缺失 backlinks
- 建議應新建的概念文章主題

使用方式：
    python scripts/lint.py                    # 執行完整品質檢查
    python scripts/lint.py --fix links        # 嘗試自動修復斷裂連結
    python scripts/lint.py --report           # 僅輸出報告（不修復）
    python scripts/lint.py --suggest          # 用 LLM 建議缺失的概念主題
"""

import argparse
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

WIKI_DIR = Path(__file__).parent.parent / "wiki"
INTERNAL_LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass
class LintReport:
    """品質檢查報告的資料結構。"""
    broken_links: list[dict] = field(default_factory=list)
    orphan_pages: list[Path] = field(default_factory=list)
    missing_backlinks: list[dict] = field(default_factory=list)
    suggested_topics: list[str] = field(default_factory=list)
    total_pages: int = 0
    total_links: int = 0

    def summary(self) -> str:
        """生成報告摘要字串。"""
        lines = [
            "=== Wiki 健康報告 ===",
            f"總頁數：{self.total_pages}",
            f"總連結數：{self.total_links}",
            f"斷裂連結：{len(self.broken_links)}",
            f"孤立頁面：{len(self.orphan_pages)}",
            f"缺失 backlinks：{len(self.missing_backlinks)}",
            f"建議新增主題：{len(self.suggested_topics)}",
        ]
        return "\n".join(lines)


def collect_all_pages() -> dict[str, Path]:
    """
    掃描 wiki/ 目錄，建立頁面名稱到路徑的映射。

    Returns:
        dict，key 為頁面標題（不含副檔名），value 為完整路徑。

    TODO:
        - 遞迴掃描 wiki/concepts/ 與 wiki/derived/
        - 正規化頁面名稱（大小寫、空格與底線互換）
        - 處理同名頁面的衝突警告
    """
    # TODO: implement
    raise NotImplementedError


def check_broken_links(pages: dict[str, Path]) -> list[dict]:
    """
    檢查所有 [[internal links]] 是否指向存在的頁面。

    Args:
        pages: collect_all_pages() 的回傳值。

    Returns:
        斷裂連結列表，每項包含：source_page、link_target、line_number。

    TODO:
        - 讀取每個 .md 檔案
        - 用 INTERNAL_LINK_PATTERN 提取所有 [[連結]]
        - 查詢 pages dict 確認目標存在
        - 記錄所有不存在的連結目標
    """
    # TODO: implement
    raise NotImplementedError


def find_orphan_pages(pages: dict[str, Path]) -> list[Path]:
    """
    找出沒有任何其他頁面連結指向的孤立頁面。

    Args:
        pages: collect_all_pages() 的回傳值。

    Returns:
        孤立頁面的路徑列表。

    TODO:
        - 建立反向連結圖（每個頁面被哪些頁面引用）
        - 找出入度為 0 的頁面（wiki/index.md 除外）
        - 孤立頁面可能需要被刪除或補充連結
    """
    # TODO: implement
    raise NotImplementedError


def check_missing_backlinks(pages: dict[str, Path]) -> list[dict]:
    """
    檢查若 A 連結 B，但 B 的 backlinks 區塊未列出 A，則標記缺失。

    Args:
        pages: collect_all_pages() 的回傳值。

    Returns:
        缺失 backlink 的列表，每項包含：page、missing_backlink_from。

    TODO:
        - 建立完整的雙向連結圖
        - 比對每個頁面的 ## Backlinks 區塊與實際引用關係
        - 回傳需補充 backlink 的頁面清單
    """
    # TODO: implement
    raise NotImplementedError


def suggest_missing_topics(pages: dict[str, Path]) -> list[str]:
    """
    呼叫 LLM 分析現有概念頁，建議應補充的缺失主題。

    Args:
        pages: collect_all_pages() 的回傳值。

    Returns:
        建議主題的字串列表。

    TODO:
        - 提取現有概念頁的標題列表
        - 建構 prompt：「以下是現有概念頁，根據 AI/LLM 領域知識，建議 10 個重要但缺失的主題」
        - 呼叫 LLM API 取得建議
        - 回傳格式化的建議主題列表
    """
    # TODO: implement
    raise NotImplementedError


def fix_broken_links(broken: list[dict]) -> None:
    """
    嘗試自動修復斷裂連結（重新命名或移除）。

    Args:
        broken: check_broken_links() 的回傳值。

    TODO:
        - 模糊比對：找到最相近的現有頁面名稱
        - 若有高信心的匹配，自動替換連結目標
        - 若無匹配，標記為待人工處理
        - 修改前備份原始檔案
    """
    logger.info("嘗試修復 %d 個斷裂連結", len(broken))
    # TODO: implement
    raise NotImplementedError


def run_lint(fix_mode: str | None = None, suggest: bool = False) -> LintReport:
    """
    執行完整的品質檢查流程。

    Args:
        fix_mode: 若非 None，指定自動修復的類型（'links'）。
        suggest: 若為 True，呼叫 LLM 建議缺失主題。

    Returns:
        完整的 LintReport 物件。
    """
    logger.info("開始掃描 wiki/...")
    pages = collect_all_pages()
    report = LintReport(total_pages=len(pages))

    report.broken_links = check_broken_links(pages)
    report.orphan_pages = find_orphan_pages(pages)
    report.missing_backlinks = check_missing_backlinks(pages)

    if suggest:
        report.suggested_topics = suggest_missing_topics(pages)

    if fix_mode == "links" and report.broken_links:
        fix_broken_links(report.broken_links)

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM Knowledge Base — Wiki 品質檢查工具")
    parser.add_argument("--fix", metavar="TARGET", help="自動修復特定問題（目前支援：links）")
    parser.add_argument("--report", action="store_true", help="僅輸出報告，不執行修復")
    parser.add_argument("--suggest", action="store_true", help="用 LLM 建議缺失的概念主題")
    args = parser.parse_args()

    fix_mode = None if args.report else args.fix
    report = run_lint(fix_mode=fix_mode, suggest=args.suggest)
    print(report.summary())


if __name__ == "__main__":
    main()
