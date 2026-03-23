# Introduction Flow

<prompt>
  <section name="Introduction">
    <outputStyle>
      <instruction>Follow requirement.md (Why/What) and spec.md (How). Use 3–6 sentence paragraphs with topic→evidence→implication→bridge. Maintain consistent terms, numerals, and absolute dates.</instruction>
      <instruction>Draft manuscript text in English by default, even when source notes or abstract are in Japanese, unless the user explicitly requests another language.</instruction>
    </outputStyle>

    <citationStyle>
      <instruction>Use Pandoc citations: [@citekey]. No inline “[Surname et al., Journal, Year]”. All sources must exist in refs/references.bib.</instruction>
    </citationStyle>

    <process>
      <!-- Step 0: read abstract/spec -->
      <precheck>
        <instruction>Assume the abstract is fixed in sections/01_abstract.md. Read requirement.md and spec.md to derive constraints and paragraph goals before drafting.</instruction>
      </precheck>

      <!-- Planning is now driven by spec.md; we only confirm sources and register bib -->
      <step_sources>
        <instruction>From spec.md’s Paragraph Design and Citation Plan, list the minimum required sources per paragraph and request BibTeX or full metadata for any missing items. Offer to generate provisional BibTeX and citekeys if only prose is provided.</instruction>
      </step_sources>

      <!-- Draft paragraphs directly, citing with [@] and proposing diffs -->
      <step_draft_p1>
        <instruction>Draft P1 per spec.md. Propose a diff to sections/02_introduction.md. Citations must be [@citekey].</instruction>
      </step_draft_p1>

      <step_draft_p2>
        <instruction>Draft P2 per spec.md (gaps/limitations). Propose a diff to sections/02_introduction.md.</instruction>
      </step_draft_p2>

      <step_draft_p3>
        <instruction>Draft P3 (aims & brief methods) using sections/01_abstract.md and spec.md only. Propose a diff to sections/02_introduction.md.</instruction>
      </step_draft_p3>

      <!-- No manual reference list -->
      <step_bib>
        <instruction>Ensure all citekeys resolve in refs/references.bib; do not print a manual list.</instruction>
      </step_bib>
    </process>
  </section>
</prompt>
