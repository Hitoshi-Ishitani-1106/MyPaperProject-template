---
name: update-root-agents-from-log
description: "修正ログを集計し、親AGENTS.mdのAUTO_RULESブロックを更新してchangelogに実行履歴を追記する。"
---

# Update Root AGENTS From Log

## Steps
1. Run `python scripts/update_root_agents_from_log.py --project-root .`.
2. Confirm updates in `AGENTS.md` (`<!-- BEGIN AUTO_RULES -->` から `<!-- END AUTO_RULES -->` の範囲のみ) and `governance/rule_changelog.md`.
3. Report the result summary (added/removed/kept, exclusions).

## Failure handling
- If the command fails, print the error cause.
- Provide retry command:
  `python scripts/update_root_agents_from_log.py --project-root .`
