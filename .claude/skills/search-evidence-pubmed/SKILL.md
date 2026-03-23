---
name: search-evidence-pubmed
description: PubMed専用のevidenceブロック生成スキル。JSONログとQAゲートで検証する。
version: 0.1.0
language: ja
inputs:
  - section_name
  - theme
  - angle_tag
  - constraints
outputs:
  - design/evidence.md (追記ブロック)
  - data/search/*.json
requirements:
  - python3
  - internet access (NCBI E-utilities)
---

# Search Evidence (PubMed)

## 適用範囲
- PubMed公式 (NCBI E-utilities) のみ。
- 将来拡張: Embase/Scopusは別スキルとして分離する。

## 禁止事項
- 存在しないPMIDや推測での要約。
- 抄録/メタデータにない数値・結論の補完。
- QA未通過のまま `design/evidence.md` を更新すること。

## 入力
- `section_name`: Introduction / Discussion-Point1 等
- `theme`: 検索したい論点
- `angle_tag`: `direct` / `convergent` / `alternative` / `support-expansion`（未指定時は `general`）
- `constraints`: 年範囲、研究デザイン、成人/小児、レビュー除外など

## 出力
- `design/evidence.md` に追記する1ブロック (テンプレ準拠)
- `data/search/*.json` に機械可読ログ
- 任意で `data/search/*.md` に生成ブロック

## 実行手順 (必須)
0. 検索キュー入力（複数ターゲット）がある場合、同一主張内で `direct` → `convergent` → `alternative` → `support-expansion` の順に処理する。
1. `references/search_flow.md` を読み、検索クエリと抽出基準を整理する。
2. PubMedで候補PMIDを抽出し、PMIDのみ先行で記録する。
3. `scripts/pubmed_fetch.py` で PMIDメタデータ/抄録を取得し、JSON保存する。
4. 必要に応じ `scripts/dedup_pmids.py` で重複除去する。
5. 抄録ベースで要約を作成し、`data/search/*.json` にまとめる。
6. `scripts/build_evidence_block.py` でテンプレに埋め込んだMDブロックを生成する。
7. `scripts/qa_pmids.py` と `scripts/qa_evidence_block.py` を実行し **全PASS** を確認する。
8. PASS後のみ `design/evidence.md` へ **diff提案**で追記する。
9. Discussionの主張補強では、`angle_tag` 単位で別々の実行ログを残し、同一主張の多角根拠を混同しない。

## JSONログ仕様 (最小)
```json
{
  "section_name": "Introduction",
  "theme": "xxx",
  "angle_tag": "direct",
  "constraints": "2015- / 成人 / RCT優先",
  "run_date": "YYYY-MM-DD",
  "query": "PubMed query string",
  "selection_note": "関連性最優先...",
  "audit_log": {
    "retrieved": 0,
    "included": 0,
    "excluded": 0,
    "excluded_breakdown": { "duplicate": 0 },
    "shortage_reason": ""
  },
  "pmid_list": [
    {
      "pmid": "12345678",
      "title": "Title from PubMed",
      "journal": "Journal Name",
      "journal_abbrev": "J Abbrev",
      "year": "2021",
      "doi": "10.xxxx/xxxx",
      "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
      "first_author": "Smith",
      "abstract": "Abstract text..."
    }
  ],
  "papers": [
    {
      "pmid": "12345678",
      "rating": "★★★",
      "topic_summary": "日本語の短いテーマ要約",
      "design": "対象/デザイン/主要手法",
      "author": "Smith",
      "year": "2021",
      "journal_abbrev": "J Abbrev",
      "summary": "3-4文の要約（効果量が無ければ明記）"
    }
  ],
  "section_summary": "1段落の総括",
  "exclusions": [
    { "pmid": "00000000", "reason": "重複" }
  ]
}
```

## QAゲート
- `scripts/qa_pmids.py`: PMID実在 + Title/Journal/Year/DOI の一致検証。
- `scripts/qa_evidence_block.py`: ブロック構造・必須項目のlint。
- **どれか1つでも失敗したら** `design/evidence.md` には反映しない。理由と修正案を出す。

## 出力フォーマット
- `assets/evidence_block_template.md` に準拠。

## 使い方 (README風)
1. Codexに依頼: 「SearchEvidenceSkillを使って section=Introduction, theme=..., constraints=...」。
   - 角度を指定する場合: `angle_tag=direct|convergent|alternative|support-expansion`
2. 生成された `data/search/*.json` を確認し、必要なら修正。
3. `SearchEvidence: run` でブロック生成 (`data/search/*.md`)。
4. `SearchEvidence: qa` で QA を実行。
5. PASS後のみ `design/evidence.md` へ差分提案 → 承認 → 適用。

## 失敗時の確認先
- `data/search/*.json` (入力ログ)
- `data/search/*.md` (生成ブロック)
- `scripts/qa_*.py` の標準出力/エラー
