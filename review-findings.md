## REVIEW CLEAN
## Code Review Audit: EvidenceTribunal (pipeline.py)
### Date: 2026-04-03
### Summary: 0 P0, 1 P1, 3 P2

---

#### P0 -- Critical

None.

#### P1 -- Important

- **P1-1** [Statistics]: The prosecution/defence scoring (lines 91-104) uses z = |theta/se| as the primary metric. Prosecution maximizes z when significant in the Cochrane direction, defence minimizes it. The scoring correctly handles direction flips by checking `s['direction'] == direction`. Edge case: if all specs have the same direction and significance, prosecution_score and defence_score collapse to the same z range, yielding UNANIMOUS verdict -- correct behavior.

#### P2 -- Minor / Enhancement

- **P2-1** [Statistics]: Adversarial gap classification thresholds (lines 163-183) are heuristic. Ratio scale: <0.1 narrow, <0.3 moderate, <0.5 wide, else extreme. Difference scale: <0.2 narrow, <0.5 moderate, <1.0 wide, else extreme. These are reasonable for the intended descriptive analysis.

- **P2-2** [Robustness]: `spearmanr` imported inside `main()` from scipy.stats (line 269). Works but could be at module level. Minor style issue.

- **P2-3** [Security]: CSV output uses `csv.DictWriter` without formula injection guards. All string fields (review_id, verdict, gap_class, prosecution_spec, defence_spec) come from controlled pipeline data, not user input. Low risk.

#### Checklist

- [x] Prosecution scoring: maximize z in Cochrane direction -- correct
- [x] Defence scoring: minimize z or find non-significant/wrong-direction -- correct
- [x] Verdict logic (lines 114-125): 4 categories (UNANIMOUS_SIGNIFICANT, UNANIMOUS_NULL, SPLIT, PARADOX) -- exhaustive and correct
- [x] Adversarial gap: `abs(prosecution_theta - defence_theta)` -- correct
- [x] Log-p gap: protects against log(0) with `max(p, 1e-20)` (line 129)
- [x] Handles empty specs (line 75: returns None)
- [x] Division by zero guard: `s['se'] > 0` check (line 93)
- [x] Spearman correlation for gap vs robustness -- appropriate nonparametric test
- [x] Output directory created with `mkdir(parents=True, exist_ok=True)` (line 187)
