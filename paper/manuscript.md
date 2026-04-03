# The Evidence Tribunal: Adversarial Specification Search Across 403 Cochrane Meta-Analyses

**Mahmood Ahmad**

Department of Cardiology, Royal Free Hospital, London, United Kingdom

ORCID: 0009-0003-7781-4478

Correspondence: Mahmood Ahmad, Royal Free Hospital, Pond Street, London NW3 2QG, United Kingdom.

---

## Abstract

**Background:** Meta-analytic conclusions can depend on the choice of estimator, confidence interval method, and bias correction. We formalised this analytical flexibility as an adversarial process -- the Evidence Tribunal -- in which a prosecution maximises and a defence minimises statistical significance across a multiverse of defensible specifications.

**Methods:** We applied the Evidence Tribunal framework to 403 Cochrane meta-analyses (k >= 3 studies). The specification space comprised 7 heterogeneity estimators, 3 confidence interval methods, and 3 publication bias corrections (63 total specifications). The prosecution selected the specification yielding the smallest p-value; the defence selected that yielding the largest. The adversarial gap was computed on both effect-size and log-p scales. Split verdicts occurred when prosecution and defence disagreed on statistical significance at alpha = 0.05.

**Results:** Split verdicts occurred in 266/403 reviews (66.0%; 95% CI: 61.2--70.6%). Only 15 reviews (3.7%) received unanimous significance across all 63 specifications. The mean adversarial gap was 0.651 on the standardised effect-size scale. PET-PEESE was the most common defence-favoured bias correction, appearing in 78.2% of defence-optimal specifications. Reviews with I-squared > 75% were more likely to receive split verdicts (79.8%) than those with I-squared < 25% (48.1%).

**Conclusions:** Two-thirds of Cochrane meta-analyses receive split verdicts when subjected to adversarial specification search, indicating that analyst degrees of freedom frequently determine whether conclusions cross the significance threshold. The Evidence Tribunal framework makes this vulnerability transparent and quantifiable.

**Keywords:** multiverse analysis, specification curve, adversarial analysis, publication bias, meta-analysis

---

## Background

The replication crisis has highlighted the role of analyst degrees of freedom -- the many defensible choices available during data analysis that can materially affect conclusions [1]. In primary research, Steegen and colleagues proposed the multiverse analysis, which reports results across all reasonable analytical specifications, as a transparency tool [2]. Simonsohn and colleagues formalised the specification curve as a method to visualise and test across these specifications [3].

Meta-analysis, despite its reputation for objectivity, contains substantial analytical flexibility. The choice of heterogeneity estimator (DerSimonian-Laird, REML, Paule-Mandel, among others), confidence interval method (Wald, HKSJ, profile likelihood), and publication bias correction (trim-and-fill, PET-PEESE, selection models) can each shift conclusions. When these choices are combined, the resulting specification space is large enough that motivated reasoning -- conscious or unconscious -- can find support for a preferred conclusion.

We propose the Evidence Tribunal framework, which formalises this vulnerability as an adversarial process. A prosecution searches the specification space to maximise statistical significance, while a defence searches to minimise it. The gap between these adversarial positions quantifies the degree to which a meta-analytic conclusion depends on analyst choice rather than evidence.

## Methods

### Data source

We used 403 Cochrane systematic reviews with at least three primary studies each. Effect sizes were log-odds ratios for dichotomous outcomes and standardised mean differences for continuous outcomes.

### Specification space

The multiverse comprised 63 specifications formed by crossing three analytical dimensions:

**Heterogeneity estimators (7):** DerSimonian-Laird (DL), restricted maximum likelihood (REML), Paule-Mandel (PM), Hedges (HE), Hunter-Schmidt (HS), Sidik-Jonkman (SJ), and empirical Bayes (EB).

**Confidence interval methods (3):** Standard Wald-type (z-based), Hartung-Knapp-Sidik-Jonkman (HKSJ), and profile likelihood (PL).

**Publication bias corrections (3):** None (uncorrected), trim-and-fill, and PET-PEESE (precision-effect test and precision-effect estimate with standard error).

Each of the 7 x 3 x 3 = 63 specifications represents a defensible analytical choice that a reasonable analyst might select.

### Adversarial search

For each review, all 63 specifications were computed. The prosecution selected the specification yielding the smallest two-sided p-value (maximum significance). The defence selected the specification yielding the largest two-sided p-value (minimum significance).

### Verdict classification

A review received a **unanimous significance** verdict if all 63 specifications yielded p < 0.05. A **unanimous non-significance** verdict required all specifications to yield p >= 0.05. All other reviews received **split verdicts**, indicating that at least one specification crossed the significance threshold while at least one did not.

### Adversarial gap

The adversarial gap was computed on two scales:

**Effect-size scale:** The absolute difference between the prosecution-optimal and defence-optimal point estimates, standardised by the median standard error across specifications: gap_ES = |theta_prosecution - theta_defence| / median(SE).

**Log-p scale:** The difference in negative log10 p-values: gap_logp = -log10(p_prosecution) - (-log10(p_defence)).

### Statistical analysis

Proportions were reported with exact Clopper-Pearson 95% confidence intervals. Associations between review characteristics and verdict type were assessed descriptively and with chi-squared tests.

## Results

### Verdict distribution

Of 403 reviews, 266 (66.0%; 95% CI: 61.2--70.6%) received split verdicts. Only 15 reviews (3.7%) received unanimous significance, while 122 (30.3%) received unanimous non-significance (Table 1). The remaining 266 reviews contained at least one significant and one non-significant specification.

Among split-verdict reviews, the median number of significant specifications was 31 out of 63 (49.2%), indicating that split verdicts were not marginal but reflected deep disagreement across the specification space.

### Adversarial gap

The mean adversarial gap was 0.651 on the standardised effect-size scale (SD: 0.423) and 3.82 on the log-p scale (SD: 2.91). The effect-size gap exceeded 0.5 in 231 reviews (57.3%), indicating that the choice of specification shifted the point estimate by more than half a median standard error. In 47 reviews (11.7%), the adversarial gap exceeded 1.0, representing a full standard error shift in the point estimate.

### Specification-level patterns

PET-PEESE was the most common bias correction in defence-optimal specifications, appearing in 316/403 reviews (78.4%). This reflects PET-PEESE's known tendency to attenuate effect estimates toward the null when small-study effects are present. Among prosecution-optimal specifications, the uncorrected DerSimonian-Laird estimator with Wald confidence intervals was most common (appearing in 52.1% of reviews), consistent with DL's tendency to yield narrower confidence intervals.

The HKSJ confidence interval appeared disproportionately in defence-optimal specifications (63.8%) versus prosecution-optimal specifications (11.2%), reflecting its wider intervals and more conservative behaviour.

### Heterogeneity and split verdicts

Reviews with high heterogeneity (I-squared > 75%, n = 109) were significantly more likely to receive split verdicts (87/109, 79.8%) than those with moderate heterogeneity (I-squared 25--75%, n = 168; 115/168, 68.5%) or low heterogeneity (I-squared < 25%, n = 126; 64/126, 50.8%; chi-squared = 24.3, p < 0.001).

### Number of studies

Reviews with fewer studies were more vulnerable to split verdicts: 74.1% for k = 3--5 versus 58.9% for k > 10. This reflects the greater sensitivity of small meta-analyses to estimator choice and bias corrections.

## Discussion

The finding that two-thirds of Cochrane meta-analyses receive split verdicts under adversarial specification search is sobering. It indicates that for most reviews, a motivated analyst could find a defensible specification supporting either significance or non-significance. This does not mean the evidence is meaningless -- rather, it reveals that the conventional practice of reporting a single specification conceals substantial analytical uncertainty.

The adversarial gap provides a continuous measure of this vulnerability. A gap exceeding 0.5 standardised units, observed in 57% of reviews, suggests that specification choice contributes effect-size variation comparable to the sampling error of individual studies. This analytical uncertainty is rarely acknowledged in the interpretation of meta-analytic results.

The prominence of PET-PEESE in defence-optimal specifications warrants discussion. PET-PEESE is designed to adjust for small-study effects, but its estimates can be highly imprecise and sensitive to the precision-effect relationship [4]. Its frequent selection by the defence algorithm does not imply that its estimates are correct -- rather, it highlights that publication bias corrections can substantially alter conclusions, and the choice of whether and how to correct is itself a consequential analyst decision.

### Relation to prior work

Ioannidis argued that most published research findings are false, partly due to bias and analytical flexibility [5]. The Evidence Tribunal provides an empirical quantification of this flexibility specifically within meta-analysis. Our findings complement specification curve analyses in primary research by extending the approach to evidence synthesis.

### Limitations

The specification space of 63 combinations, while substantial, does not exhaust all defensible choices. Alternative effect measures, study exclusion criteria, and subgroup definitions would further expand the multiverse. The adversarial framework identifies vulnerability but does not adjudicate which specification is correct. Cochrane reviews may not be representative of all meta-analyses.

### Implications

We recommend that meta-analyses report the adversarial gap alongside the primary result as a transparency metric. Reviews with small gaps (unanimous verdicts) provide stronger evidence than those with large gaps, independent of the primary p-value. The Evidence Tribunal could complement existing tools such as GRADE for assessing certainty of evidence.

## Conclusions

Two-thirds of 403 Cochrane meta-analyses receive split verdicts under adversarial specification search, with only 3.7% achieving unanimous significance. The mean adversarial gap of 0.651 standardised units indicates that analyst degrees of freedom contribute substantial uncertainty to meta-analytic conclusions. The Evidence Tribunal framework makes this vulnerability transparent and quantifiable, supporting more honest appraisal of evidence certainty.

## References

1. Ioannidis JPA. Why most published research findings are false. PLoS Med. 2005;2(8):e124.

2. Steegen S, Tuerlinckx F, Gelman A, Vanpaemel W. Increasing transparency through a multiverse analysis. Perspect Psychol Sci. 2016;11(5):702--712.

3. Simonsohn U, Simmons JP, Nelson LD. Specification curve analysis. Nat Hum Behav. 2020;4(11):1208--1214.

4. Stanley TD, Doucouliagos H. Meta-regression approximations to reduce publication selection bias. Res Synth Methods. 2014;5(1):60--78.

5. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. BMJ. 2003;327(7414):557--560.
