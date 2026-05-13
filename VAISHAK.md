# Vaishak — Task List for 2 PhD Papers

**You:** Vaishak Girish Kumar  
**Co-author:** Sanika Vilas Nanjan  
**Goal:** IEEE BIBM 2026 (conference) → IEEE/ACM TCBB (journal extension)  
**Last updated:** 2026-05-13

---

## STATUS SNAPSHOT

| Paper | Status | Next action |
|---|---|---|
| Paper 1 — BIBM 2026 | 🟡 Blocked on 2 issues | Fix InstaNovo scoring (today) |
| Paper 2 — TCBB 2027 | ⬜ Not started | Begins September 2026 |

---

## PAPER 1: IEEE BIBM 2026

**Your blocking tasks (do these this week before Sanika starts her section work).**

---

### TASK V1 — Fix InstaNovo scoring bug ⚠️ BLOCKING
**Estimated time:** 30 minutes  
**File:** `eval/run_instanovo_direct.py` and `eval/instanovo_472_split.csv`

**The bug:**  
`instanovo_summary.json` shows `aa_recall=0.0, pep_acc=0.0`. The cause: `rs.decode(seq, reverse=True)` returns a Python **list** like `['G','F','E','T',...]`, which when passed to `_clean()` gets wiped because `_clean` strips `[...]` patterns (designed for PTM notation like `[UNIMOD:35]`). Fix: join the list to a string before cleaning.

**The fix — run this script:**
```bash
cd peptide-diffusion
python eval/fix_instanovo_scores.py
```

That script (write it in `eval/fix_instanovo_scores.py`):
```python
import pandas as pd, re, json, ast

df = pd.read_csv("eval/instanovo_472_split.csv")

def clean(seq):
    # Handle both list-repr strings ['G','F',...] and plain strings
    s = str(seq)
    try:
        parsed = ast.literal_eval(s)
        if isinstance(parsed, list):
            s = "".join(str(x) for x in parsed)
    except (ValueError, SyntaxError):
        pass
    s = re.sub(r"\[.*?\]|\(.*?\)", "", s)   # strip PTM annotations
    return re.sub(r"[^A-Z]", "", s.upper())

def aa_recall(pred, true):
    if not true: return 0.0
    return sum(p==t for p,t in zip(pred, true)) / max(len(true), 1)

df["true_clean"]  = df["true_sequence"].apply(clean)
df["pred_clean"]  = df["predicted_sequence"].apply(clean)
df["aa_recall"]   = df.apply(lambda r: aa_recall(r["pred_clean"], r["true_clean"]), axis=1)
df["pep_correct"] = (df["pred_clean"] == df["true_clean"]).astype(int)

aa  = df["aa_recall"].mean() * 100
pep = df["pep_correct"].mean() * 100
print(f"InstaNovo v1.2.0 on 472-spectrum E. coli EV test split")
print(f"  AA Recall : {aa:.2f}%")
print(f"  Pep Acc   : {pep:.2f}%")

df.to_csv("eval/instanovo_472_split.csv", index=False)
summary = {"model":"instanovo-v1.2.0","test_set":"ecoli_ev_472","n_spectra":len(df),
           "aa_recall_pct":round(aa,2),"pep_acc_pct":round(pep,2)}
with open("eval/instanovo_summary.json","w") as f: json.dump(summary,f,indent=2)
print("Saved.")
```

**After running:**
- Open `eval/instanovo_summary.json` — read the real numbers
- Update the abstract gap claim (expected: your model still wins, but by a smaller margin than +26.9 pp)
- Update Table 2 in the report with the re-run numbers

---

### TASK V2 — Regenerate Figure 2a with re-run numbers
**Estimated time:** 30 minutes  
**File:** `generate_figures.py`

After V1 is done, regenerate the main results figure so the InstaNovo bar shows your re-run number, not their published number. Add a note to the figure caption: "InstaNovo evaluated on our 472-spectrum test split (same preprocessing and FDR as our model)."

```bash
python generate_figures.py
```

Check `figures/` for updated output.

---

### TASK V3 — Convert report to IEEEtran format
**Estimated time:** half a day  
**Files:** `report/report.tex` → `report/bibm_paper.tex`

Steps:
1. Copy `report/report.tex` → `report/bibm_paper.tex`
2. Change document class: `\documentclass[conference]{IEEEtran}`
3. Remove NeurIPS-specific packages and `\usepackage{neurips_2026}`
4. IEEEtran handles two columns automatically — remove any manual column splitting
5. Move figure captions to below figures (IEEEtran requires this)
6. Target: 8-10 pages (BIBM limit is 10 pages for regular papers)
7. Add this to bibliography handling: `\bibliographystyle{IEEEtran}`

**Check:** `pdflatex report/bibm_paper.tex` compiles without errors.

---

### TASK V4 — Update abstract after getting real InstaNovo numbers
**Estimated time:** 15 minutes  
**File:** `report/bibm_paper.tex` (after V3)

Current abstract says "+26.9 pp peptide accuracy over InstaNovo." Replace with the actual re-run number. Framing if the gap narrows:

> "Our model achieves X% AA recall and Y% peptide accuracy on our E. coli EV test split at 5% FDR, compared to Z% AA / W% peptide accuracy for InstaNovo evaluated under identical conditions on the same split."

Do NOT try to defend the original +26.9 number. The re-run comparison is strictly stronger for reviewers.

---

### TASK V5 — Remove limitations caveat about cross-dataset comparison
**Estimated time:** 10 minutes  
**File:** `report/bibm_paper.tex` limitations section

The class report has a line about "Test set of 472 spectra is small; BLAST confirmation pending; InstaNovo comparison is cross-dataset." After V1 and Sanika's BLAST work:
- ✅ Remove "InstaNovo comparison is cross-dataset"  
- ✅ Remove "BLAST confirmation of the 6 wastewater peptides is pending"
- Keep the 472-spectra caveat (true) — address it in the TCBB paper with NovoBench

---

### TASK V6 — Email advisor
**Estimated time:** 15 minutes

Once you have real InstaNovo numbers and the paper is in IEEEtran format:

> Subject: BIBM 2026 submission — draft attached  
> Hi [Mingchen/advisor],  
> Sanika and I have cleaned up the CSE 676 project into a BIBM submission. Attaching the draft. Would you like to review it / be listed as co-author? BIBM 2026 deadline is [date]. Happy to discuss.

Confirm the author list before submitting. If advisor wants to be co-author, that's fine — add them after Sanika (3rd author, since they didn't do the core work).

---

## PAPER 1 CHECKLIST (Vaishak side)

- [ ] V1: Fix InstaNovo scoring → get real AA/pep numbers  
- [ ] V2: Regenerate Figure 2a  
- [ ] V3: Convert to IEEEtran format  
- [ ] V4: Update abstract with real gap number  
- [ ] V5: Remove resolved limitations caveats  
- [ ] V6: Email advisor with draft  
- [ ] *(coordinate)* Confirm Sanika's BLAST results are in (her task S1)  
- [ ] *(coordinate)* Review Sanika's IEEEtran formatting pass  
- [ ] Final compile: `pdflatex report/bibm_paper.tex` — no errors, correct page count  
- [ ] **Submit to BIBM 2026**

---

## PAPER 2: TCBB Journal Extension

**Start date: September 2026** (after BIBM submission)  
**Three contributions — you own two of them.**

---

### TASK V-J1 — Mass-constrained training loss (September–October 2026)

**The idea:** Mass enforcement at inference failed (see `devnotes.md` §6). The fix is to bake it into training as a differentiable auxiliary loss. This is your original idea from the class project — run with it.

**What already exists:**  
`src/diffusion.py` line ~568 has `MASS_LOSS_WEIGHT = 0.1` and a soft-argmax mass loss. Check if it's already doing the relative-squared form `(M_pred - M_target)² / M_target²`. If not, update the formula. What's **missing**: the annealing schedule and the λ sweep.

**What to add:**
```python
# In train_diffusion(), add lambda_mass argument and annealing schedule:
# anneal: lambda linearly from 0 to lambda_mass over first 50 epochs
# Sweep: lambda_mass in {0.001, 0.01, 0.1, 1.0} x 3 seeds = 12 runs
```

**How to run:**
```bash
python retrain_all.py --lambda_mass 0.01 --seed 0
python retrain_all.py --lambda_mass 0.01 --seed 1
python retrain_all.py --lambda_mass 0.01 --seed 2
# repeat for each lambda value
```

Save results to `results/tcbb/lambda_sweep.csv` with columns: `lambda, seed, AA Recall %, Pep Acc %, mass_violation_rate`.

**Success criterion:**
- Best lambda improves pep acc by ≥1 pp AND reduces mass violations by ≥50%
- If pep acc doesn't improve but mass violations drop, that's still publishable — frame around physical consistency

---

### TASK V-J2 — MINE/InfoNCE mutual information experiment (November 2026)

**The claim:** Self-conditioning performs iterative MI maximization between x_0 and spectrum S conditioned on x_t.

**The experiment:**
1. Implement MINE or InfoNCE estimator (`src/mi_estimator.py`)
2. At each diffusion timestep t (0..199), sample (x_t, S) pairs from the test set
3. Compute I(x_0; S | x_t) using the estimator
4. Separately measure: accuracy gain from self-conditioning at each t
5. Compute Pearson r between the two curves

**Decision gate:**
- r > 0.7 → theory section goes in main paper
- 0.5–0.7 → mention directional consistency with hedged language
- r < 0.5 → switch to "score refinement under learned prior" framing, MI analysis in supplementary

**Don't write the theory section until you see r.** Run the pilot on E. coli split first (fast), then on full NovoBench if pilot looks promising.

---

### TASK V-J3 — Theory section draft (November–December 2026)

After seeing r from V-J2:
- Write `paper/04_methods.md` §4.1 — the formal derivation
- LaTeX it into `report/tcbb_paper.tex`

Reading list (do this in August 2026, on a plane or weekend):
1. Austin et al. 2021 — absorbing diffusion KL bounds (you already cite this)
2. Chen et al. 2022 "Analog Bits" — self-conditioning, no formal analysis (cite as prior)
3. Belghazi et al. 2018 "MINE" — mutual information estimator you'll implement
4. Poole et al. 2019 — variational MI bounds

---

## PAPER 2 TIMELINE (Vaishak)

| Month | Task |
|---|---|
| Sep 2026 | Implement L_mass + annealing schedule in `src/diffusion.py` |
| Sep–Oct | Run λ sweep (12 training runs). Need GPU — book UB cluster time |
| Oct | Analyze lambda_sweep.csv — pick best λ, write methods section stub |
| Nov | Run MI estimator. Compute r. Make theory decision. |
| Nov–Dec | Write theory section (or backup framing) |
| Dec | Full paper first draft with Sanika |
| Jan 2027 | IEEEtran polish, internal review |
| Feb 2027 | **Submit to TCBB** |

---

## KEY FILES (your ones)

| File | What it is |
|---|---|
| `eval/run_instanovo_direct.py` | InstaNovo re-run script (has the bug to fix) |
| `eval/instanovo_472_split.csv` | Predictions — recompute scores with fix script |
| `eval/instanovo_summary.json` | Will have real numbers after fix |
| `src/diffusion.py:568` | Existing soft mass loss — extend for TCBB |
| `generate_figures.py` | Figure generation — regenerate Fig 2a after fix |
| `report/report.tex` | Current NeurIPS report — copy to `bibm_paper.tex` |
| `paper/04_methods.md` | TCBB methods stub — you fill §4.1, §4.2, §4.3 |
| `paper/TASKS.md` | Full task board (shared with Sanika) |

---

## CONTACTS

- **Sanika:** snajan@buffalo.edu / WhatsApp  
- **Advisor (if adding):** Confirm before submitting BIBM  
- **BIBM 2026:** Check submission deadline at https://ieeebibm.org — typically late June / early July
