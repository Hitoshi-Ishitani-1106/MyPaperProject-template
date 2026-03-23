---
name: paper-search-flow
description: "PubMed 検索のフロー実行と evidence ブロック作成に使う。タスク [run_literature_search] や search_flow.md を用いた検索が必要なときに使用。"
---

# Paper Search Flow

## Steps
1. Read `.codex/AGENTS.md` and `references/search_flow.md`.
2. Collect `section_name`, `theme`, `constraints`, and target placement in `design/evidence.md` (single target or queue input from `design_gatekeeper --stage search-targets --json`).
3. If queue input is provided, process targets in order: `Introduction-*` → `Discussion-*` → others.
4. Use `$search-evidence-pubmed` to execute PubMed search with logs and QA for each target.
5. Propose a diff to append each block in `design/evidence.md` only after QA PASS.
6. Record audit logs; if shortage, document reasons and propose re-search.

## Rules
- Use PubMed only via the skill.
- Do not infer beyond abstracts.
- Keep theme/keywords traceable to the originating `design/02_plan.md` paragraph.
