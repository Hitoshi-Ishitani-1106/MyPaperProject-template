---
name: paper-title-and-titlepage
description: "タイトル案とタイトルページ草案の作成に使う。タスク [title_and_titlepage] や title_titlepage_flow.md に沿ったタイトル生成時に使用。"
---

# Paper Title and Titlepage

## Steps
1. Read `.codex/AGENTS.md`, `references/title_titlepage_flow.md`, `design/01_requirements.md`, `design/02_plan.md`, and all `sections/`.
2. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements`; if FAIL, stop and route back to `$paper-requirements`.
3. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage plan`; if FAIL, stop and route back to `$paper-plan`.
4. Generate 5 title candidates and a title page draft.
5. Propose a diff to update `sections/00_titlepage.md` (and `metadata/frontmatter.yaml` if needed).
6. If title page requirements are missing, propose a diff to `design/02_plan.md`.

## Rules
- Keep requirements consistent with the target journal.
- Use diff proposals before applying.
- Draft `sections/00_titlepage.md` in English by default, even if source notes are in Japanese.
- Never draft the title page while requirements/plan gate is FAIL.
