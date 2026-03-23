# Discussion Flow

<prompt>
  <section name="Discussion">

    <!-- PRECHECK: read design + prior sections first -->
    <precheck>
      <assumptions>
        <item>Abstract is fixed at sections/01_abstract.md.</item>
        <item>Design authority: requirement.md (Why/What) and spec.md (How) are the single sources of truth.</item>
        <item>Citations must use Pandoc syntax [@citekey]; all items live in refs/references.bib. Do NOT print inline “[Surname et al., Journal, Year]”.</item>
      </assumptions>
      <instruction>Before drafting, read requirement.md, spec.md, sections/03_methods.md, and sections/04_results.md. Extract the paragraph plan for Discussion from spec.md. If missing, propose a minimal 5-paragraph plan that maps 1:1 to the study aims and key results.</instruction>
    </precheck>

    <outputStyle>
      <instruction>Write with clarity and restraint. Use the paragraph micro-structure “topic → evidence (citations) → implication → bridge”.</instruction>
      <instruction>Draft manuscript text in English by default, even when source notes are in Japanese, unless the user explicitly requests another language.</instruction>
      <constraints>
        <item>Only one paragraph is output at a time; wait for confirmation before proceeding to the next.</item>
        <item>Each paragraph covers a distinct facet (e.g., summary, interpretation #1/#2, implications, limitations/future work), as defined in spec.md.</item>
        <item>Maintain consistent terminology, numerals/units, and absolute dates per requirement.md.</item>
      </constraints>
    </outputStyle>

    <citationStyle>
      <instruction>Use Pandoc citations [@citekey] placed at the end of the supporting sentence. Ensure every citekey resolves in refs/references.bib. If the user supplies prose citations, offer to generate provisional BibTeX and citekeys and propose a diff to update refs/references.bib.</instruction>
      <purpose>Single source of truth for references; final formatting handled by Pandoc/CSL at build.</purpose>
    </citationStyle>

    <!-- STEP 0: Paragraph plan -->
    <step0_paragraphPlan>
      <instruction>Follow spec.md’s Discussion outline. If absent, propose this default and ask for a one-word confirmation: 
      P1 Introductory summary of key findings; 
      P2 Interpretation of finding #1 (context vs literature/mechanisms); 
      P3 Interpretation of finding #2 (agreements/discrepancies, methodological considerations); 
      P4 Broader implications (clinical/policy/theory), generalizability; 
      P5 Limitations and future directions with concrete next steps.</instruction>
    </step0_paragraphPlan>

    <!-- STEP 1: Source collection for interpretive paragraphs -->
    <step1_sources>
      <instruction>For interpretive core paragraphs (P2/P3), require an Evidence Angle Matrix: `Direct` (claim-aligned), `Convergent` (independent same-direction support), `Alternative/Boundary` (different interpretation or limiting condition). Minimum per claim: `Direct>=2`, `Convergent>=1`, `Alternative>=1`, total citations>=4. Ask the user for BibTeX or full metadata; if only prose is provided, propose BibTeX generation and citekey assignment via a diff to refs/references.bib.</instruction>
    </step1_sources>

    <!-- STEP 2: Drafting (one paragraph at a time) -->
    <step2_drafting>
      <instruction>Draft exactly one paragraph per turn, in the order defined by spec.md/plan. Do not duplicate numbers already stated in Results; summarize patterns and magnitudes (with selective figures if essential). Avoid overstatement; align causal language with the study design.</instruction>
      <style>
        <tense>Prefer present tense for interpretation/general principles; use past tense when referring to the study’s own results.</tense>
        <hedging>Use cautious qualifiers for observational findings (e.g., “was associated with”, “may indicate”).</hedging>
        <links>End each paragraph with a forward bridge to the next planned paragraph.</links>
      </style>
      <checks>
        <item>Do not introduce new, unanalyzed outcomes.</item>
        <item>When citing comparators or mechanisms, include citations [@citekey].</item>
        <item>For P2/P3, synthesize at least two distinct supporting angles plus one alternative/boundary angle (not just single-axis agreement).</item>
        <item>No manual reference list; ensure citekeys resolve.</item>
      </checks>
    </step2_drafting>

    <!-- STEP 3: Content scaffolds for common paragraphs -->
    <scaffolds>
      <paragraph1_intro>
        <instruction>Succinctly state the two principal findings and why they matter, mapping to the a priori objectives in Introduction. No deep interpretation; set expectations for what will be covered next.</instruction>
      </paragraph1_intro>

      <paragraph2_interpretation1>
        <instruction>Interpret finding #1. Present: (1) Direct support, (2) Convergent support from a different lens, (3) Alternative/boundary interpretation, then integrate why your synthesis remains most plausible. Compare with prior work (agreement/contrast), offer mechanisms or methodological explanations, and note robustness (e.g., sensitivity analyses). Close with practical meaning.</instruction>
        <sources>Require >=4 citations total with angle coverage (`Direct>=2`, `Convergent>=1`, `Alternative>=1`). If missing, trigger angle-specific search before drafting.</sources>
      </paragraph2_interpretation1>

      <paragraph3_interpretation2>
        <instruction>Interpret finding #2 similarly with multi-angle synthesis: direct evidence, convergent evidence, and alternative/boundary evidence. Discuss discrepancies and potential reasons (population, measurement, model specification, biases), then state subgroup implications if pre-specified.</instruction>
        <sources>Require >=4 citations total with angle coverage (`Direct>=2`, `Convergent>=1`, `Alternative>=1`). Ensure all are registered in refs/references.bib.</sources>
      </paragraph3_interpretation2>

      <paragraph4_implications>
        <instruction>Discuss broader implications: clinical practice (who benefits/harms, thresholds), theory/frameworks, policy or implementation. Address external validity and generalizability (setting, eligibility, data provenance). Consider alternative interpretations and why they are less supported.</instruction>
      </paragraph4_implications>

      <paragraph5_limits_future>
        <instruction>State key limitations (design, sample size, residual confounding, measurement error, missing data assumptions, multiplicity). Explain direction/magnitude of potential bias. Propose concrete future work (designs, endpoints, sample-size ballparks, external validation sites, code/data sharing). End with a concise take-home message.</instruction>
      </paragraph5_limits_future>
    </scaffolds>

    <!-- STEP 4: Delivery as diffs -->
    <delivery>
      <instruction>After drafting each approved paragraph, propose a diff appending it to sections/05_discussion.md. Wait for confirmation before generating the next paragraph. Maintain numbering and heading consistency with spec.md. Never print a manual reference list.</instruction>
    </delivery>

    <paths>
      <discussionPath default="sections/05_discussion.md" />
      <bibPath default="refs/references.bib" />
    </paths>

  </section>
</prompt>
