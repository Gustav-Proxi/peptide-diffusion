# Experiments [DRAFT]

**Owner:** Sanika (5.1, 5.2, 5.3); Vaishak reviews
**Target length:** ~1 page (double-column IEEEtran)
**Status:** `[HOLD]` -- write after NovoBench data is set up (October 2026)

---

## 5.1 Datasets

### E. coli EV proteomics (BIBM baseline dataset)

- Source: E. coli extracellular vesicle proteomics dataset (same as BIBM paper)
- Size: 472 spectra at 5% FDR
- Ground truth: SEQUEST-HT database search (Xcorr-based FDR via q-value)
- Split: same train/val/test as BIBM paper -- do not re-split (preserves comparability)
- PTMs: carbamidomethyl-C (fixed), oxidized-M + deamidated-NQ (variable)
- Charge range: 2+ to 4+ (filter out charge 1 and >5)

### NovoBench (cross-species generalization)

- Source: Zhou et al. NeurIPS 2024 (https://github.com/jingbo02/NovoBench-2)
- Species: 9 (list when data confirmed)
- Splits: standardized by NovoBench authors; we use their test sets without modification
- Preprocessing: same pipeline as E. coli EV (pyOpenMS, same PTM set, same peak count limit of 800)
- Note: if any species has instrument-type metadata (HCD vs CID), log for cross-instrument analysis

### Wastewater (optional, Appendix)

- Source: same as BIBM paper, Sample 2
- Ground truth: none (metaproteomics, novel organisms)
- Use: qualitative BLAST validation of top-confidence recovered peptides
- Status: BLAST pending (6 sequences, NCBI BLASTp against nr database)

---

## 5.2 Baselines and Metrics

### Baselines

| Baseline | Type | Source | Notes |
|---|---|---|---|
| Base model (BIBM 2026) | Our prior work | Checkpoint at `../checkpoints/v2/` | No mass-constrained training |
| InstaNovo [Eloff 2024] | External | Published checkpoint + our re-run | Re-run on E. coli EV split; use published numbers for NovoBench |
| Casanovo [Yilmaz 2022] | External | Published numbers | NovoBench published results only |
| Mass-constrained (lambda sweep) | This paper | Train from scratch with L_mass | lambda in {0.001, 0.01, 0.1, 1.0} |

**Critical note:** The InstaNovo comparison in the BIBM paper used published Nature MI numbers on a different test set. For this paper, re-run InstaNovo on the E. coli EV 472-spectrum split with our preprocessing to ensure a fair comparison. This was identified as a validity issue in the BIBM paper discussion and was Fix 1 in the hardening pass.

### Metrics

Primary (report for all models and all species):
- **Amino acid (AA) recall:** fraction of correct residues in recovered peptides (position-sensitive)
- **Peptide accuracy:** fraction of peptides where the full sequence is exactly correct

Both at **5% FDR** via q-value thresholding (same code as BIBM paper).

Secondary:
- **Mass-violation rate:** fraction of decoded peptides where |M_pred - M_target| > 50 ppm (before any FDR filter). This is the primary metric for evaluating L_mass.
- **ESM-2 pseudo-perplexity:** proxy for structural plausibility of recovered sequences (lower PPL = more protein-like). Use `facebook/esm2_t6_8M_UR50D` for speed.
- **De novo coverage:** fraction of spectra with at least one decoded sequence passing FDR.

### FDR computation

Use same q-value code as BIBM paper (target-decoy approach, decoy = reversed sequences). If comparing against external baselines with different FDR methods, report both their FDR and ours separately. Do not mix FDR methods across models in the same table.

---

## 5.3 Implementation Details

### Training

- Hardware: M4 Mac (MPS backend) for development; final training on [TBD: cloud GPU or UB cluster]
- Framework: PyTorch 2+, HuggingFace Transformers
- Batch size: [same as BIBM, confirm]
- Optimizer: AdamW with cosine LR schedule
- Epochs: 200 (anneal L_mass over first 50)
- Seeds: 3 (0, 1, 2) for all experiments; report mean +/- std
- Checkpoints: save best by val peptide accuracy; use for all eval

### Inference

- Beam size: K=8 (same as BIBM)
- Mass filter: 50 ppm (same as BIBM, applied at beam search; L_mass is training-only)
- Decoder: same as BIBM 2026, unchanged [BIBM cite]

### Reproducibility

- All hyperparameters logged to JSON alongside checkpoint
- NovoBench preprocessing script: `../src/novobench_preprocess.py` (Sanika writes this)
- Mass-constrained training script: `../src/train_diffusion.py` with `--lambda_mass` flag (Vaishak adds this)
- All evaluation outputs saved to `../results/tcbb/` (do not overwrite BIBM results in `../results/`)
