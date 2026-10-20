# Model Selection

## Decision

Select **Option B: a reduced-order, explicitly bounded post-meal model** for the first working version, but only as a research model conditioned on measured meal glucose appearance and accompanied by flux-rich measurements. Do not use the current three-state sketch as an already identified model. Before coding its right-hand sides, resolve state/flux definitions against the initial experiment and perform an identifiability analysis.

Keep **Option A: reproduce the Padova T2D Simulator** as a later benchmark workstream. R2 is the strongest directly relevant published benchmark found, but its detailed equations and parameters are not available through the checked access routes. An implementation assembled from the abstract would be guesswork, not a reproduction.

## Audit of inherited Phase 0 choices

The existing scope remains intact, but the following candidate statements must not be mistaken for published facts or established, identifiable physiology:

- The meal input $R_{a,m}=M_{abs}q_m$ assumes a known normalized appearance profile and total absorbed amount. Those are not available from meal composition alone; use tracer-derived input with uncertainty for the proposed first experiment. Until then, $M_{abs}$ and $q_m$ are not estimable model parameters.
- $HGP=HGP_0\phi_H(I)$ with a bounded monotone response is a modeling constraint, not an equation extracted from R2. The fixed response to systemic insulin ignores portal exposure, delay, and other regulation.
- The glucose-only secretion function and fixed hepatic extraction fraction are candidate simplifications. Insulin/C-peptide data and a kinetic model are required before their parameters can be interpreted as separate secretion, extraction, or clearance mechanisms.
- $dX/dt=k_XI-X/\tau_X$ is a proposed first-order latent action filter, not evidence that one peripheral action state is sufficient or identifiable in T2D. The aggregate uptake equation cannot resolve tissue-specific or insulin-independent disposal.
- $Q_G$ is conserved only inside the declared systemic glucose boundary. The prior use of “conservation-based” must not imply whole-body carbon conservation; hepatic precursors and tissue storage/oxidation are not states in this boundary.
- Renal loss is set to zero only as a restricted-domain assumption, not a universal omission. Its relevance must be reviewed for the intended glucose range.

These are constraints on interpreting the existing Phase 0 candidate equations, not proposed ODE changes in this phase. No full Padova equation has been verified for direct comparison.

## Comparison

| Criterion | A. Reproduce the published Padova T2D model | B. Develop a reduced-order model |
|---|---|---|
| Scientific defensibility | High if the exact published version, equations, units, parameters, cohort, inputs, and required implementation details can be obtained and checked. Currently insufficient for implementation because the accessible record does not expose those details. | Defensible as a clearly labeled, question-specific hypothesis if every closure is explicit, unsupported parameters remain unassigned, and the model is tested against appropriate flux measurements. Not a substitute for the published simulator. |
| Implementation effort | High: abstract reports 15 ODEs and 39 parameters. Full model transcription, unit audit, data protocol, parameterization, and matching outputs are required. | Moderate for a genuinely reduced model, but the current candidate still has unresolved hepatic, secretion, clearance, and insulin-action closures. Complexity must be bounded by the experiment. |
| Data requirements | Match the triple-tracer single-meal T2D population and inputs used to identify the published model; full methods/data access are needed. | Lower only if the aim is conditional glucose/insulin trajectories using measured meal appearance. Estimating separate physiological fluxes still needs tracer data, insulin/C-peptide observations, and suitable kinetic or perturbation information. |
| Identifiability | R2's abstract reports precise parameter estimates in its study, but accessible information is insufficient to assess individual parameters, covariance, or transferability. Reproducing those claims requires the full analysis. | High risk with glucose/insulin-only data. Flux measurements and a deliberately limited number of estimable parameters are essential; latent action and effective volumes may remain weakly identified. |
| Validation feasibility | Strong in principle against the original cohort and published outputs, but only if detailed data/protocols/reference results become accessible. Not currently executable as a fidelity test. | Feasible against predeclared independent meal-challenge observations and tracer-derived fluxes, with uncertainty-aware criteria. Validates only the reduced model and stated domain. |
| Scope fit | A well-matched T2D meal simulator and useful benchmark; broader than the minimum intended subsystem. | Fits a first bounded experiment, provided measured appearance is an input and no unsupported mechanisms are claimed. |

## Are the proposed states sufficient?

The proposed $Q_G$, systemic $I$, and delayed peripheral action $X$ states can be a compact candidate for **post-meal systemic glucose and insulin trajectories under a specified input and narrow experimental domain**. They are not sufficient to identify all mechanisms named in the research objective from ordinary glucose/insulin measurements, nor to claim a comprehensive T2D physiology model.

- $Q_G$ has a pool-balance role only after its effective distribution volume and boundary are fixed. Its derivative observes the net of meal appearance, hepatic production, peripheral use, and omitted losses; it cannot separate those terms by itself.
- Systemic insulin concentration is not pancreatic secretion. Without an explicit C-peptide kinetic observation model or other secretion measurement, secretion, first-pass extraction, distribution, and systemic clearance can trade off.
- $X$ is latent and aggregate. Glucose and insulin alone may not distinguish its gain/time constant from uptake or hepatic-response parameters. It cannot represent separate hepatic and peripheral action, tissue-specific uptake, nonlinear saturation, or glucose effectiveness unless those are added and supported.
- An instantaneous hepatic response to systemic insulin is an assumption. This boundary cannot represent independent portal insulin exposure, hepatic action delay, glucagon, or substrate/glycogen dynamics.
- Treating $R_{a,m}(t)$ as measured input means the model does not predict digestion or absorption. Input uncertainty propagates to fitted glucose fluxes.
- With no C-peptide state/observation model, the current ODE sketch cannot predict C-peptide or derive secretion internally. C-peptide can be an external observation in a separately specified kinetic/deconvolution analysis.

Thus the reduced model is suitable as a **conditional flux-balance hypothesis**, not an identifiable patient-specific model until measurements demonstrate that parameters can be estimated separately.

## Minimum measurements and identifiability

| Measurement set | What it can support | What it cannot establish alone |
|---|---|---|
| Serial plasma glucose only | Glucose excursion and timing under a known experimental input. | Cannot separate meal appearance, hepatic production, peripheral uptake, renal loss, insulin secretion, or insulin action. Glucose slope is only a net flux. |
| Serial glucose plus systemic insulin | Association of measured insulin with glucose response; may constrain a deliberately simple effective response model. | Does not separate secretion from clearance/extraction, hepatic production from peripheral utilization, or usually the latent action parameters. |
| Add serial C-peptide with assay metadata and an explicit kinetic/deconvolution method | Supports estimation of endogenous insulin secretion rate; R7 describes kinetic estimation and the use/limits of standard kinetic parameters. | Does not by itself establish systemic insulin clearance or separately identify first-pass extraction and peripheral clearance. Those require an adequate insulin kinetic model and independent information. |
| Add meal and intravenous glucose tracers with enrichment measurements and a validated triple-tracer protocol | Supports time-varying meal glucose appearance and endogenous glucose production estimates; fluxes constrain the glucose balance. R6 documents why non-steady-state tracer design matters. | Flux estimates retain method/assay uncertainty and are protocol-specific; a tracer protocol is not universal ground truth. |
| Add a separate insulin kinetic or insulin-sensitivity perturbation, selected with the study team | May improve separation of insulin clearance and sensitivity/action dynamics, depending on the protocol and observation model. | No unspecified challenge guarantees identification of $CL_I$, $E_H$, $k_X$, $S_X$, and $\tau_X$ simultaneously. Establish this by sensitivity/profile-likelihood analysis first. |

At minimum for the proposed meal model: frequent glucose and insulin, C-peptide with a kinetic method, known meal composition/timing, and meal/IV tracer measurements supporting $R_{a,m}$ and endogenous production. Include specimen type, assay precision, timestamps, tracer enrichment, basal/initial conditions, treatment/protocol metadata, and subject identifiers. Effective distribution volumes and individual kinetic parameters require independent evidence or must be fixed/removed; concentration data alone do not identify an amount scale.

## Unresolved scientific decisions

1. Can the group obtain institutional or author access to the complete R2 text and any supplement, and are model data/code available on request?
2. Is the first purpose conditional prediction under measured meal appearance, or prediction of absorption from meal composition? The latter requires an absorption subsystem and more data.
3. Is C-peptide only an external secretion-identification measurement, or should model C-peptide kinetics be included as states?
4. Which glucose and insulin assay/compartment define $G$ and $I$, and how are effective volumes independently selected?
5. Can glucose-only hepatic modulation and one latent peripheral action state be distinguished under the chosen observation schedule?
6. What glucose range and conditions justify omitting renal loss, glucagon, incretins, and other regulators?
7. Which parameter subset will be fixed, estimated jointly, or excluded after structural and practical identifiability analysis?
8. What data permissions, sample size, held-out split, assay uncertainty, and predeclared statistical acceptance protocol are available?

## Proposed next-phase implementation plan

1. Obtain and review R2 full text and any author/publisher materials; transcribe its state definitions, equations, units, parameter sources, inputs, and validation protocol into a comparison table. Do not begin a replica before this gate is met.
2. Lock the experiment and observation model described in `initial_experiment.md`, including tracer protocol, sample schedule, assay uncertainty, provenance, and data access.
3. Derive candidate equations from the selected experiment; conduct dimensional, boundary, structural-identifiability, and sensitivity review. Decide whether $X$ is retained and which parameters are fixed or excluded.
4. After scientific review, implement the smallest selected ODE model with explicit input/observation interfaces and solver configuration; do not add mechanisms outside the approved scope.
5. Add unit/dimensional tests, limiting cases, positivity and mass-balance tests, solver-convergence tests, then calibrate only on designated training subjects.
6. Run predeclared held-out validation against glucose, insulin, and tracer-derived fluxes. Report uncertainty and non-identifiable parameters; make no clinical claims.
7. Pursue the Padova benchmark separately only after version-matched equations, parameters, inputs, and reference outputs are available; document differences and do not imply reproduction until comparison passes.