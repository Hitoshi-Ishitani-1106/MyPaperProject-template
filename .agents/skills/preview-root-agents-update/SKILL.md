---
name: preview-root-agents-update
description: "修正ログから親AGENTS.mdへの反映候補をプレビューする。ファイル変更なしで差分予定を確認したいときに使う。"
---

# Preview Root AGENTS Update

## Steps
1. Run `python scripts/update_root_agents_from_log.py --project-root . --dry-run`.
2. Review selected rules, promotion reasons, and exclusion counts in stdout.
3. Confirm no file is changed in this step.

## Rules
- Do not modify files.
- If command fails, report the error and show the same command for retry.
