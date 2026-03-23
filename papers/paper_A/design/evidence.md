# Evidence Library— Project <TBD>
> 目的: 決定に使う一次根拠の倉庫。plan.md は結論のみ、本ファイルは根拠の詳細を保持。

## 0. 運用
- 参照: `design/01_requirements.md`, `design/02_plan.md`, `refs/references.bib`
- ルール: 本文で使う書誌は **[@citekey]** のみ。原文抜粋は短く、出典ページ/図番号を付す。
- 更新: 「追加/修正は evidence.md → plan.md」の順で反映。Plan には数値は置かない。

## 1. エビデンス・インベントリ（採用候補）
| citekey | 種別 | 主所見/数値（短縮） | 集団/設定 | 備考（図/表/頁） | RoB/質 |
|---|---|---|---|---|---|
| Surname2021Review | Review | … | … | Fig2, p.5 | 低 |
| Seminal1998Trial  | RCT    | … | … | Table1, p.3 | 中 |

## 2. パケット（採用予定の詳細）
### [@Surname2021Review]
- 主要ポイント: …  
- 抜粋（短）: “… ” (p.5)  
- 主要数値: n=…, 効果量 … (95%CI …)  
- 適用範囲/限界: …  
- 用途（plan への紐付け）: Intro P1, Disc P2

### [@Seminal1998Trial]
- 主要ポイント: …  
- 抜粋: “… ” (Table 1)  
- 数値: …  
- 用途: …

## 3. データ抽出表（Results/Meta 連携が必要な場合）
| outcome | 比較 | 効果量 | 95%CI | p | 備考 |
|---|---|---|---|---|---|
| … | … | … | … | … | … |

## 4. 除外ログ（なぜ採用しないか）
| citekey | 除外理由（年代/集団/手法/質） | 代替 |
|---|---|---|
| Old2001Cohort | 過去規格・集団不一致 | New2022Cohort |

## 5. リスク・オブ・バイアス / 品質評価（簡易）
- ツール: RoB2 / ROBINS-I / AMSTAR2 など（必要な行のみ）
- [@Surname2021Review]: AMSTAR2 中  
- [@Seminal1998Trial]: RoB2 低

## 6. 未解決事項 / 追加収集タスク
- 例: 予測モデルの外部検証文献が不足 → 2件追加探索（TRIPOD）
