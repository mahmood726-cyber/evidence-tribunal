# Truth-Recovery Validation — evidence-tribunal

**Engine:** `pipeline.py::tribunal()` (adversarial multiverse verdict)
**Question:** Does the `SPLIT` ("conclusion depends on analyst choices") verdict
manufacture fragility on data that should be unanimous, or is it calibrated?

## VERDICT: STRONG-VALIDATION

The tribunal verdict is well-calibrated. It does NOT manufacture fragility on
genuinely-robust data, recovers truth on clear cases, and separates genuinely-borderline
MAs from clear ones — avoiding the failure mode that sank sibling tools (MultiverseMA 46%,
meta-entropy/tda-ma 64–100% false positives).

## Method
`dgp_tribunal.py` builds a realistic Fragility-Atlas-style multiverse (7 estimators × 3 CI
× 3 bias + LOO, per-spec Wald z-test at α=0.05) from a KNOWN true pooled effect.
`harness.py` feeds it to the repo's own `tribunal()`; 400 reps/regime.

## Results (measured)
| Regime | True effect | Correct verdict | Achieved | False SPLIT |
|---|---|---|---|---|
| NULL | θ=0, k=12 | UNANIMOUS_NULL | 87.8% | 11.8% |
| ROBUST | θ=0.80, k=15 | UNANIMOUS_SIGNIFICANT | 100.0% | 0.0% |
| ROBUST (heterog.) | θ=0.80, τ²=0.08 | UNANIMOUS_SIGNIFICANT | 100.0% | 0.0% |
| BORDERLINE | θ=0.18, k=10 | SPLIT legitimate | SPLIT 40.0% | — |

SPLIT separation (borderline − worst-clear) = +28.2 pts.
False-SPLIT-on-null vs k: 11.0 / 13.8 / 11.2 / 8.8% for k=5/10/20/30 — bounded, stable.

## Findings
1. 0% false SPLIT on robust effects (headline) — opposite of MultiverseMA's uncalibrated aggregation.
2. SPLIT discriminates (+28 pts borderline vs clear) — tracks genuine threshold-straddling.
3. Honest residual ~12% false SPLIT on true nulls = expected spec-multiplicity floor (~75 specs/MA),
   stable in k, NOT a relative-threshold artifact. The empirical "66% SPLIT" headline is therefore
   credible, not an artifact of an uncalibrated rule.

## Recommendation
Ship as STRONG-VALIDATION. Optional hardening: require ≥2 specs (or a fraction) to cross α before
declaring SPLIT (shaves the ~12% null over-detection); surface LOO single-study flips separately
from estimator-choice flips. Neither changes the conclusion.

Reproduce: `python truth-recovery/harness.py` and
`python -m pytest truth-recovery/test_truth_recovery.py -q`.
