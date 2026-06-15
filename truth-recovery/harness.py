"""Truth-recovery harness for the Evidence Tribunal.

Wires the repo's OWN pipeline.tribunal() against a seeded known-truth DGP and
measures whether its "SPLIT" (conclusion-depends-on-analyst-choices) verdict is
CALIBRATED or whether it MANUFACTURES fragility.

We test three known-truth regimes:
  1. NULL          : true_theta = 0          -> correct verdict = UNANIMOUS_NULL
  2. ROBUST EFFECT : large, well-powered     -> correct verdict = UNANIMOUS_SIGNIFICANT
  3. BORDERLINE    : effect near the alpha boundary -> SPLIT is legitimately expected

A SPLIT (or SIGNIFICANT) on a NULL MA is a FALSE POSITIVE.
A SPLIT (or NULL) on a ROBUST MA is a FALSE FRAGILITY.
Only regime 3 is where SPLIT *should* dominate; if SPLIT is high in 1 & 2 too,
the verdict is uncalibrated and the "66%" headline is an artifact.
"""
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline
from dgp_tribunal import make_multiverse


def run_regime(name, true_theta, k, tau2_true, n_reps, base_seed):
    verdicts = Counter()
    rows = []
    for i in range(n_reps):
        specs, meta = make_multiverse(true_theta, k, tau2_true=tau2_true,
                                      seed=base_seed + i)
        res = pipeline.tribunal(specs, meta)
        v = res['verdict'] if res else 'NONE'
        verdicts[v] += 1
        rows.append((v, meta['theta_primary']))
    n = sum(verdicts.values())
    return name, true_theta, k, verdicts, n, rows


def summarize(label, true_theta, k, verdicts, n):
    pct = {v: 100.0 * c / n for v, c in verdicts.items()}
    split = pct.get('SPLIT', 0.0)
    sig = pct.get('UNANIMOUS_SIGNIFICANT', 0.0)
    null = pct.get('UNANIMOUS_NULL', 0.0)
    par = pct.get('PARADOX', 0.0)
    print(f"\n[{label}] true_theta={true_theta:+.2f} k={k}  (n={n})")
    print(f"  UNANIMOUS_SIGNIFICANT: {sig:5.1f}%   "
          f"UNANIMOUS_NULL: {null:5.1f}%   "
          f"SPLIT: {split:5.1f}%   PARADOX: {par:4.1f}%")
    return {'split': split, 'sig': sig, 'null': null, 'paradox': par}


def main():
    print("=" * 64)
    print("EVIDENCE TRIBUNAL -- TRUTH-RECOVERY CALIBRATION")
    print("=" * 64)
    N = 400

    # Regime 1: genuine NULL. SPLIT or SIGNIFICANT here = manufactured fragility / FP.
    _, tt, k, v1, n1, _ = run_regime('null', 0.0, 12, 0.0, N, 1000)
    s1 = summarize('NULL', tt, k, v1, n1)

    # Regime 2: robust, well-powered real effect. SPLIT/NULL here = false fragility.
    _, tt, k, v2, n2, _ = run_regime('robust', 0.80, 15, 0.01, N, 5000)
    s2 = summarize('ROBUST EFFECT', tt, k, v2, n2)

    # Regime 2b: robust with realistic heterogeneity.
    _, tt, k, v2b, n2b, _ = run_regime('robust_het', 0.80, 15, 0.08, N, 9000)
    s2b = summarize('ROBUST EFFECT (heterogeneous)', tt, k, v2b, n2b)

    # Regime 3: genuinely borderline. SPLIT *should* be common & legitimate.
    _, tt, k, v3, n3, _ = run_regime('borderline', 0.18, 10, 0.02, N, 13000)
    s3 = summarize('BORDERLINE (truly fragile)', tt, k, v3, n3)

    # ---- Discrimination ----
    # False fragility rate = how often a CLEARLY-determined MA (null or robust) is
    # nonetheless labelled SPLIT.
    false_split_null = s1['split']
    false_split_robust = s2['split']
    false_split_robust_het = s2b['split']
    # On a genuine null, the only correct verdict is UNANIMOUS_NULL.
    null_correct = s1['null']
    # On a robust effect, the only correct verdict is UNANIMOUS_SIGNIFICANT.
    robust_correct = s2['sig']

    print("\n" + "=" * 64)
    print("DISCRIMINATION SUMMARY")
    print("=" * 64)
    print(f"  NULL correctly UNANIMOUS_NULL ........... {null_correct:5.1f}%")
    print(f"  ROBUST correctly UNANIMOUS_SIGNIFICANT .. {robust_correct:5.1f}%")
    print(f"  FALSE SPLIT on genuine NULL ............. {false_split_null:5.1f}%")
    print(f"  FALSE SPLIT on robust effect ........... {false_split_robust:5.1f}%")
    print(f"  FALSE SPLIT on robust (heterog.) ....... {false_split_robust_het:5.1f}%")
    print(f"  SPLIT on truly-borderline (wanted high). {s3['split']:5.1f}%")

    # Separation: does SPLIT-rate actually rise from clear -> borderline?
    clear_split = max(false_split_null, false_split_robust)
    sep = s3['split'] - clear_split
    print(f"\n  SPLIT separation (borderline - worst-clear) = {sep:+.1f} pts")

    return {
        'null': s1, 'robust': s2, 'robust_het': s2b, 'borderline': s3,
        'false_split_null': false_split_null,
        'false_split_robust': false_split_robust,
        'false_split_robust_het': false_split_robust_het,
        'borderline_split': s3['split'],
        'separation': sep,
    }


if __name__ == '__main__':
    main()
