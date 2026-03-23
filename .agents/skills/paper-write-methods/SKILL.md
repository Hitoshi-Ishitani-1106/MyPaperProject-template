---
name: paper-write-methods
description: "Methods セクションの執筆・更新に使う。タスク [write_methods] や methods_flow.md に沿った手法記述が必要なときに使用。"
---

# Paper Write Methods

## Steps
1. Read `.codex/AGENTS.md`, `references/methods_flow.md`, `design/01_requirements.md`, `design/02_plan.md`, `data/analysis/`, `data/processed/`.
2. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements`; if FAIL, stop and route back to `$paper-requirements`.
3. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage plan`; if FAIL, stop and route back to `$paper-plan`.
4. Draft Methods in `sections/03_methods.md`.
5. Propose a diff only; wait for approval.

## Rules
- Follow reporting rules in AGENTS.md.
- Use project data only.
- Write `sections/03_methods.md` in English by default unless the user explicitly requests another language.
- Never draft the section while requirements/plan gate is FAIL.
