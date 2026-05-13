# CLAUDE.md — Peptide Diffusion Journal Extension

**Working title:** *Mass-Constrained Self-Conditioned Multinomial Diffusion for De Novo Peptide Sequencing: Theory and Cross-Species Generalization*
**Authors:** Vaishak Girish Kumar, Sanika Vilas Nanjan
**Target venue:** IEEE/ACM Transactions on Computational Biology and Bioinformatics (TCBB) — rolling submission, ~6 month review cycle. Backup: IEEE Journal of Biomedical and Health Informatics (J-BHI), Briefings in Bioinformatics, or Nature Methods short communication.

**Relationship to prior work:** This paper extends the IEEE BIBM 2026 conference paper (Kumar, Revankar, Nanjan 2026) by adding three materially new contributions: (1) mass-constrained training loss, (2) cross-species generalization study, (3) information-theoretic analysis of self-conditioning. The original CFID+SGIR decoding strategy is referenced and reused but is not the contribution here.

---

## Why a journal extension and not another conference paper

Three reasons:

1. **It's how bio publishing works.** Conference paper → journal extension is the standard pattern in IEEE BIBM → TCBB, MICCAI → IEEE TMI, NeurIPS → Nature Methods. Reviewers expect it. Adcoms recognize it. Two papers off one research line is *good* CV signal, not duplicate work.

2. **It cleanly separates contributions.** The original paper covers what was built in CSE 676. This paper covers what you and Sanika built *after* the course ended, which is genuinely different work. Authorship reflects who did the new work — not a renegotiation of the old paper.

3. **It elevates the research narrative.** A conference paper says "we built a thing that works." A journal paper says "we built a thing that works, *and here's why it works, and here's where it generalizes.*" The second framing is what PhD adcoms read favorably.

---

## The three new contributions (in priority order)

### Contribution 1 — Mass-Constrained Training Loss (your idea, your build)

**The problem.** In the original paper, mass constraints were applied only at inference (knapsack-style filter on beam search candidates). All three inference-time mass enforcement strategies *degraded* accuracy. The original paper's discussion explicitly flags this as future work.

**The contribution.** Move the mass constraint into training. Specifically, add an auxiliary loss term:

```
L_total = L_VLB + λ_mass · L_mass
L_mass = E_t [(M_pred(x̂_0) − M_target)² / M_target²]
```

where `M_pred(x̂_0)` is the monoisotopic mass computed from the model's denoised sequence estimate at diffusion step *t*, and `M_target` is the measured precursor mass. The relative-squared form normalizes across peptide sizes.

**Why this works in training but not at inference.** Training-time mass constraint is differentiable through the soft argmax — the model learns to produce mass-feasible distributions internally. Inference-time constraint is a hard filter over discrete candidates and can't propagate gradients. This is the same reason scheduled sampling outperforms beam-search constraints in autoregressive seq2seq.

**Hyperparameter sweep.** λ_mass ∈ {0.001, 0.01, 0.1, 1.0}. Anneal schedule: linear from 0 to λ_mass over the first 50 epochs (lets the model learn sequence structure before tightening mass).

**Expected result.** Pep accuracy at 5% FDR improves by 2–5 pp. Mass-violation rate at decode drops by an order of magnitude. If both happen, this is the paper's load-bearing experimental contribution.

**Risk.** Could degrade AA recall if λ_mass dominates. Standard mitigation: report Pareto frontier (AA vs Pep) over the λ sweep.

---

### Contribution 2 — Cross-Species Generalization on NovoBench (Sanika lead)

**The problem.** Original paper evaluated only on E. coli EV proteomics (472 spectra). Reviewers will (correctly) ask: does this generalize beyond one prokaryote?

**The contribution.** Run the model — with and without the new mass-constrained training — on all 9 NovoBench species splits. Report per-species AA recall and peptide accuracy. Honest reporting: gains will likely shrink on species with different fragmentation patterns (HCD vs CID instruments). Frame around the **generalization gap analysis**, not just leaderboard numbers.

**Specific experiments.**
- All 9 NovoBench species, base model (BIBM paper) vs mass-constrained model (this paper).
- Per-species ESM-2 pseudo-perplexity (carries the structural plausibility analysis from BIBM, but now multi-species).
- Cross-instrument analysis: split results by HCD vs CID where metadata allows.
- Out-of-distribution test: train on E. coli only, evaluate on each NovoBench species. This is the strongest generalization signal.

**Sanika's lead.** She owns NovoBench data wrangling, preprocessing, and per-species figure generation. Methodologically she's already done this for the BIBM paper at smaller scale; this is the natural extension of her preprocessing work.

**Risk.** Performance drops on non-E. coli species. That's still a paper — just frame it as a generalization study with honest reporting. Reviewers reward honesty here; they punish overclaiming.

---

### Contribution 3 — Information-Theoretic Analysis of Self-Conditioning (joint, theory-heavy)

**The problem.** The BIBM paper shows self-conditioning gives +14.6 pp peptide accuracy and explains it by analogy to AlphaFold2 recycling. That's not a theoretical explanation — that's a hand-wave.

**The contribution.** Derive what self-conditioning actually does in the absorbing-diffusion setting. Specifically:

**Claim.** Self-conditioning is approximately performing **iterative mutual information maximization** between the partially-denoised sequence and the spectrum, subject to a divergence constraint that prevents collapse.

**Formal sketch.**
- Let `I(x_0; S | x_t)` be the conditional mutual information between the clean sequence and the spectrum given the partially-noised sequence.
- Standard absorbing diffusion estimates `p(x_0 | x_t, S)` directly.
- Self-conditioning estimates `p(x_0 | x_t, S, x̂_0^prev)`, where `x̂_0^prev` is a prior estimate.
- Show that under mild conditions, the iterative refinement step in self-conditioning is a one-step Newton-direction update on the mutual information objective.
- This gives a principled reason why self-conditioning helps more on tasks with high spectrum→sequence mutual information (peptides: clear b/y ladders) and helps less on tasks where the spectrum is noisy/incomplete.

**Experimental validation of the theory.**
- Compute `I(x_0; S | x_t)` empirically across diffusion timesteps using a variational MI estimator (MINE or InfoNCE).
- Show that self-conditioning's accuracy gain at timestep *t* correlates with MI at timestep *t*.
- If correlation > 0.7, the theory section earns its place in the paper.

**Reading list for the theory work.**
- Austin et al. 2021, "Structured Denoising Diffusion Models in Discrete State-Spaces" (your existing reference) — for the absorbing diffusion KL bounds.
- Chen et al. 2022, "Analog Bits" (your existing reference) — original self-conditioning paper, no formal analysis.
- Belghazi et al. 2018, "MINE: Mutual Information Neural Estimation."
- Poole et al. 2019, "On Variational Bounds of Mutual Information."
- Sohl-Dickstein et al. 2015, "Deep Unsupervised Learning using Nonequilibrium Thermodynamics" — for the variational lower bound machinery.

**Risk.** This is the highest-difficulty contribution. If the MI correlation is weak, the theory section becomes harder to defend. Have a backup framing: "self-conditioning as score refinement under a learned manifold prior." Less elegant but defensible.

**Why this matters for the paper.** A theory contribution is what differentiates a TCBB paper from a BIBM paper. TCBB reviewers expect either (a) significantly stronger empirical results, or (b) genuine theoretical insight. Path (a) is hard against well-funded teams. Path (b) is where two grad students with time can compete on equal footing.

---

## Contributions matrix (clean separation from BIBM paper)

| Contribution | BIBM 2026 paper | This journal paper |
|---|---|---|
| Absorbing multinomial diffusion backbone | Yes (V1) | Reused, cited |
| PeakEncoder with B/Y-ion pair bias | Yes | Reused, cited |
| Self-conditioning architecture | Yes | Reused, cited |
| CFID + SGIR decoding | Yes (Akshay's lead) | **Used as baseline only**; not a contribution of this paper |
| Wastewater cohort 1 (Sample 2) | Yes (Akshay's lead) | **Briefly cited**; not extended here |
| **Mass-constrained training loss** | No | **NEW — primary contribution** |
| **NovoBench cross-species evaluation** | No | **NEW — generalization study** |
| **Information-theoretic analysis of self-conditioning** | No | **NEW — theoretical contribution** |
| **(Optional) Fresh wastewater cohort with BLAST** | Pending in BIBM | **Extended with full BLAST + functional annotation** |

Three out of nine content rows in the journal paper are entirely new. That's ~35% new content, comfortably above the 30% bar TCBB-class journals use to distinguish "extension" from "duplicate submission." If you add the fresh wastewater cohort as a fourth new contribution, it's 40%+.

**The CFID+SGIR work stays attributed to Akshay in the BIBM paper, where it belongs. This paper just uses his published decoder as a baseline and cites it normally.**

---

## Author contributions (write this in the paper, draft now)

> **Vaishak Girish Kumar:** Conceived the mass-constrained training framework. Implemented the auxiliary loss and conducted all training experiments. Developed the information-theoretic analysis and conducted the mutual-information experiments. Writing lead.
>
> **Sanika Vilas Nanjan:** Conducted the NovoBench cross-species evaluation, including data preprocessing for all 9 species splits and per-species result analysis. Conducted the ESM-2 multi-species structural plausibility study. Generated all figures. Co-authored the methods and results sections.
>
> **Acknowledgments.** We thank Akshay Mohan Revankar for the CFID+SGIR decoding strategy and wastewater pipeline used as baseline in this study (Kumar, Revankar, Nanjan, IEEE BIBM 2026).

That acknowledgments line is genuinely correct, isn't slighting him, and accurately reflects what this paper builds on. No ambiguity, no quiet removal — just an honest contribution boundary.

---

## Submission timeline

Assumes BIBM 2026 submission lands in late August 2026.

| Date | Milestone |
|---|---|
| **May 2026 (now)** | Finish BIBM submission. Don't start journal work until BIBM is submitted. |
| **September 2026** | Start mass-constrained training experiments. Sanika begins NovoBench data prep in parallel. |
| **October 2026** | Mass-constraint loss training runs complete. NovoBench evaluation begins. |
| **November 2026** | Mutual information experiments. Theory section drafting. |
| **December 2026** | First full draft. PhD applications submitted in parallel — this paper is referenced as "in preparation" or "under review" depending on submission timing. |
| **January–February 2027** | Polish, internal review, submission to TCBB. |
| **Summer 2027** | First-round reviews back. Revision cycle. |
| **Late 2027** | Acceptance (if successful). Lands during PhD year 1. |

**Critical timing note.** This paper won't be accepted before PhD app deadlines. But "submitted to IEEE/ACM TCBB" on your CV in December 2026 *is* valuable signal — especially when paired with an accepted BIBM paper.

---

## Things to do tonight (and tonight only)

You're on a second all-nighter. Don't start journal work tonight. Tonight is for BIBM hardening (the other CLAUDE.md).

But before you sleep, write down:
1. Three sentences on the mass-constrained loss formulation (so you don't forget the framing).
2. The list of 9 NovoBench species, so Sanika can start downloading them next week.
3. The MINE/InfoNCE reading queue for the theory section.

That's it. Sleep after.

---

## What NOT to do

- Do NOT submit the journal extension before the BIBM paper is accepted or at minimum on arXiv. Reviewers at TCBB will check.
- Do NOT reframe the original BIBM contributions as if they were yours alone. The acknowledgments line above is the correct frame. Stick to it.
- Do NOT add Akshay to this paper as a courtesy if he didn't do the new work. False inflation is its own integrity issue.
- Do NOT add Mingchen to this paper unless he genuinely contributes to the new work. The BIBM paper acknowledgment is enough institutional connection.
- Do NOT try to repurpose CFID+SGIR results as if they were generated for this paper. Use them as a cited baseline and recompute them with the new mass-constrained model for fair comparison.

---

## What this gets you

When PhD adcoms read your CV in December 2026:

- **IEEE BIBM 2026 (accepted/in review):** Kumar, Revankar, Nanjan — "Self-Conditioned Multinomial Diffusion with Physics-Informed B/Y-Ion Encoding for De Novo Peptide Sequencing."
- **IEEE/ACM TCBB 2027 (submitted):** Kumar, Nanjan — "Mass-Constrained Self-Conditioned Multinomial Diffusion for De Novo Peptide Sequencing: Theory and Cross-Species Generalization."
- **MICCAI 2026 Workshop:** Kumar, Nanjan — [ReXGroundingCT pipeline paper, separate research line].

Three papers, two of them clean Vaishak+Sanika, one of them a three-author paper where you're writing lead. That's a strong narrative. No integrity asterisks attached. No quiet removals. Just legitimate, additive work that you and Sanika did together after the course ended.

That's the version of this that gets you both into the PhD programs you want.
