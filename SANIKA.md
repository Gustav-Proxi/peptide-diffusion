# Sanika — Task List for 2 PhD Papers

**You:** Sanika Vilas Nanjan  
**Co-author:** Vaishak Girish Kumar  
**Goal:** IEEE BIBM 2026 (conference) → IEEE/ACM TCBB (journal extension)  
**Last updated:** 2026-05-13

---

## STATUS SNAPSHOT

| Paper | Status | Next action |
|---|---|---|
| Paper 1 — BIBM 2026 | 🟡 Your BLAST task is blocking | Run BLAST queries (this week) |
| Paper 2 — TCBB 2027 | ⬜ Not started | Begins September 2026 |

---

## PAPER 1: IEEE BIBM 2026

**Your two tasks this week — both are blockers for submission.**

---

### TASK S1 — Run actual BLAST queries for the 6 wastewater peptides ⚠️ BLOCKING
**Estimated time:** 1–2 hours  
**File:** `eval/run_blast.py` already exists  
**Result goes in:** wastewater validation table in the paper

The current `eval/blast_results.csv` has all "NO HIT" with e_value=999 — these are placeholder sentinels, not real results. The BLAST queries need to actually run against NCBI.

**Run it:**
```bash
cd peptide-diffusion
python eval/run_blast.py
```

The script queries NCBI BLASTp for each of the 6 sequences. It caches results in `eval/blast_cache/` so you don't re-query if you re-run. Each query takes ~30–90 seconds (NCBI rate-limits web queries). Total: ~10 minutes.

**6 sequences to BLAST:**
```
FNDVIPMGEQAINTNEGAYR
NNGNAIGVDLAAIPFVAGDR
GSNYNEVVTLADVTIVQGIR
DLDVEFTALDGASVQVIAYR
ALDNAIDGGQYSFLEVAINR
QLDNNCVYLGATAGVPIAK
```

**What to look for in results:**
- If you get **hits with high identity (>70%)** to known organisms: this confirms you recovered real protein sequences from wastewater with no reference proteome. That's the headline for the wastewater section.
- If you get **hits with low identity (<40%)**: your sequences are divergent homologs — mention as novel but related.
- If you get **no hits**: genuinely novel sequences. Frame it as "de novo recovery of sequences absent from current reference databases" — this is actually the strongest outcome for the paper's narrative.

**After running:**  
Open `eval/blast_results.csv`. Copy the results into Table 4 in the report (wastewater section). Format: `Sequence | Top Hit Organism | Identity % | E-value`.

If the script errors on NCBI connection, you can run them manually at https://blast.ncbi.nlm.nih.gov/Blast.cgi (protein blast, nr database) and paste results into the CSV manually — same format.

---

### TASK S2 — IEEEtran formatting pass (your sections)
**Estimated time:** 2–3 hours  
**After Vaishak completes V3 (IEEEtran conversion)**

Vaishak converts the full document to IEEEtran. Your job: review and fix your sections:
- **Section 3 (Related Work):** your section — verify it compiles, no NeurIPS formatting artifacts
- **Table 4 (wastewater BLAST):** add the real BLAST results from S1
- **Figure 4 (ESM-2 PPL plot):** confirm the figure still renders correctly in double-column
- **Preprocessing description:** verify `src/preprocessing.py` details in §3.2 are accurate

**Compile check:**
```bash
cd report && pdflatex bibm_paper.tex
```

Fix any errors in your sections before handing back to Vaishak for final compile.

---

### TASK S3 — Review the updated abstract (10 min)
After Vaishak gets real InstaNovo numbers and updates the abstract:
- Read the new abstract
- Check that your contributions (preprocessing, FDR filtering, wastewater quality assessment, figures) are accurately described
- Flag any missing credit — speak up now, not after submission

---

## PAPER 1 CHECKLIST (Sanika side)

- [ ] S1: Run BLAST on 6 wastewater peptides → fill Table 4  
- [ ] S2: Review your IEEEtran sections — no formatting errors  
- [ ] S3: Review updated abstract  
- [ ] *(coordinate)* Confirm Vaishak's InstaNovo fix is in before final compile  
- [ ] Final read-through of your sections in compiled PDF  

---

## PAPER 2: TCBB Journal Extension

**Start date: September 2026** (after BIBM submission)  
**You lead Contribution 2 (NovoBench) — the largest single experiment in the journal paper.**

---

### TASK S-J1 — NovoBench data download and preprocessing (September 2026)

**What NovoBench is:** A standardized 9-species benchmark for de novo peptide sequencing from Zhou et al. NeurIPS 2024. Each species has standardized test splits so results are comparable across papers.

**9 species:**
```
human, mouse, yeast, arabidopsis, bacillus,
celegans, drosophila, ecoli, rice
```

**Where to get it:** https://github.com/jingbo02/NovoBench-2 (also on HuggingFace as `jingbo02/NovoBench` or `InstaDeep/novobench-2`)

**Your job:**
1. Download all 9 species test splits (mzML or parquet format)
2. Write `src/novobench_preprocess.py` — same pipeline as `src/preprocessing.py`:
   - Same PTMs: carbamidomethyl-C (fixed), oxidized-M (variable), deamidated-N/Q (variable)
   - Same charge filter: 2–4
   - Same peak limit: top 800 peaks per spectrum
   - Same FDR: 5% q-value threshold
   - **Use their standardized test splits** — do NOT re-split with your own rng
3. Check if the mzML files have HCD/CID instrument metadata in the `<instrumentConfiguration>` fields — log this per species in a CSV

**Save preprocessed data to:** `data/novobench/{species}_test.pkl` (using pickle to preserve arrays)

**Check your work:** Run `python src/novobench_preprocess.py --species ecoli` and verify the E. coli split gives similar numbers to your 472-spectrum split.

---

### TASK S-J2 — Run base model on all 9 NovoBench species (October 2026)

This is inference-only — no new training. Use the existing V2 checkpoints.

```bash
python eval/run_novobench.py \
  --species human mouse yeast arabidopsis bacillus celegans drosophila ecoli rice \
  --checkpoint checkpoints/v2/seed_0/diffusion_final.pt
```

Repeat for seed_1 and seed_2. Take the 3-seed mean ± std.

**Save to:** `results/tcbb/novobench_base.csv`

**Expected outcome:** E. coli performance matches your 472-spectrum result (sanity check). Other species will vary — human/mouse likely best (HCD fragmentation), bacterial species may be weaker.

---

### TASK S-J3 — Run mass-constrained model on all 9 species (October–November 2026)

After Vaishak completes V-J1 (mass-constrained training), re-run NovoBench with the best-lambda checkpoint:

```bash
python eval/run_novobench.py \
  --species all \
  --checkpoint checkpoints/tcbb/lambda_0.01/seed_0/diffusion_final.pt
```

**Save to:** `results/tcbb/novobench_mass_constrained.csv`

**Compare:** For each species, report `base_pep_acc` vs `mass_constrained_pep_acc`. Any species where mass-constrained is better is evidence that the new training loss generalizes.

---

### TASK S-J4 — ESM-2 structural plausibility — multi-species (November 2026)

You already ran ESM-2 PPL for the E. coli split and wastewater — this extends that work to all 9 species.

```bash
python src/esm_scoring.py \
  --diffusion_csv results/tcbb/novobench_mass_constrained.csv \
  --out_csv results/tcbb/novobench_esm2.csv
```

For each species, compute:
- Mean ESM-2 pseudo-perplexity of predicted peptides
- Fraction flagged as anomalous (z-score > 2)

**Add to paper as:** Table 5 or Figure in §6.4 (multi-species PPL distributions)

---

### TASK S-J5 — Cross-instrument analysis: HCD vs CID (November 2026)

If the metadata from S-J1 shows HCD/CID labels for any species:
- Split NovoBench results by instrument type
- Report AA recall and pep acc separately for HCD vs CID spectra
- If HCD > CID: this explains the generalization gap and frames the paper's honest conclusion

If metadata is unavailable: note it as a limitation in the paper and move on.

---

### TASK S-J6 — Figure generation for all journal results (December 2026)

**Figures you own for the journal paper:**
1. **Figure 3:** Per-species NovoBench bar chart — AA recall + pep acc across 9 species, base vs mass-constrained
2. **Figure 4:** ESM-2 PPL distributions — one violin per species, wastewater overlay
3. **Figure 5 (if HCD/CID data available):** Cross-instrument gap visualization

Generate these with white backgrounds (slide-ready). Use `generate_figures.py` as the template.

**Save to:** `paper/figures/`

---

### TASK S-J7 — Write your paper sections (December 2026)

You own these sections in `paper/`:

| Section | File | Status |
|---|---|---|
| §3 Related Work | `paper/03_related_work.md` | Stub exists |
| §4.4 NovoBench Eval Setup | `paper/04_methods.md` §4.4 | Stub exists |
| §6.2 Cross-Species Results | `paper/06_results.md` §6.2 | Stub exists |
| §6.4 ESM-2 Multi-Species | `paper/06_results.md` §6.4 | Stub exists |
| §6.5 HCD/CID Analysis | `paper/06_results.md` §6.5 | Stub exists |

**Tone guidance for related work:**
- InstaNovo: acknowledge it's strong, point out it's evaluated only on HCD (cite Eloff et al. 2025)
- DeepNovo, PointNovo: briefly mention as prior work but they predate absorbing diffusion
- NovoBench (Zhou et al.): the benchmark you're using — cite generously, they enabled your cross-species study
- MINE/InfoNCE: cite when Vaishak's theory section cites them

---

## PAPER 2 TIMELINE (Sanika)

| Month | Task |
|---|---|
| Sep 2026 | Download NovoBench, write `novobench_preprocess.py`, verify E. coli sanity check |
| Oct | Run base V2 model on all 9 species (3 seeds). Analyze per-species results. |
| Oct–Nov | Run mass-constrained model (after Vaishak has best λ checkpoint) |
| Nov | ESM-2 multi-species study. HCD/CID analysis if metadata available. |
| Dec | Generate Figures 3–5. Write your sections. |
| Jan 2027 | Review Vaishak's methods/theory sections. Compile full draft together. |
| Feb 2027 | **Submit to TCBB** |

---

## KEY FILES (your ones)

| File | What it is |
|---|---|
| `eval/run_blast.py` | BLASTp script — run it this week (Paper 1) |
| `eval/blast_results.csv` | Will have real hits after you run the script |
| `src/preprocessing.py` | Your existing pipeline — template for NovoBench preprocess |
| `src/esm_scoring.py` | ESM-2 PPL script — reuse for multi-species |
| `eval/run_novobench.py` | NovoBench inference script — ready to run (Paper 2) |
| `paper/03_related_work.md` | Your section stub |
| `paper/04_methods.md` §4.4 | Your NovoBench eval setup stub |
| `paper/06_results.md` §6.2, 6.4, 6.5 | Your results stubs |
| `paper/figures/` | Save all your figures here |
| `checkpoints/v2/` | Trained base model — use for all NovoBench inference |

---

## KEY COORDINATION POINTS (sync with Vaishak)

| Event | When | What to sync |
|---|---|---|
| Vaishak gets real InstaNovo numbers | This week | You need to know final gap before reviewing abstract |
| Vaishak finishes IEEEtran conversion | This week | You start your formatting pass after this |
| Vaishak picks best λ checkpoint | October 2026 | You need checkpoint path to run S-J3 |
| First full draft | December 2026 | Block 2–3 days to read each other's full sections |
| TCBB submission | February 2027 | Both submit cover letter together |

---

## CONTACTS

- **Vaishak:** vaishakg@buffalo.edu / WhatsApp  
- **BIBM 2026:** Check deadline at https://ieeebibm.org  
- **NovoBench repo:** https://github.com/jingbo02/NovoBench-2  
- **BLAST web UI (fallback):** https://blast.ncbi.nlm.nih.gov/Blast.cgi

---

## YOUR AUTHORSHIP POSITION

On both papers you are **second author** (Vaishak is first author / writing lead). For PhD applications, second author on two publications in IEEE BIBM + IEEE/ACM TCBB is strong, especially if you can speak to what you specifically built. When asked: *"I led the NovoBench cross-species evaluation and multi-species structural plausibility analysis, and I built the preprocessing pipeline that both papers rely on."*
