# evidence-tribunal

The Evidence Tribunal: adversarial specification search across 403 Cochrane meta-analyses.

For each review, `pipeline.py` reads the Fragility Atlas multiverse of specifications
and selects a "prosecution" spec (the strongest significant result in the Cochrane
direction) and a "defence" spec (the weakest / non-significant result). The verdict
classifies each review as `UNANIMOUS_SIGNIFICANT`, `UNANIMOUS_NULL`, or `SPLIT`
(conclusion depends on analyst choices), and reports the adversarial effect-size gap.

## Run

Point the pipeline at a local Fragility Atlas snapshot, then run it:

```
# defaults to C:\FragilityAtlas\data\output; override via env vars
set FRAGILITY_ATLAS_DIR=...   # or TRIBUNAL_SPECS_PATH / TRIBUNAL_RESULTS_PATH
python pipeline.py
```

Results are written to `data/output/` (override with `TRIBUNAL_OUTPUT_DIR`).
Pre-computed outputs for the 403-review run are committed under `data/output/`.

Tests: `python -m pytest tests/ -q`

_Status: Active (portfolio registry)._
