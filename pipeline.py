"""The Evidence Tribunal: Adversarial Meta-Analysis.

For each Cochrane review, find the BEST-CASE and WORST-CASE analytical
specifications from the multiverse. The gap between prosecution (best case
for treatment) and defence (worst case) is the adversarial uncertainty.

If prosecution can't make it significant → strong null
If defence can't make it non-significant → strong evidence
If they disagree → conclusion is analyst-dependent

Uses Fragility Atlas specification data (7 estimators × 3 CI × 3 bias × LOO).
"""

import csv
import json
import math
import time
import numpy as np
from pathlib import Path
from collections import Counter

SPECS_PATH = Path(r'C:\FragilityAtlas\data\output\fragility_atlas_specifications.csv')
RESULTS_PATH = Path(r'C:\FragilityAtlas\data\output\fragility_atlas_results.csv')
OUTPUT_DIR = Path(r'C:\Models\EvidenceTribunal\data\output')


def load_specs():
    """Load all multiverse specifications from Fragility Atlas."""
    specs = {}  # review_id -> list of spec dicts
    with open(SPECS_PATH, encoding='utf-8', errors='replace') as f:
        for row in csv.DictReader(f):
            rid = row['review_id']
            if rid not in specs:
                specs[rid] = []
            specs[rid].append({
                'estimator': row['estimator'],
                'ci_method': row['ci_method'],
                'bias_correction': row['bias_correction'],
                'leave_out': row['leave_out'],
                'theta': float(row['theta']),
                'se': float(row['se_theta']),
                'ci_lo': float(row['ci_lo']),
                'ci_hi': float(row['ci_hi']),
                'p_value': float(row['p_value']),
                'tau2': float(row['tau2']),
                'i2': float(row['i2']),
                'is_significant': row['is_significant'] == 'True',
                'direction': int(row['direction']),
            })
    return specs


def load_reviews():
    """Load review-level metadata."""
    reviews = {}
    with open(RESULTS_PATH, encoding='utf-8', errors='replace') as f:
        for row in csv.DictReader(f):
            rid = row['review_id']
            reviews[rid] = {
                'k': int(row['k']),
                'scale': row['scale'],
                'cochrane_significant': row['cochrane_significant'] == 'True',
                'cochrane_direction': int(row['cochrane_direction']),
                'robustness_score': float(row['robustness_score']),
            }
    return reviews


def tribunal(specs, review_meta):
    """Run the adversarial tribunal for one review.

    Prosecution: finds the spec with the MOST significant result (smallest p, strongest effect)
    Defence: finds the spec with the LEAST significant result (largest p, weakest effect)
    """
    if not specs:
        return None

    direction = review_meta['cochrane_direction']

    # Prosecution: maximize |theta/se| in the Cochrane direction
    # (strongest evidence FOR the treatment effect)
    prosecution_best = None
    prosecution_score = -999

    # Defence: minimize |theta/se| or flip direction
    # (strongest evidence AGAINST the treatment effect)
    defence_best = None
    defence_score = 999

    for s in specs:
        # Effect strength in Cochrane direction
        effect_strength = s['theta'] * direction  # positive = favours treatment
        z = abs(s['theta'] / s['se']) if s['se'] > 0 else 0

        # Prosecution score: want significant + correct direction + large z
        p_score = z if (s['is_significant'] and s['direction'] == direction) else -z
        if p_score > prosecution_score:
            prosecution_score = p_score
            prosecution_best = s

        # Defence score: want non-significant or wrong direction, smallest z
        d_score = z if (s['is_significant'] and s['direction'] == direction) else -z
        if d_score < defence_score:
            defence_score = d_score
            defence_best = s

    if prosecution_best is None or defence_best is None:
        return None

    # Verdicts
    prosecution_sig = prosecution_best['is_significant'] and prosecution_best['direction'] == direction
    defence_sig = defence_best['is_significant'] and defence_best['direction'] == direction

    if prosecution_sig and defence_sig:
        verdict = 'UNANIMOUS_SIGNIFICANT'
        # Even the defence can't make it non-significant
    elif not prosecution_sig and not defence_sig:
        verdict = 'UNANIMOUS_NULL'
        # Even the prosecution can't make it significant
    elif prosecution_sig and not defence_sig:
        verdict = 'SPLIT'
        # Conclusion depends on analyst choices
    else:
        verdict = 'PARADOX'
        # Defence finds it significant but prosecution doesn't (shouldn't happen)

    # Adversarial gap: difference in effect size between prosecution and defence
    gap_theta = abs(prosecution_best['theta'] - defence_best['theta'])
    gap_p = abs(math.log10(max(prosecution_best['p_value'], 1e-20)) -
                math.log10(max(defence_best['p_value'], 1e-20)))

    # Effect range (prosecution to defence)
    theta_range = [min(prosecution_best['theta'], defence_best['theta']),
                   max(prosecution_best['theta'], defence_best['theta'])]

    return {
        'verdict': verdict,
        'prosecution': {
            'theta': prosecution_best['theta'],
            'p_value': prosecution_best['p_value'],
            'significant': prosecution_sig,
            'estimator': prosecution_best['estimator'],
            'ci_method': prosecution_best['ci_method'],
            'bias_correction': prosecution_best['bias_correction'],
            'leave_out': prosecution_best['leave_out'],
        },
        'defence': {
            'theta': defence_best['theta'],
            'p_value': defence_best['p_value'],
            'significant': defence_sig,
            'estimator': defence_best['estimator'],
            'ci_method': defence_best['ci_method'],
            'bias_correction': defence_best['bias_correction'],
            'leave_out': defence_best['leave_out'],
        },
        'adversarial_gap_theta': float(gap_theta),
        'adversarial_gap_logp': float(gap_p),
        'theta_range': theta_range,
        'n_specs': len(specs),
    }


def classify_adversarial_gap(gap_theta, scale):
    """Classify the adversarial gap magnitude."""
    if scale == 'ratio':
        # On log scale, gap < 0.1 is small
        if gap_theta < 0.1:
            return 'Narrow'
        elif gap_theta < 0.3:
            return 'Moderate'
        elif gap_theta < 0.5:
            return 'Wide'
        else:
            return 'Extreme'
    else:
        if gap_theta < 0.2:
            return 'Narrow'
        elif gap_theta < 0.5:
            return 'Moderate'
        elif gap_theta < 1.0:
            return 'Wide'
        else:
            return 'Extreme'


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("The Evidence Tribunal")
    print("=" * 40)

    t0 = time.time()
    specs = load_specs()
    reviews = load_reviews()
    print(f"  Loaded {len(specs)} reviews with specifications")

    results = []
    for rid in sorted(specs.keys()):
        if rid not in reviews:
            continue
        meta = reviews[rid]
        t = tribunal(specs[rid], meta)
        if t is None:
            continue

        gap_class = classify_adversarial_gap(t['adversarial_gap_theta'], meta['scale'])

        row = {
            'review_id': rid,
            'k': meta['k'],
            'scale': meta['scale'],
            'n_specs': t['n_specs'],
            'verdict': t['verdict'],
            'prosecution_theta': round(t['prosecution']['theta'], 4),
            'prosecution_p': round(t['prosecution']['p_value'], 6),
            'prosecution_sig': t['prosecution']['significant'],
            'prosecution_spec': f"{t['prosecution']['estimator']}/{t['prosecution']['ci_method']}/{t['prosecution']['bias_correction']}",
            'defence_theta': round(t['defence']['theta'], 4),
            'defence_p': round(t['defence']['p_value'], 6),
            'defence_sig': t['defence']['significant'],
            'defence_spec': f"{t['defence']['estimator']}/{t['defence']['ci_method']}/{t['defence']['bias_correction']}",
            'adversarial_gap': round(t['adversarial_gap_theta'], 4),
            'gap_class': gap_class,
            'robustness_score': meta['robustness_score'],
        }
        results.append(row)

    elapsed = time.time() - t0
    print(f"  Processed: {len(results)} reviews in {elapsed:.1f}s")

    # VERDICTS
    verdicts = Counter(r['verdict'] for r in results)
    gap_classes = Counter(r['gap_class'] for r in results)
    gaps = [r['adversarial_gap'] for r in results]

    print(f"\n{'='*55}")
    print("THE VERDICTS")
    print(f"{'='*55}")
    for v, n in sorted(verdicts.items(), key=lambda x: -x[1]):
        print(f"  {v:25s}: {n:4d} ({100*n/len(results):.1f}%)")

    print(f"\nADVERSARIAL GAP")
    print(f"  Mean: {np.mean(gaps):.3f}")
    print(f"  Median: {np.median(gaps):.3f}")
    for gc, n in sorted(gap_classes.items(), key=lambda x: -x[1]):
        print(f"  {gc:10s}: {n:4d} ({100*n/len(results):.1f}%)")

    # KEY INSIGHT: what specs do prosecution and defence prefer?
    pros_estimators = Counter(r['prosecution_spec'].split('/')[0] for r in results)
    def_estimators = Counter(r['defence_spec'].split('/')[0] for r in results)
    pros_bias = Counter(r['prosecution_spec'].split('/')[2] for r in results)
    def_bias = Counter(r['defence_spec'].split('/')[2] for r in results)

    print(f"\nPROSECUTION PREFERS:")
    for e, n in pros_estimators.most_common(3):
        print(f"  Estimator: {e} ({n})")
    for b, n in pros_bias.most_common(3):
        print(f"  Bias correction: {b} ({n})")

    print(f"\nDEFENCE PREFERS:")
    for e, n in def_estimators.most_common(3):
        print(f"  Estimator: {e} ({n})")
    for b, n in def_bias.most_common(3):
        print(f"  Bias correction: {b} ({n})")

    # Correlation between adversarial gap and robustness
    gaps_arr = np.array(gaps)
    robust_arr = np.array([r['robustness_score'] for r in results])
    # Spearman
    from scipy.stats import spearmanr
    rho, p = spearmanr(gaps_arr, robust_arr)
    print(f"\nSpearman(adversarial_gap, robustness): rho={rho:.3f}, p={p:.4f}")

    # EXPORT
    fields = list(results[0].keys())
    with open(OUTPUT_DIR / 'tribunal_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    summary = {
        'n_reviews': len(results),
        'verdicts': dict(verdicts),
        'gap_classes': dict(gap_classes),
        'gap_mean': round(float(np.mean(gaps)), 3),
        'gap_median': round(float(np.median(gaps)), 3),
        'correlation_gap_robustness': round(float(rho), 3),
        'prosecution_top_estimator': pros_estimators.most_common(1)[0][0],
        'defence_top_estimator': def_estimators.most_common(1)[0][0],
        'prosecution_top_bias': pros_bias.most_common(1)[0][0],
        'defence_top_bias': def_bias.most_common(1)[0][0],
        'elapsed_seconds': round(elapsed, 1),
    }
    with open(OUTPUT_DIR / 'tribunal_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f"\n  Saved to {OUTPUT_DIR}/")


if __name__ == '__main__':
    main()
