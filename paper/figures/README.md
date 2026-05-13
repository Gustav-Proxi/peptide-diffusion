# Figures

**Owner:** Sanika (generation and captions); Vaishak (Figures 2, 3, 5 from MI/mass-constraint experiments)

All figure source code goes in `../../../figures/` (existing BIBM figures directory) under a `tcbb/` subdirectory. Do not overwrite existing BIBM figures.

---

## Figure budget (TCBB typical max: 10 main figures)

| # | Description | Owner | Status | Source script |
|---|---|---|---|---|
| 1 | Model architecture overview | Sanika | Adapt from BIBM Fig 1 | `figures/tcbb/fig1_architecture.py` |
| 2 | Mass-constrained loss curve (best lambda run) | Vaishak | New | `figures/tcbb/fig2_loss_curve.py` |
| 3 | Pareto frontier: AA recall vs Pep acc over lambda sweep | Vaishak | New | `figures/tcbb/fig3_pareto.py` |
| 4 | NovoBench per-species bar chart (base vs mass-constrained) | Sanika | New | `figures/tcbb/fig4_novobench_species.py` |
| 5 | MI vs timestep + gain vs timestep correlation plot | Vaishak | New | `figures/tcbb/fig5_mi_correlation.py` |
| 6 | OOD generalization: train E. coli, eval 9 species | Sanika | New | `figures/tcbb/fig6_ood.py` |
| 7 | ESM-2 PPL multi-species comparison | Sanika | New | `figures/tcbb/fig7_esm2.py` |
| 8 | HCD vs CID instrument breakdown (if metadata available) | Sanika | Contingent | `figures/tcbb/fig8_instrument.py` |

Total: 7 confirmed + 1 contingent. Under the 10-figure budget.

---

## Figure specifications (TCBB IEEE format)

- **Format:** PDF (vector) for line art and bar charts. PNG at 300 dpi minimum for raster plots.
- **Column width:** Single-column = 88 mm; double-column = 181 mm. Most figures should be single-column.
- **Font:** Times New Roman or similar serif, min 8pt in figure labels (must be readable at final print size).
- **Color:** Use colorblind-safe palette. Recommended: `seaborn-colorblind` or `tableau-colorblind10`. Avoid pure red/green pairings.
- **Caption length:** 2-3 sentences max. First sentence: what the figure shows. Second: main finding. Third (optional): additional context.

---

## Caption drafts (fill in as figures are generated)

**Figure 1:** Architecture of the mass-constrained self-conditioned multinomial diffusion model. The spectrum is encoded by the PeakEncoder (left), which incorporates B/Y-ion pair bias to capture fragment ion chemistry. The denoising transformer (center) takes the noisy token sequence and spectrum embedding as input; the optional self-conditioning preview path (dashed) feeds a prior denoised estimate x̂_0^prev as additional conditioning.

**Figure 2:** Training loss curves for L_VLB and L_mass under the annealing schedule (lambda = 0.01). L_mass is activated at epoch 0 with weight 0, increasing linearly to lambda by epoch 50. [Fill: actual numbers from training runs]

**Figure 3:** Pareto frontier of AA recall vs. peptide accuracy at 5% FDR over the lambda sweep (lambda in {0.001, 0.01, 0.1, 1.0}). Each point is the mean over 3 seeds; error bars are +/- 1 std. The base model (lambda = 0) is shown in grey. [Fill after experiments]

**Figure 4:** Per-species NovoBench evaluation (AA recall, 5% FDR). Species sorted by taxonomic distance from E. coli (training domain). Blue: base model (BIBM). Orange: mass-constrained model (this paper). InstaNovo (published NovoBench numbers) shown as dashed baseline. [Fill after experiments]

**Figure 5:** Conditional mutual information I(x_0; S | x_t) estimated by MINE (left y-axis, blue) and self-conditioning accuracy gain over unconditioned model (right y-axis, orange) across diffusion timesteps t. Pearson correlation r = [TBD]. Both curves are mean over 3 seeds; shaded regions are 95% CI.

**Figure 6:** Out-of-distribution generalization heatmap. Peptide accuracy at 5% FDR when the model is trained on E. coli EV only (472 spectra) and evaluated on each NovoBench species. Darker = higher accuracy. InstaNovo (multi-species training) shown as reference bar.

**Figure 7:** ESM-2 pseudo-perplexity of model-decoded sequences vs. database-search ground truth vs. random sequences, across all 9 NovoBench species. Lower PPL = more protein-like. Boxplots show distribution over all decoded sequences in each category.

**Figure 8 (contingent):** Performance split by instrument type (HCD vs. CID) across NovoBench species where instrument metadata is available. [Write only if metadata available]

---

## Output directory

Place all generated figure files in `figures/tcbb/output/`. Name by figure number and format:
- `fig1_architecture.pdf`
- `fig2_loss_curve.pdf`
- `fig3_pareto.pdf`
- etc.

Do not commit large generated files to git. Add `figures/tcbb/output/` to `.gitignore`.
