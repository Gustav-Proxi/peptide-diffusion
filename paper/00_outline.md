# Paper Outline

**Target:** IEEE/ACM TCBB regular paper (journal extension)
**Page limit:** 14 double-column pages (IEEEtran format), including figures and references
**Supplementary allowed:** Yes -- use for lengthy derivations and full ablation tables

---

## Section structure (with owner and target length)

```
01 Abstract                          [Vaishak]    ~250 words (TCBB hard limit)
02 Introduction                      [Vaishak]    ~1 page
03 Background / Related Work         [Sanika]     ~1.5 pages
04 Methods                           [split]      ~3 pages total
   4.1 Theoretical Framework         [Vaishak]    ~1.5 pages
   4.2 Model Architecture            [Vaishak]    ~0.5 pages  (reuse/cite BIBM)
   4.3 Mass-Constrained Training     [Vaishak]    ~0.5 pages  (NEW)
   4.4 NovoBench Eval Setup          [Sanika]     ~0.5 pages  (NEW)
05 Experiments                       [Sanika]     ~1 page
   5.1 Datasets and Preprocessing
   5.2 Baselines and Metrics
   5.3 Implementation Details
06 Results                           [split]      ~3 pages
   6.1 Mass-constraint ablation      [Vaishak]    (Table 1, λ sweep)
   6.2 NovoBench per-species         [Sanika]     (Table 2, 9 species)
   6.3 MI correlation analysis       [Vaishak]    (Figure 3)
   6.4 Cross-instrument (HCD/CID)    [Sanika]     (Table 3)
   6.5 Out-of-distribution eval      [Sanika]     (Figure 4)
   6.6 ESM-2 structural plausibility [Sanika]     (Figure 5)
07 Discussion                        [joint]      ~1 page
08 Conclusion                        [Vaishak]    ~0.5 pages
09 Acknowledgments                   [joint]      ~0.25 pages
10 References                        [joint]      ~1.5 pages (~40 refs)
-- Appendix A: Loss derivation       [Vaishak]    supplementary
-- Appendix B: Full ablation tables  [Sanika]     supplementary
```

Total target: ~14 pages. Supplementary material: unlimited.

---

## TCBB conference-extension disclosure requirements

Three places where the BIBM paper must be cited and new contributions flagged:

### 1. Page 1 footnote (Vaishak handles in LaTeX)
```
A preliminary version of this work appeared as [BIBM citation].
The present paper extends that version with: (1) mass-constrained training loss,
(2) 9-species NovoBench cross-species evaluation, and
(3) information-theoretic analysis of self-conditioning.
```

### 2. Two-block contribution list in Introduction (see 02_introduction.md)

### 3. In-section "new to this paper" markers
- Start of Section 4.2: "Section 4.2 restates the model architecture from [BIBM]; Sections 4.1, 4.3, and 4.4 are new to this work."
- Start of Section 6: "The E. coli EV evaluation (Section 6.1) extends the conference results with the mass-constrained model. Sections 6.2-6.6 are new."

### 4. Cover letter diff table (Vaishak writes at submission time)
| Area | BIBM 2026 | TCBB (this paper) |
|---|---|---|
| Architecture | PeakEncoder + absorbing diffusion | Reused + cited |
| Training loss | VLB only | VLB + mass-constrained auxiliary (NEW) |
| Decoding | Beam search + reranking (prior work) | Same baseline, not extended |
| Evaluation dataset | E. coli EV (472 spectra) | E. coli EV + 9 NovoBench species (NEW) |
| Theory | None | MI maximization analysis (NEW) |
| Cross-species | None | Full 9-species OOD study (NEW) |

---

## Figure budget (TCBB typical max: 10 main figures)

| # | Figure | Owner | Status |
|---|---|---|---|
| 1 | Model architecture overview (reuse from BIBM with update) | Sanika | Adapt |
| 2 | Mass-constrained loss curve (λ = 0.01 best run) | Vaishak | New |
| 3 | Pareto frontier: AA recall vs Pep accuracy over λ sweep | Vaishak | New |
| 4 | NovoBench per-species bar chart (base vs mass-constrained) | Sanika | New |
| 5 | MI vs timestep + gain vs timestep correlation plot | Vaishak | New |
| 6 | OOD generalization: train E. coli, eval 9 species | Sanika | New |
| 7 | ESM-2 PPL multi-species comparison | Sanika | New |
| 8 | (Optional) HCD vs CID instrument breakdown | Sanika | New |

---

## Table budget

| # | Table | Owner |
|---|---|---|
| 1 | λ sweep ablation (AA recall + Pep acc at 5% FDR) | Vaishak |
| 2 | NovoBench 9-species results: base vs mass-constrained vs baselines | Sanika |
| 3 | Cross-instrument HCD/CID split | Sanika |
| 4 | Wastewater BLAST results (6 peptides, top hit + identity %) | Vaishak |
| 5 | Author contributions | Both |

---

## Status legend
- `[DRAFT]` -- being written, not ready for review
- `[REVIEW]` -- ready for the other author to read and comment
- `[DONE]` -- reviewed and settled; only minor edits allowed
- `[HOLD]` -- blocked on experiment/data; don't write yet
