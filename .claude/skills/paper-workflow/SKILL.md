---
name: paper-workflow
description: "医学論文プロジェクトの全体フローを順次進行するためのスキル。要件定義→計画→文献→執筆→校正を一連で進めたいときに使う。"
---

# Paper Workflow

## Steps
1. Read `.codex/AGENTS.md`, `AGENTS.md`, `README.md`, `design/01_requirements.md`, `design/02_plan.md`, and relevant `skills/*/references/`.
2. Resolve `paper_dir` and run gate: `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements`.
3. If requirements gate fails, run `$paper-requirements`, ask only missing items in one structured prompt, update `design/01_requirements.md`, and re-run the requirements gate.
4. If the only remaining requirements issues are `provisional_unknown` (e.g., `現時点で不明`), ask the user explicitly whether to proceed. Continue only when user agrees and `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements --allow-provisional-unknown` passes.
5. If journal guidelines are not incorporated, run `$paper-incorporate-guidelines` and re-check requirements gate.
6. Start `$paper-plan` only after requirements gate PASS.
7. Run plan gate: `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage plan`.
8. If plan gate fails because of missing evidence/search targets, run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage search-targets --json` and auto-run `$search-evidence-pubmed` for each target (Introduction/Discussion first, and use `angle_tag` when provided), then update `design/evidence.md` and `design/02_plan.md`, and re-run plan gate.
9. If plan gate fails for other missing fields, ask only missing items, patch `design/02_plan.md`, and re-run plan gate.
10. Continue only after plan gate PASS: resolve citations (`map.tsv` → `$paper-normalize-citations` / `$paper-ingest-bibtex`).
11. Before section drafting, run `python scripts/qa_citation_web.py --scope core --report reports/qa_citation_web_prewrite.md` to verify citation existence and intent alignment for Introduction/Discussion claims; if FAIL, fix evidence/citations first.
12. After citation-web prewrite PASS, write sections in order (`$paper-write-introduction` → `$paper-write-methods` → `$paper-write-results` → `$paper-write-discussion` → `$paper-write-conclusion` → `$paper-title-and-titlepage` → `$paper-write-abstract-final`).
13. Run `$paper-proofread-all`, then mark completion with `python scripts/qa_proofread_gate.py --mark`.
14. Run output gates in order with proofread enforcement: `make qa-full` (internally: proofread-check → refs-style → citation-web(all) → citations → pandoc).
15. Stop at each diff for approval unless `vibe_full_auto` / `vibe_write_auto` are explicitly requested.

## Rules
- Use only project files as evidence; do not use external knowledge.
- Use Pandoc citations `[@citekey]` only.
- Use `skills/*/references/` as the SSOT for prompt flows.
- Never proceed to the next phase while `design_gatekeeper` is FAIL.
- `provisional_unknown` を検出した場合は、ユーザーの明示同意なしに `--allow-provisional-unknown` を使って進めない。
- Never proceed to drafting/output when `qa_citation_web.py` is FAIL (unless user explicitly accepts the risk).
- Never run final Pandoc output without passing `qa_proofread_gate.py --check` (use `make qa-full`).
- Keep manuscript section outputs in English by default (`sections/00_titlepage.md` to `sections/06_conclusion.md`) unless the user explicitly requests another language.
