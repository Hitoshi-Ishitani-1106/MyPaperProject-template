# AGENTS (Paper-Specific Template)

- 論文固有ルール（対象、投稿規定、語数、図表制約）をここに記載する。
- 全体共通ルールは親 `AGENTS.md` を参照する。
- 言語ポリシー: `design/*` は日本語デフォルト、`sections/00_titlepage.md` 〜 `sections/06_conclusion.md` はユーザー明示がない限り英語で作成する。
- フェーズゲート: `sections/02` 以降の本文執筆前に `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements` と `--stage plan` の両方が PASS であることを確認し、FAILなら本文を書かずに設計を先に埋める。
- 引用ゲート: 執筆前は `python scripts/qa_citation_web.py --scope core --report reports/qa_citation_web_prewrite.md`、出力前は `python scripts/qa_citation_web.py --scope all --report reports/qa_citation_web.md` を実行し、FAILなら進行停止する。
- proofreadゲート: `$paper-proofread-all` 実施後に `python scripts/qa_proofread_gate.py --mark` で記録し、最終出力は `make qa-full` で実行する。
