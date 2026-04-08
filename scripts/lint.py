"""
lint.py — Wiki 健康檢查輔助腳本

本模組原先直接呼叫 LLM API 進行語意分析，現已重構為輕量包裝器。
語意層面的 lint（概念不一致、建議新主題）由 Claude Code Agent 依 CLAUDE.md 規範執行。
本腳本僅處理可在本地純文字分析的部分（無需 LLM）。

使用方式：
    # 推薦：完整 lint（語意 + 結構）
    claude "請對 wiki/ 執行 lint 健康檢查"

    # 此腳本提供快速本地結構檢查（不呼叫 LLM）
    python scripts/lint.py                 # 檢查連結、孤立頁面、frontmatter
    python scripts/lint.py --broken-links  # 只檢查斷裂的相對路徑連結
    python scripts/lint.py --orphans       # 只列出孤立頁面
"""

import argparse
import logging
import re
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

WIKI_DIR = Path(__file__).parent.parent / "wiki"
MD_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FRONTMATTER_FIELDS = {"title", "tags", "created", "updated"}


def collect_wiki_pages() -> dict[str, Path]:
    """掃描 wiki/ 目錄，建立頁面名稱到路徑的映射。"""
    if not WIKI_DIR.exists():
        return {}
    pages = {}
    for p in WIKI_DIR.rglob("*.md"):
        pages[p.stem] = p
    return pages


def check_broken_links(pages: dict[str, Path]) -> list[dict]:
    """檢查所有相對路徑連結是否指向存在的檔案。"""
    broken = []
    for name, path in pages.items():
        content = path.read_text(encoding="utf-8")
        for match in MD_LINK_PATTERN.finditer(content):
            link_text, link_target = match.group(1), match.group(2)
            if link_target.startswith("http"):
                continue  # 跳過外部連結
            target_path = (path.parent / link_target).resolve()
            if not target_path.exists():
                broken.append({
                    "source": str(path.relative_to(WIKI_DIR.parent)),
                    "link_text": link_text,
                    "link_target": link_target,
                })
    return broken


def find_orphan_pages(pages: dict[str, Path]) -> list[Path]:
    """找出沒有任何其他頁面連結指向的孤立頁面（index.md 除外）。"""
    referenced: set[str] = set()
    for name, path in pages.items():
        content = path.read_text(encoding="utf-8")
        for match in MD_LINK_PATTERN.finditer(content):
            link_target = match.group(2)
            if not link_target.startswith("http"):
                target_stem = Path(link_target).stem
                referenced.add(target_stem)

    orphans = []
    for name, path in pages.items():
        if name == "index":
            continue
        if name not in referenced:
            orphans.append(path)
    return orphans


def check_frontmatter(pages: dict[str, Path]) -> list[dict]:
    """檢查概念文章是否包含必要的 frontmatter 欄位。"""
    issues = []
    concepts_dir = WIKI_DIR / "concepts"
    for name, path in pages.items():
        if not str(path).startswith(str(concepts_dir)):
            continue
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---"):
            issues.append({"page": name, "issue": "缺少 frontmatter"})
            continue
        end = content.find("---", 3)
        frontmatter_block = content[3:end] if end != -1 else ""
        for field in FRONTMATTER_FIELDS:
            if f"{field}:" not in frontmatter_block:
                issues.append({"page": name, "issue": f"frontmatter 缺少欄位：{field}"})
    return issues


def print_report(broken: list[dict], orphans: list[Path], fm_issues: list[dict]) -> None:
    """輸出檢查報告。"""
    print("\n=== Wiki 結構健康報告 ===")
    print(f"斷裂連結：{len(broken)} 處")
    print(f"孤立頁面：{len(orphans)} 篇")
    print(f"Frontmatter 問題：{len(fm_issues)} 處\n")

    if broken:
        print("【斷裂連結】")
        for b in broken:
            print(f"  {b['source']} → [{b['link_text']}]({b['link_target']}) 目標不存在")
        print()

    if orphans:
        print("【孤立頁面（無頁面連結至此）】")
        for p in orphans:
            print(f"  - {p.relative_to(WIKI_DIR.parent)}")
        print()

    if fm_issues:
        print("【Frontmatter 問題】")
        for i in fm_issues:
            print(f"  - {i['page']}：{i['issue']}")
        print()

    if not any([broken, orphans, fm_issues]):
        print("結構檢查通過！如需語意層面的 lint（概念不一致、建議新主題），請執行：")
        print('  claude "請對 wiki/ 執行 lint 健康檢查"')


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LLM Knowledge Base — Wiki 結構健康檢查（語意 lint 由 Claude Code Agent 執行）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
完整 lint（含語意分析）請使用 Claude Code Agent（依 CLAUDE.md 規範）：
  claude "請對 wiki/ 執行 lint 健康檢查"
        """,
    )
    parser.add_argument("--broken-links", action="store_true", help="只檢查斷裂的相對路徑連結")
    parser.add_argument("--orphans", action="store_true", help="只列出孤立頁面")
    args = parser.parse_args()

    pages = collect_wiki_pages()

    if not pages:
        print("wiki/ 目錄為空，尚未有任何頁面可供檢查。")
        return

    if args.broken_links:
        broken = check_broken_links(pages)
        print_report(broken, [], [])
    elif args.orphans:
        orphans = find_orphan_pages(pages)
        print_report([], orphans, [])
    else:
        broken = check_broken_links(pages)
        orphans = find_orphan_pages(pages)
        fm_issues = check_frontmatter(pages)
        print_report(broken, orphans, fm_issues)


if __name__ == "__main__":
    main()
