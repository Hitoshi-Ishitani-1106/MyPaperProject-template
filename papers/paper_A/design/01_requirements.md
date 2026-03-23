# 要件定義書 (Requirements) — Medical Paper Project

> **目的**: Codex と対話しながら、PICO、投稿規定、フロントマター、スタイル要件を明示し、以後の計画 (`design/02_plan.md`)・執筆・校正の単一の真実源（SSOT）とする。

---

## 0. プロジェクト概要
- **Project Title (internal)**: TBD
- **Target Submission Window (absolute date)**: TBD (YYYY-MM-DD)
- **Manuscript Type**: TBD（例: Original Article / Brief Report / Systematic Review）
- **Study Design (for EQUATOR)**: TBD（例: RCT / Cohort / Case–Control / SR/MA / TRIPOD）

---

## 1. PICO（または研究質問の等価枠組み）
- **Population**: TBD  
- **Intervention / Exposure / Index**: TBD  
- **Comparison / Reference**: TBD  
- **Outcomes (Primary, Secondary)**: TBD  
- **Timeframe / Setting**: TBD  

> **注**: 以後の用語はここに定義した語を正とし、表記揺れを避ける。

---

## 2. 投稿情報（ジャーナル規定）
- **Target Journal**: TBD（正式誌名）
- **Article Category**: TBD（誌の分類名）
- **EQUATOR Guideline**: TBD（例: CONSORT / STROBE / PRISMA / TRIPOD / ARRIVE / CARE）
- **Word Count Limit (main text)**: TBD（数値のみ）
- **Abstract**: 
  - **Structure**: TBD（Structured: Background/Methods/Results/Conclusions | Unstructured）
  - **Word Limit**: TBD
- **References Cap**: TBD（最大件数）
- **Tables / Figures Limits**: Tables = TBD, Figures = TBD, **Supplementary** 可否: TBD
- **Keywords**: 上限 TBD（語），区切り TBD（comma / semicolon）
- **Running Head / Short Title**: 文字数上限 TBD（または語数）
- **House Style Notes**: TBD（例: Title case / Sentence case、英綴/米綴 など）

---

## 3. フロントマター（タイトルページ要件）
> ここは誌の「Instructions for Authors / Title Page」指示を忠実に反映する。未定義なら TBD を残す。

- **Full Title**: TBD  
- **Running Head / Short Title**: TBD（上限に適合）  
- **Authors**:  
  - 形式: 氏名, 学位, 上付番号（所属対応）  
  - 例: Satoshi Maki, MD, PhD^1,^2  
  - **Equal Contribution / Joint Senior**: TBD  
- **Affiliations (numbered)**:  
  - ^1 〇〇 Department, 〇〇 University, City, Country  
  - ^2 …（TBD）
- **Corresponding Author**: 氏名 / 所属 / 郵便住所 / Email / Tel（誌の必須形式）  
- **Funding Statement**（誌の定型文に準拠）: TBD（助成機関・課題番号）  
- **Conflict of Interest / Competing Interests**: TBD（例: None declared. / 文言指定）  
- **Ethics / IRB / Consent**: TBD（番号・日付・記載場所の規定）  
- **Trial Registration / Registry ID**: TBD（該当時）  
- **ORCID IDs**: 必須/任意: TBD（必要なら各著者のID）  
- **Word Counts**: Abstract = TBD / Main text = TBD（誌が要求する場合のみ）  
- **Data / Code Availability**: 記載位置と定型文: TBD  
- **Acknowledgments**: 記載位置（Title page / 本文末 / 別セクション）: TBD

---

## 4. 書式・スタイル（統一ルール）
- **Language**: English（誌の指定に合わせ英/米綴の統一: TBD）  
- **Citation Style (CSL)**: `refs/vancouver.csl`（原則）  
- **In-text Citations**: **Pandoc 形式 `[@citekey]`**（本文で手動書式禁止）  
- **Numerals / Units**: SI を基本。桁区切り・小数点・単位表記: TBD（例: space-separated SI units）  
- **Dates**: 絶対日付（YYYY-MM-DD）で統一  
- **Abbreviations**: 初出で定義（Full term (Abbrev)）→以降略語のみ。図表キャプション初出ならそこで定義。  
- **Paragraph Pattern**: topic → evidence → implication → bridge（3–6文）

---

## 5. データ・解析（再現性）
- **Primary Dataset / Source**: TBD  
- **Study Period (absolute dates)**: TBD（YYYY-MM-DD ～ YYYY-MM-DD）  
- **Analysis Sets**: ITT / PP / Safety の定義: TBD  
- **Statistical Software & Version**: TBD（例: R 4.4.0, Stata 18, Python 3.11; packages==versions）  
- **Random Seeds / Determinism Policy**: TBD  
- **Missing Data**: 想定機構（MCAR/MAR/MNAR）と処理（例: MICE, IPW）: TBD  
- **Primary Analysis**: モデル/効果量/共変量/検定/多重性制御: TBD  
- **Sensitivity / Subgroup**: 事前規定の有無と概要: TBD  
- **Pre-registration / Protocol**: 登録ID・URL: TBD  
- **Ethics Approval / Consent**: 番号・日付・同意形態: TBD  
- **Data/Code Availability**: 公開/制限/申請経路と場所: TBD

---

## 6. 表・図・付録（配置とポリシー）
- **Tables**: 上限・配置ルール（本文/補足）: TBD  
- **Figures**: 上限・配置ルール（本文/補足）: TBD  
- **Supplementary Materials**: 可否・命名（Figure S1 / Table S1）: TBD  
- **Caption Policy**: 略語定義を脚注に記載、統計指標・母数を明示

---

## 7. 品質・整合性ゲート（提出前チェック）
- **Citations**: すべての `[@citekey]` が `refs/references.bib` に解決  
- **Numbers**: Abstract ↔ 本文 ↔ 表/図 の主要数値（N, n/%, effect size, 95%CI, p 値）一致  
- **Word/Count Caps**: 本文語数、表図数、参考文献数が上限内  
- **Headings**: 見出しレベル/命名が誌の規定に合致  
- **Front Matter**: 3章の必須項目が**完全**かつ誌の定型文/順序に準拠  
- **Stat Reporting**: p 値は3桁（`p<0.001`のみ閾値）。効果量＋95%CIを優先

---

## 8. ビルド・提出物
- **Build Config**: `pandoc.yaml`（CSL で参考文献自動整形）  
- **Deliverables**: `sections/*.md`, `sections/00_titlepage.md`, `refs/references.bib`, （任意）`metadata/frontmatter.yaml`, 図表ファイル  
- **File Naming**: 図表/補足の命名規則: TBD

---

## 9. 運用ノート
- **変更管理**: すべて **diff 提案 → 承認 → 適用**。  
- **外部情報**: 参照禁止（本リポ内の情報のみ使用）。  
- **再生成**: Abstract は原稿完成後に**最終版で置換**（差分提示のうえ承認）。

---

### ☐ 設定完了チェック（初期オンボーディング）
- [ ] Target Journal の投稿規定（Abstract/Title page/図表/参考文献）を反映  
- [ ] EQUATOR ガイドライン選定  
- [ ] Keywords 上限・Running head 上限の確定  
- [ ] Funding/COI/倫理・登録IDの書式確定  
- [ ] Statistical software & versions / seeds / missing-data policy の確定

> **使い方**: [design_requirements] タスクで質問に回答し、TBD を順に埋めてください。完了後、本書が SSOT となり、`design/02_plan.md` と整合させます。
