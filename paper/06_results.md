# Results [DRAFT]

**Owner:** Vaishak (6.1, 6.3); Sanika (6.2, 6.4, 6.5, 6.6)
**Target length:** ~3 pages (double-column IEEEtran) + supplementary tables
**Status:** `[HOLD]` -- fill after experiments complete (October-November 2026)

---

## 6.1 Mass-Constrained Training Ablation [NEW] [Vaishak]

**Key claim:** L_mass improves peptide accuracy at 5% FDR while reducing mass-violation rate, without degrading AA recall. Best lambda is 0.01.

### Table 1: Lambda sweep on E. coli EV (472 spectra, 5% FDR)

| Model | lambda | AA Recall (%) | Pep Acc (%) | Mass Viol. Rate (%) |
|---|---|---|---|---|
| Base (BIBM) | -- | 76.00 +/- 0.19 | 59.96 +/- 3.82 | [TBD] |
| + L_mass | 0.001 | [TBD] | [TBD] | [TBD] |
| + L_mass | 0.01 | [TBD] | [TBD] | [TBD] |
| + L_mass | 0.1 | [TBD] | [TBD] | [TBD] |
| + L_mass | 1.0 | [TBD] | [TBD] | [TBD] |
| InstaNovo | -- | 72.90 | [re-run] | -- |

*All values: mean +/- std over 3 seeds. InstaNovo re-run on our 472-spectrum split.*

**Expected finding:** Lambda = 0.01 gives +2-5 pp pep acc and order-of-magnitude reduction in mass-violation rate. Lambda = 1.0 may degrade AA recall (mass dominates). If so, report Pareto frontier.

**If results don't match expectations:** If mass-constrained training doesn't improve pep accuracy, the paper is still publishable -- report the negative result honestly (mass constraint is a useful regularizer for mass violations even without pep acc improvement) and frame the generalization study (Section 6.2) as the primary empirical contribution.

---

## 6.2 NovoBench Cross-Species Results [NEW] [Sanika]

**Key claim:** Mass-constrained model generalizes to non-E. coli species on at least X/9 NovoBench splits (X >= 5 is the target).

### Table 2: NovoBench 9-species evaluation (best lambda from 6.1)

| Species | Base (BIBM) AA | Base Pep | Mass-Const AA | Mass-Const Pep | InstaNovo AA | InstaNovo Pep |
|---|---|---|---|---|---|---|
| E. coli | 76.00 | 59.96 | [TBD] | [TBD] | [re-run] | [re-run] |
| Human | [TBD] | [TBD] | [TBD] | [TBD] | [pub] | [pub] |
| Yeast | [TBD] | [TBD] | [TBD] | [TBD] | [pub] | [pub] |
| Mouse | [TBD] | [TBD] | [TBD] | [TBD] | [pub] | [pub] |
| [Species 5] | [TBD] | [TBD] | [TBD] | [TBD] | [pub] | [pub] |
| [Species 6] | [TBD] | [TBD] | [TBD] | [TBD] | [pub] | [pub] |
| [Species 7] | [TBD] | [TBD] | [TBD] | [TBD] | [pub] | [pub] |
| [Species 8] | [TBD] | [TBD] | [TBD] | [TBD] | [pub] | [pub] |
| [Species 9] | [TBD] | [TBD] | [TBD] | [TBD] | [pub] | [pub] |

*[pub] = InstaNovo published NovoBench numbers. [re-run] = our re-run on E. coli split with our preprocessing.*

**Expected finding:** Our model (trained only on E. coli EV) shows competitive performance on at least 5 species. Performance may drop on species with very different fragmentation (HCD vs CID; different PTM profiles). Frame drops as honest generalization limits, not failures.

**Honest reporting note:** If our model performs worse than InstaNovo on most species (expected, since InstaNovo trains on multi-species data), frame this as: "our model generalizes from a single-species training set to X/9 species; mass-constrained training improves generalization compared to the unconstrained model in Y/9 cases."

---

## 6.3 Mutual Information Correlation Analysis [NEW] [Vaishak]

**Key claim:** Self-conditioning accuracy gain at timestep t correlates with MI(x_0; S | x_t) at timestep t, with Pearson r > 0.7.

### Figure 5: MI and self-conditioning gain across diffusion timesteps

*Plot format:*
- X-axis: diffusion timestep t (0=clean, 500=fully absorbed)
- Y-axis left: I(x_0; S | x_t) estimated by MINE/InfoNCE
- Y-axis right: delta accuracy (self-conditioned - unconditioned) at timestep t
- Expected: both curves peak at intermediate t (around t=100-200), confirming the theory claim

### Pearson r result

*If r > 0.7:* Report in text; theory section stands.
*If 0.5 < r < 0.7:* Report honestly; note that the correlation is positive and directionally consistent with the theory but not tight enough to claim a one-to-one correspondence.
*If r < 0.5:* Switch to backup framing in theory section. Report MI analysis in supplementary.

---

## 6.4 Cross-Instrument Analysis (HCD vs CID) [NEW] [Sanika]

**Status:** `[HOLD]` -- depends on NovoBench metadata having instrument labels

*If instrument metadata available in NovoBench mzML files:*

### Table 3: Performance split by instrument type

| Instrument | N spectra | Base AA | Base Pep | Mass-Const AA | Mass-Const Pep |
|---|---|---|---|---|---|
| HCD | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| CID | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |

*If metadata is not available: note in the limitations section and drop this analysis.*

---

## 6.5 Out-of-Distribution Generalization [NEW] [Sanika]

**Key claim:** The mass-constrained model, trained only on E. coli EV, transfers to non-E. coli species. This is the strongest generalization test -- most baselines use multi-species training.

*Format: heatmap or bar chart. Train on E. coli EV only (472 spectra). Eval on each of the 8 non-E. coli NovoBench species.*

Expected: zero-shot transfer works reasonably well on phylogenetically close species (other gram-negative bacteria); degrades on eukaryotes.

---

## 6.6 ESM-2 Structural Plausibility (Multi-Species) [NEW] [Sanika]

*Replicates the ESM-2 analysis from BIBM but across all 9 NovoBench species.*

**Metric:** pseudo-perplexity from ESM-2 (`facebook/esm2_t6_8M_UR50D`). Lower = more protein-like = more structurally plausible.

*Format: boxplot per species, comparing our model's decoded sequences vs. random sequences vs. database-search ground truth (where available).*

---

