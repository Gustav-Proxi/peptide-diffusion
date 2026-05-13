# Abstract [DRAFT]

**Owner:** Vaishak
**Word limit:** 250 (TCBB hard limit)
**Status:** `[DRAFT]` -- placeholder structure; fill after all results are in

---

## Draft structure

*The abstract for a TCBB methods paper should hit four beats in order: (1) problem + why hard, (2) what we do (method), (3) what we find (numbers), (4) what this means (impact). Concrete numbers are required -- reviewers read abstracts to decide if the paper is worth reviewing.*

---

## Placeholder draft

De novo peptide sequencing -- reconstructing peptide sequences directly from tandem mass spectra without a reference proteome -- remains a central challenge in metaproteomics and novel organism analysis. Existing approaches enforce precursor mass feasibility only at inference, which prevents gradient-based learning of mass-consistent sequence distributions. We present a mass-constrained extension of self-conditioned multinomial diffusion for de novo peptide sequencing, introducing an auxiliary training loss that penalizes mass-infeasible sequence distributions at every denoising step. The relative-squared mass loss (L_mass = E_t[(M_pred - M_target)^2 / M_target^2]) is differentiable through the soft argmax and annealed linearly over the first 50 training epochs, allowing the model to acquire sequence structure before tightening the mass constraint. On the E. coli EV benchmark, the mass-constrained model improves peptide accuracy by **X.X pp** at 5% FDR (lambda = 0.01) while maintaining amino acid recall, resolving a key failure mode identified in our prior work. We further evaluate cross-species generalization on all 9 NovoBench species, finding that the mass-constrained model outperforms the unconstrained baseline on **X/9** species splits. Finally, we provide an information-theoretic analysis establishing that self-conditioning performs iterative mutual information maximization between the partially-denoised sequence and the spectrum, with empirical validation showing a Pearson correlation of **r = X.XX** between MI at diffusion timestep t and sequencing accuracy gain from self-conditioning. These results suggest that mass-constrained training is a general, biologically grounded regularizer for discrete diffusion models over molecular sequences.

---

## Revision log

| Date | Change | Author |
|---|---|---|
| 2026-12-XX | First full draft after experiments complete | Vaishak |
| -- | Replace all **X.X** placeholders with real numbers | Vaishak |
| -- | Sanika review pass | Sanika |

---

## Notes

- Do not exceed 250 words.
- All bolded numbers are placeholders. Fill from results files in `../results/`.
- The last sentence should be the "generalization" claim -- reviewers at TCBB care about this.
- IEEE TCBB abstracts are indexed by IEEE Xplore. Include keywords: diffusion models, de novo peptide sequencing, mass spectrometry, cross-species generalization, self-conditioning, mutual information.

**Keywords (5-6 required by TCBB):**
de novo peptide sequencing, absorbing multinomial diffusion, mass-constrained training, cross-species generalization, self-conditioning, mutual information estimation
