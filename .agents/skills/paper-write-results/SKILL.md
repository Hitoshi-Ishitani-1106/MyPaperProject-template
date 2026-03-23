---
name: paper-write-results
description: "Results セクションの執筆・更新に使う。タスク [write_results] や results_flow.md に沿った結果記述が必要なときに使用。"
---

# Paper Write Results

## Steps
1. Read `.codex/AGENTS.md`, `references/results_flow.md`, `design/02_plan.md`, `data/processed/`, `data/figures/`, `data/tables/`.
2. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements`; if FAIL, stop and route back to `$paper-requirements`.
3. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage plan`; if FAIL, stop and route back to `$paper-plan`.
4. Draft Results in `sections/04_results.md` and prepare figure/table captions if needed.
5. Propose a diff only; wait for approval.

## Rules
- Report effect sizes and CIs where available.
- Use project data only.
- Write `sections/04_results.md` in English by default unless the user explicitly requests another language.
- Never draft the section while requirements/plan gate is FAIL.
