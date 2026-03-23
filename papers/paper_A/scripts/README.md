# Scripts

Operational and QA helpers live here.

- `design_gatekeeper.py`: gate checks for `design/01_requirements.md` and `design/02_plan.md`, plus search-target detection.
- `qa_proofread_gate.py`: proofread completion gate (`--mark` / `--check`) used by `make qa-full`.
- `qa_references_style.py`: pre-Pandoc QA for `refs/references.bib` completeness/integrity and CSL suitability (with safe auto-fix attempts).
- `qa_citation_web.py`: web-backed QA for citation existence and citation-context intent alignment (PubMed/Crossref).
- `qa_citations.py`: citation consistency QA between `sections/*.md` and `refs/references.bib`.

Analysis code for Methods should be placed in `data/analysis/`.
