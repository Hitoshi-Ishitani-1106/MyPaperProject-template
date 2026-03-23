# Conclusion Flow

<prompt>
  <section name="Conclusion">

    <!-- PRECHECK: read prior sections and design -->
    <precheck>
      <assumptions>
        <item>Abstract is fixed at sections/01_abstract.md.</item>
        <item>Design authority: requirement.md (Why/What) and spec.md (How) are the single sources of truth.</item>
        <item>Citations use Pandoc syntax [@citekey]; however, the Conclusion typically contains no new citations and must not introduce new sources.</item>
      </assumptions>
      <instruction>Before drafting, read requirement.md, spec.md, and the finalized sections/02_introduction.md, sections/03_methods.md, sections/04_results.md, and sections/05_discussion.md. Extract study goals, primary findings, and any pre-specified implications/future work.</instruction>
    </precheck>

    <instructions>
      <overview>
        <instruction>Produce a concise, self-contained synthesis (3–4 sentences). Do not restate research questions verbatim, do not introduce limitations, and do not add new information beyond prior sections.</instruction>
        <instruction>Draft manuscript text in English by default, even when source notes are in Japanese, unless the user explicitly requests another language.</instruction>
        <emphasis>Clarity, parsimony, and a strong final message are essential.</emphasis>
      </overview>

      <!-- STEP 1: Summarize main findings with purpose linkage -->
      <step1_synthesis>
        <instruction>Summarize the most important findings and implicitly link them to the overarching goals inferred from Introduction/Objectives. Avoid copying sentences; compress to essentials and focus on meaning rather than detailed numbers.</instruction>
        <data_source>sections/02_introduction.md; Objectives in spec.md/Introduction; sections/04_results.md; sections/05_discussion.md.</data_source>
      </step1_synthesis>

      <!-- STEP 2: Implications (only if pre-emphasized) -->
      <step2_implications>
        <instruction>State implications only if Discussion/Introduction/Objectives emphasized them as material (theory/practice/policy). Do not introduce new implications.</instruction>
        <data_source>sections/05_discussion.md; sections/02_introduction.md; spec.md Objectives.</data_source>
      </step2_implications>

      <!-- STEP 3: Future work (only if explicitly raised) -->
      <step3_future>
        <instruction>Include future research directions only when they were explicitly and concretely raised earlier. Avoid generic calls for more research.</instruction>
        <data_source>sections/05_discussion.md; sections/02_introduction.md; spec.md.</data_source>
      </step3_future>

      <!-- STEP 4: Strong closing statement -->
      <step4_closing>
        <instruction>End with a single, memorable sentence that captures the study’s main contribution and significance. No new data, no limitations.</instruction>
      </step4_closing>

      <!-- DELIVERY -->
      <delivery>
        <instruction>Propose a single diff that writes the 3–4 sentence Conclusion into sections/06_conclusion.md. If journal naming requires a different heading label, follow requirement.md and note the change in the diff summary.</instruction>
        <validation>Preflight: (1) length 3–4 sentences; (2) no new data/limitations/citations; (3) terminology/units align with requirement.md; (4) tense usage conforms to guidelines.</validation>
      </delivery>
    </instructions>

    <writing_guidelines>
      <guideline>Adhere to requirement.md/spec.md style rules: topic→evidence→implication→bridge micro-structure within 3–4 sentences.</guideline>
      <guideline>Do not introduce new data, limitations, or sources. Keep formal, objective tone.</guideline>
      <length>3–4 sentences total.</length>
      <tense>Use past tense for the study’s findings; present/future tense for implications or future work when included.</tense>
      <citations>Avoid adding citations in the Conclusion. If absolutely necessary due to journal policy, use [@citekey] and ensure the source already exists in refs/references.bib.</citations>
    </writing_guidelines>

    <paths>
      <conclusionPath default="sections/06_conclusion.md" />
    </paths>

  </section>
</prompt>
