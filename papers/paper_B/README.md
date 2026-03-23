# paper_B

既存論文資産を移行したワークスペースです。

## QA Flow
1. 執筆前（Intro/Discussion）  
   `python scripts/qa_citation_web.py --scope core --report reports/qa_citation_web_prewrite.md`
2. 出力前（全引用）  
   `python scripts/qa_citation_web.py --scope all --report reports/qa_citation_web.md`
3. proofread完了をマーク  
   `make proofread-mark`
4. proofreadゲート + 統合QA + DOCX出力（推奨）  
   `make qa-full`
5. （ゲートを使わない従来経路）統合QA + DOCX出力  
   `make qa`
