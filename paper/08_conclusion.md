# Conclusion [DRAFT]

**Owner:** Vaishak
**Target length:** ~0.5 pages (double-column IEEEtran), 2-3 paragraphs
**Status:** `[HOLD]` -- write last, after Discussion is done

---

## Required beats

1. Restate the problem and the key gaps this paper fills (1 sentence each)
2. Summarize the three contributions (3 sentences, one per contribution)
3. State the concrete empirical result (1-2 sentences, numbers required)
4. State the broader implication (1 sentence -- what does this mean for the field?)

---

## Placeholder draft

De novo peptide sequencing from tandem mass spectra enables protein identification without reference proteomes -- a critical capability for metaproteomics, clinical novel-organism analysis, and environmental proteomics. Prior deep learning approaches enforce precursor mass constraints only at inference, preventing the model from learning mass-consistent sequence distributions. This paper resolves this limitation with three contributions.

First, we introduce a mass-constrained training loss (L_mass) that penalizes mass-infeasible sequence distributions at every denoising step, is differentiable through the soft argmax, and is annealed over training to prevent premature mass collapse. Second, we conduct the first systematic cross-species generalization study of absorbing diffusion for de novo sequencing, evaluating on all 9 NovoBench species and including an out-of-distribution test (train on E. coli only, eval on 8 other species). Third, we provide an information-theoretic analysis establishing that self-conditioning approximates iterative mutual information maximization between the partially-denoised sequence and the spectrum, validated empirically with MINE-based estimation.

On the E. coli EV benchmark, mass-constrained training improves peptide accuracy by **X.X pp** at 5% FDR (lambda = 0.01) while reducing the mass-violation rate by [X]x. The mass-constrained model generalizes to **X/9** NovoBench species without retraining. We release all training code, checkpoints, and evaluation scripts at [repo URL].

These results suggest that physics-grounded training constraints -- where physical invariants are encoded directly into the training loss rather than applied post-hoc -- are a principled approach to improving discrete diffusion models for molecular sequence generation tasks more broadly.

---

## Notes

- Replace all **X.X** placeholders with final numbers.
- The last sentence is the "broader impact" sentence -- reviewers look for this. Keep it honest and specific; don't overclaim.
- Do not add new citations in the conclusion. Everything cited here should already appear in the paper.
- Keep it under 3 paragraphs. TCBB conclusions are short.
