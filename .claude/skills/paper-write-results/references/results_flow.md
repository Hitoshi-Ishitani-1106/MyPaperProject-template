# Results Flow

<prompt>
  <section name="Results">

    <!-- PRECHECK: read specs/methods first -->
    <precheck>
      <assumptions>
        <item>Design authority is requirement.md (Why/What) and spec.md (How).</item>
        <item>Methods are finalized or in-flight at sections/03_methods.md and define the Results subheading skeleton.</item>
        <item>Use Pandoc citations [@citekey] only when citing external benchmarks or methods-dependent references; avoid narrative citation formats.</item>
      </assumptions>
      <instruction>Before drafting, read requirement.md, spec.md, and sections/03_methods.md. Extract the exact Methods subheadings and map them 1:1 to Results. Load journal constraints (word/figure/table limits) from requirement.md.</instruction>
    </precheck>

    <instructions>
      <overview>
        <instruction>Report findings objectively and completely, mirroring Methods. Do not interpret (leave for Discussion). Keep terminology, units, denominators, and time frames consistent with requirement.md/spec.md.</instruction>
        <instruction>Draft manuscript text in English by default, even when source notes are in Japanese, unless the user explicitly requests another language.</instruction>
        <emphasis>Accuracy, completeness, logical order, and transparent denominators (N, n/%) are mandatory.</emphasis>
      </overview>

      <!-- STEP 1: Collect structured results aligned to Methods -->
      <step1_collect>
        <instruction>For each Methods subheading, request the corresponding results in a structured way. Ask for both descriptive and inferential statistics, including effect sizes and 95% CIs.</instruction>
        <userInput>
          <request>Please provide data for each Methods subheading (exact Ns, denominators, units, time windows, and any protocol deviations). Include descriptive stats (mean±SD/median[IQR]/n(%)) and inferential outputs (test used, effect size, 95% CI, p-value). If multiple analyses exist (primary, secondary, sensitivity), mark them explicitly.</request>
          <prompts>
            <prompt>Participants/Flow (CONSORT/STROBE/PRISMA): totals by stage (assessed→eligible→included→analyzed), reasons for exclusions, missingness by variable.</prompt>
            <prompt>Baseline/Exposure/Index Tests: group-wise summaries with denominators and standardized differences if applicable.</prompt>
            <prompt>Primary Outcome: effect estimate with 95% CI, test/model used, model covariates (name==version of software).</prompt>
            <prompt>Secondary/Exploratory Outcomes: same schema; clearly label multiplicity handling.</prompt>
            <prompt>Sensitivity/Robustness: list analyses and summarize direction/magnitude changes.</prompt>
            <prompt>Prediction/Classification (TRIPOD): discrimination (AUC with CI), calibration (slope/intercept; plot ref), Brier score; internal/external validation results.</prompt>
            <prompt>Harms/Adverse Events (CONSORT): counts and rates by arm/severity.</prompt>
          </prompts>
        </userInput>
      </step1_collect>

      <!-- STEP 2: Completeness check against Methods/spec -->
      <step2_completeness>
        <instruction>Cross-check provided results against sections/03_methods.md and spec.md. Identify gaps, inconsistencies, or units/date mismatches.</instruction>
        <assessment>
          <criteria>
            <item>Any Methods item without a corresponding Result?</item>
            <item>Do all Ns/denominators reconcile (ITT vs PP populations)?</item>
            <item>Are effect sizes and 95% CIs reported for all inferential results?</item>
            <item>Are multiplicity and missing-data populations consistent with Methods?</item>
            <item>Do subgroup/sensitivity analyses match the pre-specification?</item>
          </criteria>
        </assessment>
        <feedback>
          <instruction>Ask targeted questions to fill missing details; propose defaults only if allowed in requirement.md.</instruction>
          <examples>
            <example>“Methods specify multiple imputation with m=20; please provide pooled estimates and 95% CIs for the primary outcome.”</example>
            <example>“Randomization yielded N=120 per arm in Methods, but Results show N=118 analyzed. Please clarify exclusions and provide a CONSORT flow count.”</example>
          </examples>
        </feedback>
      </step2_completeness>

      <!-- STEP 3: Draft Results mirroring Methods; neutral tone -->
      <step3_draft>
        <instruction>Compose Results with subheadings identical to Methods/spec.md. Lead each subsection with what is being reported (population/analysis set), then key numbers with references to Tables/Figures. No interpretation or mechanistic claims.</instruction>
        <contentGuidelines>
          <item>Report both significant and non-significant findings. Include exact p-values (to 3 decimals; p&lt;0.001 as threshold) and effect sizes with 95% CIs.</item>
          <item>Always declare the analysis set (e.g., ITT/PP) and time window.</item>
          <item>If applicable, report protocol deviations and how they affected N.</item>
          <item>For prediction models: report optimism-corrected metrics if internal validation used; present calibration numerically (slope/intercept) and reference a calibration plot.</item>
          <item>For SR/MA (PRISMA): provide study selection counts with a PRISMA flow and summarize study characteristics; report heterogeneity (τ²/I²) and model (fixed/random) with pooled effects and 95% CIs.</item>
          <item>Ensure consistent rounding and units; avoid duplicating table content verbatim in text.</item>
        </contentGuidelines>
      </step3_draft>

      <!-- STEP 4: Tables/Figures scaffolding -->
      <step4_figtab>
        <instruction>Propose a minimal, numbered list of Tables and Figures with informative titles and one-sentence footers defining abbreviations and analysis sets. Use placeholders if data are pending.</instruction>
        <defaults>
          <item>Table 1. Baseline Characteristics (analysis set, units, SD/IQR)</item>
          <item>Figure 1. Participant Flow (CONSORT/STROBE/PRISMA)</item>
          <item>Table 2. Primary Outcome and Sensitivity Analyses (effect size, 95% CI, p, method)</item>
          <item>Table 3. Secondary Outcomes</item>
          <item>Figure 2. Model Performance (ROC) and Calibration (if TRIPOD)</item>
        </defaults>
        <note>Do not render the full tables in prose; reference them succinctly in text.</note>
      </step4_figtab>

      <!-- STEP 5: Validation before diff -->
      <step5_validate>
        <instruction>Run a preflight checklist: (1) 1:1 mapping with Methods; (2) all Ns/denominators reconcile; (3) CI/effect sizes present; (4) multiplicity noted; (5) all figure/table callouts exist and are numbered sequentially; (6) units/dates consistent with requirement.md.</instruction>
      </step5_validate>

      <!-- STEP 6: Delivery as diffs -->
      <step6_delivery>
        <instruction>Propose an ordered diff writing the Results into sections/04_results.md. If large, split per subsection but keep numbering stable. Do not output a manual reference list.</instruction>
      </step6_delivery>

      <!-- STEP 7: Minimal user prompts (gap resolution) -->
      <step7_userPrompts>
        <prompt>Provide exact Ns and denominators for each analysis set (e.g., ITT, safety population), and clarify any discrepancies from Methods.</prompt>
        <prompt>For each inferential result, please confirm the effect size definition (e.g., MD, OR, HR) and provide 95% CIs and exact p-values.</prompt>
        <prompt>If prediction modeling was performed, please provide internal/external validation metrics, and whether optimism correction or bootstrapping was used.</prompt>
      </step7_userPrompts>
    </instructions>

    <writing_guidelines>
      <guideline>Use past tense to describe obtained results. Keep neutral, objective tone; no interpretation. Maintain the “topic → evidence (numbers) → emphasis on key result → bridge to next subsection” micro-structure.</guideline>
      <consistency>Ensure global consistency of terminology, units, and absolute dates with requirement.md/spec.md.</consistency>
    </writing_guidelines>

    <paths>
      <resultsPath default="sections/04_results.md" />
      <methodsPath default="sections/03_methods.md" />
    </paths>

  </section>
</prompt>
