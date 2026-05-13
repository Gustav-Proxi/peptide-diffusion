# Shared Working Notes

**Format:** Date + author initial + note. Most recent at top.

---

## 2026-05-12 [V] Session 1 -- folder setup

Set up this paper folder based on CLAUDE1.md (journal extension plan) and CLAUDE.md (BIBM hardening plan). Key decisions made:

- **Target venue confirmed:** TCBB (IEEE/ACM Transactions on Computational Biology and Bioinformatics). Backup: J-BHI, Briefings in Bioinformatics.
- **Novelty bar:** 35% new content (3 out of 9 contribution rows are new). Adding full BLAST study pushes to 40%.
- **TCBB page limit:** 14 double-column pages (IEEEtran format). Supplementary material unlimited.
- **LaTeX class:** `\documentclass[journal]{IEEEtran}`. Use `cite` package (not natbib). Do not use `bibtex` styles from NeurIPS or ICML -- they are wrong format.
- **ScholarOne:** TCBB submits through ScholarOne Manuscripts. Upload main paper + cover letter + supplementary separately. Do not embed author names in figure filenames or PDF metadata.

**Three TCBB conference-extension disclosure mechanisms:**
1. Page 1 footnote (hardcoded by Vaishak in LaTeX at submission time)
2. Two-block contribution list in Introduction (see 02_introduction.md)
3. In-section "new to this paper" markers at start of Methods 4.2 and Results 6.1

---

## 2026-05-12 [V] Theory section framing

The theory claim is: "Self-conditioning is approximately performing iterative MI maximization between the partially-denoised sequence and the spectrum, subject to a divergence constraint."

Backup framing (if MI correlation < 0.7): "Self-conditioning as score refinement under a learned manifold prior." This is less elegant but defensible.

**Decision:** Do not invest heavily in writing the theory section until the MI correlation experiment is done (November 2026). Write the experimental scaffold first; theory text comes after we know if the claim holds.

---

## 2026-05-12 [V] Prior decoding strategy -- handling

The decoding strategy from the BIBM paper is reused as-is in this paper (same code, same hyperparameters). It is NOT a contribution of this paper -- just cite [BIBM 2026] in the Methods section where the decoder is described. Do not extend or modify it; changes would muddy the comparison.

---

## Open questions (unresolved -- resolve before submitting)

| # | Question | Status | Owner |
|---|---|---|---|
| Q1 | Does TCBB allow arXiv preprint before peer review? | Unresolved | Vaishak (check TCBB editorial policy) |
| Q3 | InfoNCE or MINE for MI estimation? | Unresolved | Vaishak (run pilot on E. coli split) |
| Q4 | Figure budget -- max 10 main figures. Plan by November. | Unresolved | Both |
| Q5 | Will UB cluster GPU time be available for training in Sept 2026? | Unresolved | Vaishak (check with advisor) |
| Q6 | Do NovoBench mzML files include instrument-type metadata (HCD vs CID)? | Unresolved | Sanika (check when data downloaded) |

---

## Notes on the relationship between BIBM and TCBB papers

The BIBM paper (Kumar et al. 2026) is the *foundation* -- it contributes the diffusion backbone, PeakEncoder, self-conditioning, and decoding strategy. The TCBB paper (Kumar, Nanjan -- this paper) builds on that foundation with:
- New training procedure (mass-constrained loss)
- New evaluation scope (9-species NovoBench + OOD)
- New theoretical analysis (MI interpretation of self-conditioning)

The BIBM contributions are reused and cited as prior work. They are not reclaimed as new contributions here.

---

## Template for adding a note

```
## YYYY-MM-DD [V/S] Topic

Note text here.
```
