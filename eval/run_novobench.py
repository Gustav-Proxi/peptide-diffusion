"""
Fix 2: Run V2 CFID+SGIR model on NovoBench 9-species splits.

Downloads NovoBench-2 test parquets from HuggingFace, runs our model on each,
reports AA recall + peptide accuracy per species.

Produces: eval/novobench_results.csv

Usage:
  cd peptide-diffusion
  python eval/run_novobench.py [--species human mouse] [--checkpoint path]
"""

import argparse
import glob
import os
import sys

import numpy as np
import pandas as pd
import torch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from diffusion import (IDX_TO_CHAR, N_PEAKS, PROTON_MASS, VOCAB, PeakEncoder,
                       TransformerDenoiser, encode_peptide, evaluate_aa_recall,
                       extract_top_peaks, load_checkpoint)

# ── NovoBench species list (NovoBench-2, Zhou et al. NeurIPS 2024) ────────────
# HF dataset: InstaDeep/novobench or jingbo02/NovoBench-2
# Each species is a separate config/split in the dataset.
SPECIES = [
    "human",
    "mouse",
    "yeast",
    "arabidopsis",
    "bacillus",
    "celegans",
    "drosophila",
    "ecoli",
    "rice",
]

AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


def load_novobench_species(species: str, cache_dir: str) -> list[dict] | None:
    """Download and return spectra for a NovoBench species."""
    try:
        from datasets import load_dataset
    except ImportError:
        print("  Install datasets: pip install datasets")
        return None

    print(f"  Downloading NovoBench-2 {species}...")
    try:
        ds = load_dataset(
            "InstaDeep/novobench-2",
            name=species,
            split="test",
            cache_dir=cache_dir,
            trust_remote_code=True,
        )
    except Exception as e:
        print(f"  Failed (InstaDeep/novobench-2): {e}")
        try:
            ds = load_dataset(
                "jingbo02/NovoBench",
                name=species,
                split="test",
                cache_dir=cache_dir,
                trust_remote_code=True,
            )
        except Exception as e2:
            print(f"  Failed (jingbo02/NovoBench): {e2}")
            return None

    spectra = []
    for row in ds:
        mz = np.array(row.get("mz_array", row.get("mz", [])), dtype=np.float32)
        intensity = np.array(
            row.get("intensity_array", row.get("intensities", [])), dtype=np.float32
        )
        peptide_raw = row.get("sequence", row.get("modified_sequence", ""))
        # Strip PTMs to canonical AA sequence
        import re

        peptide = re.sub(r"[^A-Z]", "", str(peptide_raw).upper())
        if not all(c in AMINO_ACIDS for c in peptide):
            continue
        prec_mz = float(row.get("precursor_mz", 0.0))
        charge = int(row.get("precursor_charge", 2))
        spectra.append(
            {
                "mz": mz,
                "intensity": intensity,
                "peptide": peptide,
                "precursor_mz": prec_mz,
                "charge": charge,
            }
        )
    print(f"  Loaded {len(spectra)} spectra for {species}")
    return spectra


def build_arrays(spectra):
    """Convert spectrum list to peak arrays + encoded y + masses."""
    peaks_list, y_list, mass_list, raw_list = [], [], [], []
    for s in spectra:
        peaks_list.append(extract_top_peaks(s["mz"], s["intensity"], N_PEAKS))
        y_list.append(encode_peptide(s["peptide"]))
        prec_mz = s.get("precursor_mz") or 0.0
        charge = s.get("charge") or 0
        neutral = float(charge) * (float(prec_mz) - PROTON_MASS) if charge else 0.0
        mass_list.append(neutral)
        raw_list.append(
            (
                np.asarray(s["mz"], dtype=np.float32),
                np.asarray(s["intensity"], dtype=np.float32),
            )
        )
    return (
        np.array(peaks_list, dtype=np.float32),
        np.array(y_list),
        np.array(mass_list, dtype=np.float32),
        raw_list,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--species",
        nargs="+",
        default=SPECIES,
        help="Species to evaluate (default: all 9)",
    )
    parser.add_argument(
        "--checkpoint",
        default=None,
        help="Path to a single checkpoint. Default: best seed_0 V2 final.",
    )
    parser.add_argument(
        "--max-spectra",
        type=int,
        default=2000,
        help="Max spectra per species (default 2000 for speed)",
    )
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # ── Find checkpoint(s) ─────────────────────────────────────────────────────
    if args.checkpoint:
        ckpt_paths = [args.checkpoint]
    else:
        v2_dir = os.path.join(ROOT, "checkpoints", "v2")
        ckpt_paths = sorted(
            glob.glob(os.path.join(v2_dir, "seed_*/diffusion_final.pt"))
        )
        if not ckpt_paths:
            ckpt_paths = sorted(
                glob.glob(os.path.join(v2_dir, "seed_*/diffusion_best.pt"))
            )
        if not ckpt_paths:
            # Fall back to top-level checkpoints
            ckpt_paths = sorted(
                glob.glob(
                    os.path.join(ROOT, "checkpoints", "seed_*/diffusion_final.pt")
                )
            )
        if not ckpt_paths:
            raise FileNotFoundError(
                "No V2 checkpoints found. Pass --checkpoint explicitly."
            )

    print(f"Using checkpoints: {[os.path.basename(p) for p in ckpt_paths]}")

    cache_dir = os.path.join(ROOT, "eval", "novobench_cache")
    os.makedirs(cache_dir, exist_ok=True)

    rows = []
    for ckpt_path in ckpt_paths:
        seed_name = os.path.basename(os.path.dirname(ckpt_path))
        print(f"\n=== Checkpoint: {ckpt_path} ===")
        encoder, denoiser = load_checkpoint(ckpt_path, device=device)

        for species in args.species:
            print(f"\n--- Species: {species} ---")
            spectra = load_novobench_species(species, cache_dir)
            if spectra is None or len(spectra) == 0:
                print(f"  Skipping {species} (no data)")
                rows.append(
                    {
                        "seed": seed_name,
                        "species": species,
                        "n_spectra": 0,
                        "AA Recall %": float("nan"),
                        "Pep Acc %": float("nan"),
                    }
                )
                continue

            if args.max_spectra and len(spectra) > args.max_spectra:
                rng = np.random.default_rng(42)
                idx = rng.choice(len(spectra), args.max_spectra, replace=False)
                spectra = [spectra[i] for i in idx]
                print(f"  Subsampled to {len(spectra)} spectra")

            X, y, masses, raw_peaks = build_arrays(spectra)

            aa_rec, pep_acc = evaluate_aa_recall(
                encoder,
                denoiser,
                X,
                y,
                masses,
                batch_size=128,
                results_dir=os.path.join(ROOT, "eval", "novobench_preds"),
                device=device,
                use_cfid=True,
                use_sgir=True,
                raw_peaks=raw_peaks,
            )
            print(f"  {species}: AA={aa_rec:.2f}%  Pep={pep_acc:.2f}%")
            rows.append(
                {
                    "seed": seed_name,
                    "species": species,
                    "n_spectra": len(spectra),
                    "AA Recall %": aa_rec,
                    "Pep Acc %": pep_acc,
                }
            )

    df = pd.DataFrame(rows)
    print("\n=== NovoBench Summary ===")
    summary = (
        df.groupby("species")[["AA Recall %", "Pep Acc %"]]
        .mean()
        .sort_values("Pep Acc %", ascending=False)
    )
    print(summary.to_string())

    out_path = os.path.join(ROOT, "eval", "novobench_results.csv")
    df.to_csv(out_path, index=False)
    print(f"\nSaved → eval/novobench_results.csv")


if __name__ == "__main__":
    main()
