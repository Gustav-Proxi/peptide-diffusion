# Related Work [DRAFT]

**Owner:** Sanika (first draft); Vaishak reviews
**Target length:** ~1.5 pages (double-column IEEEtran)
**Status:** `[DRAFT]` -- stub with required coverage areas; Sanika fills in

---

## Coverage areas (must address all five)

### 3.1 De novo peptide sequencing methods

*Cover the evolution from pre-deep-learning to current SOTA. End each paragraph with a gap statement pointing to what this paper addresses.*

**Pre-deep-learning baselines:**
- PepNovo [Frank & Pevzner 2005] -- scoring function over fragmentation patterns
- PEAKS DB [Zhang et al. 2012] -- hybrid de novo + database

**Deep learning methods:**
- DeepNovo [Tran et al. 2017] -- LSTM sequence model conditioned on spectrum features. First to frame de novo as seq2seq. Gap: no mass constraint in training.
- PointNovo [Qiao et al. 2021] -- set-based encoding (point cloud) of spectrum. Gap: autoregressive decoding, no self-conditioning.
- Casanovo [Yilmaz et al. 2022] -- transformer seq2seq. Strong baseline. Gap: mass constraint only at inference.
- InstaNovo [Eloff et al. 2024] -- transformer + discrete diffusion, trained on 9 species. SOTA. Gap: mass constraint at inference only; no theoretical analysis of self-conditioning.

**Our prior work:**
- Kumar et al. 2026 (BIBM) -- absorbing multinomial diffusion with self-conditioning. Reused here as baseline; this paper extends it.

### 3.2 Diffusion models for discrete sequences

*Cover discrete diffusion broadly, then narrow to amino acid sequences.*

- D3PM [Austin et al. 2021] -- structured absorbing diffusion in discrete state spaces. Foundation for our approach.
- Analog Bits [Chen et al. 2022] -- introduced self-conditioning. No formal analysis.
- MDLM [Sahoo et al. 2024] -- masked diffusion language model. Close to our setting; different application.
- EvoDiff [Alamdari et al. 2023] -- diffusion for protein sequence design. Different problem (unconditional protein generation vs. conditional peptide sequencing from spectra).

*Gap: None of these impose physically grounded mass constraints during training. This paper is the first to do so for the peptide sequencing task.*

### 3.3 Cross-species generalization in proteomics

*This is required because Contribution 2 is a cross-species study.*

- NovoBench [Zhou et al. NeurIPS 2024] -- benchmark with 9-species splits and standardized evaluation protocol. *This is the benchmark we use.*
- Multi-species training of InstaNovo [Eloff et al. 2024] -- trains jointly on 9 species. Evaluated on each held-out species.
- Cross-species transfer in protein structure prediction -- AlphaFold2 [Jumper et al. 2021] context: structure generalizes well; sequence-level tasks generalize less well.

*Gap: No prior de novo sequencing method has been evaluated specifically on the out-of-distribution case (train on single species, eval on all 9). This paper provides that study.*

### 3.4 Information-theoretic analysis of generative models

*Required to justify Contribution 3.*

- MINE [Belghazi et al. 2018] -- neural mutual information estimation via KL lower bound.
- InfoNCE [van den Oord et al. 2018] -- contrastive MI lower bound; lower variance than MINE.
- Poole et al. 2019 -- on variational bounds of MI; taxonomy of estimators.
- Self-conditioning as score refinement -- brief coverage of the implicit manifold prior interpretation (our backup framing if MI correlation is weak).

### 3.5 Mass constraint enforcement in peptide identification

*Must discuss the prior approaches we improve on.*

- Knapsack beam search [our BIBM paper] -- inference-time filter. Degraded accuracy. This is the negative result that motivates the training-time approach.
- PPM-based post-hoc filtering -- standard in database search pipelines. Not differentiable.
- Constrained decoding approaches from NLP -- e.g., NEUROLOGIC [Lu et al. 2021] -- constrained beam search. Analogous to our inference-time approach; same fundamental limitation.

---

## Draft notes (Sanika)

- Each subsection should be 2-3 paragraphs max. Related work is not a literature dump -- it is a gap analysis.
- End each subsection with a one-sentence gap statement that points forward to what this paper does.
- Cite papers by first author + year in the draft; Vaishak will format for IEEEtran at LaTeX stage.
- The BIBM paper (our prior work) must be cited here with a clear statement that this paper is its extension.
- If a cited paper is not in `references.md`, add it there when you add the citation here.

## Status tracking

- [ ] 3.1 De novo methods -- Sanika first draft
- [ ] 3.2 Discrete diffusion -- Sanika first draft
- [ ] 3.3 Cross-species generalization -- Sanika first draft
- [ ] 3.4 Information-theoretic analysis -- Vaishak first draft (theory-heavy)
- [ ] 3.5 Mass constraint enforcement -- Vaishak first draft
- [ ] Full review pass -- other author reviews after both draft
