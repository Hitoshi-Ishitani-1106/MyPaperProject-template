# paper_A

既存論文資産を移行したワークスペースです。

## 構成
- `sections/` 本文
- `design/` 要件・計画・根拠
- `data/processed/` 解析済みデータ
- `data/analysis/` Methods参照用の解析コード
- `data/tables/` 掲載テーブルのソース
- `data/figures/` 掲載図（SVG推奨）
- `refs/` BibTeX と CSL
- `scripts/` QA など補助スクリプト
- `exports/` 生成物

## ビルド
```bash
make qa
```

`make qa` は `qa_references_style` → `qa_citation_web(scope=all)` → `qa_citations` の順に実行し、その後 `pandoc.yaml` で DOCX を生成します。
proofread完了を強制したい場合は、`make proofread-mark` の後に `make qa-full` を使ってください（mark後に本文が更新されると `qa-full` は失敗します）。

## 執筆前の推奨ゲート
```bash
python scripts/qa_citation_web.py --scope core --report reports/qa_citation_web_prewrite.md
```

Introduction / Discussion の主要主張で、引用文献の実在性と引用意図（文脈）が合っているかをWeb照合で確認します。
