#!/usr/bin/env python3
"""Update root AGENTS.md auto-rules block from governance/preference_log.csv."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
import re
import sys
import unicodedata

AUTO_SECTION_TITLE = "## Auto-updated preferences"
BEGIN_MARKER = "<!-- BEGIN AUTO_RULES -->"
END_MARKER = "<!-- END AUTO_RULES -->"

REQUIRED_HEADERS = [
    "timestamp",
    "paper_id",
    "section",
    "category",
    "before_text",
    "after_text",
    "reason",
    "next_rule",
    "scope",
    "target_file",
    "status",
    "reviewer",
]

RULE_LINE_RE = re.compile(r"^\d+\.\s+\[(?P<category>[^\]]+)\]\s+(?P<rule>.+)$")


@dataclass
class LogEntry:
    timestamp_raw: str
    timestamp: datetime | None
    scope: str
    status: str
    category: str
    rule_text: str
    rule_key: str


@dataclass
class RuleAggregate:
    rule_text: str
    categories: Counter[str] = field(default_factory=Counter)
    scopes: Counter[str] = field(default_factory=Counter)
    evidence_count: int = 0
    adopted_count: int = 0
    candidate_count: int = 0

    def add(self, entry: LogEntry) -> None:
        self.categories[entry.category] += 1
        self.scopes[entry.scope] += 1
        self.evidence_count += 1
        if entry.status == "adopted":
            self.adopted_count += 1
        elif entry.status == "candidate":
            self.candidate_count += 1

    @property
    def primary_category(self) -> str:
        if not self.categories:
            return "uncategorized"
        return self.categories.most_common(1)[0][0]

    @property
    def main_scope(self) -> str:
        if not self.scopes:
            return "unknown"
        return ", ".join(scope for scope, _ in self.scopes.most_common())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update root AGENTS.md auto-rules from governance/preference_log.csv."
    )
    parser.add_argument("--project-root", default=".", help="Project root path.")
    parser.add_argument("--days", type=int, default=30, help="Recent-day window for candidates.")
    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
        help="Minimum frequency in the recent window for candidate rules.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes only (no file writes).",
    )
    parser.add_argument(
        "--include-paper-rules",
        action="store_true",
        help="Also consider paper-scope rules for promotion.",
    )
    return parser.parse_args()


def parse_timestamp(raw: str) -> datetime | None:
    text = (raw or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is not None:
            return parsed.astimezone().replace(tzinfo=None)
        return parsed
    except ValueError:
        pass
    formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d",
        "%Y%m%d",
    )
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def normalize_rule_text(text: str) -> str:
    s = unicodedata.normalize("NFKC", text or "").strip()
    if not s:
        return ""
    translate_table = str.maketrans(
        {
            "、": ",",
            "。": ".",
            "，": ",",
            "．": ".",
            "；": ";",
            "：": ":",
        }
    )
    s = s.translate(translate_table)
    s = re.sub(r"\s*([,.;:])\s*", r"\1 ", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.strip(" .,;:")
    return s


def rule_key_from_text(text: str) -> str:
    return normalize_rule_text(text).casefold()


def load_log_entries(csv_path: Path) -> tuple[list[LogEntry], Counter[str]]:
    exclusions: Counter[str] = Counter()
    entries: list[LogEntry] = []

    if not csv_path.exists():
        raise FileNotFoundError(f"Preference log not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        missing = [h for h in REQUIRED_HEADERS if h not in fieldnames]
        if missing:
            raise ValueError(f"Missing CSV headers: {', '.join(missing)}")

        for row in reader:
            status = (row.get("status") or "").strip().lower()
            scope = (row.get("scope") or "").strip().lower()
            category = normalize_rule_text(row.get("category") or "") or "uncategorized"
            normalized_rule = normalize_rule_text(row.get("next_rule") or "")

            if status == "rejected":
                exclusions["rejected"] += 1
                continue
            if not normalized_rule:
                exclusions["empty_next_rule"] += 1
                continue
            if status not in {"candidate", "adopted"}:
                exclusions["unknown_status"] += 1
                continue

            entry = LogEntry(
                timestamp_raw=(row.get("timestamp") or "").strip(),
                timestamp=parse_timestamp(row.get("timestamp") or ""),
                scope=scope,
                status=status,
                category=category,
                rule_text=normalized_rule,
                rule_key=rule_key_from_text(normalized_rule),
            )
            entries.append(entry)

    return entries, exclusions


def select_rules(
    entries: list[LogEntry],
    days: int,
    threshold: int,
    include_paper_rules: bool,
    exclusions: Counter[str],
) -> tuple[dict[str, RuleAggregate], Counter[str]]:
    now = datetime.now()
    cutoff = now - timedelta(days=days)

    allowed_scopes = {"global"}
    if include_paper_rules:
        allowed_scopes.add("paper")

    adopted_entries: list[LogEntry] = []
    candidate_entries: list[LogEntry] = []

    for entry in entries:
        if entry.scope not in allowed_scopes:
            exclusions["out_of_scope"] += 1
            continue
        if entry.status == "adopted":
            adopted_entries.append(entry)
        elif entry.status == "candidate":
            candidate_entries.append(entry)

    recent_candidate_count: Counter[str] = Counter()
    for entry in candidate_entries:
        if entry.timestamp is None:
            exclusions["invalid_candidate_timestamp"] += 1
            continue
        if entry.timestamp >= cutoff:
            recent_candidate_count[entry.rule_key] += 1

    selected: list[LogEntry] = []
    for entry in adopted_entries:
        selected.append(entry)
    for entry in candidate_entries:
        if entry.timestamp is None:
            continue
        count = recent_candidate_count.get(entry.rule_key, 0)
        if count >= threshold:
            selected.append(entry)
        else:
            exclusions["candidate_below_threshold"] += 1

    aggregates: dict[str, RuleAggregate] = {}
    duplicate_rows = 0
    for entry in selected:
        if entry.rule_key not in aggregates:
            aggregates[entry.rule_key] = RuleAggregate(rule_text=entry.rule_text)
        else:
            duplicate_rows += 1
        aggregates[entry.rule_key].add(entry)

    if duplicate_rows:
        exclusions["duplicate_normalized_rule"] += duplicate_rows

    promotion_reasons = Counter()
    for agg in aggregates.values():
        if agg.adopted_count > 0:
            promotion_reasons["adopted"] += 1
        elif agg.candidate_count > 0:
            promotion_reasons["candidate_frequent"] += 1

    return aggregates, promotion_reasons


def render_auto_rules_block(
    aggregates: dict[str, RuleAggregate],
    days: int,
    threshold: int,
    include_paper_rules: bool,
    generated_at: datetime,
) -> str:
    lines = [BEGIN_MARKER]
    lines.append(f"Generated at: {generated_at.isoformat(timespec='seconds')}")
    lines.append(
        "Conditions: "
        f"days={days}, threshold={threshold}, include-paper-rules={str(include_paper_rules).lower()}"
    )
    lines.append("")
    if not aggregates:
        lines.append("No rules matched current conditions.")
    else:
        lines.append("Rules:")
        sorted_rules = sorted(
            aggregates.values(),
            key=lambda r: (-r.evidence_count, r.primary_category, r.rule_text),
        )
        for index, agg in enumerate(sorted_rules, start=1):
            lines.append(f"{index}. [{agg.primary_category}] {agg.rule_text}")
            lines.append(f"   - 根拠件数: {agg.evidence_count}")
            lines.append(f"   - 主な出典 scope: {agg.main_scope}")
    lines.append(END_MARKER)
    return "\n".join(lines)


def ensure_auto_section(content: str) -> str:
    if BEGIN_MARKER in content and END_MARKER in content:
        return content

    section = "\n\n".join(
        [
            AUTO_SECTION_TITLE,
            BEGIN_MARKER,
            END_MARKER,
        ]
    )
    if content.endswith("\n"):
        return content + "\n" + section + "\n"
    return content + "\n\n" + section + "\n"


def replace_auto_block(content: str, block: str) -> str:
    start = content.find(BEGIN_MARKER)
    end = content.find(END_MARKER)
    if start == -1 or end == -1 or end < start:
        raise ValueError("Auto-rules markers are missing or invalid in AGENTS.md.")
    end += len(END_MARKER)
    return content[:start] + block + content[end:]


def parse_existing_rule_keys(content: str) -> set[str]:
    if BEGIN_MARKER not in content or END_MARKER not in content:
        return set()
    start = content.find(BEGIN_MARKER) + len(BEGIN_MARKER)
    end = content.find(END_MARKER, start)
    block = content[start:end]
    keys: set[str] = set()
    for line in block.splitlines():
        m = RULE_LINE_RE.match(line.strip())
        if not m:
            continue
        key = rule_key_from_text(m.group("rule"))
        if key:
            keys.add(key)
    return keys


def append_changelog(
    changelog_path: Path,
    generated_at: datetime,
    added: int,
    removed: int,
    kept: int,
    promotion_reasons: Counter[str],
    exclusions: Counter[str],
    days: int,
    threshold: int,
    include_paper_rules: bool,
) -> None:
    lines = []
    lines.append(
        f"- {generated_at.isoformat(timespec='seconds')}: Root AGENTS auto-rules update executed."
    )
    lines.append(
        f"  - 親AGENTS.md 反映件数: 追加 {added} / 削除 {removed} / 維持 {kept}"
    )
    lines.append(
        "  - 昇格理由: "
        f"adopted={promotion_reasons.get('adopted', 0)}, "
        f"candidate頻出={promotion_reasons.get('candidate_frequent', 0)}"
    )
    if exclusions:
        sorted_exclusions = ", ".join(
            f"{key}={value}" for key, value in sorted(exclusions.items())
        )
    else:
        sorted_exclusions = "none"
    lines.append(f"  - 除外件数: {sorted_exclusions}")
    lines.append(
        "  - 実行条件: "
        f"days={days}, threshold={threshold}, include-paper-rules={str(include_paper_rules).lower()}"
    )

    with changelog_path.open("a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    agents_path = project_root / "AGENTS.md"
    log_path = project_root / "governance" / "preference_log.csv"
    changelog_path = project_root / "governance" / "rule_changelog.md"

    try:
        entries, exclusions = load_log_entries(log_path)
        aggregates, promotion_reasons = select_rules(
            entries=entries,
            days=args.days,
            threshold=args.threshold,
            include_paper_rules=args.include_paper_rules,
            exclusions=exclusions,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not agents_path.exists():
        print(f"ERROR: AGENTS.md not found: {agents_path}", file=sys.stderr)
        return 1

    generated_at = datetime.now()
    original = agents_path.read_text(encoding="utf-8")
    prepared = ensure_auto_section(original)
    old_keys = parse_existing_rule_keys(prepared)

    block = render_auto_rules_block(
        aggregates=aggregates,
        days=args.days,
        threshold=args.threshold,
        include_paper_rules=args.include_paper_rules,
        generated_at=generated_at,
    )
    updated = replace_auto_block(prepared, block)
    new_keys = set(aggregates.keys())

    added = len(new_keys - old_keys)
    removed = len(old_keys - new_keys)
    kept = len(new_keys & old_keys)

    print("Root AGENTS auto-rule update preview")
    print(
        "Conditions: "
        f"days={args.days}, threshold={args.threshold}, include-paper-rules={str(args.include_paper_rules).lower()}"
    )
    print(f"Rules selected: {len(new_keys)} (added={added}, removed={removed}, kept={kept})")
    if promotion_reasons:
        reasons = ", ".join(
            f"{k}={v}" for k, v in sorted(promotion_reasons.items())
        )
    else:
        reasons = "none"
    print(f"Promotion reasons: {reasons}")
    if exclusions:
        excluded_text = ", ".join(f"{k}={v}" for k, v in sorted(exclusions.items()))
    else:
        excluded_text = "none"
    print(f"Excluded: {excluded_text}")
    print("")
    print(block)

    if args.dry_run:
        print("\nDry run mode: no files were changed.")
        return 0

    if not changelog_path.exists():
        print(f"ERROR: Changelog not found: {changelog_path}", file=sys.stderr)
        return 1

    agents_path.write_text(updated, encoding="utf-8")
    append_changelog(
        changelog_path=changelog_path,
        generated_at=generated_at,
        added=added,
        removed=removed,
        kept=kept,
        promotion_reasons=promotion_reasons,
        exclusions=exclusions,
        days=args.days,
        threshold=args.threshold,
        include_paper_rules=args.include_paper_rules,
    )

    print("\nUpdated files:")
    print(f"- {agents_path}")
    print(f"- {changelog_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
