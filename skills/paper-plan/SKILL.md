---
name: paper-plan
description: "design/02_plan.md を設計・更新するためのスキル。タスク [design_plan] 実行や plan_flow.md に沿った計画整理で使う。"
---

# Paper Plan

## Steps
1. Read `.codex/AGENTS.md`, `references/plan_flow.md`, `design/evidence.md`, `sections/01_abstract.md`, `design/02_plan.md`, and `design/01_requirements.md`.
2. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements`; if FAIL, stop and send user back to `$paper-requirements`.
3. If remaining requirements issues are only `provisional_unknown` (e.g., `現時点で不明`), ask the user whether to proceed provisionally; continue only when user agrees and `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements --allow-provisional-unknown` passes.
4. Draft/update `design/02_plan.md` with `[pmid:XXXXXXX]` placeholders only; keep numeric data in evidence.
5. For Discussion P2/P3 claims, add an Evidence Angle Matrix (`Direct`, `Convergent`, `Alternative/Boundary`) and assign placeholders for each angle.
6. Ensure minimum support policy per claim: `Direct>=2`, `Convergent>=1`, `Alternative>=1`, total citations `>=4`.
7. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage search-targets --json` and auto-detect literature gaps from Introduction/Discussion.
8. If search targets exist, auto-run `$search-evidence-pubmed` for each target with generated keywords and `angle_tag` (if present), update `design/evidence.md`, and then patch `design/02_plan.md` with new PMID placeholders.
9. Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage plan` and iterate until PASS.
10. After approval and PASS, remind the post-plan steps (map.tsv → register BibTeX → replace PMID → run `python scripts/qa_citation_web.py --scope core --report reports/qa_citation_web_prewrite.md` → verify).

## Rules
- Do not use external knowledge.
- Use diff proposals before applying.
- Do not proceed to section drafting while plan gate is FAIL.
- Do not accept single-angle support for core Discussion interpretation claims.
- Do not silently proceed when requirements has `provisional_unknown`; require explicit user approval.
- Require citation-web prewrite PASS before section drafting.
