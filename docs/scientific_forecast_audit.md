# Scientific Forecasting Audit

**Audit date:** 2026-10-19  
**Scope:** Existing PhysioTwin ODE, synthetic observations, forecast ensemble, benchmark metrics, event-risk outputs, evidence/data access.  
**Data analyzed:** Repository's deterministic synthetic fixtures only; no human records were loaded.

## Executive Finding

The existing engine is a numerically reproducible illustrative ODE, not an observation-conditioned or validated glucose forecaster. Its default 360-minute run reproducibly reaches 1.572149 mmol/L at 248 minutes. The low result is not a solver artifact: it persists across LSODA, RK45 and BDF and across the tested tolerances/output grids. The configured initial state is not a fasting steady state, and the same equations' meal-free steady state is approximately 2.038 mmol/L. Numerical mass-balance closure demonstrates consistent accounting inside the declared pool; it does not establish physiological plausibility.

The forecast code does not estimate model states from the observed synthetic CGM. It simulates from time zero with the generator's exact parameter set and initial conditions, retrieves the hidden ODE state at the requested cutoff, and continues from there. The observations are generated from that same ODE trajectory with seeded independent Gaussian noise. The resulting RMSE of 0.12 mmol/L is therefore a same-generator, single-synthetic-profile consistency result with privileged model state/parameter knowledge, not held-out patient forecasting performance.

The reported 100% hypoglycemia probability is not an estimated probability. It is a hand-written function of the deterministic ensemble-mean nadir, capped at one. The nominal 95% interval is the central percentile range of an arbitrary, narrow parameter-perturbation ensemble. It has no demonstrated calibration and excludes observation/state uncertainty. No ODE correction is scientifically supportable from the repository's evidence; the safe correction is to withdraw probability/calibration claims and label the projection and interval according to what they actually represent.

## Existing Model And Provenance

### States, equations and units

Time is minutes. The engine state vector is $y=(Q_G,I,X)$:

| State | Meaning | Units | Observation status |
|---|---|---|---|
| $Q_G$ | Amount in a fixed effective systemic glucose pool | mmol | Not measured by the synthetic stream; computed from $V_GG$. |
| $I$ | Systemic insulin concentration after lumped first-pass extraction | pmol/L | Not observed in the generated stream; simulated. |
| $X$ | Latent aggregate peripheral insulin-action filter | dimensionless | Unobserved and simulated; not a measured biological concentration. |

The implemented balances are:

$$\frac{dQ_G}{dt}=R_{a,m}+HGP-R_d,\qquad G=Q_G/V_G$$

$$V_I\frac{dI}{dt}=(1-E_H)S_\beta(G)-CL_I I$$

$$\frac{dX}{dt}=k_X I-X/\tau_X,\qquad R_d=(CL_G+S_XX)G$$

The glucose terms have units mmol/min; $Q_G/V_G$ has units mmol/L. The insulin amount rate and both insulin fluxes have units pmol/min. Both action-state terms have units min$^{-1}$. The implementation's amount/concentration conversion and signs are dimensionally consistent for the declared fixed-volume pool. Renal loss is omitted, and the balance is not whole-body glucose or carbon conservation.

### Closures and meal input

- Meal appearance is $R_{a,m}=M_{abs}(t/\tau_m^2)e^{-t/\tau_m}$ for $t\ge0$, a normalized shape-2 gamma forcing with total asymptotic amount $M_{abs}$. It begins at zero and peaks at $t=\tau_m$. It is not gastric emptying, intestinal absorption, splanchnic extraction, or a meal-composition model. The meal marker in the synthetic stream is just configured $M_{abs}$ at $t=0$, not an independently measured meal.
- Hepatic glucose production uses the reciprocal hinge $HGP_0/[1+\max(I-I_{ref},0)/K_H]$. Its instantaneous systemic-insulin response, threshold and parameters are illustrative, not sourced from the reviewed Padova abstract or validated data.
- Peripheral disposal is $(CL_G+S_XX)G$. It is aggregate and linear in glucose, with one latent action state; it does not resolve tissue uptake, glucose effectiveness, glycogen/storage, oxidation, or renal loss.
- Secretion is $S_{\beta,0}+k_\beta\max(G-G_\beta,0)$. It has a constant 40 pmol/min floor in the baseline even at very low glucose. With $E_H=0.35$, that floor supplies 26 pmol/min systemically. First-pass extraction is fixed; systemic clearance is first order. These forms and values are hypotheses, not fitted physiology.
- The action initialization $X_0=k_XI_0\tau_X=15.36$ is equilibrium of the isolated action filter at $I_0=80$ pmol/L, not an observed state and not a steady state of the coupled system.
- The configured values $V_G=12$ L, $V_I=8$ L, meal amount/time constant, flux scales, gains, thresholds, extraction and clearance have no traceable numeric source or patient fit. They are explicitly hypothetical in the configuration and metadata.

### Basal consistency and low-glucose cause

For the configured initial state $G=5.5$ mmol/L, $I=80$ pmol/L and $X=15.36$, the implemented derivatives at meal time zero are:

| Derivative | Value | Interpretation |
|---|---:|---|
| $dQ_G/dt$ | +0.3488 mmol/min | $R_a=0$, $HGP=1.0$, $R_d=0.6512$ mmol/min at initialization. |
| $dI/dt$ | +4.4875 pmol/L/min | Systemic insulin appearance exceeds clearance. |
| $dX/dt$ | 0 | Only the isolated action filter is initialized at equilibrium. |

Thus the nominal fasting inputs do not initialize a coupled fasting steady state. Solving the meal-free equilibrium equations for the same parameters yields approximately $G=2.03804$ mmol/L, $I=216.667$ pmol/L and $X=41.6$. At that low glucose the secretion floor persists; insulin remains elevated, the action state is large, and the hepatic closure suppresses production. This mathematical equilibrium is itself physiologically implausible, a structural closure/parameter problem rather than a numerical integration problem.

For the full baseline meal run, integrated meal input is 69.9975 mmol, HGP is 108.0532 mmol, and disposal is 222.6300 mmol. Net modeled removal is about 44.5793 mmol over 360 minutes. The numerical pool residual is about $1.51\times10^{-5}$ mmol. The dominant explanations are the unsupported uptake/action parameterization, persistent secretion floor and resulting insulin/action, instantaneous HGP suppression, and non-steady initial conditions. No single one is established as the unique biological cause. The prior diagnostics provide the detailed trajectory and flux accounting in `reports/phase1_1_diagnostics.md`.

## Numerical Behavior

The baseline was reproduced with `python -m physiotwin.experiment --config experiments/phase1_initial/config.v1.json --output <temporary-directory>`. All 721 glucose samples matched the preserved CSV exactly (maximum absolute difference 0 mmol/L); the original output directory was not used for reproduction.

| Solver/settings | Minimum glucose (mmol/L) | Time (min) | Glucose balance residual (mmol) |
|---|---:|---:|---:|
| LSODA, rtol $10^{-7}$, atol $10^{-9}$, output step 0.5 min | 1.572149197 | 248 | $1.51\times10^{-5}$ |
| LSODA, rtol $10^{-6}$, atol $10^{-8}$, output step 0.5 min | 1.572146285 | 248 | $-7.84\times10^{-5}$ |
| LSODA, rtol $10^{-10}$, atol $10^{-12}$, output step 0.5 min | 1.572148981 | 248 | $4.30\times10^{-7}$ |
| RK45, rtol $10^{-7}$, atol $10^{-9}$, output step 0.5 min | 1.572157842 | 248 | $5.75\times10^{-4}$ |
| BDF, rtol $10^{-7}$, atol $10^{-9}$, output step 0.5 min | 1.572149870 | 248 | $1.01\times10^{-4}$ |

The trajectory's low nadir is stable to roughly $10^{-5}$ mmol/L among these runs, while quadrature/balance residuals depend more on solver/tolerance. `SolverSettings.dt` sets the reported `t_eval` grid; `solve_ivp` is not given `max_step=dt`, so the existing “dt” sensitivity test is not an internal integration-step convergence study. Existing tests cover some 60- and 90-minute cases, not a full physiological validation or systematic 360-minute convergence budget. Solver success, nonnegative states and near-closed accounting do not make the operating range plausible. The engine throws on negative solver states rather than clipping its physiological states; the observation generator separately floors noisy synthetic CGM at 0.5 mmol/L, which can censor low simulated observations.

## Forecast, Evaluation And Uncertainty Audit

### Forecast lineage

`run_forecast` generates an observation stream for presentation, but only uses it to return the historical segment. Forecast construction instead:

1. Reads the synthetic patient's exact configured parameters and initial conditions.
2. Runs `simulate_model` from $t=0$ through the requested horizon.
3. Extracts $Q_G,I,X$ from that full model run at the cutoff.
4. Starts each forward ensemble member from that same unperturbed model state.

It does not assimilate the historical CGM values, estimate the current glucose state from them, infer insulin or $X$, or estimate parameters from a training cohort. The forecast is a continuation conditional on known generator parameters and hidden state, not a patient forecast from available observations. It is not leakage of future CGM rows in the narrow temporal sense, but it is privileged same-generator knowledge and does not satisfy the requested observation-conditioned benchmark.

### RMSE 0.12 mmol/L

`python scripts/run_demo.py` reproduced a 0.12 mmol/L rounded RMSE and 0.10 mmol/L MAE for the ODE continuation; persistence was 1.63 RMSE and linear trend 0.36 RMSE. Each score uses one synthetic profile, seed 42, a single cutoff at 120 minutes, one 180-minute horizon and 36 future 5-minute CGM points. The ODE's output is interpolated onto those target timestamps. The three predictions are compared on the same timestamps and all glucose errors use mmol/L; this aspect is internally consistent.

The target samples are noisy observations generated from the same ODE/parameters used by the continuation. The ODE forecaster has access to the generating parameters and latent cutoff state, while persistence/trend use observed CGM. This is not an equal-information comparison and the single synthetic score is not an independent subject-held-out test. The `target_leakage_prevented` field is hard-coded by the metric function and the test only checks that Boolean; it is not a leakage audit. No rolling-origin or 30/60/120-minute horizon benchmark exists. The returned TIR/TBR/TAR values are percentages of **predictions** inside ranges, not forecast accuracy or agreement with target TIR.

### Ensemble interval

The forecast ensemble contains the base parameter set plus independent Gaussian multiplicative perturbations of $S_X$ (nominal SD 8%), $\tau_m$ (6%) and $CL_I$ (6%), with hard-coded clipping bounds. These distributions, bounds and independence are not estimated from data or parameter covariance. No observation noise, state-estimation uncertainty, initial-condition uncertainty, meal uncertainty or model-form uncertainty is propagated. All perturbed runs share the unperturbed model state at the cutoff, which is inconsistent with recomputing a coherent perturbed pre-cutoff state.

The displayed nominal 95% band is a percentile envelope over these arbitrary samples, not a calibrated confidence or predictive interval. In one descriptive check at the demo cutoff, it covered 36/36 latent synthetic values (guaranteed here because the exact base trajectory is an ensemble member) and 32/36 noisy CGM values (88.9%), with mean width about 0.376 mmol/L. These 36 correlated points from one same-generator case cannot establish 95% coverage. No calibration set, subject-level interval coverage, coverage uncertainty or horizon-specific coverage is provided.

## Event-Risk Audit

`risk.py` defines a hypoglycemia event as any sampled latent synthetic value below 3.9 mmol/L and severe hyperglycemia as any sampled value above 13.9 mmol/L within the forecast horizon. There is no duration criterion. The reference trajectory is generated by the same ODE, not an independent clinical label; the 2.5-minute sample grid may miss events between points. The returned `ground_truth_verified` only indicates whether the synthetic generated latent path crosses a threshold; it does not validate the predictor.

Hypoglycemia probability is not calculated as the fraction of ensemble trajectories with an event, and no probability model is fitted. If the mean nadir is below threshold, code computes $\min(1,0.5+(3.9-G_{nadir})/2)$; otherwise it uses another hand-selected distance formula. At the reproduced nadir near 1.58 mmol/L this saturates at 100%. Hyperglycemia probability is similarly a hand-picked function of mean peak/distance. The deterministic threshold crossing and arbitrary ensemble do not justify probabilistic interpretation, calibration, discrimination, or a clinical alert. The UI labels these numbers “Probability” and calls them risk; that overstates what the implementation computes. The mechanistic text describes terms in the assumed ODE, not validated causal physiology.

## Data And Literature Availability

- **Repository observations:** No real glucose/CGM, insulin, C-peptide, medication, meal-timing or tracer records are stored. `synthetic.py` hard-codes four profiles and their metadata/parameters. These are synthetic cases, not four independent patients or a cohort suitable for a subject-held-out population claim.
- **Observation process:** `observations.py` samples the ODE at a fixed interval and adds seeded independent Gaussian noise (default SD 0.15 mmol/L). It has no verified device model, sensor lag, correlated error, missingness, calibration drift or observed meal/medication records. Its “true glucose” is the ODE latent state.
- **T2D data:** The repository's Phase 1.3 audit says GSE153792 is transcriptomic data, not CGM/meal flux data, and that no suitable matched subject-level glucose/flux data were found. The dataset was not downloaded and its explicit redistribution license was not verified. It cannot validate T2D glucose dynamics.
- **T1D methods benchmark:** A permissioned longitudinal T1D CGM dataset could support a separately labeled generic forecasting-method benchmark if its terms, measurement protocol, subject identifiers and required covariates are verified. It would not validate T2D physiology or transfer performance to T2D. No such dataset is currently present or verified for use here.
- **Padova T2D simulator:** `docs/literature_audit.md` records the accessible abstract's report of a 15-ODE, 39-parameter model identified in 51 people with T2D, but no accessible full equations, parameter tables, detailed protocol, participant-level validation data, linked supplement/data or verified executable implementation in the checked routes. A faithful reproduction is not currently possible from the available material; reconstructing it from the abstract would be unsupported.
- **Licensing:** No patient dataset license or data-use terms are established in this repository. Do not redistribute any candidate data until source terms are verified.

## Track Conclusions

**A. Mechanistic physiology:** retain the current ODE only as an illustrative accounting/software fixture. No equation, parameter or state correction is supported by independent measurements or a source-specific replacement model. A conservation-preserving arbitrary retune would conceal, not resolve, the scientific problem.

**B. Data-driven forecasting:** no real time-series data are currently available for development or held-out evaluation. Persistence and linear trend can be benchmarked as methods on synthetic streams with explicit same-generator limitations; no learned model is warranted on four scripted profiles.

**C. Synthetic experiments:** useful for deterministic software tests, numerical checks and recovery of deliberately simulated behavior. They cannot establish T2D physiology, external prediction or clinical validity. Keep outputs, metrics, names and UI provenance separate from real-data tracks.

## Verification Record And Claims Ladder

Pre-change commands run:

- `python -m pytest -q`: 21 passed, 652 warnings (FastAPI/Starlette and pytest-asyncio deprecations in the environment).
- Baseline reproduction command: `python -m physiotwin.experiment --config experiments/phase1_initial/config.v1.json --output <temporary-directory>`; 721 rows; maximum difference from preserved baseline glucose column: 0 mmol/L.
- `python scripts/run_demo.py`: RMSE 0.12 mmol/L, MAE 0.10 mmol/L, single 36-point synthetic evaluation; hypoglycemia probability 100%; mean ODE nadir about 1.58 mmol/L at +125 minutes.

PhysioTwin currently demonstrates level **1: numerical execution** for the declared fixture. It does not establish level **2: physiological plausibility** over the simulated low range, level **3: held-out measurement prediction**, or level **4: clinical validation**. The synthetic score and event output must not be used to claim levels 3 or 4.