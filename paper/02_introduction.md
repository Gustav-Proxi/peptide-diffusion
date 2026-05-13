# Introduction [DRAFT]

**Owner:** Vaishak
**Target length:** ~1 page (double-column IEEEtran)
**Status:** `[DRAFT]`

---

## Required beats (in order)

1. **Biological motivation** -- why de novo peptide sequencing matters
2. **Problem statement** -- what makes it hard (no reference proteome, mass constraint)
3. **Prior work gap** -- what existing approaches miss (one paragraph max; detailed treatment in Related Work)
4. **This paper's approach** -- one sentence per contribution
5. **Two-block contribution list** -- explicit BIBM vs. journal separation (TCBB requirement)
6. **Paper organization** -- one sentence

---

## Draft

### Opening (biological motivation)

Tandem mass spectrometry (MS/MS) is the primary tool for large-scale protein identification, but conventional database search methods require a reference proteome -- a complete catalog of all proteins expected in the sample. This requirement fails precisely where it matters most: metaproteomics of mixed microbial communities, clinical samples from immunocompromised patients, and environmental samples from novel ecosystems where no reference is available [CITE]. De novo peptide sequencing addresses this limitation by reconstructing peptide sequences directly from fragment ion spectra, without any database assumption.

The core challenge is combinatorial: even short peptides of 10-20 residues have 20^10 - 20^20 possible sequences. The mass spectrometer constrains this space by measuring the precursor ion mass (MS1), which bounds the total peptide mass within ~50 ppm, and by recording the fragment ion series (MS2), which provides partial sequence ladder information. Existing deep learning approaches model this as a sequence generation problem conditioned on the spectrum [CITE DeepNovo, Casanovo, PointNovo, InstaNovo], but all enforce the precursor mass constraint only at inference -- as a post-hoc filter over beam search candidates. This hard, non-differentiable filter cannot propagate mass feasibility back into the model during training, leaving the learned distribution systematically biased toward mass-infeasible sequences that must be pruned at test time.

### Gap and approach

In our prior work [BIBM 2026 cite], we introduced self-conditioned absorbing multinomial diffusion for de novo sequencing, achieving **X.X pp** higher peptide accuracy than InstaNovo [cite] on the E. coli EV benchmark. However, all three inference-time mass enforcement strategies we evaluated degraded accuracy, confirming that post-hoc mass correction is not the right abstraction. This work resolves that open problem by moving mass enforcement into training.

We present three new contributions:

### Two-block contribution list (TCBB extension disclosure)

**In our prior conference paper [BIBM 2026 cite], we contributed:**
(i) An absorbing multinomial diffusion model for discrete amino acid sequences, with a physics-informed PeakEncoder incorporating B/Y-ion pair bias.
(ii) A self-conditioning architecture (preview-refine loop) adapted from [Chen 2022] that improves peptide accuracy by +14.6 pp.
(iii) Evaluation on E. coli EV proteomics (472 spectra at 5% FDR).

**The present journal paper additionally contributes:**
(i) **Mass-constrained training loss.** An auxiliary term L_mass = E_t[(M_pred(x̂_0) - M_target)^2 / M_target^2] that makes mass feasibility differentiable through the soft argmax, with an annealing schedule that allows the model to acquire sequence structure before tightening the constraint. (Section 4.3)
(ii) **NovoBench cross-species generalization study.** Full evaluation on all 9 NovoBench species [cite], including out-of-distribution testing (train on E. coli, evaluate across species) and cross-instrument (HCD vs. CID) analysis. Led by Sanika Najan. (Sections 4.4, 6.2-6.5)
(iii) **Information-theoretic analysis of self-conditioning.** We prove that iterative self-conditioning approximately performs mutual information maximization between the partially-denoised sequence and the spectrum, subject to a divergence constraint. We validate this claim empirically with a MINE-based MI estimator, showing that MI at diffusion timestep t predicts self-conditioning gain at that timestep (Pearson r = **X.XX**). (Section 4.1, 6.3)

### Paper organization

Section 2 reviews related work. Section 3 states the problem formally. Section 4 presents the theoretical framework, model, mass-constrained loss, and experimental setup. Section 5 describes experiments. Section 6 reports results. Section 7 discusses implications and limitations. Section 8 concludes.

---

## Revision notes

- All bolded **X.X** values are placeholders; fill from results.
- The two-block contribution list is a TCBB requirement for conference extensions -- do not remove or collapse it.
- Keep each paragraph tight. Introduction should not exceed 1 page in double-column format.
- The decoding strategy from the BIBM paper is reused as-is and cited; it is not a contribution of this paper.
