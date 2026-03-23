#!/usr/bin/env python3
"""Gate to enforce proofread completion before full QA/Pandoc build."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_iso_utc(value: str) -> datetime:
    x = value.strip()
    if x.endswith("Z"):
        x = x[:-1] + "+00:00"
    dt = datetime.fromisoformat(x)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def collect_targets(paper_dir: Path) -> list[Path]:
    targets: list[Path] = []
    sections = paper_dir / "sections"
    if sections.exists():
        targets.extend(sorted([p for p in sections.glob("*.md") if p.is_file()]))
    for rel in ("design/01_requirements.md", "design/02_plan.md", "refs/references.bib"):
        p = paper_dir / rel
        if p.exists():
            targets.append(p)
    return targets


def mark(stamp_path: Path, note: str) -> int:
    stamp_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "proofread_done_at": utc_now_iso(),
        "note": note.strip(),
    }
    stamp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Proofread gate: MARKED -> {stamp_path}")
    return 0


def check(stamp_path: Path, paper_dir: Path) -> int:
    if not stamp_path.exists():
        print(
            "Proofread gate: FAIL (stamp missing). "
            "Run `$paper-proofread-all` and then `python scripts/qa_proofread_gate.py --mark`."
        )
        return 2

    try:
        payload = json.loads(stamp_path.read_text(encoding="utf-8"))
    except Exception:
        print(f"Proofread gate: FAIL (invalid stamp JSON): {stamp_path}")
        return 2

    raw_ts = str(payload.get("proofread_done_at", "")).strip()
    if not raw_ts:
        print(f"Proofread gate: FAIL (proofread_done_at missing): {stamp_path}")
        return 2

    try:
        marked_at = parse_iso_utc(raw_ts)
    except Exception:
        print(f"Proofread gate: FAIL (invalid timestamp): {raw_ts}")
        return 2

    stale: list[str] = []
    for target in collect_targets(paper_dir):
        mtime = datetime.fromtimestamp(target.stat().st_mtime, tz=timezone.utc)
        if mtime > marked_at:
            stale.append(str(target))

    if stale:
        print("Proofread gate: FAIL (content changed after proofread mark).")
        for path in stale[:30]:
            print(f"  - {path}")
        print("Run `$paper-proofread-all` again, then re-mark with --mark.")
        return 2

    print(f"Proofread gate: PASS (marked_at={marked_at.isoformat()})")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Proofread completion gate")
    parser.add_argument("--paper-dir", default=".", help="Paper workspace root")
    parser.add_argument(
        "--stamp",
        default="reports/proofread_status.json",
        help="Path to proofread stamp file from paper-dir",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--mark", action="store_true", help="Mark proofread as completed now")
    mode.add_argument("--check", action="store_true", help="Check proofread gate")
    parser.add_argument(
        "--note",
        default="",
        help="Optional note to store when marking (e.g., reviewer initials or summary)",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    paper_dir = Path(args.paper_dir).resolve()
    stamp_path = (paper_dir / args.stamp).resolve()

    if args.mark:
        return mark(stamp_path, args.note)
    return check(stamp_path, paper_dir)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
