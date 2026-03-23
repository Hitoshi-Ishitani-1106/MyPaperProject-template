# Requirements Flow

<prompt>
  <section name="Requirements">
    <outputStyle>
      <instruction>Work in Japanese unless the user explicitly supplies English source text. Keep responses concise and action oriented.</instruction>
    </outputStyle>

    <process>
      <precheck>
        <instruction>Read `.codex/AGENTS.md`, `AGENTS.md`, and existing `design/01_requirements.md` to identify missing fields (投稿規定、PICO、語数/図表上限など)。Run `python scripts/design_gatekeeper.py --paper-dir <paper_dir> --stage requirements` first and treat reported items as mandatory missing inputs. `provisional_unknown`（例: 現時点で不明）が残る場合は、次へ進む前にユーザーへ明示確認を取る。</instruction>
      </precheck>

      <step_collect>
        <instruction>Ask the user for missing inputs in a single structured prompt. Include: 対象誌・投稿規定ソース、研究目的/PICO、語数・図表・参考文献上限、タイトルページ要件、想定読者、査読環境メモ。すでに埋まっている項目は再質問しない。</instruction>
      </step_collect>

      <step_validate>
        <instruction>Confirm whichファイルがSingle Source of Truthかを再掲し、未記入項目が残っていないかチェック。投稿規定は `skills/search-evidence-pubmed/references/search_flow.md` で扱うPMIDプレースホルダ運用と矛盾しないよう整合を取る。`design_gatekeeper --stage requirements` が PASS になるまで再確認する。もし `provisional_unknown` のみ残る場合は、ユーザーに「未確定のまま次に進むか」を確認し、同意時のみ `--allow-provisional-unknown` を使って暫定PASS扱いにする。</instruction>
      </step_validate>

      <step_diff>
        <instruction>Propose a diff for `design/01_requirements.md` that fills only the missing sections, keeps既存テキスト, and明示する: (a) evidence収集はPMIDベースで管理、(b) citekeyは採用確定後に発行, (c) 除外ログ運用は `design/evidence.md` を参照する。</instruction>
      </step_diff>

      <step_followup>
        <instruction>一覧表やチェックリストの更新が必要なら提案し、`map.tsv` など後続タスクの準備は plan フェーズに先送りする。requirements gate が FAIL の間は `design/02_plan.md` に進まない。</instruction>
      </step_followup>
    </process>
  </section>
</prompt>
