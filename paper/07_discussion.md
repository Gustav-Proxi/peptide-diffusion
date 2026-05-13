# Discussion [DRAFT]

**Owner:** Joint (Vaishak drafts first; Sanika adds cross-species analysis commentary)
**Target length:** ~1 page (double-column IEEEtran)
**Status:** `[HOLD]` -- write after results are in

---

## Structure

TCBB discussion sections are expected to do three things, in order:
1. Interpret the main findings (what do the numbers mean biologically/methodologically?)
2. Identify and explain failure modes (honest reporting -- reviewers reward this)
3. State limitations and future work

---

## Planned content

### What the mass constraint accomplishes

The key insight from the mass-constrained training results is not just the accuracy improvement -- it is that mass feasibility can be *learned*, not filtered. The original paper's negative result (inference-time mass correction hurts accuracy) is explained by the fundamental limitation of hard constraints over discrete candidates: they cannot propagate gradient signal back to the model. By incorporating L_mass at training time, the model learns to produce mass-feasible *distributions*, not just mass-feasible *samples*. This distinction is the same as the difference between constrained beam search and constrained training in seq2seq: the latter is strictly more powerful because it shapes the learned prior.

*Vaishak: add 2-3 sentences connecting to the analogy with scheduled sampling in seq2seq. Cite if needed.*

### What the cross-species results show (Sanika contributes)

*Fill in after NovoBench results:*

If our model generalizes well: the B/Y-ion pair bias in the PeakEncoder may be capturing a physics-grounded fragmentation pattern that is *species-independent* (fragment ion physics does not change across organisms). This would explain why a model trained on 472 E. coli spectra transfers non-trivially to [X] other species.

If generalization is limited: the failure mode is likely species-specific PTMs (different modification profiles) or instrument differences (HCD vs CID produce different ion series ratios). This is an honest limitation to state explicitly.

*In either case, framing: "We report our results honestly. Gains on non-E. coli species are [larger/smaller] than on E. coli EV. The largest contributors to the gap are [instrument type / PTM profile / taxonomic distance]. These are solvable with multi-species training, which we leave for future work."*

### What the MI correlation means

*Fill in after MI experiments:*

If r > 0.7: "Self-conditioning improves accuracy most at the diffusion timesteps where the conditional MI between sequence and spectrum is highest -- i.e., where the spectrum provides the most information about the clean sequence that is not already captured by the noisy sequence alone. This empirical finding is consistent with our theoretical analysis (Section 4.1) and provides the first MI-based explanation for the effectiveness of self-conditioning in discrete diffusion."

If r < 0.7: Use backup framing. "The correlation between MI and accuracy gain is positive (r = [X]) but not tight. A more conservative framing: self-conditioning acts as a score-refinement step that refines the initial denoised estimate toward the manifold of protein-like sequences, with the spectrum providing a guiding gradient. We present this as a hypothesis for future theoretical work."

### Failure modes (error analysis -- TCBB addition, required)

*Sanika: after NovoBench results, identify the 2-3 most common failure modes in cross-species eval and report them explicitly. Examples:*
- Charge state confusion (high-charge spectra are harder to decode)
- PTM misattribution (oxidized-M vs deamidated-N confusion)
- Long peptide degradation (>20 residues, absorbing schedule runs out of capacity)

*Vaishak: identify failure modes in MI correlation experiment.*

### Limitations

1. **Single-species training:** Our model is trained only on E. coli EV proteomics (472 spectra). InstaNovo and Casanovo use multi-species training. The out-of-distribution evaluation (Section 6.5) quantifies the cost of this limitation; multi-species training is the natural extension.

2. **MI estimator variance:** MINE and InfoNCE are known to have high variance on small datasets. The MI correlation analysis uses [N] spectra; a larger held-out set would give tighter confidence intervals.

3. **Theory assumptions:** The formal claim in Section 4.1 holds under [state assumptions clearly -- e.g., Gaussian approximation of the posterior, or mild conditions on the absorbing schedule]. Tightening the assumptions is future theoretical work.

### Future work

- Multi-species training with mass-constrained loss (expected to improve generalization)
- Adaptive lambda schedule (anneal based on MI signal at each timestep, not fixed)
- Extension to post-translational modifications beyond carbamidomethyl-C and oxidized-M
- Formal proof of the MI claim under non-Gaussian posteriors
