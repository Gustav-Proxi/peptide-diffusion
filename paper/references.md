# References

**Owner:** Both (add citations as you write; Vaishak formats for IEEEtran at LaTeX stage)
**Format:** Add in rough APA here; convert to IEEEtran BibTeX at submission

---

## Must-cite (paper cannot be submitted without these)

### Prior work (ours)
- [BIBM2026] Kumar, V.G., Nanjan, S.V., et al. "Self-Conditioned Multinomial Diffusion with Physics-Informed B/Y-Ion Encoding for De Novo Peptide Sequencing." *IEEE BIBM 2026.* (**Must appear on page 1 footnote + Introduction + Related Work**)

### De novo sequencing baselines
- [DeepNovo] Tran, N.H., Zhang, X., Xin, L., Shan, B., Li, M. "De novo peptide sequencing by deep learning." *PNAS*, 2017.
- [Casanovo] Yilmaz, M., Fondrie, W.E., Bittremieux, W., Oh, S., Noble, W.S. "De novo mass spectrometry peptide sequencing with a transformer model." *ICML*, 2022.
- [PointNovo] Qiao, R., Tran, N.H., Xin, L., Shan, B., Li, M., Berendsen, R., & Ma, B. "Computationally instrument-resolution-independent de novo peptide sequencing for high-resolution devices." *Nature Methods*, 2021.
- [InstaNovo] Eloff, K., Mehta, L.K., et al. "De novo peptide sequencing with InstaNovo: Accurate, database-free protein sequencing for next generation proteomics." *Nature Machine Intelligence*, 2024.

### Diffusion models (discrete)
- [D3PM] Austin, J., Johnson, D.D., Ho, J., Tarlow, D., van den Berg, R. "Structured Denoising Diffusion Models in Discrete State-Spaces." *NeurIPS*, 2021.
- [DDPM] Ho, J., Jain, A., Abbeel, P. "Denoising Diffusion Probabilistic Models." *NeurIPS*, 2020.
- [AnalogBits] Chen, T., Zhang, R., Hinton, G. "Analog Bits: Generating Discrete Data using Diffusion Models with Self-Conditioning." *ICLR*, 2023. (**Original self-conditioning paper -- no formal analysis**)
- [SohDickstein] Sohl-Dickstein, J., Weiss, E., Maheswaranathan, N., Ganguli, S. "Deep Unsupervised Learning using Nonequilibrium Thermodynamics." *ICML*, 2015.
- [MDLM] Sahoo, S., Arriola, M., et al. "Simple and Effective Masked Diffusion Language Models." *NeurIPS*, 2024.

### Mutual information estimation
- [MINE] Belghazi, M.I., Baratin, A., Rajeshwar, S., Ozair, S., Bengio, Y., Courville, A., Hjelm, D. "MINE: Mutual Information Neural Estimation." *ICML*, 2018.
- [InfoNCE] van den Oord, A., Li, Y., Vinyals, O. "Representation Learning with Contrastive Predictive Coding." *arXiv*, 2018.
- [Poole2019] Poole, B., Ozair, S., van den Oord, A., Alemi, A., Tucker, G. "On Variational Bounds of Mutual Information." *ICML*, 2019.

### Cross-species generalization
- [NovoBench] Zhou, J., et al. "NovoBench: Benchmarking Deep Learning-based De Novo Protein Sequence Design." *NeurIPS*, 2024. (**This is the benchmark we use**)

### Protein structure (context)
- [AlphaFold2] Jumper, J., et al. "Highly accurate protein structure prediction with AlphaFold." *Nature*, 2021.
- [ESM2] Lin, Z., Akin, H., Rao, R., et al. "Evolutionary-scale prediction of atomic level protein structure with a language model." *Science*, 2023.

### Mass spec / proteomics
- [PepNovo] Frank, A., Pevzner, P. "PepNovo: de novo peptide sequencing via probabilistic network modeling." *Analytical Chemistry*, 2005.
- [PEAKS] Zhang, J., et al. "PEAKS DB: de novo sequencing assisted database search for sensitive and accurate peptide identification." *Molecular & Cellular Proteomics*, 2012.

---

## Reading queue (must read before finalizing theory section)

**Priority 1 -- read immediately:**
- [ ] Austin et al. 2021 (D3PM) -- understand absorbing diffusion KL bounds for theory section
- [ ] Belghazi et al. 2018 (MINE) -- understand estimator before implementing
- [ ] Chen et al. 2022 (Analog Bits) -- confirm no formal self-conditioning analysis exists

**Priority 2 -- read before writing theory draft:**
- [ ] Poole et al. 2019 -- understand MI estimator taxonomy
- [ ] van den Oord 2018 (InfoNCE) -- compare with MINE for implementation choice
- [ ] Sohl-Dickstein 2015 -- VLB machinery for Appendix A derivation

**Priority 3 -- before Related Work finalization:**
- [ ] NovoBench (Zhou 2024) -- understand benchmark splits and evaluation protocol
- [ ] InstaNovo (Eloff 2024) -- understand their multi-species training setup
- [ ] Casanovo (Yilmaz 2022) -- understand transformer baseline

---

## Citations to add (placeholder -- add as you write sections)

*Add here as you write. Format: [ShortKey] Authors, "Title", Venue, Year.*

- [ ] Constrained decoding (NEUROLOGIC) -- for Related Work 3.5
- [ ] Scheduled sampling -- for Discussion (analogy to mass-constrained training)
- [ ] pyOpenMS -- for software citation
- [ ] SEQUEST-HT -- for ground truth method
