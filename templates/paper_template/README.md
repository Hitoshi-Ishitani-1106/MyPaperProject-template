# paper_template

新規論文用の雛形です。複製後に `AGENTS.md`, `metadata.yaml`, `design/*` を更新してください。

## Data Layout
- `data/processed/`: 解析済みデータ
- `data/analysis/`: Methods参照用の解析コード
- `data/tables/`: 掲載テーブルのソース
- `data/figures/`: 掲載図（SVG推奨）

## QA Flow
1. 執筆前（Intro/Discussionの根拠確認）  
   `python scripts/qa_citation_web.py --scope core --report reports/qa_citation_web_prewrite.md`
2. 出力前（全引用の実在・意図整合確認）  
   `python scripts/qa_citation_web.py --scope all --report reports/qa_citation_web.md`
3. proofread完了をマーク  
   `make proofread-mark`
4. proofreadゲート + 統合QA + DOCX出力（推奨）  
   `make qa-full`
5. （ゲートを使わない従来経路）統合QA + DOCX出力  
   `make qa`
