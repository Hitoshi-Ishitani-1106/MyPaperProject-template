---
name: paper-write-abstract-final
description: "最終版 Abstract の作成・置換に使う。タスク [write_abstract_final] や abstract_flow.md に沿った最終アブストラクト生成時に使用。"
---

# Paper Write Abstract Final

## Steps
1. Read `.codex/AGENTS.md`, `references/abstract_flow.md`, `design/01_requirements.md`, and all `sections/`.
2. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements`; if FAIL, stop and route back to `$paper-requirements`.
3. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage plan`; if FAIL, stop and route back to `$paper-plan`.
4. Draft the final Abstract and replace `sections/01_abstract.md`.
5. Propose a replacement diff only; wait for approval.

## Rules
- Keep consistent with final results and limits.
- Use Pandoc citations only.
- Write `sections/01_abstract.md` in English by default unless the user explicitly requests another language.
- Never finalize abstract while requirements/plan gate is FAIL.
