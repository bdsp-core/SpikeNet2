# Data source & provenance — SpikeNet2 (Li et al. 2025)

## Raw / source data + weights (canonical home)
- **bdsp.io project:** `spikenet2` — *SpikeNet 2.0* → https://bdsp.io/content/spikenet/2.0/  · DOI [10.60508/mbxb-hn49](https://doi.org/10.60508/mbxb-hn49)
- **S3 (credentialed / restricted):** `s3://bdsp-opendata-restricted/spikenet2/`
  - `EEG/` — continuous EEG (~260 GB) · `Events/` — event `.mat` files (~35 GB)
  - `Models/new_weights.ckpt` — the trained model (369 MB); `Models/1s-round11-hardmine-chan_weights-v1.ckpt` — earlier round
- Dataset: 17,524 EEGs (MGH/BWH) + 188 (Human Epilepsy Project) + 100 (SCORE-AI).

## Proximal artifact committed in this repo (de-identified)
`conbine_localization_predictions.csv` — 848 events, per-channel model predictions + labels, subjects as surrogate `Bonobo####` IDs (no PHI). Feeds `2_localization.ipynb` (the localization figure regenerates from it with no download).

## Raw → derived lineage
1. **Raw EEG + expert spike annotations** (the `spikenet2` dataset) →
2. **SpikeNet2 model** (`train_model.py` → `continurous.py` → hard-mining → `train_hard_mining.py`) → `new_weights.ckpt` (on S3).
3. **Inference** (`1_calculate_local_predictions.ipynb` / `prediction.ipynb`) on EEG + weights → `predictions.csv` / `conbine_localization_predictions.csv`.
4. **Figures**: localization figure from the committed CSV (no data needed); detection/ROC figures from `predictions.csv`.

Weights + raw EEG are **not** committed (they live on S3); the small localization CSV is.
