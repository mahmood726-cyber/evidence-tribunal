"""Unit tests for the tribunal engine logic in pipeline.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pipeline


def _spec(theta, se, p, sig, direction, **kw):
    base = {
        'estimator': kw.get('estimator', 'FE'),
        'ci_method': kw.get('ci_method', 'Wald'),
        'bias_correction': kw.get('bias_correction', 'none'),
        'leave_out': kw.get('leave_out', 'none'),
        'theta': theta,
        'se': se,
        'ci_lo': theta - 1.96 * se,
        'ci_hi': theta + 1.96 * se,
        'p_value': p,
        'tau2': 0.0,
        'i2': 0.0,
        'is_significant': sig,
        'direction': direction,
    }
    return base


def test_empty_specs_returns_none():
    assert pipeline.tribunal([], {'cochrane_direction': 1}) is None


def test_split_verdict():
    # one strong significant spec, one non-significant spec, direction = +1
    specs = [
        _spec(0.5, 0.1, 0.001, True, 1),   # prosecution favourite
        _spec(0.1, 0.2, 0.6, False, 1),    # defence favourite
    ]
    res = pipeline.tribunal(specs, {'cochrane_direction': 1})
    assert res is not None
    assert res['verdict'] == 'SPLIT'
    assert res['prosecution']['significant'] is True
    assert res['defence']['significant'] is False
    # adversarial gap is the absolute theta difference
    assert abs(res['adversarial_gap_theta'] - 0.4) < 1e-9


def test_unanimous_significant():
    specs = [
        _spec(0.5, 0.1, 0.001, True, 1),
        _spec(0.6, 0.1, 0.0005, True, 1),
    ]
    res = pipeline.tribunal(specs, {'cochrane_direction': 1})
    assert res['verdict'] == 'UNANIMOUS_SIGNIFICANT'


def test_unanimous_null():
    specs = [
        _spec(0.05, 0.2, 0.8, False, 1),
        _spec(0.02, 0.3, 0.9, False, 1),
    ]
    res = pipeline.tribunal(specs, {'cochrane_direction': 1})
    assert res['verdict'] == 'UNANIMOUS_NULL'


def test_zero_se_does_not_crash():
    # se == 0 must not raise ZeroDivisionError
    specs = [_spec(0.5, 0.0, 0.001, True, 1)]
    res = pipeline.tribunal(specs, {'cochrane_direction': 1})
    assert res is not None


def test_classify_gap_ratio_and_diff():
    assert pipeline.classify_adversarial_gap(0.05, 'ratio') == 'Narrow'
    assert pipeline.classify_adversarial_gap(0.6, 'ratio') == 'Extreme'
    assert pipeline.classify_adversarial_gap(0.1, 'diff') == 'Narrow'
    assert pipeline.classify_adversarial_gap(1.5, 'diff') == 'Extreme'
