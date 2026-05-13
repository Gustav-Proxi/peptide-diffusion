"""
Fix 1: Run InstaNovo v1.2.0 on our 472-spectrum E. coli EV test split.

Produces:
  eval/instanovo_472_split.csv   — per-spectrum results
  eval/instanovo_summary.json    — aggregate AA recall + pep acc
"""

import glob
import json
import os
import re
import sys

import numpy as np
import pandas as pd
import torch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from preprocessing import load_labeled_spectra

# ── Reproduce exact 70/15/15 split (rng seed=42) ──────────────────────────────
BASE = os.path.join(ROOT, "data", "raw")
mzml_paths = sorted(glob.glob(os.path.join(BASE, "Ecoli_EV_*.mzML")))
xlsx_paths = sorted(
    glob.glob(os.path.join(BASE, "Database search output_Ecoli_EV_*.xlsx"))
)

if not mzml_paths:
    raise FileNotFoundError(f"No mzML files under {BASE}")

print(f"Loading spectra from {[os.path.basename(p) for p in mzml_paths]}")
all_spectra = []
for mz, xl in zip(mzml_paths, xlsx_paths):
    all_spectra.extend(load_labeled_spectra(mz, xl, max_spectra=5000))

N = len(all_spectra)
rng = np.random.default_rng(42)
idx = rng.permutation(N)
n_tr = int(0.70 * N)
n_va = int(0.15 * N)
te_idx = idx[n_tr + n_va :]
test_spectra = [all_spectra[i] for i in te_idx]
print(f"Total: {N}, test split: {len(test_spectra)}")

# ── Write parquet (InstaNovo default-partition naming) ─────────────────────────
parquet_dir = os.path.join(ROOT, "eval", "ecoli_test_parquet")
os.makedirs(parquet_dir, exist_ok=True)
parquet_path = os.path.join(parquet_dir, "dataset-ms-default-0000-of-0001.parquet")

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
sdf_df.to_parquet(parquet_path, index=False)
print(f"Wrote parquet: {parquet_path}")

from instanovo.inference import BeamSearchDecoder
from instanovo.transformer.data import TransformerDataProcessor
# ── Load InstaNovo ─────────────────────────────────────────────────────────────
from instanovo.transformer.model import InstaNovo
from instanovo.utils.data_handler import SpectrumDataFrame
from torch.utils.data import DataLoader

print("\nLoading InstaNovo pretrained model (instanovo-v1.2.0)...")
model, config = InstaNovo.from_pretrained("instanovo-v1.2.0")
device = torch.device("cpu")
model = model.to(device)
model.eval()
print(f"Model on {device}")

# ── Build dataset ─────────────────────────────────────────────────────────────
rs = model.residue_set
proc = TransformerDataProcessor(
    residue_set=rs,
    n_peaks=config.get("n_peaks", 200),
    min_mz=config.get("min_mz", 50.0),
    max_mz=config.get("max_mz", 2500.0),
    min_intensity=config.get("min_intensity", 0.01),
    remove_precursor_tol=config.get("remove_precursor_tol", 2.0),
    annotated=True,
)

sdf = SpectrumDataFrame.load(
    parquet_dir,
    lazy=False,
    is_annotated=True,
    shuffle=False,
    add_spectrum_id=True,
)
hf_ds = sdf.to_dataset(in_memory=True)
ds = proc.process_dataset(hf_ds)
dl = DataLoader(ds, batch_size=32, shuffle=False, collate_fn=proc.collate_fn)
print(f"DataLoader: {len(ds)} spectra in {len(dl)} batches")

# ── Decoder ───────────────────────────────────────────────────────────────────
decoder = BeamSearchDecoder(model, float_dtype=torch.float32)

# ── Inference ─────────────────────────────────────────────────────────────────
print("\nRunning inference...")
all_preds, all_targets, all_scores = [], [], []

with torch.no_grad():
    for bi, batch in enumerate(dl):
        spectra = batch["spectra"].to(device)
        precursors = batch["precursors"].to(device)

        result = decoder.decode(
            spectra=spectra,
            precursors=precursors,
            beam_size=5,
            max_length=config.get("max_length", 40),
            return_beam=False,
        )

        # predictions is a list of token-lists e.g. [['T','G','F',...], ...]
        raw_preds = result["predictions"]
        preds = ["".join(toks) for toks in raw_preds]
        all_preds.extend(preds)

        if "peptides" in batch:
            targets = [rs.decode(seq, reverse=True) for seq in batch["peptides"]]
        else:
            targets = [""] * len(preds)
        all_targets.extend(targets)

        raw_scores = result.get("prediction_log_probability", [0.0] * len(preds))
        all_scores.extend(
            raw_scores if isinstance(raw_scores, list) else raw_scores.tolist()
        )

        done = min((bi + 1) * 32, len(ds))
        print(f"  {done}/{len(ds)}", end="\r", flush=True)

print(f"\nDone. {len(all_preds)} predictions.")


# ── Metrics ───────────────────────────────────────────────────────────────────
def _clean(seq: str) -> str:
    seq = re.sub(r"\[.*?\]|\(.*?\)", "", str(seq))
    return re.sub(r"[^A-Z]", "", seq.upper())


def _aa_recall(pred: str, true: str) -> float:
    if not true:
        return 0.0
    return sum(p == t for p, t in zip(pred, true)) / max(len(true), 1)


rows_out = []
for i, (pred_raw, true_raw, score) in enumerate(
    zip(all_preds, all_targets, all_scores)
):
    pred_c = _clean(str(pred_raw))
    true_c = _clean(str(true_raw))
    rows_out.append(
        {
            "spectrum_id": i,
            "true_sequence": true_raw,
            "predicted_sequence": pred_raw,
            "true_clean": true_c,
            "pred_clean": pred_c,
            "aa_recall": _aa_recall(pred_c, true_c),
            "pep_correct": int(pred_c == true_c),
            "score": score,
        }
    )

df = pd.DataFrame(rows_out)
aa_rec = df["aa_recall"].mean() * 100
pep_acc = df["pep_correct"].mean() * 100

print(f"\n{'='*55}")
print(f"InstaNovo v1.2.0  |  our 472-spectrum test split")
print(f"  AA Recall  : {aa_rec:.2f}%")
print(f"  Pep Acc    : {pep_acc:.2f}%")
print(f"  n spectra  : {len(df)}")
print(f"{'='*55}")

out_dir = os.path.join(ROOT, "eval")
df.to_csv(os.path.join(out_dir, "instanovo_472_split.csv"), index=False)
print(f"Saved → eval/instanovo_472_split.csv")

summary = {
    "model": "instanovo-v1.2.0",
    "test_set": "ecoli_ev_472",
    "n_spectra": len(df),
    "aa_recall_pct": round(aa_rec, 2),
    "pep_acc_pct": round(pep_acc, 2),
}
with open(os.path.join(out_dir, "instanovo_summary.json"), "w") as f:
    json.dump(summary, f, indent=2)
print(f"Saved → eval/instanovo_summary.json")
