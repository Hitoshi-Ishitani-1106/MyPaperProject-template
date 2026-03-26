# MyPaperProject

## Quick Start

### Option A: Use this template（推奨）
GitHub の "Use this template" ボタンをクリックし、自分のリポジトリとして作成してください。

### Option B: ZIP ダウンロード
Code → Download ZIP でダウンロードし、好きな場所に展開してください。

### Option C: git clone
```bash
git clone https://github.com/Hitoshi-Ishitani-1106/MyPaperProject-template.git MyProject
cd MyProject
rm -rf .git
git init
```

---

複数論文を同一親ディレクトリで管理するための運用ルートです。  
**使用ツール: Codex デスクトップアプリ**

## ディレクトリ構成

- `.agents/skills/` : Codex が参照するスキル集
- `.codex/` : Codex 実行時の共通補助ルール
- `governance/` : 修正ログと規則変更履歴
- `templates/paper_template/` : 新規論文の雛形
- `papers/paper_A/`, `papers/paper_B/` : 論文ごとの独立ワークスペース

## 新規論文の作り方

1. `templates/paper_template` を `papers/paper_X` に複製する。
2. `papers/paper_X/AGENTS.md` に投稿先規定・語数・図表制約を記載する。
3. `papers/paper_X/metadata.yaml` と `design/*` を埋める。

例:
```bash
cp -R templates/paper_template papers/paper_C
```

## 引用検証ゲート（推奨）

- 執筆前: `python papers/<paper_id>/scripts/qa_citation_web.py --scope core --report papers/<paper_id>/reports/qa_citation_web_prewrite.md`
- 出力前: `python papers/<paper_id>/scripts/qa_citation_web.py --scope all --report papers/<paper_id>/reports/qa_citation_web.md`
- 統合: `cd papers/<paper_id> && make qa`

## proofread強制ゲート（任意）

- proofread実施後にマーク: `cd papers/<paper_id> && make proofread-mark`
- 強制ゲート付き出力: `cd papers/<paper_id> && make qa-full`
- `qa-full` は、`proofread-mark` 後に本文/設計/参考文献が更新されているとFAILで停止します。

## ルール反映先の判断基準

- `global` : 論文横断で使う規則。反映先は `AGENTS.md`（親）。
- `paper` : 単一論文固有の規則。反映先は `papers/<paper_id>/AGENTS.md`。
- `skill` : 特定スキル手順の改善。反映先は `.agents/skills/<skill_name>/SKILL.md`。

## 修正ログ運用フロー

1. 記録: `governance/preference_log.csv` に「1修正1行」で追記。
2. 採用判断: 同種修正の再発頻度・効果を確認。
3. 反映: 採用時に `AGENTS.md` または `.agents/skills/<skill_name>/SKILL.md` へ反映。
4. 履歴化: `governance/rule_changelog.md` に採用変更を記録。

## 親AGENTSへの手動反映手順

- preview: `python scripts/update_root_agents_from_log.py --project-root . --dry-run`
- update: `python scripts/update_root_agents_from_log.py --project-root .`
- 結果確認: `AGENTS.md` の `<!-- BEGIN AUTO_RULES -->` 〜 `<!-- END AUTO_RULES -->` の差分と `governance/rule_changelog.md` の追記内容
