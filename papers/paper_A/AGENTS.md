# AGENTS (paper_A Specific)

このファイルは `paper_A` 専用ルールです。

## 対象
- 対象ディレクトリ: `papers/paper_A/`
- 本文: `sections/`
- 設計: `design/`

## 投稿規定・制約（論文固有）
- 投稿先・語数・図表上限・必須セクションは `design/01_requirements.md` をSSOTとする。
- 章構成と主張順序は `design/02_plan.md` をSSOTとする。
- 根拠の出典ログは `design/evidence.md` をSSOTとする。
- 言語ポリシー: `design/*` は日本語デフォルト。`sections/00_titlepage.md` 〜 `sections/06_conclusion.md` は、ユーザーが明示しない限り英語で作成・更新する。

## 編集ルール
- 本文の意味変更を伴う改稿は、設計資料との整合を確認してから行う。
- 図表・引用の参照整合が崩れる変更は、必ず同一PR/同一変更で修正する。
- 本文執筆（`sections/02`〜`sections/06`）を開始する前に `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements` と `--stage plan` を実行し、両方PASSを確認する。FAIL時は執筆を止め、`design/` を先に更新する。
- 引用実在/意図整合のゲートとして、執筆前に `python scripts/qa_citation_web.py --scope core --report reports/qa_citation_web_prewrite.md`、出力前に `python scripts/qa_citation_web.py --scope all --report reports/qa_citation_web.md` を実行し、FAIL時は修正完了まで次へ進まない。
- 最終出力前に `$paper-proofread-all` を実行し、`python scripts/qa_proofread_gate.py --mark` で記録する。最終出力は `make qa-full` を使う。
