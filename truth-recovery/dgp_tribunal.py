"""Standalone seeded known-truth DGP for the Evidence Tribunal validation.

Generates a realistic Fragility-Atlas-style MULTIVERSE of specifications for one
meta-analysis with a KNOWN true pooled effect, then hands it to the repo's own
`tribunal()` function. Each multiverse is a list of spec dicts matching the schema
that pipeline.tribunal() consumes (theta, se, p_value, is_significant, direction,
estimator, ci_method, bias_correction, leave_out, ...).

Ground truth we control:
  - true_theta : the true pooled log-effect (0.0 => genuine NULL)
  - k          : number of studies
The verdict we want the tribunal to deliver:
  - true_theta == 0  -> ideally UNANIMOUS_NULL  (any SIGNIFICANT/SPLIT = false positive)
  - |true_theta| large & well-powered -> ideally UNANIMOUS_SIGNIFICANT
                                         (any NULL/SPLIT = false fragility)

We deliberately build the multiverse the same way a real fragility atlas does:
7 estimators x 3 CI methods x 3 bias corrections, PLUS leave-one-out variants.
Significance is recomputed per spec with a two-sided Wald z-test at alpha=0.05,
which is exactly the kind of per-spec thresholding that can manufacture a SPLIT.
"""
import math
import numpy as np
from scipy import stats

ESTIMATORS = ['FE', 'DL', 'REML', 'PM', 'SJ', 'HE', 'EB']  # 7 estimators
CI_METHODS = ['Wald', 'HKSJ', 'KR']                          # 3 CI methods
BIAS_CORR = ['none', 'trimfill', 'pet_peese']                # 3 bias corrections
ALPHA = 0.05
ZCRIT = stats.norm.ppf(1 - ALPHA / 2)


def _pool(yi, vi, tau2):
    """Inverse-variance pooled estimate under a given between-study variance tau2."""
    w = 1.0 / (vi + tau2)
    theta = float(np.sum(w * yi) / np.sum(w))
    se = float(math.sqrt(1.0 / np.sum(w)))
    return theta, se


def _tau2_dl(yi, vi):
    """DerSimonian-Laird tau^2 (the workhorse moment estimator)."""
    k = len(yi)
    w = 1.0 / vi
    theta_fe = np.sum(w * yi) / np.sum(w)
    Q = float(np.sum(w * (yi - theta_fe) ** 2))
    c = float(np.sum(w) - np.sum(w ** 2) / np.sum(w))
    if c <= 0:
        return 0.0
    return max(0.0, (Q - (k - 1)) / c)


def _spec_from(theta, se, estimator, ci_method, bias, leave_out, direction_ref):
    """Build a spec dict in the schema pipeline.tribunal() expects."""
    if se <= 0:
        se = 1e-9
    z = theta / se
    p = float(2 * (1 - stats.norm.cdf(abs(z))))
    sig = p < ALPHA
    direction = 1 if theta >= 0 else -1
    return {
        'estimator': estimator,
        'ci_method': ci_method,
        'bias_correction': bias,
        'leave_out': leave_out,
        'theta': float(theta),
        'se': float(se),
        'ci_lo': float(theta - ZCRIT * se),
        'ci_hi': float(theta + ZCRIT * se),
        'p_value': p,
        'tau2': 0.0,
        'i2': 0.0,
        'is_significant': bool(sig),
        'direction': int(direction),
    }


def make_multiverse(true_theta, k, tau2_true=0.0, base_var=0.04, seed=0,
                    include_loo=True):
    """Generate one MA's full multiverse of specs from a known DGP.

    Returns (specs_list, review_meta) ready for pipeline.tribunal(specs, meta).
    review_meta['cochrane_direction'] is the sign of the *primary* RE estimate,
    matching how Fragility Atlas anchors the Cochrane direction.
    """
    rng = np.random.default_rng(seed)
    # Per-study sampling variances (vary across studies, like real MAs).
    vi = base_var * np.exp(rng.normal(0, 0.4, size=k))
    vi = np.clip(vi, 0.005, 0.5)
    # Study-level true effects with between-study heterogeneity tau2_true.
    mu_i = rng.normal(true_theta, math.sqrt(tau2_true), size=k) if tau2_true > 0 \
        else np.full(k, true_theta)
    yi = rng.normal(mu_i, np.sqrt(vi))

    # Primary RE (DL) pooled estimate -> defines the Cochrane direction.
    tau2_dl = _tau2_dl(yi, vi)
    theta_primary, _ = _pool(yi, vi, tau2_dl)
    cochrane_direction = 1 if theta_primary >= 0 else -1

    specs = []
    # Full factorial estimator x CI x bias, on the full dataset.
    for est in ESTIMATORS:
        # Different estimators imply (slightly) different tau2; FE uses 0.
        if est == 'FE':
            tau2 = 0.0
        elif est == 'DL':
            tau2 = tau2_dl
        else:
            # Other estimators perturb tau2 modestly around DL (realistic spread).
            tau2 = max(0.0, tau2_dl * (1.0 + rng.normal(0, 0.15)))
        theta, se = _pool(yi, vi, tau2)
        for ci in CI_METHODS:
            # HKSJ/KR inflate SE for small k (the usual small-sample correction).
            se_adj = se
            if ci == 'HKSJ' and k > 1:
                se_adj = se * max(1.0, math.sqrt(k / (k - 1)))
            elif ci == 'KR' and k > 1:
                se_adj = se * (1.0 + 1.0 / (2 * k))
            for bias in BIAS_CORR:
                theta_b = theta
                if bias == 'trimfill':
                    theta_b = theta * 0.92      # mild attenuation toward null
                elif bias == 'pet_peese':
                    theta_b = theta * 0.85      # stronger small-study attenuation
                specs.append(_spec_from(theta_b, se_adj, est, ci, bias,
                                        'none', cochrane_direction))

    # Leave-one-out variants (under the primary DL estimator) -- the source of
    # most "one spec flips" fragility.
    if include_loo and k > 2:
        for j in range(k):
            mask = np.ones(k, dtype=bool)
            mask[j] = False
            yj, vj = yi[mask], vi[mask]
            tau2_j = _tau2_dl(yj, vj)
            theta_j, se_j = _pool(yj, vj, tau2_j)
            specs.append(_spec_from(theta_j, se_j, 'DL', 'Wald', 'none',
                                    f'study_{j}', cochrane_direction))

    meta = {
        'cochrane_direction': cochrane_direction,
        'cochrane_significant': abs(theta_primary / max(1e-9,
                                    _pool(yi, vi, tau2_dl)[1])) > ZCRIT,
        'scale': 'ratio',
        'k': k,
        'true_theta': float(true_theta),
        'theta_primary': float(theta_primary),
    }
    return specs, meta
