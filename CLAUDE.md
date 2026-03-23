# AGENTS (Global Rules)

このファイルは `MyPaperProject` 全体に適用する共通ルールです。

## 文体・表記
- 断定を避け、データに基づく記述を優先する。
- 略語は初出で定義し、以降は同一略語に統一する。
- 単位・数値フォーマット・時制を原稿内で統一する。
- 統計記述は原則 `効果量 -> 95%CI -> p値` の順で記載する。

## 言語ポリシー
- ユーザー対話と設計文書（`design/01_requirements.md`, `design/02_plan.md`, `design/evidence.md`）は日本語をデフォルトとする。
- 原稿本文（`sections/00_titlepage.md`, `sections/01_abstract.md`, `sections/02_introduction.md`, `sections/03_methods.md`, `sections/04_results.md`, `sections/05_discussion.md`, `sections/06_conclusion.md`）は、ユーザーが明示しない限り英語で作成・更新する。
- 入力資料（抄録・メモ・エビデンス）が日本語でも、本文の出力言語は英語デフォルトを維持する。

## フェーズゲート（必須）
- `sections/02_introduction.md` 以降の本文執筆を開始する前に、必ず `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements` と `--stage plan` を実行し、両方PASSであることを確認する。
- requirements gate が FAIL の場合は、本文執筆を中断し、`$paper-requirements` で不足情報の質問と `design/01_requirements.md` 更新を先に完了させる。
- plan gate が FAIL の場合は、本文執筆を中断し、`$paper-plan`（必要に応じて `search-evidence-pubmed`）で `design/02_plan.md` を先に完了させる。
- ユーザーが最初にアブストラクトだけを渡した場合でも、上記ゲートを満たすまでは本文ドラフト（`sections/02`〜`sections/06`）を書き始めない。
- 最終出力は `make qa-full` を推奨し、`$paper-proofread-all` 実施後に `python scripts/qa_proofread_gate.py --mark` で記録されていない場合は出力前に停止する。

## 引用・再現性
- 本文中の引用は Pandoc 形式 `[@citekey]` を使用する。
- 参照先は各論文ディレクトリ配下の `refs/references.bib` をSSOTとする。
- 再現性に関わる設定変更は、該当論文の `design/` と `scripts/` に記録する。
- 引用実在性と引用文脈の整合は `python scripts/qa_citation_web.py` で検証し、FAIL時は修正完了まで次工程へ進まない。

## ルール反映の基本方針
- 複数論文で再利用されるルールはこの親 `AGENTS.md` に反映する。
- 論文固有の制約は `papers/<paper_id>/AGENTS.md` に反映する。
- スキル固有の手順は `skills/<skill_name>/SKILL.md` に反映する。

## Auto-updated preferences

<!-- BEGIN AUTO_RULES -->
Generated at: 2026-02-07T13:33:55
Conditions: days=30, threshold=3, include-paper-rules=false

No rules matched current conditions.
<!-- END AUTO_RULES -->
