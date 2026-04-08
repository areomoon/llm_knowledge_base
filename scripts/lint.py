"""
lint.py — Wiki 連結掃描工具

掃描 wiki/ 目錄，偵測斷裂的 Markdown 連結與孤立頁面。
輸出問題報告供 Claude Code Agent 參考修復。

LLM 驅動的品質建議（缺失主題、概念合併）由 Agent 執行（見 CLAUDE.md）。

使用方式：
    python scripts/lint.py              # 執行完整連結掃描
    python scripts/lint.py --verbose    # 顯示所有已驗證的連結
"""

import argparse
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

WIKI_DIR = Path(__file__).parent.parent / "wiki"
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)


@dataclass
class LintReport:
    broken_links: list[dict] = field(default_factory=list)
    orphan_pages: list[Path] = field(default_factory=list)
    missing_index_entries: list[Path] = field(default_factory=list)
    total_pages: int = 0
    total_links: int = 0
    checked_links: int = 0

    def summary(self) -> str:
        lines = [
            "=== Wiki 健康報告 ===",
            f"掃描頁面：{self.total_pages}",
            f"掃描連結：{self.total_links}（相對連結 {self.checked_links} 個）",
            f"斷裂連結：{len(self.broken_links)}",
            f"孤立頁面：{len(self.orphan_pages)}",
            f"索引缺漏：{len(self.missing_index_entries)}",
        ]
        return "\n".join(lines)


def collect_wiki_pages() -> dict[Path, str]:
    """回傳 wiki/ 中所有 .md 檔案的路徑 → 內容映射。"""
    if not WIKI_DIR.exists():
        return {}
    return {
        p: p.read_text(encoding="utf-8")
        for p in sorted(WIKI_DIR.rglob("*.md"))
    }


def check_broken_links(pages: dict[Path, str], verbose: bool = False) -> tuple[list[dict], int, int]:
    """
    掃描所有頁面的 Markdown 連結，回傳斷裂連結列表。

    只檢查相對路徑連結（跳過 http:// 和錨點 #）。
    """
    broken: list[dict] = []
    total_links = 0
    checked_links = 0

    for page_path, content in pages.items():
        for match in MARKDOWN_LINK_RE.finditer(content):
            link_text, link_target = match.group(1), match.group(2)
            total_links += 1

            # 跳過外部 URL 和純錨點
            if link_target.startswith(("http://", "https://", "mailto:", "#")):
                continue

            # 處理錨點部分（如 file.md#section）
            target_path_str = link_target.split("#")[0]
            if not target_path_str:
                continue

            checked_links += 1
            target_path = (page_path.parent / target_path_str).resolve()

            if not target_path.exists():
                broken.append({
                    "source": str(page_path.relative_to(WIKI_DIR.parent)),
                    "link_text": link_text,
                    "link_target": link_target,
                })
                if not verbose:
                    logger.warning("斷裂連結：%s → %s (在 %s)",
                                   link_text, link_target,
                                   page_path.relative_to(WIKI_DIR.parent))
            elif verbose:
                logger.info("  OK  %s → %s", link_text, link_target)

    return broken, total_links, checked_links


def find_orphan_pages(pages: dict[Path, str]) -> list[Path]:
    """
    找出沒有任何其他頁面連結指向的孤立頁面（排除 index.md）。
    """
    index_md = WIKI_DIR / "index.md"
    candidate_pages = {p for p in pages if p != index_md}
    referenced: set[Path] = set()

    for page_path, content in pages.items():
        for match in MARKDOWN_LINK_RE.finditer(content):
            link_target = match.group(2).split("#")[0]
            if not link_target or link_target.startswith(("http://", "https://")):
                continue
            resolved = (page_path.parent / link_target).resolve()
            referenced.add(resolved)

    return sorted(p for p in candidate_pages if p.resolve() not in referenced)


def find_missing_index_entries(pages: dict[Path, str]) -> list[Path]:
    """
    找出 wiki/concepts/ 和 wiki/derived/ 中未出現在 index.md 的檔案。
    """
    index_path = WIKI_DIR / "index.md"
    if not index_path.exists():
        return []

    index_content = index_path.read_text(encoding="utf-8")
    missing: list[Path] = []

    for subdir in ("concepts", "derived"):
        subdir_path = WIKI_DIR / subdir
        if not subdir_path.exists():
            continue
        for md_file in sorted(subdir_path.glob("*.md")):
            # 確認檔案相對路徑或名稱有出現在 index.md 中
            rel_path = md_file.relative_to(WIKI_DIR)
            if str(rel_path) not in index_content and md_file.stem not in index_content:
                missing.append(md_file)

    return missing


def run_lint(verbose: bool = False) -> LintReport:
    """執行完整的連結掃描並回傳報告。"""
    logger.info("掃描 %s ...", WIKI_DIR)
    pages = collect_wiki_pages()

    report = LintReport(total_pages=len(pages))

    broken, total_links, checked = check_broken_links(pages, verbose=verbose)
    report.broken_links = broken
    report.total_links = total_links
    report.checked_links = checked

    report.orphan_pages = find_orphan_pages(pages)
    report.missing_index_entries = find_missing_index_entries(pages)

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM Knowledge Base — Wiki 連結掃描工具")
    parser.add_argument("--verbose", "-v", action="store_true", help="顯示所有已驗證的連結")
    args = parser.parse_args()

    report = run_lint(verbose=args.verbose)
    print(report.summary())

    if report.broken_links:
        print("\n--- 斷裂連結 ---")
        for item in report.broken_links:
            print(f"  {item['source']}: [{item['link_text']}]({item['link_target']})")

    if report.orphan_pages:
        print("\n--- 孤立頁面 ---")
        for p in report.orphan_pages:
            print(f"  {p.relative_to(WIKI_DIR.parent)}")

    if report.missing_index_entries:
        print("\n--- 索引缺漏 ---")
        for p in report.missing_index_entries:
            print(f"  {p.relative_to(WIKI_DIR.parent)}")

    if not any([report.broken_links, report.orphan_pages, report.missing_index_entries]):
        print("\n✓ 所有檢查通過。")
    else:
        print("\n提示：在 Claude Code 中執行 `lint --fix` 讓 Agent 修復上述問題。")


if __name__ == "__main__":
    main()
