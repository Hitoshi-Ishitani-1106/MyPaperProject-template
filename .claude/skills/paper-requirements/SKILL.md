---
name: paper-requirements
description: "design/01_requirements.md を整備するためのスキル。タスク [design_requirements] 実行や requirements_flow.md に基づく要件洗い出し時に使う。"
---

# Paper Requirements

## Steps
1. Read `.codex/AGENTS.md`, `references/requirements_flow.md`, `skills/paper-workflow/references/guidelines_core.md`, `design/01_requirements.md`, `sections/01_abstract.md`.
2. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements` to list missing fields.
3. Ask only missing items in one structured prompt (PICO, journal, word/figure limits, ethics, reporting standards).
4. Propose a diff to update `design/01_requirements.md` without deleting unrelated content.
5. After applying approved diff, re-run requirements gate.
6. If remaining issues are only `provisional_unknown` (e.g., `現時点で不明`), ask explicit confirmation: whether to proceed to plan with unresolved fields.
7. Proceed only when either (a) normal gate PASS, or (b) user explicitly approves and `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements --allow-provisional-unknown` passes.

## Rules
- Keep PMID placeholders; assign citekeys only after adoption.
- Use project files only.
- Do not start `design/02_plan.md` work while requirements gate is FAIL.
- Do not silently treat `現時点で不明` as completed; always ask user confirmation before provisional pass.
