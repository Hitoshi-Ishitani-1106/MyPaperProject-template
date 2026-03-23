# Abstract Flow

<prompt>
  <section name="Abstract Generation">

    <!-- PRECHECK: design + prior sections + overwrite policy -->
    <precheck>
      <assumptions>
        <item>Abstract was initially provided in sections/01_abstract.md.</item>
        <item>Design authority: requirement.md (Why/What) and spec.md (How) are the single sources of truth.</item>
        <item>The regenerated abstract must REPLACE the initial one once all core sections are complete.</item>
      </assumptions>
      <instruction>Before drafting, read requirement.md, spec.md, and finalized sections/02_introduction.md, sections/03_methods.md, sections/04_results.md, sections/05_discussion.md, and sections/06_conclusion.md. Confirm target-journal constraints (word limit; structured vs unstructured; mandatory subheadings; statistical reporting rules).</instruction>
    </precheck>

    <instructions>
      <overview>
        <instruction>Generate an English abstract from the completed manuscript (Intro, Methods, Results, Discussion, Conclusion). Follow the target journal’s rules exactly. Do not introduce new information or citations.</instruction>
        <instruction>Keep the abstract in English by default even if source notes or prior drafts are in Japanese, unless the user explicitly requests another language.</instruction>
        <emphasis>Clarity, concision, strict word-limit compliance, and faithful synthesis are mandatory.</emphasis>
      </overview>

      <!-- Step 1: obtain journal rules & exemplars -->
      <step1_guidelines>
        <instruction>Request author‐guideline snippets and 1–2 recent exemplar abstracts from the same journal to learn style and structure.</instruction>
        <user_prompt>
Please provide:
1) Journal’s abstract instructions (English): word limit; structured vs unstructured; required subheadings; any statistical style rules.
2) One or two recent example abstracts from the same journal (full text in English).
        </user_prompt>
      </step1_guidelines>

      <!-- Step 2: analyze constraints and exemplars -->
      <step2_analysis>
        <instruction>Extract: (a) word limit; (b) structure type and required subheadings; (c) content/tense rules; (d) typical sentence length and level of detail; (e) recurrent phrasing patterns.</instruction>
      </step2_analysis>

      <!-- Step 3: draft abstract from completed sections -->
      <step3_draft>
        <instruction>Compose the abstract in English strictly within the journal’s format. Prefer structured (Background/Methods/Results/Conclusions) if required; otherwise produce a single coherent paragraph. Do not include references or citekeys.</instruction>
        <content_extraction>
          <item><b>Background:</b> 1–2 sentences stating the problem and aim, inferred from Introduction and Conclusion.</item>
          <item><b>Methods:</b> 1–3 sentences covering design, setting/participants, interventions or exposures (if any), primary outcomes, and analysis approach (concise; past tense).</item>
          <item><b>Results:</b> 1–3 sentences with the most important findings; include key numerics only if space permits; avoid p-values unless explicitly required.</item>
          <item><b>Conclusions:</b> 1–2 sentences stating the main takeaway and its meaning/implication consistent with Discussion/Conclusion.</item>
        </content_extraction>
        <writing_style>
          <item>Keep formal, objective tone; avoid unexplained jargon/abbreviations.</item>
          <item>Past tense for methods/results; present/future for implications when used.</item>
          <item>Maintain terminology/units consistent with requirement.md/spec.md and the main text.</item>
        </writing_style>
        <validation>
          <item>Meets word limit; matches required structure; contains no new data or limitations; no citations.</item>
        </validation>
        <user_prompt>
Here is a draft Abstract (journal-compliant). Please confirm or request edits. Upon approval I will write it to sections/01_abstract.md via a diff.
        </user_prompt>
      </step3_draft>

      <!-- Step 4: write via diff -->
      <step4_delivery>
        <instruction>Propose a diff that writes the approved abstract to sections/01_abstract.md (overwriting the initial placeholder).</instruction>
      </step4_delivery>

      <!-- Step 5: FINAL REGENERATION & REPLACEMENT AFTER MANUSCRIPT COMPLETION -->
      <step5_final_regeneration>
        <trigger>When sections/02–06 are finalized and requirement.md/spec.md indicate readiness for submission.</trigger>
        <instruction>Regenerate the abstract once more using the final manuscript and journal rules, optimizing wording and compression. Present the final abstract for a brief check, then propose a diff that REPLACES sections/01_abstract.md.</instruction>
        <guardrails>
          <item>No new claims beyond the final manuscript.</item>
          <item>Respect word/structure rules; avoid p-values unless required.</item>
        </guardrails>
      </step5_final_regeneration>
    </instructions>

    <writing_guidelines>
      <guideline>Adhere to requirement.md/spec.md style rules; maintain global consistency of terms, numerals, and absolute dates.</guideline>
      <guideline>Do not include limitations in the abstract unless the journal explicitly requires them.</guideline>
      <guideline>Prefer effect sizes/absolute differences over p-values unless guidelines mandate otherwise.</guideline>
      <tense>Past for methods/results; present/future for implications when included.</tense>
    </writing_guidelines>

    <paths>
      <abstractPath default="sections/01_abstract.md" />
    </paths>

  </section>
</prompt>
