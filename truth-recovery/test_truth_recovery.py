"""Truth-recovery assertions for the Evidence Tribunal.

These lock in the CALIBRATION findings: the repo's own tribunal() verdict must
not manufacture fragility on robust data, must recover the truth on clear cases,
and must separate genuinely-borderline MAs from clear ones.

Run: python -m pytest truth-recovery/test_truth_recovery.py -q
"""
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline
from dgp_tribunal import make_multiverse


def _rates(true_theta, k, tau2, n, seed):
    c = Counter()
    for i in range(n):
        specs, meta = make_multiverse(true_theta, k, tau2_true=tau2, seed=seed + i)
        r = pipeline.tribunal(specs, meta)
        c[r['verdict'] if r else 'NONE'] += 1
    tot = sum(c.values())
    return {v: 100.0 * cnt / tot for v, cnt in c.items()}


def test_robust_effect_never_manufactures_fragility():
    # A large, well-powered effect must come back UNANIMOUS_SIGNIFICANT, with
    # essentially zero false SPLIT. This is the MultiverseMA/meta-entropy failure
    # mode (46-100% false fragility) -- the tribunal must avoid it.
    r = _rates(0.80, 15, 0.01, 300, 5000)
    assert r.get('UNANIMOUS_SIGNIFICANT', 0) >= 95.0
    assert r.get('SPLIT', 0) <= 3.0


def test_robust_with_heterogeneity_still_robust():
    r = _rates(0.80, 15, 0.08, 300, 9000)
    assert r.get('UNANIMOUS_SIGNIFICANT', 0) >= 90.0
    assert r.get('SPLIT', 0) <= 5.0


def test_genuine_null_recovered_mostly_null():
    # On a true null, UNANIMOUS_NULL must dominate and false SPLIT stays bounded
    # (spec-multiplicity floor ~12%, not a fragility blowout).
    r = _rates(0.0, 12, 0.0, 300, 1000)
    assert r.get('UNANIMOUS_NULL', 0) >= 80.0
    assert r.get('SPLIT', 0) <= 20.0
    assert r.get('UNANIMOUS_SIGNIFICANT', 0) <= 3.0


def test_borderline_separates_from_clear():
    # SPLIT must be markedly more common on genuinely-borderline MAs than on
    # clear (null/robust) ones -- i.e. the verdict discriminates.
    clear_robust = _rates(0.80, 15, 0.01, 300, 5000).get('SPLIT', 0)
    clear_null = _rates(0.0, 12, 0.0, 300, 1000).get('SPLIT', 0)
    borderline = _rates(0.18, 10, 0.02, 300, 13000).get('SPLIT', 0)
    assert borderline >= 25.0
    assert borderline - max(clear_robust, clear_null) >= 10.0


def test_verdict_uses_per_spec_significance():
    # Contract: a multiverse that is unanimously significant-in-direction yields
    # UNANIMOUS_SIGNIFICANT; mixing one non-sig spec yields SPLIT.
    def spec(theta, se, p, sig, d=1):
        return {'estimator': 'DL', 'ci_method': 'Wald', 'bias_correction': 'none',
                'leave_out': 'none', 'theta': theta, 'se': se,
                'ci_lo': theta - 1.96 * se, 'ci_hi': theta + 1.96 * se,
                'p_value': p, 'tau2': 0.0, 'i2': 0.0,
                'is_significant': sig, 'direction': d}
    meta = {'cochrane_direction': 1}
    assert pipeline.tribunal(
        [spec(0.5, 0.1, 1e-4, True), spec(0.6, 0.1, 1e-5, True)], meta
    )['verdict'] == 'UNANIMOUS_SIGNIFICANT'
    assert pipeline.tribunal(
        [spec(0.5, 0.1, 1e-4, True), spec(0.05, 0.3, 0.8, False)], meta
    )['verdict'] == 'SPLIT'
