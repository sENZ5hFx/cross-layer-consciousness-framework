# Copyright (c) 2025-2026 Haley Ann Bird. All rights reserved.
# CLCE - Cross-Layer Consciousness Engine
# scripts/watermark_check.py
"""
Automated copyright header auditor.
Run from repo root: python scripts/watermark_check.py
Returns exit code 0 if all Python files have required copyright header.
Returns exit code 1 with file list if any are missing.

Also generates a WATERMARK_REPORT.md for audit trail.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

REQUIRED_HEADER_FRAGMENT = "Copyright (c) 2025-2026 Haley Ann Bird"
REPO_ROOT = Path(__file__).parent.parent
PROTOTYPE_DIR = REPO_ROOT / "prototype"
SCRIPTS_DIR = REPO_ROOT / "scripts"
REPORT_PATH = REPO_ROOT / "WATERMARK_REPORT.md"

EXCLUDE_FILES = {"__init__.py"}


def check_file(path: Path) -> bool:
    """Return True if file contains required copyright header in first 5 lines."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            head = "".join(f.readline() for _ in range(5))
        return REQUIRED_HEADER_FRAGMENT in head
    except Exception:
        return False


def get_required_header(filepath: Path) -> str:
    rel = filepath.relative_to(REPO_ROOT)
    return (
        f"# Copyright (c) 2025-2026 Haley Ann Bird. All rights reserved.\n"
        f"# CLCE\u2122 - Cross-Layer Consciousness Engine\n"
        f"# {rel}\n"
    )


def main():
    python_files = []
    for search_dir in [PROTOTYPE_DIR, SCRIPTS_DIR]:
        if search_dir.exists():
            for f in search_dir.rglob("*.py"):
                if f.name not in EXCLUDE_FILES:
                    python_files.append(f)

    missing = []
    present = []
    for f in sorted(python_files):
        if check_file(f):
            present.append(f)
        else:
            missing.append(f)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    report_lines = [
        "# CLCE™ Watermark Audit Report",
        f"\n**Run at:** {timestamp}  ",
        f"**Total Python files scanned:** {len(python_files)}  ",
        f"**Files with copyright header:** {len(present)}  ",
        f"**Files MISSING copyright header:** {len(missing)}  ",
        "\n---\n",
    ]

    if missing:
        report_lines.append("## ❌ Files Missing Copyright Header\n")
        for f in missing:
            rel = f.relative_to(REPO_ROOT)
            report_lines.append(f"- `{rel}`")
            report_lines.append(f"\n  **Required header:**\n  ```python\n  {get_required_header(f).strip()}\n  ```\n")
    else:
        report_lines.append("## ✅ All files have correct copyright headers\n")

    report_lines.append("\n---\n")
    report_lines.append("## ✅ Files With Copyright Header\n")
    for f in present:
        rel = f.relative_to(REPO_ROOT)
        report_lines.append(f"- `{rel}`")

    report_content = "\n".join(report_lines)
    REPORT_PATH.write_text(report_content, encoding="utf-8")
    print(report_content)

    if missing:
        print(f"\n[FAIL] {len(missing)} file(s) missing copyright header.")
        sys.exit(1)
    else:
        print(f"\n[PASS] All {len(present)} files have copyright headers.")
        sys.exit(0)


if __name__ == "__main__":
    main()
