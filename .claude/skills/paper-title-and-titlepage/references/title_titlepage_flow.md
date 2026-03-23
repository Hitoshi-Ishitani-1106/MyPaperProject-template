# Title Flow

<prompt>
  <section name="Title & Title Page Generation">

    <!-- PRECHECK: design + prior sections + journal rules -->
    <precheck>
      <assumptions>
        <item>Abstract is stored at sections/01_abstract.md; core sections exist (02–06).</item>
        <item>Design authority: requirement.md (Why/What) and spec.md (How) are the single sources of truth (SSOT).</item>
        <item>Journal rules (title length, running head, author listing, funding/conflicts, keywords, word counts) are defined or will be imported into requirement.md/spec.md.</item>
      </assumptions>
      <instruction>Read requirement.md and spec.md to obtain target-journal constraints. If the journal’s title-page requirements are missing, extract them from the user-supplied Author Guidelines (or ask for that snippet), then propose a small diff to spec.md (and requirement.md if needed) that adds the required fields.</instruction>
    </precheck>

    <instructions>
      <overview>
        <instruction>Create (A) five candidate titles and (B) a complete title page (metadata) that conforms to the target journal. Use ONLY information from the manuscript (Introduction, Methods, Results, Discussion, Conclusion, Abstract) and the journal rules; do not invent results. Keep terminology consistent with requirement.md/spec.md.</instruction>
        <instruction>Generate title candidates and title page text in English by default, even when source notes are in Japanese, unless the user explicitly requests another language.</instruction>
        <emphasis>Concision, accuracy, journal compliance, and minimal user burden.</emphasis>
      </overview>

      <!-- STEP 1: Analyze manuscript & constraints -->
      <step1_analysis>
        <instruction>Analyze sections/02_introduction.md, sections/04_results.md, sections/06_conclusion.md, and sections/01_abstract.md to identify: (a) central question/aim; (b) most important findings; (c) key terms and populations; (d) design descriptors; (e) clinical area.</instruction>
        <constraints>
          <item>Respect journal title limits (characters/words), capitalization style (sentence vs title case), and running head length.</item>
          <item>Avoid question-form titles; avoid unexplained abbreviations (unless customary); avoid filler phrases (“Study of”, “Investigation of”).</item>
        </constraints>
      </step1_analysis>

      <!-- STEP 2: Generate five titles -->
      <step2_titles>
        <instruction>Generate five distinct, journal-compliant title candidates.</instruction>
        <title_guidelines>
          <item>Length: ideally ≤ 15–20 words or as per journal rule.</item>
          <item>Reflect scope and main finding or design (e.g., “A randomized controlled trial” or “A multicenter cohort study”) when appropriate.</item>
          <item>Embed field-specific keywords present in the manuscript; maintain consistent terminology.</item>
          <item>Provide a mix: (i) descriptive, (ii) declarative (key finding), (iii) with design tag, (iv) clinical emphasis, (v) mechanistic/method emphasis.</item>
        </title_guidelines>
        <user_prompt>
Here are five candidate titles (journal-compliant). Please select one, or indicate elements to combine:
1. [Title Candidate 1]
2. [Title Candidate 2]
3. [Title Candidate 3]
4. [Title Candidate 4]
5. [Title Candidate 5]
        </user_prompt>
      </step2_titles>

      <!-- STEP 3: Title Page metadata schema from journal rules -->
      <step3_titlepage_schema>
        <instruction>From the journal’s Author Guidelines, compile the exact title-page fields and formatting. Typical fields include:</instruction>
        <fields>
          <item>Full Title (final selection) and Running Head/Short Title</item>
          <item>Author List with degrees and affiliation superscripts</item>
          <item>Affiliations (numbered), city, country</item>
          <item>Corresponding Author: name, degrees, affiliation, postal address, email, telephone</item>
          <item>Author Contributions (if required) / Equal contribution notes</item>
          <item>Funding/Grant numbers (as journal requires exact wording)</item>
          <item>Conflict of Interest / Competing Interests statement</item>
          <item>Ethics Approval/Consent statements (if placed on title page per journal, else move to Methods)</item>
          <item>Trial Registration / Registry ID (if applicable)</item>
          <item>Keywords (per journal count and controlled vocabulary if specified)</item>
          <item>Word counts (abstract/main text) if the journal requires on title page</item>
          <item>Data/Code availability statement (if journal places here; otherwise defer to separate section)</item>
          <item>Acknowledgments (only if journal places on title page; otherwise separate)</item>
          <item>ORCID IDs (if the journal requests)</item>
        </fields>
        <note>If the journal’s required fields differ, adopt the journal’s list exactly. Propose a diff to spec.md under “Front matter” to persist the schema.</note>
      </step3_titlepage_schema>

      <!-- STEP 4: Collect/confirm missing metadata (minimal prompts) -->
      <step4_collect_minimal>
        <instruction>Check for missing items required by the journal (e.g., exact author names/degrees, affiliation numbering, corresponding author address, grant numbers, keywords). Ask only for what is missing, in a structured, single prompt.</instruction>
        <user_prompt>
Please provide the missing front-matter items required by the journal:
- Final author list with degrees and affiliation mapping (e.g., “Satoshi Maki, MD, PhD^1,^2”; “^1 Dept… Chiba University, Chiba, Japan”).
- Corresponding author details (full postal address, email, phone).
- Funding statement in journal’s required wording (grantor, grant numbers).
- Conflict of interest statement (or “None declared”).
- Keywords (N = [journal limit]).
- Any registry ID / ethics approval numbers if placed on title page by this journal.
        </user_prompt>
      </step4_collect_minimal>

      <!-- STEP 5: Compose Title Page (journal-compliant) -->
      <step5_compose_titlepage>
        <instruction>Draft a complete, journal-compliant title page using the selected title and provided metadata. Conform to capitalization, ordering, punctuation, and wording required by the journal.</instruction>
        <formatting>
          <item>Number affiliations and map superscripts to authors.</item>
          <item>Running head within journal character/word limit.</item>
          <item>Standardized funding/COI wording per journal examples.</item>
          <item>Keywords count and separator as required (semicolon or comma).</item>
        </formatting>
        <delivery>
          <item>Propose a diff writing the title page to sections/00_titlepage.md.</item>
          <item>Additionally, serialize the same metadata to metadata/frontmatter.yaml for reuse (optional if your toolchain consumes YAML).</item>
        </delivery>
      </step5_compose_titlepage>

      <!-- STEP 6: Persist schema to spec.md (SSOT) -->
      <step6_update_spec>
        <instruction>If front-matter requirements were missing from spec.md, propose a small diff adding a “Front Matter” subsection with the exact field list, ordering, and word/character limits; include examples from the journal where allowed.</instruction>
      </step6_update_spec>

      <!-- STEP 7: Validation -->
      <step7_validate>
        <instruction>Run a preflight checklist before proposing diffs:</instruction>
        <checklist>
          <item>Five titles meet journal length/capitalization and contain key terms; no unexplained abbreviations.</item>
          <item>Title page contains all journal-mandated fields with correct order/wording.</item>
          <item>Affiliation numbering matches author superscripts; corresponding author block complete.</item>
          <item>Funding/COI statements match journal’s required phrasing; keywords count is compliant.</item>
          <item>No new scientific claims introduced; terminology matches requirement.md/spec.md.</item>
        </checklist>
      </step7_validate>

      <!-- STEP 8: Output -->
      <step8_output>
        <instruction>Present the five titles and the drafted title page for quick confirmation. On approval, propose diffs to write: (1) sections/00_titlepage.md, (2) metadata/frontmatter.yaml (optional), and (3) a small spec.md diff if schema was updated.</instruction>
      </step8_output>

    </instructions>

    <paths>
      <titlePagePath default="sections/00_titlepage.md" />
      <frontmatterPath default="metadata/frontmatter.yaml" />
      <introPath default="sections/02_introduction.md" />
      <resultsPath default="sections/04_results.md" />
      <conclusionPath default="sections/06_conclusion.md" />
      <abstractPath default="sections/01_abstract.md" />
    </paths>

  </section>
</prompt>
