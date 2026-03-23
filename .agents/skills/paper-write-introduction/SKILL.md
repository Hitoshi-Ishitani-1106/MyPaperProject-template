---
name: paper-write-introduction
description: "Introduction を執筆・更新するときに使用。タスク [write_introduction] の実行や intro_flow.md に沿った導入文作成が必要な場合に使う。"
---

# Paper Write Introduction

## Steps
1. Read `.codex/AGENTS.md`, `design/02_plan.md`, `design/evidence.md`, `skills/paper-workflow/references/guidelines_core.md`, `references/intro_flow.md`.
2. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements`; if FAIL, stop and route back to `$paper-requirements`.
3. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage plan`; if FAIL, stop and route back to `$paper-plan`.
4. If evidence is missing, propose PubMed keywords and ask to run `$search-evidence-pubmed`.
5. Draft the Introduction in `sections/02_introduction.md` with P1→P2→P3 order.
6. Propose a diff only; wait for approval unless `vibe_*` is requested.

## Rules
- Use only project sources.
- Use Pandoc citations `[@citekey]`.
- Write `sections/02_introduction.md` in English by default unless the user explicitly requests another language.
- Never draft the section while requirements/plan gate is FAIL.
