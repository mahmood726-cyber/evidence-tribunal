# E156 Protocol — `evidence-tribunal`

This repository is the source code and dashboard backing an E156 micro-paper on the [E156 Student Board](https://mahmood726-cyber.github.io/e156/students.html).

---

## `[54]` The Evidence Tribunal: Adversarial Specification Search Across 403 Cochrane Meta-Analyses

**Type:** methods  |  ESTIMAND: Adversarial verdict (Unanimous/Split)  
**Data:** 403 Cochrane reviews via Fragility Atlas specifications

### 156-word body

Can adversarial specification search quantify how much a meta-analytic conclusion depends on analyst choices rather than underlying evidence? The Evidence Tribunal applies prosecution-defence framing to 403 Cochrane reviews, where prosecution maximizes significance and defence minimizes it, across seven estimators, three confidence interval methods, and three bias corrections. For each review, the adversarial gap between strongest and weakest specifications is computed on effect-size and log-p-value scales, classified as narrow, moderate, wide, or extreme. Of 403 reviews, 266 (66 percent, 95% CI 61 to 71) received split verdicts where prosecution achieved significance but defence did not, while only 15 yielded unanimous significance. The mean adversarial gap was 0.651 with median 0.157, and PET-PEESE was the most common defence-favored bias correction. This framework reveals that most published meta-analytic conclusions are potentially vulnerable to reasonable alternative analytical specifications. However, the limitation of relying on pre-computed specification data means the current multiverse does not include Bayesian priors or alternative effect-size metrics.

### Submission metadata

```
Corresponding author: Mahmood Ahmad <mahmood.ahmad2@nhs.net>
ORCID: 0000-0001-9107-3704
Affiliation: Tahir Heart Institute, Rabwah, Pakistan

Links:
  Code:      https://github.com/mahmood726-cyber/evidence-tribunal
  Protocol:  https://github.com/mahmood726-cyber/evidence-tribunal/blob/main/E156-PROTOCOL.md
  Dashboard: https://mahmood726-cyber.github.io/evidence-tribunal/

References (topic pack: fragility index):
  1. Walsh M, Srinathan SK, McAuley DF, et al. 2014. The statistical significance of randomized controlled trial results is frequently fragile: a case for a Fragility Index. J Clin Epidemiol. 67(6):622-628. doi:10.1016/j.jclinepi.2013.10.019
  2. Atal I, Porcher R, Boutron I, Ravaud P. 2019. The statistical significance of meta-analyses is frequently fragile: definition of a fragility index for meta-analyses. J Clin Epidemiol. 111:32-40. doi:10.1016/j.jclinepi.2019.03.012

Data availability: No patient-level data used. Analysis derived exclusively
  from publicly available aggregate records. All source identifiers are in
  the protocol document linked above.

Ethics: Not required. Study uses only publicly available aggregate data; no
  human participants; no patient-identifiable information; no individual-
  participant data. No institutional review board approval sought or required
  under standard research-ethics guidelines for secondary methodological
  research on published literature.

Funding: None.

Competing interests: MA serves on the editorial board of Synthēsis (the
  target journal); MA had no role in editorial decisions on this
  manuscript, which was handled by an independent editor of the journal.

Author contributions (CRediT):
  [STUDENT REWRITER, first author] — Writing – original draft, Writing –
    review & editing, Validation.
  [SUPERVISING FACULTY, last/senior author] — Supervision, Validation,
    Writing – review & editing.
  Mahmood Ahmad (middle author, NOT first or last) — Conceptualization,
    Methodology, Software, Data curation, Formal analysis, Resources.

AI disclosure: Computational tooling (including AI-assisted coding via
  Claude Code [Anthropic]) was used to develop analysis scripts and assist
  with data extraction. The final manuscript was human-written, reviewed,
  and approved by the author; the submitted text is not AI-generated. All
  quantitative claims were verified against source data; cross-validation
  was performed where applicable. The author retains full responsibility for
  the final content.

Preprint: Not preprinted.

Reporting checklist: PRISMA 2020 (methods-paper variant — reports on review corpus).

Target journal: ◆ Synthēsis (https://www.synthesis-medicine.org/index.php/journal)
  Section: Methods Note — submit the 156-word E156 body verbatim as the main text.
  The journal caps main text at ≤400 words; E156's 156-word, 7-sentence
  contract sits well inside that ceiling. Do NOT pad to 400 — the
  micro-paper length is the point of the format.

Manuscript license: CC-BY-4.0.
Code license: MIT.

SUBMITTED: [ ]
```


---

_Auto-generated from the workbook by `C:/E156/scripts/create_missing_protocols.py`. If something is wrong, edit `rewrite-workbook.txt` and re-run the script — it will overwrite this file via the GitHub API._