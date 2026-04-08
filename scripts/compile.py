"""
compile.py — 待編譯檔案狀態工具

列出 raw/ 中尚未編譯的原始檔案，供 Claude Code Agent 參考。
實際的編譯工作由 Agent 執行（見 CLAUDE.md）。

使用方式：
    python scripts/compile.py --status     # 列出所有待編譯檔案
    python scripts/compile.py --all        # 列出所有原始檔案（含已編譯）
"""

import argparse
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"


def get_raw_files() -> list[Path]:
    """掃描 raw/ 目錄，回傳所有 .md 原始檔案（排除 .meta.json）。"""
    if not RAW_DIR.exists():
        return []
    return sorted(p for p in RAW_DIR.rglob("*.md") if not p.name.endswith(".meta.json"))


def is_compiled(raw_path: Path) -> bool:
    """檢查原始檔案是否已有 compiled_at 紀錄。"""
    meta_path = raw_path.with_suffix(".meta.json")
    if not meta_path.exists():
        return False
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        return bool(meta.get("compiled_at"))
    except (json.JSONDecodeError, OSError):
        return False


def print_status(show_all: bool = False) -> None:
    """印出原始檔案的編譯狀態。"""
    files = get_raw_files()
    if not files:
        print("raw/ 目錄為空，尚無原始檔案。")
        print(f"提示：使用 python scripts/ingest.py --type article --url <URL> 新增文章。")
        return

    pending = [f for f in files if not is_compiled(f)]
    done = [f for f in files if is_compiled(f)]

    if show_all:
        print(f"\n=== 所有原始檔案 ({len(files)} 筆) ===")
        for f in files:
            status = "✓ 已編譯" if is_compiled(f) else "○ 待編譯"
            print(f"  {status}  {f.relative_to(RAW_DIR.parent)}")
    else:
        print(f"\n=== 待編譯檔案 ({len(pending)} / {len(files)} 筆) ===")
        if not pending:
            print("  所有檔案均已編譯。")
        for f in pending:
            print(f"  {f.relative_to(RAW_DIR.parent)}")

    print(f"\n已編譯：{len(done)} 筆 | 待編譯：{len(pending)} 筆")
    if pending:
        print("提示：在 Claude Code 中執行 `compile` 讓 Agent 處理待編譯檔案。")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LLM Knowledge Base — 待編譯檔案狀態工具"
    )
    parser.add_argument(
        "--status", action="store_true", default=True,
        help="列出待編譯的原始檔案（預設行為）"
    )
    parser.add_argument(
        "--all", action="store_true", dest="show_all",
        help="列出所有原始檔案（含已編譯）"
    )
    args = parser.parse_args()
    print_status(show_all=args.show_all)


if __name__ == "__main__":
    main()
