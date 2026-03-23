# Methods Flow

<prompt>
  <section name="Materials and Methods">

    <!-- PRECHECK: read specs and abstract first -->
    <precheck>
      <assumptions>
        <item>Abstract is finalized at sections/01_abstract.md.</item>
        <item>Design authority: requirement.md (Why/What) and spec.md (How) are the single sources of truth.</item>
        <item>Citations use Pandoc syntax [@citekey]; all entries must exist in refs/references.bib.</item>
      </assumptions>
      <instruction>Before drafting, read requirement.md and spec.md to extract: study type, target journal constraints, paragraph/subheading plan, and mandatory reporting checklist (EQUATOR family).</instruction>
    </precheck>

    <instructions>
      <overview>
        <instruction>Write Methods to enable replication. Follow the reporting guideline selected in spec.md, and enforce internal consistency with requirement.md (terminology, numerals/units, absolute dates).</instruction>
        <instruction>Draft manuscript text in English by default, even when source notes are in Japanese, unless the user explicitly requests another language.</instruction>
        <emphasis>Transparency, accuracy, completeness, and reproducibility (code/data/software) are mandatory.</emphasis>
      </overview>

      <!-- STEP 1: Study type (from spec.md; no open-ended ask unless missing) -->
      <step1_studyType>
        <instruction>Use the study type defined in spec.md (e.g., RCT/observational/systematic review/meta-analysis/diagnostic or prognostic model). If missing, propose one based on the abstract and requirement.md, then confirm.</instruction>
      </step1_studyType>

      <!-- STEP 2: EQUATOR mapping (confirm, not re-decide) -->
      <step2_reportingGuideline>
        <instruction>Adopt the reporting guideline specified in spec.md. Typical map: CONSORT (RCT), STROBE (observational), PRISMA (SR/MA), ARRIVE (animal), TRIPOD (prediction model), CARE (case report). If unspecified, propose the most appropriate and request a one-word confirmation.</instruction>
        <deliverable>Instantiate a checklist (bulleted in-editor only) to ensure all required items are covered; do not include the checklist in the manuscript.</deliverable>
      </step2_reportingGuideline>

      <!-- STEP 3: Subheadings derive from spec.md + guideline -->
      <step3_subheadings>
        <instruction>From spec.md’s subheading plan and the chosen guideline, generate the Methods subheading list. Keep journal style (title case vs sentence case) consistent.</instruction>
        <defaults>
          <CONSORT>Study Design; Participants; Interventions; Outcomes; Sample Size; Randomization; Allocation Concealment; Blinding; Statistical Analysis</CONSORT>
          <STROBE>Study Design; Setting; Participants; Variables; Data Sources and Measurement; Bias; Study Size; Quantitative Variables; Statistical Methods</STROBE>
          <TRIPOD>Source of Data; Participants; Outcome; Predictors; Sample Size; Missing Data; Statistical Analysis Methods; Model Development; Internal Validation; Performance Measures</TRIPOD>
          <PRISMA>Eligibility Criteria; Information Sources; Search Strategy; Selection Process; Data Collection Process; Data Items; Risk of Bias Assessment; Effect Measures; Synthesis Methods</PRISMA>
        </defaults>
        <userInput>If spec.md lacks a subheading, propose it and proceed after a brief confirmation.</userInput>
      </step3_subheadings>

      <!-- STEP 4: Draft each subheading with replication-level detail -->
      <step4_content>
        <globalRequirements>
          <item>Define all variables/outcomes precisely; align terms with requirement.md’s glossary.</item>
          <item>Population & setting: inclusion/exclusion, time frame (absolute dates), sites, ethics approval ID, consent model.</item>
          <item>Data provenance: sources, extraction procedures, adjudication, inter-rater assessment where relevant.</item>
          <item>Interventions/exposures: who, what, when, where, how much; fidelity and protocol deviations.</item>
          <item>Measurements: instruments/software with manufacturer, model, version; calibration; units.</item>
          <item>Sample size: a priori calculation or justification; assumptions; effect size; power; alpha.</item>
          <item>Randomization/Blinding (if applicable): sequence generation, allocation concealment, masking levels.</item>
          <item>Missing data: mechanism assumptions (MCAR/MAR/MNAR), diagnostics, handling (e.g., multiple imputation specs), sensitivity analyses.</item>
          <item>Statistical analysis: primary/secondary analyses; model forms; covariates; interactions; multiplicity control; robust/sandwich SE where relevant; exact software/versions; random seeds.</item>
          <item>Prediction-model specifics (TRIPOD): preprocessing, feature engineering, class imbalance handling; model algorithm and hyperparameters; resampling schema (k-fold/bootstrapping); internal/external validation; performance metrics (AUC, calibration, Brier, decision-curve); model specification for reproducibility.</item>
          <item>Reproducibility: OS, language/runtime versions, key packages (name==version); analysis plan preregistration (ID/link) if any; code and data availability statements (even if restricted, describe access pathway).</item>
        </globalRequirements>
        <style>Tense: past for performed procedures; present for established properties. Keep 3–6 sentences per subsection when possible; avoid stacked modifiers; define acronyms on first use.</style>
        <citations>Use [@citekey] where methods reference published techniques or tools. Ensure all citekeys resolve in refs/references.bib; do not print inline “[Surname et al., Journal, Year]”.</citations>
      </step4_content>

      <!-- STEP 5: Diff-based delivery -->
      <step5_delivery>
        <instruction>Propose a single cohesive diff to write Methods into the target path (default: sections/03_methods.md). If large, stage as ordered diffs per subheading. Never output a manual reference list.</instruction>
        <validation>Run a preflight checklist: (1) all citekeys resolve; (2) subheadings match guideline/spec.md; (3) units/dates consistent with requirement.md; (4) seeds/versions present if code was used.</validation>
      </step5_delivery>

      <!-- STEP 6: Journal-specific tightening -->
      <step6_journalTuning>
        <instruction>Apply target-journal constraints from requirement.md (word limits, subheading names, house style). If conflicts arise, prefer journal rules and update spec.md via a small diff suggestion.</instruction>
      </step6_journalTuning>

      <!-- STEP 7: Minimal user prompts (confirmation, not re-design) -->
      <step7_userPrompts>
        <prompt>If the reporting guideline is not specified in spec.md, please confirm the best match (CONSORT/STROBE/TRIPOD/PRISMA/ARRIVE/CARE): [proposed].</prompt>
        <prompt>Two items are missing for reproducibility: (a) software versions, (b) random seed policy. Please provide or allow me to propose defaults.</prompt>
        <prompt>Missing-data handling is not specified. Confirm the mechanism assumption (MCAR/MAR/MNAR) and your preferred method (complete-case / MICE / IPW). I can draft sensitivity analyses accordingly.</prompt>
      </step7_userPrompts>
    </instructions>

    <writing_guidelines>
      <guideline>Adhere to requirement.md/spec.md. Keep topic→evidence→implication→bridge within each subsection where feasible. Maintain consistent terminology and units.</guideline>
    </writing_guidelines>

    <paths>
      <methodsPath default="sections/03_methods.md" />
      <bibPath default="refs/references.bib" />
    </paths>

  </section>
</prompt>
