---
name: paper-write-discussion
description: "Discussion セクションの執筆・更新に使う。タスク [write_discussion] や discussion_flow.md に沿った考察記述が必要なときに使用。"
---

# Paper Write Discussion

## Steps
1. Read `.codex/AGENTS.md`, `references/discussion_flow.md`, `design/02_plan.md`, `design/evidence.md`.
2. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements`; if FAIL, stop and route back to `$paper-requirements`.
3. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage plan`; if FAIL, stop and route back to `$paper-plan`.
4. For each core claim (P2/P3), verify multi-angle evidence (`direct`, `convergent`, `alternative`) from plan/evidence.
5. If evidence is missing, propose angle-specific keywords and ask to run `$search-evidence-pubmed` with `angle_tag`.
6. Draft Discussion in `sections/05_discussion.md` one paragraph at a time.
7. Propose a diff for each paragraph; wait for approval.

## Rules
- Use only project evidence.
- Keep citations in Pandoc format.
- Write `sections/05_discussion.md` in English by default unless the user explicitly requests another language.
- Do not finalize P2/P3 with single-angle support; require multi-angle synthesis and minimum support volume.
- Never draft the section while requirements/plan gate is FAIL.
