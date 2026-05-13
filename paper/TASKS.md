# Task Board

Last updated: 2026-05-12

---

## Active (September 2026 sprint)

| # | Task | Owner | Status | Deadline |
|---|---|---|---|---|
| T1 | Implement mass-constrained training loss (L_mass, λ sweep) | Vaishak | Not started | Oct 2026 |
| T2 | NovoBench dataset download + preprocessing for all 9 species | Sanika | Not started | Oct 2026 |
| T3 | MINE/InfoNCE MI estimator implementation | Vaishak | Not started | Nov 2026 |
| T4 | Run base model on all 9 NovoBench species (no retraining) | Sanika | Not started | Oct 2026 |
| T5 | Run mass-constrained model on all 9 NovoBench species | Sanika | Not started | Oct 2026 |
| T6 | ESM-2 pseudo-perplexity multi-species study | Sanika | Not started | Nov 2026 |
| T7 | Cross-instrument analysis (HCD vs CID split) | Sanika | Not started | Nov 2026 |
| T8 | Out-of-distribution test: train E. coli, eval all NovoBench | Both | Not started | Nov 2026 |
| T9 | Theory section draft: self-conditioning as MI maximization | Vaishak | Not started | Nov 2026 |
| T10 | MI correlation experiment (gain at timestep t vs MI at t) | Vaishak | Not started | Nov 2026 |
| T12 | Full paper first draft | Both | Not started | Dec 2026 |
| T13 | Internal review pass (each reads the other's sections) | Both | Not started | Jan 2027 |
| T14 | TCBB LaTeX conversion + formatting | Vaishak | Not started | Jan 2027 |
| T15 | Submit to TCBB | Vaishak | Not started | Feb 2027 |

---

## Blocked

| # | Task | Blocked by | Note |
|---|---|---|---|
| T1-T15 | All journal work | BIBM submission | Do not start until BIBM is submitted (May 2026) |

---

## Completed

| # | Task | Completed | Note |
|---|---|---|---|
| -- | BIBM paper (CP2) | 2026-05-01 | Beats InstaNovo on both metrics. Report at `report/report.pdf` -- this is the foundation this paper extends |

---

## Writing assignments

### Vaishak (lead)
- Abstract (final version)
- Introduction
- Methods 4.1: Mass-constrained training loss formulation
- Methods 4.2: Information-theoretic analysis of self-conditioning
- Methods 4.3: MI estimation procedure (MINE/InfoNCE)
- Results 6.1: Mass-constraint ablation (λ sweep)
- Results 6.3: MI correlation analysis
- Discussion (first draft)
- Conclusion
- TCBB LaTeX conversion

### Sanika (co-author)
- Methods 4.4: NovoBench dataset description + preprocessing
- Results 6.2: NovoBench per-species results (Table 2)
- Results 6.4: Cross-instrument analysis
- Results 6.5: Out-of-distribution generalization
- Results 6.6: ESM-2 multi-species structural plausibility
- All figures (generation + captions)
- Related work (first draft, Vaishak reviews)

### Joint
- Author contributions statement
- Acknowledgments
- Reference list curation
- Final proofreading

---

## Hyperparameter decisions (log here, don't bury in NOTES)

| Parameter | Value | Rationale |
|---|---|---|
| λ_mass sweep | {0.001, 0.01, 0.1, 1.0} | Log-spaced decade sweep; covers 3 orders of magnitude |
| λ_mass anneal | Linear 0 → λ over first 50 epochs | Lets model learn sequence structure before tightening mass |
| MI estimator | MINE or InfoNCE (TBD) | InfoNCE is lower-variance; MINE is tighter bound. Try both. |
| NovoBench splits | All 9 species | Full benchmark; no cherry-picking |
| FDR threshold | 5% | Consistent with BIBM paper |

---

## Open questions (resolve before submitting)

- [ ] Does TCBB allow preprint arXiv posting before peer review? Check editorial policy.
- [ ] InfoNCE vs MINE for MI estimation -- run pilot on E. coli split to decide.
- [ ] Theory section: if MI correlation < 0.7, use backup framing ("self-conditioning as score refinement under learned manifold prior"). Decide by Nov 2026.
- [ ] Figure count: TCBB typical max is 10 main figures. Plan budget early.
