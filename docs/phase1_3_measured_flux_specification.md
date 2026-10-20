# PhysioTwin Phase 1.3: Minimum Measured-Flux Specification

**Status:** Proposed analysis contract only. It is not implemented, no dataset currently meets it, and it makes no glucose prediction. See `phase1_3_dataset_audit.md` for the source-access findings and `phase1_3_research_design_decision.md` for the decision gate.

## 1. General Balance And Pool Definition

Start with the general mass balance:

$$
\frac{dM_G}{dt}=R_{in}-R_{out}
$$

Define $M_G(t)$ as glucose amount (mmol) in a declared, well-mixed **effective systemic glucose pool**. This pool is not total-body glucose and does not track hepatic glycogen/precursors, tissue storage, or oxidation. For a one-pool approximation using a measured systemic glucose concentration $C_G(t)$ (mmol/L):

$$
M_G(t)=V_{G,eff}C_G(t),\qquad V_{G,eff}\text{ in L}
$$

$V_{G,eff}$ is an effective model volume, not automatically plasma volume or a directly measured anatomical space. A mass-valued balance requires a source-supported value/estimator and uncertainty for this volume. If it cannot be justified, report concentration observations and fluxes separately; do not call $C_G$ a glucose mass or produce an absolute mmol residual. A concentration-form equation would still require the scale $1/V_{G,eff}$:

$$
\frac{dC_G}{dt}=\frac{R_{in}-R_{out}}{V_{G,eff}}
$$

## 2. Candidate Boundary And Flux Definitions

For a meal challenge, the narrow candidate boundary is systemic circulating glucose with meal-derived and endogenous appearance as inputs. Candidate losses are peripheral disposal and renal urinary glucose loss. Other material boundary fluxes must either be excluded with a stated, justified domain or explicitly represented; they must not be silently hidden in disposal.

| Flux | Definition and sign in pool | Units | Measurement status/method | Required alignment and limitations |
|---|---|---|---|---|
| $R_{a,m}(t)$ | Meal-derived glucose appearing in systemic circulation; positive input. | mmol/min | Estimated from meal tracer enrichment, tracer dose and a declared kinetic/tracer protocol; enrichments/doses are observations, rate is derived/model-estimated. | Same subject, meal, visit and clock as glucose. Preserve tracer infusion waveform and actual sample times. Method-specific smoothing/model uncertainty and temporal covariance must be carried. |
| $HGP(t)$ / $EGP(t)$ | Endogenous glucose production (primarily hepatic in this boundary); positive input. Use the source protocol's definition, e.g. EGP, rather than silently equating every estimate to liver-only flux. | mmol/min | Estimated from IV tracer enrichment/infusion and an explicit non-steady-state method; not directly read from a glucose assay. | Same experiment and time bins as $R_{a,m}$ and glucose. Tracer non-steady-state assumptions, enrichment errors, infusion mismatch and model dependence matter. |
| $R_d(t)$ | Aggregate glucose disposal/disappearance from the defined pool; negative term. Its tissue/storage/oxidation composition depends on the method and boundary. | mmol/min | Potentially tracer/model-estimated under a declared protocol. If calculated as the residual of this same balance, it is derived, not independently observed. | Requires a method capable of separating total disappearance and synchronized data. If only other fluxes exist, leave the combined removal residual unresolved; do not label it $R_d$. |
| $R_{renal}(t)$ | Glucose excreted in urine; negative term. | mmol/min | Derived from timed urine glucose concentration × collected urine volume divided by collection duration, with collection completeness and assay uncertainty. | Collection intervals must align to the blood/tracer analysis intervals; discrete urine collections do not identify fine-scale rates. Include when the glucose range or protocol makes omission unjustified. |
| $C_G(t)$ | Systemic plasma/serum glucose concentration; observed state-related quantity, not a flux or mass. | mmol/L | Direct assay/device observation with specimen type, calibration, precision and units recorded. | Exact timestamps and assay error needed. Plasma/serum/whole-blood readings are not silently interchangeable. |
| $M_G(t)$ | Amount in the defined pool; quantity required by the mass balance. | mmol | Derived from $V_{G,eff}C_G(t)$ under a declared one-pool/fixed-volume assumption. | Volume uncertainty and any volume-concentration covariance affect the amount difference. Concentration alone does not identify the absolute mass scale. |

### Conditional Balance

With the stated boundary and all four rates available:

$$
\frac{dM_G}{dt}=R_{a,m}+HGP-R_d-R_{renal}
$$

or in a finite interval $[t_0,t_1]$:

$$
\epsilon_M=V_{G,eff}[C_G(t_1)-C_G(t_0)]-\int_{t_0}^{t_1}\left(R_{a,m}+HGP-R_d-R_{renal}\right)dt
$$

The result $\epsilon_M$ is a measurement-plus-numerical balance residual, not a biological mechanism. If only $R_{a,m}$ and HGP are available, one may calculate:

$$
R_{loss,unresolved}^{cum}=\int_{t_0}^{t_1}(R_{a,m}+HGP)dt-[M_G(t_1)-M_G(t_0)]
$$

This is a **combined unresolved cumulative removal** only if the boundary has no other material input or loss. If renal loss, omitted sources/sinks, volume change, or pool exchange may matter, those contributions remain confounded in the residual. It is not uniquely identified peripheral disposal.

## 3. Minimum Required Data Contract

A complete analysis row set must retain, at minimum:

- Stable pseudonymous `subject_id`, `condition_id`/visit, meal/protocol identifier, source-record identifiers, and actual timestamps with timezone/elapsed-time origin documented.
- Same-subject glucose concentrations and specimen/assay metadata; tracer enrichment observations and tracer dose/infusion schedules; flux estimates with the method and version that generated them; and uncertainty/covariance information.
- A supported effective pool volume (or an explicit decision to restrict output to a concentration-equivalent balance that does not claim absolute mass).
- Independent disposal estimate if $R_d$ is to be named as a flux, and timed urinary glucose measurements if renal loss is included or its omission cannot be justified.
- Missingness flags and quality-control/exclusion records. No joining across unrelated studies, subjects, meals or visits; no row-order matching; no replacement of an absent flux with a population average or zero.

The published protocol's sampling schedule must be used or prospectively justified. No universal sample interval is assigned here: sampling must resolve the meal appearance and tracer transients at the temporal resolution claimed, with actual collection times retained. Flux estimates commonly depend on neighboring observations and a kinetic estimation procedure; they are not independent point samples just because they are exported on a regular grid.

## 4. Time Alignment And Numerical Integration

Use a shared elapsed-time axis for same-subject measurements from the same experiment. Preserve original times. Predefine how asynchronous glucose assays, tracer samples, infusion rates and timed urine collections are aligned. Do not interpolate across long gaps or extrapolate beyond the observed window without a validated method.

For an interval balance, integrate fluxes on the observation interval using the documented estimator and a predeclared quadrature appropriate to its time support (for example, trapezoidal integration of an explicitly interpolated rate curve). Report interpolation/integration uncertainty and sensitivity to time-grid choices. Do not differentiate noisy glucose samples as the primary balance check when the integrated endpoint form is available. A solver is not needed for an accounting identity and must not be used to invent missing measurements.

## 5. Uncertainty And Residual Interpretation

Let $\Delta M=V_{G,eff}(C_1-C_0)$ and let the integrated signed flux sum be $F=\int(R_{a,m}+HGP-R_d-R_{renal})dt$. Then $\epsilon_M=\Delta M-F$. Its uncertainty must include:

- glucose assay error and endpoint covariance;
- uncertainty in $V_{G,eff}$ and its dependence/covariance with glucose or tracer-derived estimates;
- tracer enrichment, infusion, kinetic-method and flux-estimation uncertainty;
- temporal covariance among estimated rates and covariance between glucose and flux estimates when shared data/methods induce it;
- time alignment, interpolation, numerical quadrature, urine collection and incomplete-collection uncertainty as relevant.

In general,

$$
\operatorname{Var}(\epsilon_M)=\operatorname{Var}(\Delta M)+\operatorname{Var}(F)-2\operatorname{Cov}(\Delta M,F)
$$

and $\operatorname{Var}(F)$ must account for covariance over time, not assume independent pointwise flux errors without evidence. No numerical uncertainty can be propagated from the records currently available because no aligned physiological observations or assay/tracer covariance data were obtained. Report the residual with an uncertainty interval and methods; do not use it to tune a closure.

## 6. Narrowest Defensible Initial Calculation

**Current evidence does not support a complete measured-flux balance.** If a suitable future or newly accessed dataset provides same-subject serial glucose, $R_{a,m}$ and HGP, and a supported $V_{G,eff}$, the first defensible calculation is an interval glucose-pool change minus integrated measured/estimated inputs. Report the remaining term as unresolved combined removal (including unmeasured renal/other boundary fluxes), with propagated uncertainty. Do not call it measured $R_d$, fit it into the current $CL_G+S_XX$ closure, or claim future prediction.

To extend this to a complete bounded balance, independently estimate $R_d$ and measure/justify $R_{renal}$ over the same intervals, and state the included-pool assumptions. If those quantities or effective volume are unavailable, report the narrower concentration/flux comparison only. This does not require insulin, C-peptide, $X$, or the current ODE for the glucose accounting identity; those measurements are needed for separate mechanistic questions about secretion and insulin action.

## 7. Explicit Assumptions And Unresolved Questions

**Assumptions for the proposed calculation:** fixed effective volume over the interval; well-mixed pool; compatible units and timing; stated boundary; a valid flux-estimation method; and no omitted material boundary process unless it remains in an unresolved residual.

**Unresolved:** Which exact dataset/protocol provides the matched flux observations? What defines the systemic glucose pool and $V_{G,eff}$? Does the tracer method provide independent $R_d$ or only a net residual? Is renal loss relevant in the selected population/domain? What are assay/tracer errors and their temporal correlations? What temporal resolution is supportable by the sampling schedule? These decisions require source-data and scientific review before implementation.

**Not claimed:** a complete presently available dataset, a validated physiological model, individualized parameter identification, a predicted glucose trajectory, clinical validity, or digital-twin status.
