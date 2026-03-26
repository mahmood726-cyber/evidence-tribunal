# The Evidence Tribunal: Two-Thirds of Cochrane Meta-Analysis Conclusions Depend on Who Does the Analysis

## Authors

Mahmood Ahmad^1

^1 Royal Free Hospital, London, United Kingdom

Correspondence: mahmood.ahmad2@nhs.net | ORCID: 0009-0003-7781-4478

---

## Abstract

**Objective:** To quantify how much meta-analysis conclusions depend on analyst choices by framing evidence synthesis as an adversarial process.

**Design:** Adversarial multiverse analysis of 403 Cochrane systematic reviews.

**Data sources:** Pairwise70 dataset with Fragility Atlas multiverse specifications (7 estimators, 3 CI methods, 3 bias corrections, leave-one-out variants).

**Methods:** For each review, two adversarial "lawyers" selected from the full specification space: the prosecution chose the specification producing the strongest evidence for treatment efficacy; the defence chose the specification producing the weakest. A verdict of UNANIMOUS SIGNIFICANT required even the defence to find significance; UNANIMOUS NULL required even the prosecution to fail; SPLIT indicated the conclusion depended on specification choice. The adversarial gap — the difference in effect size between prosecution and defence — quantified analyst-dependent uncertainty.

**Results:** Of 403 reviews, 266 (66.0%) received SPLIT verdicts — meaning the same data can yield either a significant or non-significant result depending on analytical choices. Only 15 reviews (3.7%) were unanimously significant; 122 (30.3%) were unanimously null. The median adversarial gap was 0.157 on the log scale, with 21.6% of reviews showing extreme gaps (>0.5). The prosecution systematically preferred specifications without bias correction (54%), while the defence preferred PET-PEESE correction (45%). Both sides favoured Fixed Effects estimation (87-91%) for its tighter confidence intervals. The adversarial gap was weakly correlated with multiverse robustness (rho=0.096), indicating it captures a distinct dimension of evidence quality.

**Conclusions:** Two-thirds of treatment conclusions in Cochrane meta-analyses depend on who does the analysis. This adversarial framing reveals that the boundary between "significant" and "non-significant" is a methodological choice, not an empirical fact, for the majority of systematic reviews. Routine reporting of adversarial gaps alongside pooled estimates would make this analyst-dependence transparent.

---

## What is already known on this topic

- Multiverse analysis shows that different analytical specifications can yield different conclusions from the same data
- The Fragility Atlas demonstrated that 56% of Cochrane meta-analyses have fragile conclusions
- Analyst degrees of freedom are a recognised source of bias in primary research, but their role in meta-analysis is underappreciated

## What this study adds

- Two-thirds of Cochrane meta-analysis conclusions are SPLIT — significant under some specifications, non-significant under others
- Only 3.7% of reviews produce conclusions that survive adversarial challenge
- The prosecution (arguing for treatment efficacy) systematically avoids bias correction; the defence uses it
- Both sides exploit Fixed Effects for its tighter CIs, revealing a structural vulnerability in meta-analytic inference
- The adversarial gap is complementary to — not redundant with — multiverse robustness

---

## 1. Introduction

Meta-analysis is presented as objective synthesis: given the same data, any competent analyst should reach the same conclusion. Yet the analyst must choose an effect size measure, a heterogeneity estimator, a confidence interval method, whether to apply bias correction, and which studies to include. Each choice can change whether the result crosses the threshold of statistical significance.

Multiverse analysis addresses this by computing results across all reasonable specifications and reporting the distribution. But multiverse analysis is agnostic about direction — it treats all specifications equally, without asking the adversarial question: if an analyst WANTED to show the treatment works, could they find a specification that supports this? And if another analyst WANTED to show it doesn't, could they find one that contradicts?

We introduce the Evidence Tribunal: an adversarial framework that explicitly asks how much meta-analysis conclusions depend on analyst intent. Rather than averaging across specifications (multiverse) or counting how many agree (robustness), we find the BEST and WORST case for each review and measure the gap.

## 2. Methods

### 2.1 Specification Space

We used the Fragility Atlas specification space for 403 Cochrane systematic reviews: 7 heterogeneity estimators (FE, DL, REML, PM, ML, HS, SJ) crossed with 3 CI methods (Wald, HKSJ, t-distribution) and 3 bias corrections (none, trim-and-fill, PET-PEESE), plus leave-one-out variants, yielding up to 36,288 specifications per review.

### 2.2 Adversarial Selection

**Prosecution** (argues for treatment efficacy): Selected the specification maximising the z-statistic (|theta/SE|) in the Cochrane-reported treatment direction, conditional on achieving statistical significance.

**Defence** (argues against): Selected the specification minimising the z-statistic, preferring non-significant results or results in the opposite direction.

### 2.3 Verdicts

- **UNANIMOUS SIGNIFICANT**: Both prosecution and defence find significance in the treatment direction
- **UNANIMOUS NULL**: Neither can achieve significance
- **SPLIT**: Prosecution finds significance, defence does not — conclusion is analyst-dependent

### 2.4 Adversarial Gap

The adversarial gap is |theta_prosecution - theta_defence|, measuring the range of effect sizes achievable through specification choice. Classified as Narrow (<0.1), Moderate (0.1-0.3), Wide (0.3-0.5), or Extreme (>0.5) on the log scale.

## 3. Results

### 3.1 Verdicts

Of 403 reviews: 266 (66.0%) SPLIT, 122 (30.3%) UNANIMOUS NULL, 15 (3.7%) UNANIMOUS SIGNIFICANT. The vast majority of treatment conclusions are analyst-dependent.

### 3.2 Adversarial Gap

The mean gap was 0.651 (median 0.157). 160 reviews (39.7%) had narrow gaps; 87 (21.6%) had extreme gaps exceeding 0.5 on the log scale. Reviews with extreme gaps are those where analytical choices have the greatest power to change conclusions.

### 3.3 Adversarial Strategies

The prosecution overwhelmingly preferred no bias correction (54%) and Fixed Effects estimation (88%). This reveals the mechanism: avoiding bias correction preserves inflated effect estimates, and FE provides the narrowest CIs, maximising the chance of significance.

The defence preferred PET-PEESE bias correction (45%) and also Fixed Effects (91%). The defence uses bias correction to shrink the effect toward null, but also uses FE because the tighter CIs make it harder to achieve significance when the corrected effect is small.

The shared preference for FE is notable: both sides exploit FE's tight CIs for opposite purposes. This reveals a structural vulnerability — the choice between FE and RE is not neutral; it is adversarially exploitable.

### 3.4 Relationship to Robustness

The adversarial gap was weakly correlated with the Fragility Atlas robustness score (Spearman rho=0.096, p=0.053). This near-zero correlation means adversarial uncertainty captures something fundamentally different from multiverse robustness. A review can be robust (most specifications agree) yet have a large adversarial gap (the disagreeing minority includes both significant and non-significant results).

## 4. Discussion

### 4.1 The 66% Problem

Two-thirds of Cochrane meta-analyses have conclusions that are simultaneously defensible as significant AND non-significant, depending on analytical choices. This is not a failure of any individual analyst — it is a structural property of the evidence itself. When the true effect is near the boundary of clinical or statistical significance, any reasonable set of analytical options will span both sides.

### 4.2 Implications

**For guideline panels:** A SPLIT verdict should trigger enhanced scrutiny. The panel should know not only the primary estimate but also the prosecution and defence estimates, making the analyst-dependence explicit.

**For journal editors:** Requiring authors to report the adversarial gap alongside the pooled estimate would prevent selective specification — the reader would see that the conclusion depends on methodological choices the author made.

**For the GRADE framework:** The adversarial gap could be incorporated as a dimension of imprecision or inconsistency, providing a more nuanced assessment than I-squared alone.

### 4.3 Limitations

The adversarial framework assumes the specification space captures all reasonable analytical choices. Unreasonable specifications (e.g., fixed effects with k=3 and I-squared=90%) may dominate the adversarial extremes. The binary significant/non-significant framing oversimplifies clinical decision-making. The adversarial selection is post-hoc and does not model how actual analysts behave.

## 5. Conclusions

Two-thirds of Cochrane meta-analysis conclusions depend on who does the analysis. The adversarial gap — measuring the range of achievable results through specification choice — reveals that the prosecution systematically avoids bias correction while the defence exploits it. Routine adversarial reporting would make this analyst-dependence transparent and compel the field to reckon with the boundary between evidence and analytical choice.

---

## Data Availability

Code and results: https://github.com/mahmood726-cyber/evidence-tribunal

## Funding
None.

## Competing Interests
The author declares no competing interests.

## References
1. Steegen S, et al. Increasing transparency through a multiverse analysis. Perspect Psychol Sci. 2016;11(5):702-712.
2. Higgins JPT, et al. Cochrane Handbook. Version 6.4, 2023.
3. Del Re AC. A practical tutorial on conducting meta-analysis in R. Quant Methods Psychol. 2015;11(1):37-50.
4. Stanley TD, Doucouliagos H. Meta-regression approximations to reduce publication selection bias. Res Synth Methods. 2014;5:60-78.
