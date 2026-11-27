# F-ATT-01 | evidence matrix (2026-10-12)

**Decision: include in M02/H1.** No new article, no changes to registered analyses. Publisher/academic abstracts and DOI checked, full-text validation pending.

| Work | Year | DOI | Question | Method | Reported result / limit | Similarity |
|---|---:|---|---|---|---|---|
| ctsem, Driver et al. | 2017 | [DOI](https://doi.org/10.18637/jss.v077.i05) | Irregular time | SDE SEM | Handles time gaps, not MNAR | high |
| Regularized CTSEM | 2023 | [DOI](https://doi.org/10.1037/met0000550) | Complex dynamics | LASSO CTSEM | Addresses unequal intervals | high |
| Luo & Hu, Temporal Misalignment | 2024 | [DOI](https://doi.org/10.1080/10705511.2023.2207749) | Lag bias | DSEM simulation | Model adjustment beats naive | very high |
| Fang & Wang, DSEM Missing Data | 2024 | [DOI](https://doi.org/10.1080/10705511.2023.2287967) | N/T requirements | Simulation | Precision affected; full text needed | high |
| Slipetz et al., Missing Data in EMA | 2025 | [DOI](https://doi.org/10.1080/00273171.2025.2469055) | MAR/MNAR | Kalman vs imputation | Kalman strong; MNAR harder | very high |
| Losardo et al., Planned Missingness | 2024 | [DOI](https://doi.org/10.1007/978-3-031-56318-8_26) | Sampling plans | Monte Carlo | Placement matters | high |
| Reiter & Schoedel, Never miss a beep | 2024 | [DOI](https://doi.org/10.3758/s13428-023-02252-9) | Nonresponse | Mobile sensing | Context predicts compliance | very high |
| Tammilehto et al., Attachment Dynamics | 2025 | [DOI](https://doi.org/10.1177/01461672251333472) | Attachment states | EMA/DSEM | Security predicts lower insecurity | high |
| Attachment and Emotion Regulation | 2022 | [DOI](https://doi.org/10.1080/02699931.2022.2081534) | Lag associations | EMA | Psychological precedent | medium |
| Schneider et al., EMA Auxiliary Variables | 2026 | [DOI](https://doi.org/10.1177/25152459261479197) | Prompt nonresponse | Tutorial and code | Observed covariate corrections | very high |
| Wan & Liu, Mixed Missing Mechanisms | 2026 | [DOI](https://doi.org/10.1080/00273171.2026.2700050) | Mixed missingness | Longitudinal models | Direct overlap; full text pending | very high |
| Cho et al., Nonignorable Daily Diary | 2026 | [DOI](https://doi.org/10.1017/psy.2026.10120) | MNAR | Bayesian selection | Direct precedent | very high |
| Benson et al., Time-Related EMA | 2026 | [DOI](https://doi.org/10.1177/25152459251401191) | Event timing | Survival review | Time modeling established | high |
| Attachment Manifestations in Daily Life | 2022 | [DOI](https://doi.org/10.1007/s42761-022-00117-6) | Context | Ambulatory N=263 | Context-linked states | medium |

## Estimand and design
Independent estimand candidate: identified set of continuous-time lag parameters under specified missingness mechanisms, its diameter and coverage. Without assumptions, unconstrained MNAR does not identify a point value. Test with two observationally equivalent generators, irregular timestamps and explicit response models. Baselines: complete-case lag, DSEM, ctsem, Kalman MAR, auxiliary-variable MAR, IPW and Bayesian selection. Metrics: bias, coverage, false sign and effective lags. CPU simulation only, no recruitment.

## Novelty and ownership
M02 owns identifiability; H1 owns substantive lag hypotheses. Generic EMA missingness comparisons already exist (Slipetz 2025, Schneider/Wan/Cho 2026). New standalone work requires a distinct partial-identification result and independent non-ARC generator. Otherwise sensitivity appendix.

## Search and next actions
2026-10-12. Queries: `EMA missingness MNAR 2026`, `prompt nonresponse auxiliary variables`, `continuous time SEM irregular sampling`, `attachment dynamics EMA`. Sources: PubMed, APS, Wiley, Springer, JSS. [Proposal](../FUTURE_RESEARCH_PROPOSALS.md).

- [ ] Verify full texts of 2025–2026 closest methods.
- [ ] Formalize observational equivalence and sensitivity bounds.
- [ ] Run held-out non-ARC simulation and standard baselines.
- [ ] Reassess only after overlap/novelty gate.
