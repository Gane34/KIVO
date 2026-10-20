# PhysioTwin Phase 1.1: Baseline Glucose-Trajectory Diagnosis

## Finding

The low glucose value is reproduced from the checked-in illustrative configuration. No flux-sign, unit, solver-success, meal-normalization, or material accounting defect was found in this run. The glucose pool falls because modeled disposal exceeds modeled appearance by 44.58 mmol over the 360-minute interval. That is a consequence of the selected hypothetical parameter values and explicit illustrative closures, with a contribution from the hypothetical initial conditions. Whether the closures are scientifically appropriate is unresolved; this report does not endorse them as physiology.

The checked-in configuration and generated baseline outputs were preserved. The engine was rerun in memory from `experiments/phase1_initial/config.v1.json`; the configuration SHA-256 was `31b9b894bfe41848e439ce2d271896b4c863118da40eb755259a0243e8b979a8`. The reproduced glucose samples matched `outputs/phase1_initial_experiment/results.csv` exactly (maximum absolute difference 0.0 mmol/L).

## Equations And Boundary

The model states are glucose-pool amount $Q_G$ (mmol), systemic insulin concentration $I$ (pmol/L), and aggregate peripheral action $X$ (dimensionless). Derived glucose concentration is $G=Q_G/V_G$ (mmol/L). Time is minutes.

$$
\frac{dQ_G}{dt}=R_{a,m}+HGP-R_d,\qquad G=\frac{Q_G}{V_G}
$$

$$
V_I\frac{dI}{dt}=(1-E_H)S_\beta(G)-CL_I I
$$

$$
\frac{dX}{dt}=k_XI-\frac{X}{\tau_X},\qquad R_d=(CL_G+S_XX)G
$$

For this illustrative run, the documented closures are:

$$
R_{a,m}=M_{abs}\frac{t}{\tau_m^2}e^{-t/\tau_m},\quad
HGP=\frac{HGP_0}{1+\max(I-I_{ref},0)/K_H},\quad
S_\beta=S_{\beta,0}+k_\beta\max(G-G_\beta,0)
$$

The modeled glucose boundary is a systemic pool: meal appearance and HGP enter; aggregate peripheral utilization leaves; renal loss is set to zero. It is not a whole-body glucose or carbon balance. The functional forms and all numeric configuration values are hypothetical, not literature-derived or fitted. See `docs/phase1_model_closures.md` for the pre-implementation provenance review.

## Reproduced State Trajectory

| Quantity | Initial | Minimum (time) | Maximum (time) | Final at 360 min |
|---|---:|---:|---:|---:|
| $Q_G$ (mmol) | 66.0000 | 18.8658 (248 min) | 85.9625 (39.5 min) | 21.4206 |
| $G$ (mmol/L) | 5.5000 | **1.57215 (248 min)** | 7.16354 (39.5 min) | 1.78505 |
| $I$ (pmol/L) | 80.0000 | 80.0000 (0 min) | 413.639 (80.5 min) | 220.156 |
| $X$ (dimensionless) | 15.3600 | 15.3600 (0 min) | 64.7293 (124 min) | 43.5579 |

The initial $X$ is calculated by the isolated-filter rule $X_0=k_X I_0\tau_X$; the initial glucose and insulin values are hypothetical inputs, not a measured fasting steady state. At time zero, $R_{a,m}=0$, $HGP=1.000$ mmol/min, and $R_d=0.6512$ mmol/min, so $dQ_G/dt=+0.3488$ mmol/min. Initial secretion is 70 pmol/min, systemic insulin appearance is 45.5 pmol/min, and clearance is 9.6 pmol/min, giving $dI/dt=+4.4875$ pmol/L/min. The initial state is therefore not a steady state of the full model.

## Glucose Fluxes

Rates below are positive magnitudes with the sign shown separately in the $Q_G$ balance. Integrated values are over 0-360 minutes. Minima/maxima are from the 0.5-minute saved output grid.

| Flux | Balance sign | Units | Rate range (time of extrema) | Integrated contribution |
|---|---:|---|---|---:|
| Meal appearance $R_{a,m}$ | + | mmol/min | 0 to 0.919699 (max at 28 min) | +69.997471 mmol |
| Hepatic production $HGP$ | + | mmol/min | 0.131735 (min at 80.5 min) to 1.000000 (max at 0 min) | +108.053187 mmol |
| Peripheral disposal $R_d$ | - | mmol/min | 0.317742 (min at 273 min) to 1.258522 (max at 69 min) | -222.630004 mmol |

Total modeled glucose input was $69.997471+108.053187=178.050658$ mmol, versus 222.630004 mmol removed. Thus the integrated net change is -44.579346 mmol. The observed change is $Q_G(360)-Q_G(0)=-44.579361$ mmol; their difference is the reported numerical pool residual, $1.51\times10^{-5}$ mmol. This is a substantial modeled net removal, not a hidden balance discrepancy.

To show the composition of $R_d$, its two terms were integrated from the sampled 0.5-minute output using the trapezoidal rule (an approximation): basal clearance $CL_GG$ contributed 93.282 mmol (41.9%) and the action-dependent term $S_XXG$ contributed 129.348 mmol (58.1%). Their approximate sum, 222.629938 mmol, agrees with the solver-dense integrated disposal diagnostic of 222.630004 mmol.

At the glucose minimum (248 min), $G=1.57215$ mmol/L, $I=235.387$ pmol/L, and $X=49.9559$. The pointwise rates are $R_{a,m}=0.003152$, $HGP=0.319013$, and $R_d=0.322117$ mmol/min, leaving an approximately balanced instantaneous rate near the nadir. HGP is suppressed to 0.319 of its hypothetical basal scale at that point and to 0.1317 at peak insulin. This behavior follows the chosen instantaneous insulin-suppression closure.

## Insulin Balance

Secretion is a portal source; extraction occurs before systemic appearance. The systemic concentration equation uses the remaining fraction as its source and clearance as its sink.

| Quantity | Units | Rate range (time of extrema) | Integrated amount over 360 min |
|---|---|---|---:|
| Beta-cell secretion $S_\beta$ | pmol/min | 40.000 (minimum at 101.5 min) to 119.906 (maximum at 39.5 min) | 19,835.200 pmol secreted |
| First-pass extraction $E_HS_\beta$ | pmol/min | 14.000 to 41.967 (maximum at 39.5 min) | 6,942.320 pmol extracted |
| Systemic insulin appearance $(1-E_H)S_\beta$ | pmol/min | 26.000 to 77.939 (maximum at 39.5 min) | 12,892.880 pmol entering systemic pool |
| Systemic clearance $CL_I I$ | pmol/min | 9.600 to 49.637 (maximum at 80.5 min) | 11,771.636 pmol cleared |

The factors are dimensionally consistent: $S_\beta$ is pmol/min, $E_H$ is dimensionless, and $CL_I I=(\mathrm{L/min})(\mathrm{pmol/L})$ is pmol/min. The systemic insulin amount changes from $V_I I_0=640.000$ pmol to $V_I I_{360}=1,761.245$ pmol, a +1,121.245 pmol change. Integrated systemic appearance minus clearance is +1,121.244 pmol; the reported insulin balance residual is -0.000683 pmol. Secretion, extraction, systemic entry, and clearance are not conflated in this accounting.

The secretion closure has a floor: whenever $G\leq G_\beta=4.5$ mmol/L, it continues to secrete $S_{\beta,0}=40$ pmol/min rather than tending to zero. That floor supplies 26 pmol/min systemically under $E_H=0.35$. With $CL_I=0.12$ L/min, this source alone implies a low-glucose systemic insulin equilibrium of $26/0.12=216.667$ pmol/L. The final insulin value, 220.156 pmol/L, is near this closure-implied level, while action remains elevated. This is a mathematical consequence of the hypothetical secretion and clearance values, not a claim about actual basal physiology.

## Input Normalization And Horizon

The declared shape-2 gamma profile is normalized on $[0,\infty)$:

$$
q_m(t)=\frac{t}{\tau_m^2}e^{-t/\tau_m},\qquad
\int_0^\infty q_m(t)\,dt=1
$$

Thus $R_{a,m}=M_{abs}q_m$ integrates to the configured $M_{abs}=70$ mmol over an infinite horizon. With $T=360$ min and $\tau_m=28$ min, the captured fraction is $1-e^{-T/\tau_m}(1+T/\tau_m)=0.999963868$. The run delivers 69.997471 mmol and leaves 0.002529 mmol (0.00361%) in the analytic tail. The meal input peaks at $t=\tau_m=28$ min. The meal input is therefore normalized and almost fully captured; it does not explain the low result through an excess input or a normalization error.

The horizon includes the glucose nadir and essentially all meal appearance, but it does not show return to the initial state or a settled response. At 360 min, glucose is 1.78505 mmol/L and rising at about 0.002168 mmol/L/min; insulin is 220.156 pmol/L and falling at about 0.05233 pmol/L/min; $X=43.5579$ and falling at about 0.02683 per minute. The glucose minimum is already inside the interval, but late recovery behavior is truncated.

## Diagnosis And Limitations

- **Flux/accounting defect:** not supported by this run. Units and signs match the documented equations, and both amount balances close to solver accuracy. The pool itself has a real modeled negative net balance over the interval.
- **Hypothetical parameters:** a major source of the result. The configuration explicitly labels all values hypothetical; $M_{abs}$, distribution volumes, HGP scale/response, uptake gains, insulin secretion, extraction, clearance, and action dynamics have no traceable numeric source or calibration here.
- **Functional closures:** a major source of the result and an unresolved scientific decision. The glucose-only secretion floor produces persistent systemic insulin entry; systemic insulin instantaneously suppresses HGP; and the one-state action filter retains elevated disposal after the meal input wanes. No data establish these forms or their adequacy for this trajectory.
- **Initial conditions:** contribute to the transient but do not alone explain the result. Initial glucose is 5.5 mmol/L and insulin is 80 pmol/L, while $X_0=15.36$ is set by an isolated-filter equilibrium. The full model initially has rising glucose and insulin, then develops high insulin and delayed action.
- **Finite horizon:** captures 99.9964% of the meal input and the glucose nadir, but truncates recovery. It cannot account for why the nadir occurred; extending the unchanged run would only characterize later relaxation.

The minimum is therefore best attributed to a combination of hypothetical values and unvalidated closures, with initial conditions shaping the transient. It is not evidence that the implemented balances are numerically broken, and the code result cannot establish physiological adequacy. The low value lies outside any reviewed or validated operating domain for this prototype.

## Candidate Actions For Scientific Review

No corrective model change is made here. Before changing equations or values, review these decisions with the scientific team:

1. Decide whether the thresholded secretion floor is defensible for the intended question; if not, specify an evidence-supported secretion function and the C-peptide/insulin measurements needed to constrain it. Do not tune the floor against this synthetic curve.
2. Decide whether systemic insulin is an acceptable instantaneous input to the hepatic production response, and whether the bounded reciprocal-hinge function is retained, replaced, or supplied from measured HGP. Use tracer-supported flux data rather than curve appearance as the criterion.
3. Define supported sources or estimation procedures for $V_G$, $V_I$, basal fluxes, clearances, gains, time constants, and initial conditions. Establish identifiability before fitting or reporting subject-specific values.
4. State the admissible glucose domain and whether omission of renal loss and other regulation is defensible there. Do not claim the current trajectory is valid in the low-glucose range.
5. If recovery is an experiment endpoint, predeclare an extended horizon as a numerical diagnostic using the unchanged baseline parameters; do not treat a longer run as a physiological correction.

No new mechanism, drug effect, personalization, parameter tuning, or alternative configuration is introduced. No regression test was added because this diagnosis found no software defect. The existing complete suite should still be run after this report is added.