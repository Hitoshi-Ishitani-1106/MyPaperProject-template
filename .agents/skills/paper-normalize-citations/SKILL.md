---
name: paper-normalize-citations
description: "書誌情報の正規化と citekey 付与、refs/references.bib への登録、[pmid:]→[@citekey] 置換に使う。タスク [normalize_and_register_citations] に対応。"
---

# Paper Normalize Citations

## Steps
1. Read `.codex/AGENTS.md`, `refs/references.bib`, `design/02_plan.md`, `skills/paper-workflow/references/guidelines_core.md`, and any provided `map.tsv`.
2. Validate missing fields; ask for DOI/PMID if needed.
3. Generate consistent citekeys (e.g., SurnameYEARKeyterm) without changing provided keys.
4. Propose a diff to update `refs/references.bib`.
5. Propose a diff to replace `[pmid:XXXXXXX]` with `[@citekey]` across `design/02_plan.md` and `sections/`.
6. Wait for approval before applying.

## Rules
- Do not invent bibliographic data.
- Use Pandoc citation format only.
