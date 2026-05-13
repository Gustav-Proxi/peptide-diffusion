# Methods [DRAFT]

**Owner:** Vaishak (4.1, 4.2, 4.3); Sanika (4.4)
**Target length:** ~3 pages total (double-column IEEEtran)
**Status:** `[DRAFT]`

> Note at top of this section in paper: "Section 4.2 restates the model architecture from [BIBM 2026]; Sections 4.1, 4.3, and 4.4 are new to this work."

---

## 4.1 Theoretical Framework: Self-Conditioning as MI Maximization [NEW] [HOLD pending experiments]

**Owner:** Vaishak
**Status:** `[HOLD]` -- write after MI experiments in November 2026

### Setup

Let `S` denote the MS/MS spectrum (set of (m/z, intensity) pairs), `x_0` the clean amino acid sequence (a sequence in {1,...,20}^L), and `x_t` the partially-absorbed sequence at diffusion step t. Define:

```
I(x_0; S | x_t) -- conditional mutual information between clean sequence and spectrum,
                   given the noisy sequence at step t
```

Standard absorbing diffusion estimates `p(x_0 | x_t, S)` directly. Self-conditioning estimates `p(x_0 | x_t, S, x̂_0^prev)` where `x̂_0^prev` is a prior denoised estimate.

### Main claim

**Claim.** Under mild conditions on the absorbing process, each self-conditioning step is a one-step Newton-direction update on the mutual information objective `I(x_0; S | x_t)`, subject to a KL divergence constraint that prevents distribution collapse.

### Formal derivation (to be completed)

*Sketch -- fill in with full derivation for Appendix A:*

1. Write the ELBO as a function of `p(x_0 | x_t, S)`.
2. Show that the gradient of the ELBO with respect to the model parameters, evaluated at the prior estimate `x̂_0^prev`, has the form of a MI gradient up to a constant.
3. Self-conditioning replaces a single forward pass with an iterative refinement that converges to the fixed point -- show this fixed point corresponds to the MI maximizer under the KL constraint.

### Experimental validation

- Compute `I(x_0; S | x_t)` empirically across timesteps using MINE [Belghazi 2018] or InfoNCE [van den Oord 2018].
- Compute self-conditioning accuracy gain at each timestep t vs. unconditioned baseline.
- Report Pearson r between MI(t) and accuracy_gain(t).
- Threshold: if r > 0.7, the theory section stands as written. If r < 0.7, switch to backup framing: "self-conditioning as score refinement under learned manifold prior."

### References for this section

- Austin et al. 2021 (D3PM) -- for absorbing diffusion KL bounds
- Chen et al. 2022 (Analog Bits) -- original self-conditioning, no formal analysis (our gap)
- Belghazi et al. 2018 (MINE)
- Poole et al. 2019 -- variational MI bounds
- Sohl-Dickstein et al. 2015 -- VLB machinery

---

## 4.2 Model Architecture [REUSED from BIBM 2026]

**Owner:** Vaishak
**Status:** `[DRAFT]` -- adapt from BIBM paper, add "reused, cited" markers

### Forward process (absorbing diffusion)

At each diffusion step t, amino acid tokens are independently absorbed to a MASK token with probability beta(t), following a cosine noise schedule. The forward marginal is:

```
q(x_t | x_0) = prod_i [ (1 - beta_bar(t)) * delta(x_t_i = x_0_i) + beta_bar(t) * delta(x_t_i = MASK) ]
```

T = 500 steps, cosine schedule from Austin et al. 2021.

### Spectrum encoder (PeakEncoder)

Input: MS/MS spectrum as sequence of (m/z, intensity) pairs (max 800 peaks).
Encoding: sinusoidal m/z embedding + learnable B/Y-ion pair bias (learned compatibility between b-ion and y-ion peaks that sum to precursor mass +/- 1 Da). *This is a contribution of the BIBM paper; restated here for self-containment.*

### Self-conditioning (preview-refine loop)

With probability p_sc = 0.5 during training, a "preview" denoising step is run and x̂_0^prev is passed as additional conditioning to the main denoising step. This prevents the model from over-relying on the preview at inference. At inference, self-conditioning is always used: a fast single-step denoising produces x̂_0^prev, then the full T-step refinement is conditioned on it.

### Decoding (reused from BIBM 2026, not extended here)

*The decoding strategy from the BIBM paper is used as-is; results are reported for completeness and fair comparison. Full description in [BIBM cite]; we omit it here to avoid duplication.*

Beam search (K=8) with knapsack constraint (50 ppm), followed by candidate reranking [BIBM cite]. For new experiments in this paper, the same decoder is used unchanged to isolate the effect of mass-constrained training.

---

## 4.3 Mass-Constrained Training Loss [NEW]

**Owner:** Vaishak
**Status:** `[DRAFT]`

### Motivation

The BIBM paper applied mass constraints only at inference -- specifically, knapsack beam search filtered candidates to those within 50 ppm of the precursor mass. All three inference-time mass enforcement strategies tested degraded peptide accuracy. The reason is structural: inference-time constraint is a hard filter over discrete candidates and cannot propagate gradients. Mass feasibility must be learned, not filtered.

### Loss formulation

The modified training objective:

```
L_total = L_VLB + lambda_mass * L_mass

L_VLB  = sum_t E_{q(x_t|x_0)} [ -log p_theta(x_0 | x_t, S) ]

L_mass = E_t [ (M_pred(x̂_0) - M_target)^2 / M_target^2 ]
```

where:
- `M_pred(x̂_0)` is the monoisotopic mass computed from the model's denoised sequence estimate x̂_0 at diffusion step t. Computed by taking the soft argmax over the per-position amino acid probability distribution and multiplying by the standard amino acid mass table.
- `M_target` is the measured precursor mass from the MS1 scan.
- The relative-squared form normalizes across peptide sizes (longer peptides have higher absolute mass variance).

**Why this works in training but not at inference:** L_mass is differentiable through the soft argmax at training time. At inference, the sequence is discrete (hard argmax or beam search), so no gradient flows. The same distinction explains why scheduled sampling outperforms beam-search constraints in seq2seq models.

### Annealing schedule

Linear anneal: lambda_mass increases from 0 to lambda_mass^target over the first 50 epochs (of 200 total training epochs). This allows the model to acquire sequence structure under L_VLB before the mass constraint tightens.

Rationale: premature mass constraint can collapse the distribution to a single mass-feasible sequence early in training, preventing the model from exploring the sequence space needed to learn b/y-ion patterns.

### Hyperparameter sweep

lambda_mass in {0.001, 0.01, 0.1, 1.0}. Report Pareto frontier of AA recall vs. peptide accuracy over the sweep. Expected: lambda = 0.01 is optimal; lambda = 1.0 likely degrades AA recall as mass constraint dominates.

### Evaluation

All models trained with 3 random seeds. Primary metric: peptide accuracy at 5% FDR. Secondary: AA recall, mass-violation rate (fraction of decoded peptides where |M_pred - M_target| > 50 ppm).

Expected result: pep accuracy improves 2-5 pp; mass-violation rate drops by order of magnitude. If both hold, this is the paper's primary empirical contribution.

---

## 4.4 NovoBench Cross-Species Evaluation Setup [NEW]

**Owner:** Sanika
**Status:** `[HOLD]` -- write when NovoBench data downloaded (September 2026)

### Dataset

NovoBench (Zhou et al. NeurIPS 2024): 9 species, standardized mzML splits.

*Sanika: fill in species list when data downloaded. From memory: human, yeast, E. coli, mouse, rice, arabidopsis, bacillus, streptomyces, one more. Verify against the NovoBench paper/repo.*

Species list (TBD):
1. E. coli (EV, same as BIBM training set -- use as internal consistency check)
2. Human
3. Yeast
4. Mouse
5. (5-9 to fill from NovoBench metadata)

### Preprocessing

- Use same preprocessing pipeline as BIBM paper: pyOpenMS mzML reader, charge state filtering, PTMs (carbamidomethyl-C fixed, oxidized-M + deamidated-NQ variable).
- NovoBench provides standardized splits -- do not re-split. Use their test sets directly.
- Log any species where preprocessing fails or produces <100 test spectra. Don't drop silently.

### Experiments

Four comparisons per species:
1. Base model (BIBM paper, no mass-constrained training) -- inference-only, no retraining
2. Mass-constrained model (best lambda from Section 4.3 sweep) -- trained on E. coli EV, eval on all species
3. InstaNovo [Eloff 2024] -- published numbers where available; re-run on each NovoBench split where not
4. Casanovo [Yilmaz 2022] -- published numbers

Out-of-distribution experiment: train only on E. coli EV (N=472), eval on all 8 non-E. coli species. This is the strongest generalization signal -- most baselines train on multi-species data.

### Metrics

- AA recall at 5% FDR (primary)
- Peptide accuracy at 5% FDR (primary)
- Per-species ESM-2 pseudo-perplexity (structural plausibility proxy)
- Cross-instrument split: HCD vs CID where metadata available

### Figure plan (Sanika owns all)

- Figure 4: per-species bar chart, base vs mass-constrained, grouped by species
- Figure 5: OOD generalization heatmap (train species x eval species)
- Figure 6: ESM-2 PPL comparison across species
