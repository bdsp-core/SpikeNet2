# Reproduce — SpikeNet2 (Li et al., NEJM AI 2025)

Two tiers, matching the two-tier data model:

## 1. Localization figure/results — from committed data (verified 2026-07-07)
No download, no model, no GPU. Regenerates from the committed
`conbine_localization_predictions.csv` (848 events × 19-channel predictions, de-identified `Bonobo####` IDs):

```bash
pip install -r requirements.txt   # + pandas, matplotlib, seaborn, scikit-learn
jupyter nbconvert --to notebook --execute 2_localization.ipynb
# or run its cells: reads ./conbine_localization_predictions.csv -> localization figure + per-class report
```
Verified output: per-class AUC ≈ **0.913 / 0.854 / 0.831 / 0.806**, accuracy ≈ 0.70.

## 2. Detection figures (ROC etc.) — needs weights + EEG data
Heavier path (GPU recommended):
1. Get credentialed access to the dataset (`bdsp.io/content/spikenet/2.0/`) and download EEG + the model checkpoint (`DATA_SOURCE.md`).
2. `1_calculate_local_predictions.ipynb` (or `prediction.ipynb`) — load `new_weights.ckpt`, run inference → `predictions.csv`.
3. The figure cells turn `predictions.csv` into the ROC/detection figures.

To retrain from scratch: `train_model.py` → `continurous.py` → `hard_mining.ipynb` → `train_hard_mining.py` (see README).

## Requirements
Python 3.10, `requirements.txt` (PyTorch/Lightning for the model path; pandas/matplotlib/seaborn/scikit-learn for the localization figure). Weights + EEG data are **not** committed — see `DATA_SOURCE.md`.
