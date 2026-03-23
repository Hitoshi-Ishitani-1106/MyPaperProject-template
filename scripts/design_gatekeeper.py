#!/usr/bin/env python3
"""Gate checks for requirements/plan and search-target detection from plan."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, List

UNRESOLVED_TOKEN_RE = re.compile(
    r"\bTBD\b|<<\s*placeholder\s*>>|\bTODO\b|未定|未入力|要確認|要検索",
    re.IGNORECASE,
)
PROVISIONAL_UNKNOWN_RE = re.compile(
    r"現時点で不明|未確定|未決定|候補選定中|未詳|unknown\b|n/?a\b|not\s+determined",
    re.IGNORECASE,
)
PMID_RE = re.compile(r"\[pmid:\d+\]", re.IGNORECASE)
CITEKEY_RE = re.compile(r"\[@[^\]]+\]")
BOLD_COLON_EMPTY_RE = re.compile(r"^-\s+\*\*[^*]+\*\*:\s*$")
PLAIN_COLON_EMPTY_RE = re.compile(r"^-\s+[^:]+:\s*$")
UNCHECKED_RE = re.compile(r"^-\s+\[\s\]\s+")
IGNORE_UNRESOLVED_LINE_RES = [
    re.compile(r"^>\s+.*TBD", re.IGNORECASE),
    re.compile(r"^##\s+\d+\.\s+未決事項（TBD リスト）", re.IGNORECASE),
    re.compile(r"^>\s+\*\*更新方法\*\*:.*TBD", re.IGNORECASE),
]
DISCUSSION_DEPTH_TARGET_PARAS = {2, 3}
DISCUSSION_MIN_TOTAL_CITATIONS = 4
DISCUSSION_MIN_ANGLE_COUNTS = {"direct": 2, "convergent": 1, "alternative": 1}

ANGLE_LABEL_PATTERNS = {
    "direct": re.compile(r"(direct|直接|一致|同方向の主要根拠)", re.IGNORECASE),
    "convergent": re.compile(r"(convergent|補強|別角度賛成|独立支持|同方向補強)", re.IGNORECASE),
    "alternative": re.compile(r"(alternative|boundary|別解釈|境界条件|異論|反対|逆方向)", re.IGNORECASE),
}

ANGLE_DEFAULT_TERMS = {
    "direct": ["direct evidence", "primary population match", "main outcome support"],
    "convergent": ["convergent evidence", "independent cohort", "external consistency"],
    "alternative": ["alternative explanation", "boundary condition", "competing interpretation"],
}


@dataclass
class LineIssue:
    line: int
    reason: str
    text: str


@dataclass
class ParagraphBlock:
    section: str
    paragraph_id: str
    line_start: int
    text: str


def _safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Missing file: {path}")


def collect_line_issues(text: str) -> List[LineIssue]:
    issues: List[LineIssue] = []
    for idx, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("<!--") and line.endswith("-->"):
            continue

        if UNRESOLVED_TOKEN_RE.search(line):
            if any(p.search(line) for p in IGNORE_UNRESOLVED_LINE_RES):
                continue
            issues.append(LineIssue(idx, "unresolved_token", raw.rstrip()))
            continue

        # "現時点で不明" などの暫定未確定値を検出する。
        # 主に "key: value" 形式の項目行を対象にし、本文中の一般表現は過検出しにくくする。
        field_like = (line.startswith("-") and ":" in line) or line.startswith("|")
        if field_like and PROVISIONAL_UNKNOWN_RE.search(line):
            issues.append(LineIssue(idx, "provisional_unknown", raw.rstrip()))
            continue

        if UNCHECKED_RE.match(line):
            issues.append(LineIssue(idx, "unchecked_checkbox", raw.rstrip()))
            continue

        if BOLD_COLON_EMPTY_RE.match(line) or PLAIN_COLON_EMPTY_RE.match(line):
            issues.append(LineIssue(idx, "empty_field", raw.rstrip()))

    return issues


def _section_range(lines: List[str], section_header_re: re.Pattern[str]) -> tuple[int, int] | None:
    start_idx = None
    for idx, line in enumerate(lines):
        if section_header_re.search(line):
            start_idx = idx
            break
    if start_idx is None:
        return None

    end_idx = len(lines)
    for idx in range(start_idx + 1, len(lines)):
        if lines[idx].startswith("### "):
            end_idx = idx
            break
    return start_idx, end_idx


def extract_paragraph_blocks(plan_text: str, section_name: str) -> List[ParagraphBlock]:
    lines = plan_text.splitlines()
    if section_name == "Introduction":
        section_re = re.compile(r"^###\s+2\.1\s+Introduction", re.IGNORECASE)
    elif section_name == "Discussion":
        section_re = re.compile(r"^###\s+2\.4\s+Discussion", re.IGNORECASE)
    else:
        raise ValueError(f"Unsupported section: {section_name}")

    block_range = _section_range(lines, section_re)
    if block_range is None:
        return []

    start, end = block_range
    para_start_re = re.compile(r"^-\s+\*\*(P\d+[^*]*)\*\*")

    starts: List[tuple[int, str]] = []
    for idx in range(start + 1, end):
        m = para_start_re.match(lines[idx].strip())
        if m:
            starts.append((idx, m.group(1).strip()))

    blocks: List[ParagraphBlock] = []
    for pos, (line_idx, para_id) in enumerate(starts):
        next_line_idx = starts[pos + 1][0] if pos + 1 < len(starts) else end
        text = "\n".join(lines[line_idx:next_line_idx]).strip()
        blocks.append(
            ParagraphBlock(
                section=section_name,
                paragraph_id=para_id,
                line_start=line_idx + 1,
                text=text,
            )
        )
    return blocks


def _requires_citation(block: ParagraphBlock) -> bool:
    para_num = _extract_para_number(block.paragraph_id)
    lower = block.text.lower()

    if "引用不要" in block.text:
        return False

    if block.section == "Introduction":
        if para_num == 3 or "aim" in lower:
            return False
        return True

    if block.section == "Discussion":
        # Force evidence filling for core interpretation paragraphs.
        if para_num in {2, 3, 4}:
            return True
        return para_num is not None and para_num >= 1

    return True


def _extract_para_number(paragraph_id: str) -> int | None:
    m = re.match(r"P(\d+)", paragraph_id, re.IGNORECASE)
    if not m:
        return None
    return int(m.group(1))


def _extract_claim_text(block_text: str) -> str:
    for raw in block_text.splitlines():
        stripped = raw.strip()
        if "主張:" in stripped:
            return stripped.split("主張:", 1)[1].strip()
    return ""


def _extract_evidence_text(block_text: str) -> str:
    for raw in block_text.splitlines():
        stripped = raw.strip()
        if "主要エビデンス:" in stripped:
            return stripped.split("主要エビデンス:", 1)[1].strip()
    return ""


def _has_placeholder(value: str) -> bool:
    return bool(UNRESOLVED_TOKEN_RE.search(value) or PROVISIONAL_UNKNOWN_RE.search(value))


def _clean_phrase(value: str) -> str:
    value = re.sub(r"\[[^\]]+\]", " ", value)
    value = re.sub(r"\s+", " ", value)
    value = value.strip(" -:、,。")
    return value


def extract_pico_terms(requirements_text: str) -> dict[str, str]:
    lines = requirements_text.splitlines()
    fields: dict[str, str] = {
        "population": "",
        "intervention": "",
        "comparison": "",
        "outcome": "",
        "setting": "",
    }

    patterns = {
        "population": [r"Population\*\*:\s*(.+)$", r"Population\s*:\s*(.+)$"],
        "intervention": [r"Intervention[^:]*:\s*(.+)$", r"Exposure[^:]*:\s*(.+)$"],
        "comparison": [r"Comparison[^:]*:\s*(.+)$", r"Reference[^:]*:\s*(.+)$"],
        "outcome": [r"Outcomes?[^:]*:\s*(.+)$", r"主要評価項目\s*:\s*(.+)$"],
        "setting": [r"Timeframe[^:]*:\s*(.+)$", r"Setting[^:]*:\s*(.+)$"],
    }

    for line in lines:
        stripped = line.strip(" -")
        for key, key_patterns in patterns.items():
            if fields[key]:
                continue
            for pattern in key_patterns:
                m = re.search(pattern, stripped, re.IGNORECASE)
                if not m:
                    continue
                candidate = _clean_phrase(m.group(1))
                if candidate and not _has_placeholder(candidate):
                    fields[key] = candidate
                break

    return fields


def _build_terms(block: ParagraphBlock, pico: dict[str, str]) -> list[str]:
    claim = _clean_phrase(_extract_claim_text(block.text))
    evidence = _clean_phrase(_extract_evidence_text(block.text))
    para_topic = _clean_phrase(_paragraph_topic(block.paragraph_id))
    base = [
        claim,
        evidence,
        para_topic,
        pico.get("population", ""),
        pico.get("intervention", ""),
        pico.get("outcome", ""),
    ]
    deduped: list[str] = []
    for item in base:
        if not item:
            continue
        if _has_placeholder(item):
            continue
        if item not in deduped:
            deduped.append(item)
    for fallback in _default_keywords(block):
        if fallback not in deduped:
            deduped.append(fallback)
    return deduped[:6]


def _paragraph_topic(paragraph_id: str) -> str:
    if ":" in paragraph_id:
        return paragraph_id.split(":", 1)[1].strip()
    return paragraph_id.strip()


def _default_keywords(block: ParagraphBlock) -> list[str]:
    para_num = _extract_para_number(block.paragraph_id)
    if block.section == "Introduction":
        if para_num == 1:
            return ["epidemiology", "burden", "clinical significance"]
        if para_num == 2:
            return ["knowledge gap", "controversy", "unmet need"]
        if para_num == 3:
            return ["study aim", "hypothesis", "objective"]
    if block.section == "Discussion":
        if para_num == 1:
            return ["key findings", "summary", "clinical meaning"]
        if para_num == 2:
            return ["mechanism", "consistency with prior studies", "effect interpretation"]
        if para_num == 3:
            return ["heterogeneity", "subgroup", "alternative explanation"]
        if para_num == 4:
            return ["clinical implication", "generalizability", "implementation"]
        if para_num == 5:
            return ["limitations", "bias", "future research"]
    return []


def _extract_citations(text: str) -> list[str]:
    return PMID_RE.findall(text) + CITEKEY_RE.findall(text)


def _count_angle_citations(block_text: str) -> dict[str, int]:
    counts = {k: 0 for k in ANGLE_LABEL_PATTERNS}
    for raw in block_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        line_cites = _extract_citations(line)
        if not line_cites:
            continue
        for angle, pattern in ANGLE_LABEL_PATTERNS.items():
            if pattern.search(line):
                counts[angle] += len(line_cites)
                break
    return counts


def _discussion_depth_targets(block: ParagraphBlock, pico: dict[str, str]) -> list[dict[str, object]]:
    if block.section != "Discussion":
        return []

    para_num = _extract_para_number(block.paragraph_id)
    if para_num not in DISCUSSION_DEPTH_TARGET_PARAS:
        return []

    targets: list[dict[str, object]] = []
    para_token = block.paragraph_id.split()[0].rstrip(":")
    section_label = f"{block.section}-{para_token}"
    terms = _build_terms(block, pico)
    angle_counts = _count_angle_citations(block.text)
    total_citations = len(_extract_citations(block.text))
    constraints = "2015年以降, 成人優先, 原著中心, レビュー<=3"

    for angle, min_count in DISCUSSION_MIN_ANGLE_COUNTS.items():
        if angle_counts.get(angle, 0) >= min_count:
            continue
        angle_terms = ANGLE_DEFAULT_TERMS[angle]
        merged_terms = [*terms]
        for token in angle_terms:
            if token not in merged_terms:
                merged_terms.append(token)
        targets.append(
            {
                "section_name": f"{section_label}-{angle}",
                "line": block.line_start,
                "reason": f"depth_gap,missing_angle_{angle}",
                "theme": " / ".join(merged_terms[:6]),
                "keywords": merged_terms[:6],
                "angle_tag": angle,
                "constraints": constraints,
                "skill": "search-evidence-pubmed",
            }
        )

    if total_citations < DISCUSSION_MIN_TOTAL_CITATIONS:
        expansion_terms = [*terms]
        for token in ["support expansion", "multi-angle evidence"]:
            if token not in expansion_terms:
                expansion_terms.append(token)
        targets.append(
            {
                "section_name": f"{section_label}-support",
                "line": block.line_start,
                "reason": "depth_gap,insufficient_support_volume",
                "theme": " / ".join(expansion_terms[:6]),
                "keywords": expansion_terms[:6],
                "angle_tag": "support-expansion",
                "constraints": constraints,
                "skill": "search-evidence-pubmed",
            }
        )

    return targets


def build_search_targets(plan_text: str, requirements_text: str) -> list[dict[str, object]]:
    pico = extract_pico_terms(requirements_text)
    targets: list[dict[str, object]] = []

    for section in ("Introduction", "Discussion"):
        blocks = extract_paragraph_blocks(plan_text, section)
        for block in blocks:
            citations = _extract_citations(block.text)
            has_unresolved = _has_placeholder(block.text)
            needs_citation = _requires_citation(block)
            has_gap = needs_citation and len(citations) == 0
            depth_targets = _discussion_depth_targets(block, pico)

            if not (has_gap or has_unresolved or depth_targets):
                continue

            terms = _build_terms(block, pico)
            constraints = "2015年以降, 成人優先, 原著中心, レビュー<=3"
            reason_parts = []
            if has_gap:
                reason_parts.append("citation_gap")
            if has_unresolved:
                reason_parts.append("unresolved_placeholder")

            para_token = block.paragraph_id.split()[0].rstrip(":")
            section_label = f"{block.section}-{para_token}"
            if has_gap or has_unresolved:
                targets.append(
                    {
                        "section_name": section_label,
                        "line": block.line_start,
                        "reason": ",".join(reason_parts),
                        "theme": " / ".join(terms) if terms else f"{section} {block.paragraph_id}",
                        "keywords": terms,
                        "constraints": constraints,
                        "skill": "search-evidence-pubmed",
                    }
                )
            targets.extend(depth_targets)

    return targets


def evaluate_requirements(requirements_path: Path, allow_provisional_unknown: bool = False) -> dict[str, object]:
    text = _safe_read(requirements_path)
    issues = collect_line_issues(text)
    blocking_issues: list[LineIssue] = []
    warning_issues: list[LineIssue] = []
    for issue in issues:
        if issue.reason == "provisional_unknown" and allow_provisional_unknown:
            warning_issues.append(issue)
            continue
        blocking_issues.append(issue)
    return {
        "path": str(requirements_path),
        "pass": len(blocking_issues) == 0,
        "issue_count": len(blocking_issues),
        "issues": [issue.__dict__ for issue in blocking_issues],
        "warning_count": len(warning_issues),
        "warnings": [issue.__dict__ for issue in warning_issues],
    }


def evaluate_plan(
    plan_path: Path, requirements_text: str, allow_provisional_unknown: bool = False
) -> dict[str, object]:
    text = _safe_read(plan_path)
    issues = collect_line_issues(text)
    targets = build_search_targets(text, requirements_text)

    has_intro = bool(extract_paragraph_blocks(text, "Introduction"))
    has_disc = bool(extract_paragraph_blocks(text, "Discussion"))
    structure_issues: list[dict[str, object]] = []
    if not has_intro:
        structure_issues.append({"line": 0, "reason": "missing_section", "text": "Introduction paragraph block missing"})
    if not has_disc:
        structure_issues.append({"line": 0, "reason": "missing_section", "text": "Discussion paragraph block missing"})

    all_issues = [*issues, *[LineIssue(i["line"], i["reason"], i["text"]) for i in structure_issues]]
    blocking_issues: list[LineIssue] = []
    warning_issues: list[LineIssue] = []
    for issue in all_issues:
        if issue.reason == "provisional_unknown" and allow_provisional_unknown:
            warning_issues.append(issue)
            continue
        blocking_issues.append(issue)
    passed = len(blocking_issues) == 0 and len(targets) == 0

    return {
        "path": str(plan_path),
        "pass": passed,
        "issue_count": len(blocking_issues),
        "issues": [issue.__dict__ for issue in blocking_issues],
        "warning_count": len(warning_issues),
        "warnings": [issue.__dict__ for issue in warning_issues],
        "search_target_count": len(targets),
        "search_targets": targets,
    }


def format_text_report(stage: str, payload: dict[str, object]) -> str:
    lines: list[str] = []

    if stage in {"requirements", "all"} and "requirements" in payload:
        req = payload["requirements"]
        status = "PASS" if req["pass"] else "FAIL"
        lines.append(f"[requirements] {status} - {req['issue_count']} issue(s)")
        for issue in req["issues"][:30]:
            lines.append(f"  L{issue['line']}: {issue['reason']} | {issue['text']}")
        if req.get("warning_count", 0):
            lines.append(
                f"  provisional_unknown (allowed): {req['warning_count']} issue(s) "
                f"(run without --allow-provisional-unknown to enforce)"
            )
            for issue in req.get("warnings", [])[:30]:
                lines.append(f"  W L{issue['line']}: {issue['reason']} | {issue['text']}")

    if stage in {"plan", "all"} and "plan" in payload:
        plan = payload["plan"]
        status = "PASS" if plan["pass"] else "FAIL"
        lines.append(f"[plan] {status} - {plan['issue_count']} issue(s), {plan['search_target_count']} search target(s)")
        for issue in plan["issues"][:30]:
            lines.append(f"  L{issue['line']}: {issue['reason']} | {issue['text']}")
        if plan.get("warning_count", 0):
            lines.append(
                f"  provisional_unknown (allowed): {plan['warning_count']} issue(s) "
                f"(run without --allow-provisional-unknown to enforce)"
            )
            for issue in plan.get("warnings", [])[:30]:
                lines.append(f"  W L{issue['line']}: {issue['reason']} | {issue['text']}")
        for target in plan["search_targets"][:30]:
            angle = f", angle={target['angle_tag']}" if "angle_tag" in target else ""
            lines.append(
                f"  search {target['section_name']} (L{target['line']}): {target['reason']}{angle} | theme={target['theme']}"
            )

    if stage == "search-targets" and "search_targets" in payload:
        targets = payload["search_targets"]
        lines.append(f"[search-targets] {len(targets)} item(s)")
        for target in targets:
            angle = f", angle={target['angle_tag']}" if "angle_tag" in target else ""
            lines.append(
                f"  {target['section_name']} (L{target['line']}): {target['reason']}{angle} | theme={target['theme']}"
            )

    return "\n".join(lines)


def resolve_paths(paper_dir: Path) -> tuple[Path, Path]:
    req = paper_dir / "design" / "01_requirements.md"
    plan = paper_dir / "design" / "02_plan.md"
    return req, plan


def run(stage: str, paper_dir: Path, allow_provisional_unknown: bool = False) -> tuple[dict[str, object], int]:
    req_path, plan_path = resolve_paths(paper_dir)

    payload: dict[str, object] = {
        "stage": stage,
        "paper_dir": str(paper_dir),
        "generated_at": date.today().isoformat(),
    }

    try:
        req_result: dict[str, object] | None = None
        req_text = ""

        if stage in {"requirements", "plan", "all", "search-targets"}:
            req_result = evaluate_requirements(req_path, allow_provisional_unknown=allow_provisional_unknown)
            req_text = _safe_read(req_path)

        if req_result is not None and stage in {"requirements", "all"}:
            payload["requirements"] = req_result

        if stage in {"plan", "all"}:
            plan_result = evaluate_plan(
                plan_path, req_text, allow_provisional_unknown=allow_provisional_unknown
            )
            payload["plan"] = plan_result

        if stage == "search-targets":
            plan_text = _safe_read(plan_path)
            payload["search_targets"] = build_search_targets(plan_text, req_text)

    except FileNotFoundError as exc:
        payload["error"] = str(exc)
        return payload, 1

    if stage == "requirements":
        return payload, 0 if payload.get("requirements", {}).get("pass") else 2

    if stage == "plan":
        return payload, 0 if payload.get("plan", {}).get("pass") else 2

    if stage == "all":
        req_pass = payload.get("requirements", {}).get("pass", False)
        plan_pass = payload.get("plan", {}).get("pass", False)
        return payload, 0 if req_pass and plan_pass else 2

    return payload, 0


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gate check requirements/plan and detect search targets.")
    parser.add_argument("--paper-dir", required=True, help="Path to paper workspace (contains design/).")
    parser.add_argument(
        "--stage",
        required=True,
        choices=["requirements", "plan", "search-targets", "all"],
        help="Validation or extraction stage.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument(
        "--allow-provisional-unknown",
        action="store_true",
        help="Treat provisional unknown values (e.g., 現時点で不明) as warnings instead of blocking errors.",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    paper_dir = Path(args.paper_dir).resolve()
    payload, exit_code = run(
        args.stage, paper_dir, allow_provisional_unknown=args.allow_provisional_unknown
    )

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(format_text_report(args.stage, payload))

    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
