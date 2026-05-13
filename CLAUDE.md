# CLAUDE.md — Peptide Diffusion Paper Hardening

**Repo:** https://github.com/AkshayRevankarDev/peptide-diffusion
**Goal:** Take the existing CSE 676 report from "good results, untrustworthy comparison" to "IEEE BIBM 2026 submittable."
**Owner:** Vaishak (writing lead, methods). Coordinate with Akshay (decoding, wastewater) and Sanika (preprocessing, figures).

---

## Why we're doing this

The current report claims +26.9 pp peptide accuracy over InstaNovo (72.9 / 33.1 → 76.0 / 60.0). The number is real, but it compares **your model on your 472-spectrum test split** against **InstaNovo's published Nature MI numbers on a different test set**. No IEEE reviewer will accept that. Three fixes turn this into a paper.

---

## Fix 1 — Re-run InstaNovo on our test split (CRITICAL)

This is the single load-bearing change. Without it, the headline is unrecoverable in review.

**Steps:**
1. Clone InstaNovo from https://github.com/instadeepai/InstaNovo. Pin the commit used in Eloff et al. 2025.
2. Download their published checkpoint (multi-species training, no fine-tuning).
3. Build an inference adapter that takes our 472-spectrum E. coli EV test split (same mzML files, same preprocessing, same charge state filtering, same fixed/variable PTMs) and runs InstaNovo on it.
4. Apply our same FDR pipeline (5% via q-value thresholding) on their confidence scores. Use the same q-value computation code we use for our model. This is non-negotiable for a fair comparison.
5. Report AA recall and peptide accuracy. Save raw predictions to `eval/instanovo_472_split.csv`.

**Expected outcome:** Gap shrinks. If it shrinks from +26.9 pp to +10-15 pp, that's still a strong paper. If it disappears, we know the gap was a test-set artifact and we have a different paper to write (ablation of self-conditioning as a general absorbing-diffusion technique).

**Time budget:** 3-4 hours including debugging.

---

## Fix 2 — NovoBench cross-species evaluation

472 spectra is too small for a full conference paper. NovoBench (Zhou et al. NeurIPS 2024) is the standard.

**Steps:**
1. Download NovoBench from https://github.com/jingbo02/NovoBench-2. They provide 9-species splits.
2. Run our V2 model (CFID+SGIR) on each species split. Use existing inference code; no retraining.
3. Report AA recall and peptide accuracy per species.
4. Add as Table 5 in the paper. Expected: gain may shrink on species with very different fragmentation patterns (HCD vs CID). Be honest about it.
5. If our gain holds on ≥5 of 9 species, that's the cleanest possible story.

**Time budget:** 2-3 hours, mostly data loading.

---

## Fix 3 — BLAST wastewater peptides

Limitations section flags this. ~1 hour, big credibility return.

**Steps:**
1. Take the 6 sequences from Table 4 of the report.
2. Run NCBI BLASTp against the `nr` database (or `env_nr` for environmental samples). Use the web interface or `Bio.Blast.NCBIWWW` if scripted.
3. For each peptide, record top hit organism + identity %. Add as Table 5 (or Appendix).
4. If any peptide has high-identity match to a known organism, that's actual evidence we recovered real protein sequence without a reference proteome — the headline of the wastewater section.

**Time budget:** 1 hour if scripted, 30 min if done by hand on the BLAST web UI.

---

## Stretch (only if Fix 1-3 finish early)

### Mass constraints in training (genuine new contribution for the journal extension)

The report's "future work" line. Implement as auxiliary loss:
```
L_mass = λ * (predicted_mass - target_mass)^2
```
where `predicted_mass` is computed from the argmax sequence at the final diffusion step. Start with λ = 0.01.

If this gives even +1 pp at training time, it becomes the headline addition for an IEEE/ACM TCBB journal extension. Don't try this tonight if Fix 1-3 aren't done.

---

## Coordination

- **Vaishak:** Drives Fix 1 (InstaNovo rerun) — methods-side, you wrote the diffusion backbone, you know the eval harness.
- **Akshay:** Drives Fix 3 (BLAST) — you own the wastewater pipeline. Run it locally or via NCBI web BLAST.
- **Sanika:** Drives Fix 2 (NovoBench) — you own preprocessing, so cross-species data wrangling is your lane. Also: figures will need rebuilding to include InstaNovo-on-our-split.

Sync via Discord/WhatsApp every 4 hours tonight. Don't run InstaNovo and NovoBench evaluation on the same GPU at the same time; sequence them.

---

## Definition of done (for this hardening pass)

- [ ] InstaNovo numbers on our 472-spectrum split logged
- [ ] NovoBench results table generated
- [ ] BLAST table generated
- [ ] Report Section 5 + 6 updated with all three
- [ ] Figure 2a regenerated with InstaNovo-on-our-split bar (not published number)
- [ ] Abstract gap claim revised to reflect re-run number
- [ ] Limitations section trimmed to remove items now resolved

---

## What NOT to do tonight

- Don't rewrite the paper structure. The current report is well-organized.
- Don't add new model contributions. Three (PeakEncoder bias, self-conditioning, CFID+SGIR) is enough.
- Don't run new training. All three fixes are inference-only.
- Don't pull a third all-nighter to chase Fix 4+. Stretch goal is journal extension, not BIBM.

---

## After tonight

Once Fix 1-3 are merged: email Mingchen with the updated report attached and ask about IEEE submission + co-authorship. Email draft is in the project plan doc.
