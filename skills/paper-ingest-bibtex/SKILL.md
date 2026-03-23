---
name: paper-ingest-bibtex
description: "refs/inbox.bib を取り込み、design/evidence.md と references.bib に反映する作業に使う。タスク [ingest_bibtex_inbox] に対応。"
---

# Paper Ingest BibTeX Inbox

## Steps
1. Read `.codex/AGENTS.md` and confirm `refs/inbox.bib` exists.
2. Check for duplicate citekeys in `refs/references.bib`; stop and report if found.
3. For each entry, propose diffs in order: `design/evidence.md` → `refs/references.bib` → `design/02_plan.md` → `refs/inbox.bib`.
4. Ensure the inbox is empty and report next steps.

## Rules
- Use diff proposals for every step.
- Do not change citekeys.
