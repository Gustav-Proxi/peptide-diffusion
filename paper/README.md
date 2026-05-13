# Paper: Mass-Constrained Self-Conditioned Multinomial Diffusion for De Novo Peptide Sequencing

**Full title:** Mass-Constrained Self-Conditioned Multinomial Diffusion for De Novo Peptide Sequencing: Theory and Cross-Species Generalization

**Authors:**
- **Vaishak Girish Kumar** (lead) — vaishakgkumar@gmail.com
- **Sanika Vilas Nanjan** (co-author) — snajan@buffalo.edu

**Target venue:** IEEE/ACM Transactions on Computational Biology and Bioinformatics (TCBB)
- Rolling submission, ~6 month review cycle
- Backup: IEEE J-BHI, Briefings in Bioinformatics, Nature Methods (short comm)

**Extends:** Kumar et al. "Self-Conditioned Multinomial Diffusion with Physics-Informed B/Y-Ion Encoding for De Novo Peptide Sequencing." IEEE BIBM 2026.

---

## How this folder is organized

| File | Purpose | Owner |
|---|---|---|
| [00_outline.md](00_outline.md) | Full paper structure, section lengths, section owners | Both |
| [01_abstract.md](01_abstract.md) | Abstract draft + revision log | Vaishak |
| [02_introduction.md](02_introduction.md) | Introduction + motivation | Vaishak |
| [03_related_work.md](03_related_work.md) | Related work survey | Both |
| [04_methods.md](04_methods.md) | Methods: mass-constrained loss + theory | Vaishak |
| [05_experiments.md](05_experiments.md) | Experimental setup, datasets, metrics | Sanika |
| [06_results.md](06_results.md) | Results tables and figure references | Both |
| [07_discussion.md](07_discussion.md) | Discussion, generalization analysis | Both |
| [08_conclusion.md](08_conclusion.md) | Conclusion + future work | Vaishak |
| [references.md](references.md) | Full reference list + reading queue | Both |
| [TASKS.md](TASKS.md) | Task board, deadlines, current status | Both |
| [NOTES.md](NOTES.md) | Shared working notes, decisions, blockers | Both |
| [figures/README.md](figures/README.md) | Figure specs, ownership, generation scripts | Sanika |

---

## The three new contributions (vs BIBM paper)

1. **Mass-constrained training loss** — L_mass auxiliary term moves mass enforcement from inference into training. Vaishak's lead. Primary empirical contribution.
2. **NovoBench cross-species evaluation** — 9-species generalization study. Sanika's lead. Establishes generalizability beyond E. coli.
3. **Information-theoretic analysis of self-conditioning** — formal claim that self-conditioning approximates iterative MI maximization. Joint theory work. Differentiates this as a TCBB paper.

**Novelty bar:** TCBB requires ~30% new content over the conference version. Three new contributions out of nine total content rows = ~35%.

---

## Collaboration workflow

- **Primary writing:** Each author drafts their owned sections directly in the `.md` files here.
- **Review cycle:** Drafts get a `[DRAFT]` tag in the section header. When ready for review, change to `[REVIEW]`. After revision, `[DONE]`.
- **Decisions:** Log any non-obvious decision in [NOTES.md](NOTES.md) with date and rationale.
- **Conflicts:** If you disagree with something in a section you don't own, add a `> [Sanika/Vaishak note: ...]` blockquote rather than editing directly. Discuss then resolve.
- **Final LaTeX:** Once all sections reach `[DONE]`, Vaishak converts to the TCBB LaTeX template.

---

## Do NOT do

- Do not reframe BIBM contributions (PeakEncoder, self-conditioning, prior decoding strategy) as contributions of this paper. Cite and use as baseline.
- Do not submit before the BIBM paper is accepted or on arXiv.
- Do not add any AI attribution anywhere.

---

## Submission timeline

| Date | Milestone | Who |
|---|---|---|
| May 2026 | Finish BIBM submission. No journal work yet. | Both |
| September 2026 | Start mass-constrained training runs. Sanika begins NovoBench prep. | Both |
| October 2026 | Training complete. NovoBench eval begins. | Both |
| November 2026 | MI experiments. Theory section drafting. | Both |
| December 2026 | First full draft. Reference as "in preparation" on PhD apps. | Both |
| Jan-Feb 2027 | Polish, internal review, submit to TCBB. | Both |
| Summer 2027 | First-round reviews back. Revision cycle. | Both |
| Late 2027 | Acceptance (if successful). Lands during PhD year 1. | -- |
