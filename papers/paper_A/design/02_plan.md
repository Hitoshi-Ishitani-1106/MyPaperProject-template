# 計画書 (Plan) — Medical Paper Project

> **目的**: `design/01_requirements.md`（SSOT）と `design/evidence.md` を基に、章構成・段落ゴール・引用計画・図表計画を定義し、執筆/校正/最終出力の一貫性を担保する。

---

## 0. 入力と適用範囲
- **参照**: `design/01_requirements.md`, `design/evidence.md`, `refs/references.bib`
- **対象誌**: TBD（要件は requirements に準拠）
- **EQUATOR**: TBD（例: CONSORT / STROBE / PRISMA / TRIPOD）
- **用語・単位**: 本計画の「§7 用語表・数値規則」を正とする

---

## 1. 理論アーク（Theory Arc）
- **Selected Arc**: TBD（1–2文で主張の流れを明示）
- **Alternatives**  
  - **A**: TBD（利点/懸念）  
  - **B**: TBD（利点/懸念）  
  - **C**: TBD（利点/懸念）  
- **採用理由**: TBD（対象誌との適合性・新規性・臨床的意義）

---

## 2. 主張マップ（Claims & Evidence Map）
> 各段落は **topic → evidence → implication → bridge**（3–6文）。**引用は `[@citekey]`** のみ。

### 2.1 Introduction
- **P1: Field & Significance**  
  - 主張: TBD  
  - 主要エビデンス: TBD（例: [@ReviewYYYYTopic], [@SeminalYYYYTopic]）
- **P2: Gap / Limitation / Controversy**  
  - 主張: TBD  
  - 主要エビデンス: TBD（最新 SR/MA または大規模コホート ≥2）
- **P3: Aim & Overview**  
  - 主張: 明示的目的/仮説 + 方法概観（自家情報。引用不要）  
  - リンク: Methods への橋渡し

### 2.2 Methods（EQUATOR 準拠のサブ見出しと最小要件）
> **選択ガイドライン**: TBD（CONSORT/STROBE/TRIPOD/PRISMA 等）

- **Study Design**: 研究種別・期間（絶対日付）・施設  
- **Participants / Setting**: 組入/除外、対象集団定義、倫理番号/同意  
- **Interventions / Exposures / Index & Reference (該当時)**: 内容・実施・遵守  
- **Outcomes / Variables**: 定義、測定時点、尺度  
- **Sample Size**: 事前算定/根拠、仮定、α、power  
- **Randomization / Allocation / Blinding（該当時）**: 手順、隠蔽  
- **Data Sources & Measurement**: 器具/ソフト（メーカー/バージョン）、較正  
- **Missing Data**: 機構（MCAR/MAR/MNAR）と処理（例: MICE）  
- **Statistical Analysis**: 主解析モデル、効果量、共変量、相互作用、感度解析、Multiplicity  
- **Prediction（TRIPOD 時）**: 前処理、再標本化、ハイパーパラメータ、内部/外部検証、評価指標（AUC・校正）  
- **Reproducibility**: OS/言語/パッケージ==version、乱数seed、登録ID、コード/データの所在

### 2.3 Results（Methods の鏡像）
- **Participants/Flow**: 解析集団（ITT/PP/安全）・除外理由（図: Flow）  
- **Baseline / Exposures / Index Tests**: 群別要約 + 母数  
- **Primary Outcome**: 効果量 + 95%CI + p 値（3桁）  
- **Secondary / Exploratory**: 同様、Multiplicity 方針を明示  
- **Sensitivity / Subgroup**: 方向・大きさ・一貫性  
- **Prediction（TRIPOD）**: AUC(95%CI)、校正傾き/切片、Brier、外部検証

### 2.4 Discussion（5 段落の計画）
- **P1 要約**: 主要所見 1・2 の簡潔提示と意義  
- **P2 解釈#1**: 所見1の解釈（整合/相違、機序/方法論的説明）  
- **P3 解釈#2**: 所見2の解釈（サブグループ含意があれば）  
- **P4 含意**: 臨床/政策/理論、一般化可能性、代替解釈への対応  
- **P5 限界と今後**: バイアス方向/大きさ、具体的将来研究案、要点

### 2.5 Conclusion（3–4文）
- 研究の中核的貢献と含意（新規情報や限界の導入はしない）

---

## 3. 引用計画（Citation Plan）
- **必要配分（最小）**: Review ≥1、Seminal ≥1、最新 SR/MA or 大規模コホート ≥1  
- **予定 citekeys（追加可）**:  
  - Introduction P1: [@Surname20XXTopic], [@Seminal19XXKey]  
  - P2: [@RecentSR20XXKey], [@Cohort20XXKey]  
  - Methods（手法引用が必要な場合）: [@Method20XXTool]  
- **Bib 運用**: すべて `refs/references.bib` に登録。欠落項目は `normalize_and_register_citations` で補完。

---

## 4. 図表計画（最小構成と役割）
> 章本文は重複記述を避け、**要点＋図表参照**で記述する。

- **Figure 1. Participant Flow**（CONSORT/STROBE/PRISMA）  
  - 役割: 解析集団・除外の透明化
- **Table 1. Baseline Characteristics**  
  - 役割: 群の比較可能性と分布
- **Table 2. Primary Outcome & Sensitivity Analyses**  
  - 役割: 主要効果量、95%CI、p 値、感度分析
- **Table 3. Secondary Outcomes**  
  - 役割: 主要以外の結果の整理
- **Figure 2. Model Performance & Calibration（TRIPOD 時）**  
  - 役割: 識別・校正の可視化
- **Supplementary（必要時）**: Figure S1 / Table S1（命名規則は requirements）

> **脚注方針**: 略語定義・母数・統計手法の要約を記載。

---

## 5. フロントマター（タイトルページ計画の反映）
- **必須項目**: Full Title / Running head（上限）/ 著者 + 学位 + 上付所属 / 所属一覧 / Corresponding（住所・Email・Tel）/ Funding（助成名・番号・定型文）/ COI / Ethics・登録ID（誌の規定による）/ Keywords（上限・区切り）/ ORCID（必要時）/ Word counts（誌が要求する場合）  
- **保存先**: `sections/00_titlepage.md`（必要に応じ `metadata/frontmatter.yaml` に複製）  
- **不足時**: `design/01_requirements.md` を更新（diff 提案）

---

## 6. セクション別ゴール（執筆時のチェック用）
- **Introduction**: 問題の意義 → 具体的ギャップ → 明示的目的  
- **Methods**: 再現可能性（装置/版数/seed/解析仕様/欠測）  
- **Results**: Methods 鏡像の順序・母数整合・効果量＋95%CI  
- **Discussion**: 過度な因果表現回避（観察研究）、一般化可能性と代替解釈  
- **Conclusion**: 3–4文、要点と意義、**新情報を追加しない**

---

## 7. 用語表・数値規則（Glossary & Numerics）
- **用語表（正規形）**:  
  - 例）myocardial infarction（MI）/ chronic obstructive pulmonary disease（COPD）/ …（TBD）
- **数値規則**:  
  - p 値: 小数 3 桁（`p<0.001` 例外）  
  - 効果量: OR/HR/RR/MD/Δ のいずれかを明示、**95%CI** 併記  
  - 母数: **N, n/%** を明示、解析集団（ITT/PP/安全）を付記  
  - 単位: SI を基本、桁と小数の統一（TBD）  
  - 日付: YYYY-MM-DD の絶対日付

---

## 8. ジャーナル適合（要件トラッキング）
- **語数上限（本文/Abstract）**: TBD / TBD  
- **図表上限**: Tables = TBD, Figures = TBD, Supplementary = TBD  
- **参考文献上限**: TBD  
- **Heading 命名/大文字規則**: TBD（Title case / Sentence case）  
- **チェック**: 超過時の圧縮方針（どこを何語削るか）: TBD

---

## 9. 実行計画（Diff 運用）
- **Introduction**: P1→P2→P3 の順に `sections/02_introduction.md` へ diff 提案  
- **Methods**: 上記サブ見出しで `sections/03_methods.md` へ diff 提案  
- **Results**: Methods 鏡像で `sections/04_results.md` へ diff 提案  
- **Discussion**: 1 段落ずつ承認→`sections/05_discussion.md` に追記  
- **Conclusion**: 3–4 文を `sections/06_conclusion.md` に提案  
- **Abstract（最終置換）**: 完成後に `sections/01_abstract.md` を置換 diff  
- **Title Page**: `sections/00_titlepage.md` を作成/更新（不足メタは一括質問）

---

## 10. 未決事項（TBD リスト）
- Target Journal / Article Category / EQUATOR / 主要引用候補（citekeys）/ Keywords 上限・区切り / Running head 上限 / Funding 文言・番号 / COI 文言 / 統計ソフト & 版数 / seeds / 欠測処理 / 図表上限 / 参考文献上限 / 用語表の確定

---

> **更新方法**: [design_plan] タスクを実行し、上記の **TBD** を `diff` で埋めてください。以後、執筆・校正は本計画に**厳密準拠**します。
