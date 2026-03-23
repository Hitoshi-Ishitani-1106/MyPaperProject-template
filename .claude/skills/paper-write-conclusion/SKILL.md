---
name: paper-write-conclusion
description: "Conclusion セクションの執筆・更新に使う。タスク [write_conclusion] や conclusion_flow.md に沿った結論記述が必要なときに使用。"
---

# Paper Write Conclusion

## Steps
1. Read `.codex/AGENTS.md`, `references/conclusion_flow.md`, `sections/02_introduction.md` through `sections/05_discussion.md`.
2. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements`; if FAIL, stop and route back to `$paper-requirements`.
3. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage plan`; if FAIL, stop and route back to `$paper-plan`.
4. Draft a 3–4 sentence conclusion in `sections/06_conclusion.md`.
5. Propose a diff only; wait for approval.

## Rules
- Do not add new information or citations.
- Keep the tone consistent with the manuscript.
- Write `sections/06_conclusion.md` in English by default unless the user explicitly requests another language.
- Never draft the section while requirements/plan gate is FAIL.
