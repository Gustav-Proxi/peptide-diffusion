"""
Fix 1: Re-run InstaNovo on our 472-spectrum E. coli EV test split.

Produces eval/instanovo_472_split.csv with columns:
  spectrum_id, true_sequence, predicted_sequence, aa_recall, pep_correct, score

Then computes and prints aggregate AA recall and peptide accuracy using the same
metric functions as our model evaluation.

Usage:
  cd peptide-diffusion
  python eval/run_instanovo.py
"""

import glob
import os
import sys

import numpy as np
import pandas as pd
import torch

# ── Project imports ────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from diffusion import (IDX_TO_CHAR, aa_recall, build_diffusion_dataset,
                       decode_tokens)
from preprocessing import CHAR_TO_IDX, VOCAB, load_labeled_spectra

# ── Data paths (same as eval_novels.py) ────────────────────────────────────────
BASE = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
mzml_paths = sorted(glob.glob(os.path.join(BASE, "Ecoli_EV_*.mzML")))
xlsx_paths = sorted(
    glob.glob(os.path.join(BASE, "Database search output_Ecoli_EV_*.xlsx"))
)

if not mzml_paths:
    raise FileNotFoundError(f"No mzML files under {BASE}")

print(f"Loading spectra from {[os.path.basename(p) for p in mzml_paths]}")

# ── Reproduce our exact 70/15/15 split (rng seed=42) ──────────────────────────
all_spectra = []
for mzml, xlsx in zip(mzml_paths, xlsx_paths):
    all_spectra.extend(load_labeled_spectra(mzml, xlsx, max_spectra=5000))

N = len(all_spectra)
rng = np.random.default_rng(42)
idx = rng.permutation(N)
n_tr = int(0.70 * N)
n_va = int(0.15 * N)
te_idx = idx[n_tr + n_va :]

test_spectra = [all_spectra[i] for i in te_idx]
print(f"Test split: {len(test_spectra)} spectra")

# ── Build parquet for InstaNovo ────────────────────────────────────────────────
rows = []
for s in test_spectra:
    rows.append(
        {
            "mz_array": s["mz"].tolist(),
            "intensity_array": s["intensity"].tolist(),
            "precursor_mz": float(s["precursor_mz"]) if s["precursor_mz"] else 0.0,
            "precursor_charge": int(s["charge"]) if s["charge"] else 2,
            "sequence": s["peptide"],
        }
    )

sdf_df = pd.DataFrame(rows)

parquet_dir = os.path.join(os.path.dirname(__file__), "ecoli_test_parquet")
os.makedirs(parquet_dir, exist_ok=True)
parquet_path = os.path.join(parquet_dir, "dataset-ms-test-0000-of-0001.parquet")
sdf_df.to_parquet(parquet_path, index=False)
print(f"Wrote parquet: {parquet_path} ({len(sdf_df)} rows)")

# ── Run InstaNovo inference ────────────────────────────────────────────────────
out_csv = os.path.join(os.path.dirname(__file__), "instanovo_raw_predictions.csv")

cmd = (
    f"instanovo transformer predict "
    f"--data-path {parquet_dir} "
    f"--output-path {out_csv} "
    f"--instanovo-model instanovo-v1.2.0 "
    f"--evaluation "  # annotated mode: computes against ground truth
)
print(f"\nRunning: {cmd}\n")
ret = os.system(cmd)
if ret != 0:
    print("WARNING: instanovo returned non-zero exit code. Checking output anyway...")

# ── Parse InstaNovo output and compute our metrics ─────────────────────────────
if not os.path.exists(out_csv):
    raise FileNotFoundError(
        f"InstaNovo did not write {out_csv}. Check logs above for errors."
    )

preds = pd.read_csv(out_csv)
print(f"\nInstaNovo output columns: {list(preds.columns)}")
print(preds.head(3).to_string())

# Column names vary by instanovo version — handle both
seq_col = next(
    (c for c in preds.columns if "sequence" in c.lower() and "target" not in c.lower()),
    None,
)
truth_col = next(
    (c for c in preds.columns if "target" in c.lower() or "true" in c.lower()), None
)
score_col = next(
    (
        c
        for c in preds.columns
        if "score" in c.lower() or "log_prob" in c.lower() or "confidence" in c.lower()
    ),
    None,
)

if seq_col is None:
    raise ValueError(f"Cannot find predicted sequence column in {list(preds.columns)}")

print(f"\nUsing columns: pred={seq_col!r}  truth={truth_col!r}  score={score_col!r}")


def _clean(seq):
    """Strip PTM notation (e.g. M+15.994, +57.021) and non-AA characters."""
    import re

    # Remove modification annotations like [+57.021] or (Oxidation) or +15.994 after AA
    seq = re.sub(r"\[.*?\]", "", str(seq))
    seq = re.sub(r"\(.*?\)", "", seq)
    seq = re.sub(r"[^A-Z]", "", seq.upper())
    return seq


def _aa_recall(pred: str, true: str) -> float:
    if not true:
        return 0.0
    n = min(len(pred), len(true))
    matches = sum(p == t for p, t in zip(pred, true))
    return matches / max(len(true), 1)


results = []
for _, row in preds.iterrows():
    pred_raw = str(row[seq_col]) if seq_col else ""
    true_raw = str(row[truth_col]) if truth_col else ""
    score_val = float(row[score_col]) if score_col and pd.notna(row[score_col]) else 0.0

    pred_clean = _clean(pred_raw)
    true_clean = _clean(true_raw)

    rec = _aa_recall(pred_clean, true_clean)
    correct = int(pred_clean == true_clean)

    results.append(
        {
            "spectrum_id": row.get("prediction_id", row.name),
            "true_sequence": true_raw,
            "predicted_sequence": pred_raw,
            "true_clean": true_clean,
            "pred_clean": pred_clean,
            "aa_recall": rec,
            "pep_correct": correct,
            "score": score_val,
        }
    )

results_df = pd.DataFrame(results)

aa_rec_mean = results_df["aa_recall"].mean() * 100
pep_acc_mean = results_df["pep_correct"].mean() * 100

print(f"\n{'='*50}")
print(f"InstaNovo on our 472-spectrum test split")
print(f"  AA Recall  : {aa_rec_mean:.2f}%")
print(f"  Pep Acc    : {pep_acc_mean:.2f}%")
print(f"  n spectra  : {len(results_df)}")
print(f"{'='*50}\n")

out_final = os.path.join(os.path.dirname(__file__), "instanovo_472_split.csv")
results_df.to_csv(out_final, index=False)
print(f"Saved → {out_final}")

summary = {
    "model": "instanovo-v1.2.0",
    "test_set": "ecoli_ev_472",
    "n_spectra": len(results_df),
    "aa_recall_pct": round(aa_rec_mean, 2),
    "pep_acc_pct": round(pep_acc_mean, 2),
}
import json

summary_path = os.path.join(os.path.dirname(__file__), "instanovo_summary.json")
with open(summary_path, "w") as f:
    json.dump(summary, f, indent=2)
print(f"Saved → {summary_path}")
