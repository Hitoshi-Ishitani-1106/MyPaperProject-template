# Logging Guide

## 基本方針
- 1修正1行で `governance/preference_log.csv` に短く記録する。
- 同種修正が繰り返されたら規則化し、原則として親 `AGENTS.md` へ反映する。
- 個人情報や患者識別情報はログに記載しない。
- オートメーションは使わず、今回は手動更新で運用する。
- `paper` 固有ルールは自動反映せず、`papers/<paper_id>/AGENTS.md` で手動管理する。
- 例外的に `paper` ルールを親へ取り込む場合のみ `--include-paper-rules` を使う。

## 運用手順
1. 修正発生: before/after と理由を1行で追記。
2. 集計確認: 同カテゴリの再発を確認。
3. 採用判断: `status` を `adopted` / `rejected` へ更新。
4. 反映:
   - 事前確認: `python scripts/update_root_agents_from_log.py --project-root . --dry-run`
   - 更新実行: `python scripts/update_root_agents_from_log.py --project-root .`
5. 履歴化: `governance/rule_changelog.md` に記録。
