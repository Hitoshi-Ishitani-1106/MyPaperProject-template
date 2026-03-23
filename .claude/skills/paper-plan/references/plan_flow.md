# Plan Flow

<prompt>
  <section name="Plan">
    <outputStyle>
      <instruction>Respond in Japanese. Use short actionable sentences and referenceファイル byパス when必要.</instruction>
    </outputStyle>

    <process>
      <precheck>
        <instruction>Read `design/01_requirements.md`, `design/evidence.md`, existing `design/02_plan.md`, and `skills/search-evidence-pubmed/references/search_flow.md` to capture constraints and現在のPMIDインベントリ。開始前に `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements` を実行し、PASS でなければ plan 作業を開始しない。`provisional_unknown` のみが残る場合は、ユーザーに次工程へ進めるか明示確認し、同意時のみ `--allow-provisional-unknown` を使って続行する。</instruction>
      </precheck>

      <step_evidence_sync>
        <instruction>List the最新のサーチブロック（`## 【セクション名】｜...`）を確認し、各論点に必要なPMIDがevidence.mdに揃っているか検証。欠けている場合は `search-evidence-pubmed` の再実行候補として記録する。</instruction>
      </step_evidence_sync>

      <step_placeholder_plan>
        <instruction>Draft or update `design/02_plan.md` so that引用はすべて `[pmid:XXXXXXXX]` 形式のプレースホルダを用いる（角括弧 + 接頭語 pmid: + 数字のみ）。数値や詳細な効果量は evidence.md に留め、Plan 側は主張ゴールと参照の位置づけに集中する。入力が未確定でも致命的でない場合は、後続ステップで置換できるよう `TBD:` や `<<placeholder>>` など明確なプレースホルダを残し、未決項目をチャットで列挙する。</instruction>
      </step_placeholder_plan>

      <step_exclusion_log>
        <instruction>Ensure `design/evidence.md` の「除外ログ」に未採用PMIDと理由（重複/症例報告/対象外など）が追記されているか確認し、欠落があればユーザーに補記を促す。</instruction>
      </step_exclusion_log>

      <step_prioritise>
        <instruction>セクションごとに「用途タグ（例：Intro Known、Results Primary）」を提示し、PMIDの優先順位を提案。`design/evidence.md` の最新ブロックと星評価（★★★/★★/★）を参照し、まずは★★★を採用候補に挙げ、不足時のみ★★以下を補完する。原著では**PICOに直接一致する高品質研究**を最優先で押さえ、Discussion の主張コアはこれらを根拠に構成する。そのうえで全体像の妥当性を示す補強として系統的レビュー/メタ解析を配置する。レビューは最大3件、古典は最大3件までとし、原著優先ルールも併記。</instruction>
      </step_prioritise>

      <step_evidence_angle_matrix>
        <instruction>Discussion の P2/P3 の各主張には必ず「Evidence Angle Matrix」を設ける。最低3角度を明示する：`Direct`（主張とPICOが直接一致）、`Convergent`（別設計/別集団でも同方向）、`Alternative/Boundary`（別解釈・境界条件）。各角度に `[pmid:XXXXXXX]` を割り当て、最低要件 `Direct>=2`, `Convergent>=1`, `Alternative>=1`, 合計>=4 を満たす。</instruction>
      </step_evidence_angle_matrix>

      <step_auto_search_trigger>
        <instruction>Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage search-targets --json` to auto-detect citation gaps and depth gaps from `design/02_plan.md` (especially Introduction and Discussion). For each returned target, automatically invoke `$search-evidence-pubmed` with: `section_name`, `theme` (generated keywords), `constraints` (2015- / 成人優先 / 原著中心 / レビュー≤3), and `angle_tag` when provided (`direct` / `convergent` / `alternative` / `support-expansion`). Append approved evidence blocks to `design/evidence.md`, then reflect new `[pmid:XXXXXXX]` placeholders back into `design/02_plan.md`.</instruction>
      </step_auto_search_trigger>

      <step_diff>
        <instruction>Propose diffs for `design/02_plan.md` only. Diff should: (a) 保持する既存本文, (b) 参照は `[pmid:XXXXXXX]`, (c) P段落ごとに目的→証拠→含意を述べる, (d) Discussion P2/P3 に角度別根拠（Direct/Convergent/Alternative）を明示。citekeyやBibTeXは生成しない。適用後に `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage plan` を実行し、PASS でなければ次工程へ進まない。</instruction>
      </step_diff>

      <step_freeze_plan>
        <instruction>After the plan is承認されたら、以下の5ステップを人間に実行してもらうよう必ず案内する：(1) `design/02_plan.md` と `design/evidence.md` からPMIDを抽出（例: 正規表現 `\[pmid:(\d+)\]` → `map.tsv` 作成）、(2) 採用PMIDについてBibTeXを整備し `refs/references.bib` へ登録、(3) `[pmid:XXXXXXX]` を `[@citekey]` に一括置換、(4) `python scripts/qa_citation_web.py --scope core --report reports/qa_citation_web_prewrite.md` を実行して実在・意図整合を確認、(5) 置換後の Plan と関連セクションを確認。未実施の場合は本文執筆に進まないよう繰り返し注意喚起する。</instruction>
      </step_freeze_plan>
    </process>
  </section>
</prompt>
