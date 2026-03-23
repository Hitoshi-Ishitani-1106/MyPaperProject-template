---
name: paper-proofread-all
description: "全体校正レポートと修正提案に使う。タスク [proofread_all] や proofread_flow.md に沿った校正を実行するときに使用。"
---

# Paper Proofread All

## Steps
1. Read `.codex/AGENTS.md`, `references/proofread_flow.md`, all `sections/`, `refs/references.bib`, and `design/*`.
2. Output a PROPOSE report only.
3. After approval, generate diffs for the approved items only.

## Rules
- Do not apply changes without approval.
- Keep citations in Pandoc format.
