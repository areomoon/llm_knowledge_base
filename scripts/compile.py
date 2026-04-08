"""
compile.py — Claude Code Agent 觸發腳本

本模組原先直接呼叫 LLM API 進行編譯，現已重構為輕量包裝器。
實際的編譯邏輯由 Claude Code Agent 依 CLAUDE.md 規範執行。

使用方式：
    # 推薦：直接使用 Claude Code（依 CLAUDE.md 規範執行完整流程）
    claude "請 compile raw/ 目錄的所有新增內容"
    claude "請 compile raw/articles/my-article.md"

    # 此腳本提供輔助功能（掃描狀態、不呼叫 LLM）
    python scripts/compile.py --status     # 顯示未處理的 raw/ 檔案清單
    python scripts/compile.py --list-raw   # 列出所有 raw/ 檔案及其狀態
"""

import argparse
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"
WIKI_DIR = Path(__file__).parent.parent / "wiki"


def get_compiled_index() -> dict:
    """讀取已編譯的檔案紀錄（.compiled_index.json）。"""
    index_path = Path(__file__).parent.parent / ".compiled_index.json"
    if index_path.exists():
        return json.loads(index_path.read_text(encoding="utf-8"))
    return {}


def list_raw_files() -> list[Path]:
    """列出 raw/ 目錄下所有 .md 和 .pdf 原始檔案。"""
    if not RAW_DIR.exists():
        return []
    return sorted(
        p for p in RAW_DIR.rglob("*")
        if p.suffix in (".md", ".pdf") and not p.name.endswith(".meta.json")
    )


def show_status() -> None:
    """顯示 raw/ 檔案的編譯狀態。"""
    compiled = get_compiled_index()
    raw_files = list_raw_files()

    if not raw_files:
        print("raw/ 目錄為空，或尚未新增任何原始資料。")
        print(f"請先執行 ingest.py 或手動將 .md 檔案放入 {RAW_DIR}/")
        return

    pending = []
    done = []

    for f in raw_files:
        rel = str(f.relative_to(Path(__file__).parent.parent))
        if rel in compiled:
            done.append((rel, compiled[rel].get("compiled_at", "未知時間")))
        else:
            pending.append(rel)

    print(f"\n=== Raw 檔案狀態 ===")
    print(f"總計：{len(raw_files)} 個 | 已編譯：{len(done)} | 待處理：{len(pending)}\n")

    if pending:
        print("【待處理（未編譯）】")
        for f in pending:
            print(f"  - {f}")
        print()
        print("提示：執行以下指令讓 Claude Code Agent 進行編譯：")
        print('  claude "請 compile raw/ 目錄的所有新增內容"')

    if done:
        print("【已編譯】")
        for f, t in done:
            print(f"  - {f}（編譯於 {t}）")


def list_raw() -> None:
    """列出所有 raw/ 檔案路徑。"""
    raw_files = list_raw_files()
    if not raw_files:
        print("raw/ 目錄為空。")
        return
    for f in raw_files:
        print(f)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LLM Knowledge Base — 編譯狀態工具（語意編譯由 Claude Code Agent 執行）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
實際編譯請使用 Claude Code Agent（依 CLAUDE.md 規範）：
  claude "請 compile raw/ 目錄的所有新增內容"
  claude "請對 wiki/ 執行 lint 健康檢查"
  claude "請回答：什麼是 RLHF？"
        """,
    )
    parser.add_argument("--status", action="store_true", help="顯示 raw/ 檔案的編譯狀態")
    parser.add_argument("--list-raw", action="store_true", help="列出所有 raw/ 檔案路徑")
    args = parser.parse_args()

    if args.list_raw:
        list_raw()
    else:
        # 預設顯示狀態
        show_status()


if __name__ == "__main__":
    main()
