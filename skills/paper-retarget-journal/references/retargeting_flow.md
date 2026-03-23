# Revision Flow

<retargeting-assistance-system name="Retargeting Flow (Free-Text Journal Guidelines)">

  <!-- PRECHECK -->
  <precheck>
    <assumptions>
      <item>SSOT: design/01_requirements.md（現行規定）と design/02_plan.md（理論アーク）。</item>
      <item>本文: sections/00_titlepage.md … 06_conclusion.md。書誌: refs/references.bib（Pandoc/CSL）。</item>
      <item>入力: ユーザーがチャットに貼り付けた **投稿規定の長文（原文）**。構造化不要。</item>
    </assumptions>
    <policy>
      <item>外部検索や推測は禁止。貼付テキストとSSOTのみで判断。</item>
      <item>本文変更は「PROPOSE（計画）→ APPROVE（承認）→ APPLY（diff）」の順。</item>
      <item>科学的主張やデータは変更しない（体裁・構造・語数・スタイルのみ適合）。</item>
    </policy>
  </precheck>

  <system-overview>
    Paste full author guidelines (free text). The system parses and normalizes key requirements, computes the delta vs current SSOT, proposes a minimal-change compliance plan, and generates unified diffs to make the manuscript submission-ready for the new journal.
  </system-overview>

  <!-- STEP 1: Free-text parsing & normalization -->
  <step1-ingest-parse-normalize>
    <actions>
      <item>長文から規定を抽出し、以下の **正規化スキーマ** にマッピングする。抽出根拠の原文断片（quote）と **信頼度 (high/med/low)** を付す。</item>
      <item>曖昧/欠落は“UNKNOWN”で保持し、**最小限**の確認質問だけを提示。</item>
    </actions>
    <schema name="JournalRequirements">
      <field>journal_name (string)</field>
      <field>article_type (enum/string)</field>
      <field>word_limit_main (int)</field>
      <field>abstract.type (structured/unstructured); abstract.word_limit (int); abstract.required_headings (list)</field>
      <field>keywords.max_count (int); keywords.delimiter (comma/semicolon)</field>
      <field>figures.max (int); tables.max (int); supplementary.policy (text)</field>
      <field>references.cap (int); references.style (CSL-like name or notes)</field>
      <field>titlepage.fields (ordered list: title, running_head_limit, authors_format, affiliations_format, corresponding_block, funding_text, coi_text, ethics_text, registration_text, data_availability_text, orcid, word_counts)</field>
      <field>spelling (US/UK); units_style (SI etc.)</field>
      <field>double_blind (yes/no); anonymization_rules (text)</field>
      <field>cover_letter.required (yes/no); cover_letter.notes (text)</field>
      <field>other.special (list: figure file formats, color policy, graphical abstract, checklist uploads etc.)</field>
    </schema>
    <output name="Normalized Requirements (PROPOSE)">
      <format>YAML block with fields above; each field includes: value, quote, confidence</format>
    </output>
    <user_prompt lang="ja">
      新雑誌の投稿規定を以下のように抽出しました（YAML）。不明は UNKNOWN として残しています。差分計画の作成に進めてよければ「approve delta」、不足を埋める場合は「revise: <項目>=<値>」と指示してください。確認が必要なのは次のみ：<自動選抜の要点質問（最大3項目）>
    </user_prompt>
  </step1-ingest-parse-normalize>

  <!-- STEP 2: Delta vs current SSOT -->
  <step2-delta-computation>
    <actions>
      <item>design/01_requirements.md（現行）とNormalized Requirements（新）を突合。差分表を生成。</item>
    </actions>
    <output name="Requirements Delta (PROPOSE)">
      <table columns="Rule | Old (requirements.md) | New (parsed) | Impact | Confidence">
        <!-- 例行で数行を埋める -->
      </table>
    </output>
    <user_prompt lang="ja">差分を確認してください。承認は「approve delta」。修正は「revise delta: <指示>」。</user_prompt>
  </step2-delta-computation>

  <!-- STEP 3: Minimal-Change Compliance Plan -->
  <step3-compliance-plan>
    <policy>意味保持・最小改変。語数/構成/タイトルページ/CSL/綴り/見出し/図表/参考文献の**定量適合**を優先。</policy>
    <plan name="Compliance Plan (PROPOSE)">
      <sections>
        <item>Abstract 再構成（構造化⇄非構造化、語数）</item>
        <item>Title page（著者・所属・コレスポ・Funding/COI/Ethics/Registration/Data availability の文言・順序）</item>
        <item>Main text 語数圧縮/拡張（優先削減: 重複→一般論→冗長説明）</item>
        <item>Figures/Tables 上限対応（統合/補足移行/連番更新/キャプション規則）</item>
        <item>References 上限対応（重複候補の間引き方針＋影響最小の候補列挙）</item>
        <item>Spelling/Style（US⇄UK、一括変換の除外語リスト付）</item>
        <item>CSL 切替（`pandoc.yaml` の csl: 更新、必要なら `refs/<new>.csl` 追加）</item>
        <item>Policy blocks（Data availability/Ethics/Registration/COI/Funding の定型化と挿入位置）</item>
        <item>匿名化（double-blind 時の自己引用/謝辞/データ共有の扱い）</item>
      </sections>
      <metrics>想定語数変動（章別）、削減/補足に回す図表/参考文献の候補リスト（理由付）。</metrics>
    </plan>
    <user_prompt lang="ja">計画を承認しますか？ 承認は「approve plan」。個別修正は「revise plan: <指示>」。</user_prompt>
  </step3-compliance-plan>

  <!-- STEP 4: Diffs generation & settings -->
  <step4-generate-diffs>
    <gate>「approve plan」後に実装。まずプレビューとして diff を提示、承認後に適用。</gate>
    <outputs>
      <item>sections/01_abstract.md（再構成/語数調整）の diff</item>
      <item>sections/00_titlepage.md（＋metadata/frontmatter.yaml 任意）の diff</item>
      <item>各章の語数圧縮/見出し命名修正の diff（最小改変）</item>
      <item>図表参照・キャプション・連番の diff、必要に応じ Supplementary への移行</item>
      <item>参考文献の間引き提案（本文 citekey は保持、`refs/references.bib` は原則不変）</item>
      <item>`pandoc.yaml` の `csl:` 差替 diff と `refs/<new>.csl` 追加 diff（必要時）</item>
      <item>US/UK 綴り一括変換の安全適用 diff（曖昧語は提案止まり）</item>
      <item>rebuttal/change_log.md に1行1変更で記録</item>
    </outputs>
    <user_prompt lang="ja">差分を提示しました。適用は「apply diffs」。個別適用は「apply: abstract, titlepage, intro…」。</user_prompt>
  </step4-generate-diffs>

  <!-- STEP 5: Final compliance review -->
  <step5-final-review>
    <checks>
      <item>語数/図表/参考文献/キーワード/Running head の定量合致</item>
      <item>Abstract 構造/語数/時制、禁止事項の遵守</item>
      <item>見出し階層・命名、匿名化要件の充足</item>
      <item>COI/Funding/Ethics/Registration/Data availability の誌定型文準拠</item>
      <item>Spelling（US/UK）と単位の全章一貫性</item>
      <item>`proofreading_flow_propose_approve_apply` を再実行</item>
    </checks>
    <user_prompt lang="ja">最終確認をお願いします。追加の微修正は「revise <対象>: <指示>」。</user_prompt>
  </step5-final-review>

  <!-- STEP 5.5: Word exports for submission -->
  <step5_5-word-export>
    <purpose>Prepare DOCX deliverables (clean and tracked) for the new journal.</purpose>
    <actions>
      <item>`pandoc --defaults=pandoc.yaml --output exports/retarget/R{round}_before.docx` を差分適用前に実行し、`apply diffs` 後に同コマンドで `R{round}_after.docx` を出力する（`mkdir -p exports/retarget`）。</item>
      <item>Microsoft Word の比較機能で `R{round}_before.docx` と `R{round}_after.docx` を突き合わせ、トラック変更付き `R{round}_tracked.docx` を作成する。</item>
      <item>タイトルページやカバーレターなど個別ファイルが必要なら `pandoc <file>.md --from markdown --to docx --output exports/retarget/<file>.docx` を用い、引用が必要な場合のみ `--citeproc --csl … --bibliography …` を追加する。</item>
      <item>必要に応じて QA ログやチェックリストを `exports/retarget/` に保存する。</item>
    </actions>
    <notes>
      <item>Before/After Docx を Word の比較に通すと、編集部に提出する公式トラック変更ファイルを生成できる。</item>
      <item>出力名は雑誌名やリビジョン番号に合わせて変更してよい。</item>
    </notes>
  </step5_5-word-export>

  <response-style>
    <lang>日本語で合意形成。出力（diff・定型文）は英語でも可。短文・正確・一貫性重視。</lang>
  </response-style>

</retargeting-assistance-system>
