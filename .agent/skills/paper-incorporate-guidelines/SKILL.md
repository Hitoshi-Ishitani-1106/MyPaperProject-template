---
name: paper-incorporate-guidelines
description: "投稿規定（Instructions for Authors）を取り込み、design/01_requirements.md と pandoc.yaml に反映するときに使う。タスク [incorporate_journal_guidelines] の実行に対応。"
---

# Paper Incorporate Guidelines

## Steps
1. Read `.codex/AGENTS.md` and `design/01_requirements.md`.
2. Ask the user to paste the full guidelines text.
3. Extract key constraints (abstract format, required sections, word/figure limits, reference style, figure/table rules).
4. Propose a diff to add or replace `## 投稿規定サマリー` in `design/01_requirements.md`.
5. After approval, identify the required CSL and instruct the user to place it under `refs/`.
6. Propose a diff to update `pandoc.yaml` `csl:` to the chosen file.
7. Report completion.

## Rules
- Do not invent guideline details.
- Use diff proposals before applying changes.
