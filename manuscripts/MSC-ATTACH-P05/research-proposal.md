# Research proposal

## F-ATT-01 (candidate): Informative missingness and irregular temporal sampling in dynamic attachment assessment

**Working title:** *Informative Nonresponse and Irregular Sampling in Dynamic Attachment Assessment*.
**Priority:** high for a *novel methods contribution*, not automatic promotion.

**Independent question.** When the probability of responding to a phone prompt depends on an unobserved psychological state or recent interpersonal action, under which conditions are lagged effects of desired closeness, perceived closeness and subsequent approach/distancing identifiable? Does modeling sampling timing improve operating characteristics?

**Method.** Simulation-only Monte Carlo with independently controlled latent psychological dynamics, MNAR/MAR and time-dependent missingness, missed notifications, overnight intervals and unequal prompt delays. Compare complete-case lag regressions, IPW when assumptions permit, state-space/Kalman approaches and prespecified sensitivity/joint observation-process models. Include identifiability counterexamples, generator mismatch and held-out settings. Preserve the current H1 generating model as *one* case; evaluate independent dynamical systems beyond ARC.

**Endpoints.** Parameter bias, interval coverage, false discovery/non-detection, effective informative lags, and robustness under varying sampling and model misspecification. Mark nonidentifiable regimes, not misleading point recovery.

**Distinction.** H1 owns the substantive desired-state and discrepancy hypotheses; M02 owns controller identifiability. This proposed article would own **observation-process inference/generalizable methods**, not a reprint of H1 sample-size Monte Carlo.

**Cost.** No participant study: existing code and CPU simulations. Optional secondary datasets may later assess external calibration only if participant rights, time stamps and constructs are compatible.

**GO:** verified methodological gap, meaningful independent estimand, strong baselines and reproducible improvement or useful impossibility result. **NO-GO:** standard EMA missing-data methods already answer the question or contribution is only a parameter table for H1.

**TODO**
- [ ] P0 Review EMA/ESM MAR/MNAR, time-varying missingness, continuous/discrete-time state-space literature and document the exact gap.
- [ ] P0 Define additional generators and independent non-ARC benchmark; freeze sampling processes and power/precision metrics.
- [ ] P1 Run repeated Monte Carlo baseline comparisons, include failures and sensitivity/identifiability boundaries.
- [ ] P1 Independent novelty audit; decide whether this belongs as H1 supplement or standalone paper before a new folder.

