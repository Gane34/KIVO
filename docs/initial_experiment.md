# Initial Experiment Proposal

## Experiment

**One standardized triple-tracer mixed-meal challenge in a documented T2D cohort**, designed to observe systemic glucose/insulin response and independently constrain meal appearance and endogenous glucose production. This is a proposed research protocol, not a clinical recommendation, validated protocol, or experiment already performed by PhysioTwin.

The choice is motivated by R2, which reports identifying its T2D meal simulator from a single triple-tracer mixed meal in 51 participants, and R6, which describes a triple-tracer strategy for reducing non-steady-state error in postprandial estimates of meal appearance and endogenous glucose production. The accessible R2 full methods and detailed protocol were not available in this audit. Therefore the exact meal, tracer identities/doses/infusion waveforms, sampling times, eligibility criteria, and sample size must come from an accessible validated protocol and approved research/ethics review; they are not specified or invented here.

## Inputs and protocol records

- A documented fasting/basal observation period and relevant treatment/visit metadata; medication handling is defined by the approved study protocol, not this model document.
- One fixed, fully characterized mixed-meal composition, amount, and ingestion timing, selected from the source protocol before enrollment. Record available carbohydrate and input units; do not infer absorbed glucose from a meal label alone.
- Oral meal tracer and intravenous glucose tracer infusion schedules from the selected validated triple-tracer protocol. Record isotope, dose, infusion timing/rate, preparation, and assay method exactly from that source.
- A prespecified serial venous sampling schedule covering fasting baseline and post-meal response, copied from or justified against the selected protocol. Record actual collection times as well as nominal times.
- No model drug intervention in this first experiment. The first question is meal-flux identifiability, not treatment-effect prediction.

If a dataset matching this design is obtained retrospectively with participant-level raw observations and provenance, use its documented protocol unchanged. GSE153792 is not a substitute and must remain separate.

## Measurements and model roles

| Quantity | Role | Required record |
|---|---|---|
| Plasma glucose | Primary observed output | Serial concentration, specimen, assay, units, precision, actual timestamp. |
| Plasma insulin | Primary observed output and action-driver observation | Serial concentration, assay metadata, units, precision, actual timestamp. Not treated as secretion rate. |
| Plasma C-peptide | Secretion-identification observation | Serial concentration and assay data; use an explicit, cited C-peptide kinetic/deconvolution method to estimate secretion rate. Concentration is not a secretion rate. |
| Tracer enrichments | Inputs to flux-estimation procedure | Raw enrichments, tracer dosing/infusion records, assay precision, model/protocol used for flux calculation. |
| Meal rate of appearance, $R_{a,m}(t)$ | Measured/estimated forcing input to reduced model | Derived with the declared tracer method and uncertainty. The reduced model is conditional on this input; it does not predict absorption. |
| Endogenous glucose production, $HGP(t)$ | Independent flux output for comparison/parameter constraint | Tracer-derived trajectory and uncertainty; treat as an estimated reference, not exact truth. |
| Peripheral utilization, if estimable | Flux-balance comparison | Derive only with an explicitly documented tracer/balance method and uncertainty; do not label a residual as direct tissue measurement. |

## Expected qualitative behavior

- Meal-derived appearance is nonnegative during its observed appearance window and declines as the meal input is absorbed, within tracer-method resolution.
- Circulating glucose shows a meal-associated excursion relative to measured baseline; its magnitude and timing vary by participant and are observations, not prescribed constants.
- Endogenous glucose production is expected to change after the meal, often showing suppression in the cited triple-tracer physiological context (R6); its magnitude and time course in the selected T2D cohort are to be measured, not imposed from R6.
- Insulin and C-peptide responses depend on each participant's residual beta-cell function. No universal response size or direction is assumed for every participant.
- The fitted glucose balance should account for measured meal appearance, estimated hepatic production, estimated peripheral removal, and any explicitly modeled loss without a hidden residual flux.

These are qualitative hypotheses and design expectations. They do not constitute patient-level clinical predictions.

## Quantitative acceptance criteria

No numerical physiological cutoff is set here. Before data access/model fitting, preregister the following criteria using assay/tracer uncertainty and the solver error budget from the chosen protocol:

1. **Numerical closure:** cumulative glucose-pool accounting residual (initial amount + integrated inputs - integrated outputs - final amount) must be within independently estimated numerical integration error; report residual and tolerance-refinement behavior.
2. **Flux agreement:** held-out subject predictions of tracer-derived $HGP(t)$ and any independently estimable utilization flux must be compared pointwise and over the meal interval with propagated measurement/estimation uncertainty. A discrepancy outside the combined 95% uncertainty interval is a flagged mismatch, not something to remove by post hoc parameter tuning.
3. **Observation agreement:** for each held-out glucose and insulin observation define $z=(y-\hat y)/\sqrt{\sigma^2_{assay}+\sigma^2_{predictive}}$. Report residual mean, RMSE, and a preregistered goodness-of-fit statistic against the assay-based error model; flag rejection at a preregistered 0.05 significance level and inspect time-structured residuals using a prespecified test. These are proposed statistical conventions, not clinical thresholds.
4. **Uncertainty calibration:** use nominal 95% predictive intervals as a proposed statistical criterion; report empirical coverage and its subject-level binomial confidence interval, plus interval width. Treat poor coverage or intervals too broad to be informative as failure; do not judge fit from point estimates alone.
5. **Identifiability gate:** do not report individual estimates for parameters whose profile/sensitivity analysis shows they cannot be separated under this schedule. If fluxes or kinetic parameters are non-identifiable, reduce the parameter set or change the experiment before claiming success.
6. **Scope gate:** passing these criteria supports only conditional post-meal model adequacy for this protocol and sampled population. It is not clinical validation or proof of treatment-response prediction.

The assay error model, numerical tolerances, and exact goodness-of-fit statistic must be selected and frozen in a protocol before held-out evaluation. The 95% uncertainty/coverage convention and 0.05 significance level above are proposed analysis choices, not physiological reference values or facts from R2; review them before preregistration.

## Feasibility gate

This experiment requires access to a tracer-capable protocol/data source, serial hormone assays, and appropriate research approvals. If these are unavailable, the next task is source-data/access feasibility, not substituting glucose-only observations or transcriptomic data and not proceeding to individual parameter estimation.