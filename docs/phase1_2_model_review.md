# PhysioTwin Phase 1.2: Scientific Model-Structure Review

## Decision

The current three-state model is **not defensible for calibration or physiological prediction in its present form**. Its equations are dimensionally coherent accounting equations and the implementation is reproducible, but most constitutive functions and all numeric values are hypothetical. Ordinary glucose and insulin observations do not distinguish the mechanisms assigned to those functions; several parameter combinations are structurally or practically confounded.

Recommend **Option B as the next scientific work package**: use independently measured or method-estimated meal appearance and endogenous glucose production as inputs, use secretion estimates only when supported by C-peptide kinetic analysis, and compare the glucose-pool balance to independently supported glucose disposal where available. Treat this initially as conditional flux accounting, not a calibrated forward predictor. Keep Option A only as a deterministic software/solver test. Defer Option C until full equations, parameters, protocol, data, and reference results for a selected publication are accessible. No implementation or baseline change is authorized by this review.

## Scope And Evidence Standard

The current boundary is a fixed-volume systemic glucose pool plus systemic insulin concentration and a latent aggregate action state. Glucose enters from meal appearance and endogenous hepatic production, and leaves through aggregate disposal; renal loss is omitted. Insulin secretion enters portal blood, a fraction is removed by a lumped hepatic first-pass term, and systemic insulin is cleared. This is not a whole-body carbon balance. The Phase 1.1 run is an internally consistent hypothetical example, not evidence for these closures.

The references support the existence, importance, measurement, or modeling of the listed physiological processes. They do **not** validate the particular Phase 1.0 functional forms. Numeric parameter values in `experiments/phase1_initial/config.v1.json` have no traceable published source and are not estimates. “Identifiable” below distinguishes structural information from practical identifiability in the proposed one-meal design; no identifiability analysis has yet been run on data.

## Closure-by-Closure Assessment

### 1. Meal appearance

**Current definition.**

$$
q_m(t)=\begin{cases}\frac{t}{\tau_m^2}e^{-t/\tau_m},&t\geq0\\0,&t<0\end{cases},\qquad R_{a,m}(t)=M_{abs}q_m(t)
$$

Here $q_m$ is in min$^{-1}$, $M_{abs}$ in mmol, and $R_{a,m}$ in mmol/min. The biological interpretation is meal-derived glucose appearance in the systemic pool after the unmodeled gut/splanchnic processes; this is an external forcing, not an absorption state.

**Evidence and form.** Tracer studies estimate meal appearance. R1 reports use of triple-tracer-derived meal appearance and subsystem forcing functions; R6 describes a triple-tracer protocol designed to reduce non-steady-state error when estimating meal appearance and endogenous production. That evidence supports measuring or supplying $R_{a,m}(t)$, not the shape-2 gamma form, its time scale, or an absorbed amount inferred from a meal label. The local gamma function is an illustrative mathematical assumption.

**Domain and limitations.** Nonnegative time and appearance, one meal beginning at time zero, known absorbed amount, fixed single-peaked profile, and no uncertainty in the input are assumed. It cannot predict gastric emptying, absorption, splanchnic extraction, meal composition effects, or multiple irregular inputs. The Phase 1.1 horizon captured 99.9964% of this hypothetical gamma integral, but this numerical normalization does not establish that the profile resembles a real meal.

**Parameters and identifiability.** $M_{abs}$ (mmol) and $\tau_m$ (min) are hypothetical. With an externally supplied tracer-derived rate curve, neither is needed as a fitted closure parameter. They cannot be separately inferred reliably from glucose concentration alone because hepatic production and disposal also affect the same net pool slope. Dense tracer enrichment, meal and tracer dosing records, and uncertainty in the flux-estimation method are needed to estimate meal appearance.

### 2. Hepatic glucose production

**Current definition.**

$$
HGP=HGP_0\phi_H(I),\qquad \phi_H(I)=\frac{1}{1+\max(I-I_{ref},0)/K_H}
$$

$HGP$ and $HGP_0$ are mmol/min; $I$ and $I_{ref}$ are pmol/L; $K_H$ is pmol/L. It represents endogenous hepatic glucose appearance, instantaneously suppressed by systemic insulin above a selected reference.

**Evidence and form.** Meal studies measure or estimate endogenous glucose production. R6 reports post-meal suppression under its triple-tracer protocol. This supports the relevance of the flux and a context-specific suppression observation; it does not establish a reciprocal hinge, a threshold at $I_{ref}$, an instantaneous response, a monotone law over all conditions, or systemic insulin as a proxy for portal/hepatic exposure. The local reciprocal hinge is explicitly proposed, not a published equation.

**Domain and limitations.** The closure restricts HGP to $(0,HGP_0]$ and makes it nonincreasing in systemic insulin. It omits glucagon, portal insulin, hepatic action delay, substrate availability, glycogen, circadian regulation, and other state dependence. At the Phase 1.1 nadir, the assumed response gives 0.319 mmol/min from a hypothetical 1 mmol/min scale; at peak insulin it falls to 0.132 mmol/min. These are outputs of the assumption, not externally observed physiology.

**Parameters and identifiability.** $HGP_0$ (mmol/min), $I_{ref}$ (pmol/L), and $K_H$ (pmol/L) are hypothetical/unassigned. $HGP_0$ is not identifiable from glucose alone. $I_{ref}$ and $K_H$ can trade off over a limited insulin range, and HGP cannot be separated from meal appearance or disposal using only the glucose slope. Tracer-derived HGP across the meal, serial insulin, and a declared model for tracer uncertainty are required; a one-meal design may still not identify all response parameters.

### 3. Beta-cell insulin secretion

**Current definition.**

$$
S_\beta(G)=S_{\beta,0}+k_\beta\max(G-G_\beta,0)
$$

$S_\beta$ and $S_{\beta,0}$ are pmol/min; $G$ and $G_\beta$ are mmol/L; $k_\beta$ is pmol L/(min mmol). It represents pancreatic secretion into portal blood as an instantaneous function of glucose alone.

**Evidence and form.** Glucose-responsive secretion is a relevant process, and R1/R2 report modeling insulin secretion. R7 documents estimation of insulin secretion rates from plasma C-peptide using a two-compartment C-peptide kinetic model. Neither source supports this thresholded-affine law, its threshold, its lack of delay, or a constant secretion floor. The glucose-only law also omits incretin and other regulation; no secretion or C-peptide observation model exists in the current engine.

**Persistent floor concern.** The illustrative closure continues $S_{\beta,0}=40$ pmol/min at every glucose at or below 4.5 mmol/L. With $E_H=0.35$, it still introduces 26 pmol/min systemically. Under $CL_I=0.12$ L/min, that floor alone corresponds to an insulin equilibrium of $216.7$ pmol/L. The Phase 1.1 final insulin, 220.2 pmol/L, is close to this value. This is a direct mathematical consequence of the closure and parameter set; it is not evidence that secretion remains constant at low glucose.

**Domain and limitations.** Nonnegative glucose and secretion are enforced by construction. The kink at $G_\beta$ is not a demonstrated biological threshold. A constant floor across fasting and low glucose can dominate late behavior, and the affine response is unbounded at high glucose. Delays, glucose rate-of-change effects, beta-cell impairment/heterogeneity, and non-glucose regulators are absent.

**Parameters and identifiability.** $S_{\beta,0}$ (pmol/min), $G_\beta$ (mmol/L), and $k_\beta$ (pmol L/(min mmol)) are hypothetical. Glucose plus insulin alone cannot distinguish secretion from hepatic extraction and systemic clearance. Serial C-peptide with assay data and an explicit, justified kinetic/deconvolution model can support secretion estimates (R7); it does not automatically identify insulin extraction or clearance. Dense glucose/C-peptide observations and an adequate stimulus range are needed to estimate a response curve.

### 4. Hepatic insulin extraction and systemic insulin clearance

**Current definition.**

$$
V_I\frac{dI}{dt}=(1-E_H)S_\beta-CL_I I
$$

$V_I$ is L, $I$ is pmol/L, $E_H$ is dimensionless, $S_\beta$ is pmol/min, and $CL_I$ is L/min. $E_HS_\beta$ is the portal secretion removed before systemic appearance; $CL_I I$ is a proposed first-order systemic sink.

**Evidence and form.** First-pass extraction and systemic clearance are distinct physiological processes, and insulin kinetics are needed to quantify circulating insulin. The registry correctly labels $E_H$ and $CL_I$ unresolved. No source in the current evidence package supports a fixed individual extraction fraction, this exact first-order systemic clearance closure, or the configured values. R7 concerns C-peptide kinetics and secretion inference; it is not a source for insulin clearance kinetics.

**Domain and limitations.** The model assumes fixed effective insulin distribution volume, constant extraction fraction, and clearance proportional to systemic concentration. It has no portal/systemic compartments, time-varying clearance, or insulin kinetic measurement model. It predicts no C-peptide despite the proposed experiment using C-peptide to infer secretion.

**Parameters and identifiability.** $V_I$ (L), $E_H$ (dimensionless), and $CL_I$ (L/min) are unassigned/hypothetical. Written as a concentration derivative, $dI/dt=((1-E_H)/V_I)S_\beta-(CL_I/V_I)I$. With only $I(t)$, ratios and the unknown secretion function are confounded; $E_H$, secretion scale, $V_I$, and clearance cannot be separated. C-peptide-derived secretion plus suitable insulin kinetic data may help, but extraction still requires a defined portal-to-systemic model or independent information. Plasma insulin alone is insufficient.

### 5. Peripheral glucose disposal

**Current definition.**

$$
R_d=(CL_G+S_XX)G
$$

$R_d$ is mmol/min; $CL_G$ and $S_X$ are L/min; $X$ is dimensionless; $G$ is mmol/L. It represents aggregate peripheral removal with an insulin-independent baseline clearance plus a component proportional to the latent action signal.

**Evidence and form.** Glucose utilization is a measurable/modelled flux in R1 and triple-tracer work. Bergman et al. (R4) compared seven glucose-disappearance models in conscious dogs after intravenous glucose, using measured insulin as input and glucose as output; their selected nonlinear model yielded an insulin-sensitivity index from a ratio of parameters. This is evidence that glucose disappearance can be modeled under a specific perturbation, not evidence for this linear-in-$G$ two-term closure or transport to a human mixed meal/T2D cohort.

**Domain and limitations.** This closure is nonnegative for nonnegative states and scales linearly with glucose. It collapses tissue uptake, storage, oxidation, glucose effectiveness, renal loss, and other disposal into one term or omits them. The model cannot interpret $R_d$ as a direct tissue flux without independent support. In the baseline run, disposal integrated to 222.63 mmol and exceeded total inputs by 44.58 mmol; numerical balance closure verifies the implemented accounting, not the biological plausibility of this disposal trajectory.

**Parameters and identifiability.** $CL_G$ and $S_X$ are both L/min and hypothetical. Glucose concentration alone observes net appearance minus removal; $CL_G$ and insulin-dependent removal trade off with $R_{a,m}$ and HGP. Tracer-derived flux data can constrain disposal, but if disposal is computed as a residual from the same glucose balance it is not an independent validation target. Independent flux measurements or a perturbation with predeclared observation model are needed.

### 6. Delayed insulin-action state

**Current definition.**

$$
\frac{dX}{dt}=k_XI-\frac{X}{\tau_X}
$$

$X$ is dimensionless; $k_X$ is L/(pmol min); $I$ is pmol/L; and $\tau_X$ is min. It is an unobserved first-order low-pass filter from systemic insulin to aggregate peripheral action.

**Evidence and form.** Dynamic insulin action is a recognized modeling concept. R4 provides a glucose-disappearance/insulin-sensitivity modeling precedent under IV glucose perturbation. That precedent does not select the present latent-state equation, its direct systemic-insulin drive, its time constant, or its use as the sole mediator of aggregate peripheral uptake in a T2D meal response. The filter is a proposed closure.

**Structural identifiability issue.** The absolute scale of $X$ is unobserved. For any $c>0$, the transformations $X'=cX$, $k_X'=ck_X$, and $S_X'=S_X/c$ leave both the transformed action equation and the product $S_XX$ in $R_d$ unchanged (with the initial action state transformed consistently). Therefore $k_X$ and $S_X$ cannot be separately identified from $G$ and $I$ trajectories under this model without fixing a scale by convention or observing an independent quantity related to $X$. Even the effective action gain and $\tau_X$ can be practically confounded with $CL_G$, hepatic response, and the input fluxes in a single meal.

**Domain and limitations.** This linear filter has one time scale, no saturation, no explicit effect compartment observation, no independent hepatic action, and no effect of glucose on action dynamics. $X_0=k_XI_0\tau_X$ is equilibrium of the isolated filter under constant initial insulin, not a measured fasting action state or a full-system steady state. Serial glucose and insulin alone do not validate $X$.

**Parameters and identifiability.** $k_X$ (L/(pmol min)), $\tau_X$ (min), and $S_X$ (L/min) are hypothetical. Dense serial insulin/glucose, known flux inputs, informative perturbations, and a declared scale constraint are prerequisites even for estimating an effective action dynamic. The proposed one-meal observation design does not establish separate individual values.

## What The Available Observables Can Distinguish

The proposed experiment has serial glucose, insulin, C-peptide, and tracer enrichments. These are more informative than glucose/insulin alone, but its exact protocol, data access, sampling schedule, and error model are not yet selected.

- **Glucose only:** observes the net pool slope. It cannot separate $R_{a,m}$, HGP, $R_d$, or omitted losses, nor identify insulin secretion/action mechanisms.
- **Glucose plus systemic insulin:** adds an observed association, but secretion, extraction, clearance, HGP, disposal, and latent action still trade off.
- **Add C-peptide with a declared kinetic model:** supports endogenous secretion-rate estimation. It does not, by itself, identify hepatic extraction, insulin distribution volume, or systemic insulin clearance.
- **Add validated triple-tracer flux estimates:** supports meal appearance and HGP estimates with method uncertainty. Disposal may be estimable only if the selected protocol supports it; a balance residual alone is not independent evidence.
- **Volume and latent-scale confounding:** $V_G$ and $V_I$ are effective volumes, not observed anatomical quantities. Concentration data alone do not set amount scales. The $k_X$/$S_X$ scale symmetry is structural, not merely a low-power-data issue.

The three states are therefore not sufficient to distinguish the mechanisms named in the research question from the measurements currently specified. A structural/practical identifiability analysis on a locked observation model is a gate before parameter estimation. No dataset or uncertainty model is currently present to run that analysis.

## Published Alternatives And Comparison

The following descriptions are limited to verified publications/abstracts. No equations are attributed to an inaccessible full text.

| Published work | Verifiable model/method evidence | Relevance and limits for PhysioTwin |
|---|---|---|
| Dalla Man, Rizza & Cobelli, 2007 (R1) | The abstract describes a postprandial glucose-insulin simulation model, subsystem decomposition, and parametric subsystem models developed with a forcing-function strategy. A triple-tracer meal database provided quasi-model-independent estimates of meal appearance, endogenous production, glucose utilization, and insulin secretion; the strategy was also applied to a smaller T2D database. | A relevant published meal-model and flux-rich identification precedent. The exact equations, parameters, and observation model are not included in the accessible source material reviewed here, so it is not a formula library to copy or a model reproduced by this repository. |
| Bergman et al., 1979 (R4) | The abstract reports seven glucose-disappearance models evaluated after IV glucose in conscious dogs, with measured insulin as input and glucose as output; a nonlinear model was selected and insulin sensitivity was a ratio of model parameters. | Demonstrates a perturbation-specific mechanistic route for estimating an insulin-sensitivity index. It is not a meal-appearance, beta-cell secretion, or T2D meal model, and its exact selected equation is not transcribed here. |
| Basu et al., 2003 (R6) | A triple-tracer protocol was designed to reduce non-steady-state bias in estimating meal appearance and endogenous production; the abstract contrasts it with dual-tracer one-compartment estimates. | Supports improving the measurement/input and flux side of Option B. It is a tracer methodology, not a glucose-insulin ODE closure. |
| Van Cauter et al., 1992 (R7) | The abstract describes estimating insulin secretion from plasma C-peptide with a two-compartment distribution/degradation model and evaluates standard versus individual kinetic parameters. | Supports an explicit secretion-observation/deconvolution path. It does not identify insulin extraction/clearance from C-peptide alone and is not evidence for the Phase 1 thresholded-affine secretion law. |
| Visentin, Cobelli & Dalla Man, 2020 (R2; Padova T2D simulator) | The abstract reports a 15-differential-equation, 39-parameter glucose/insulin/C-peptide meal model identified in 51 T2D subjects using a single triple-tracer mixed meal, and reports simulated glucose, insulin, and C-peptide outputs. | The most directly relevant T2D benchmark. The full equations, parameter table, detailed protocol, and executable reference implementation were not available in the prior access audit. Reproducing it from the abstract would be guesswork; no Padova equation is claimed or copied here. |

### Options

| Option | Scientific defensibility now | Data and effort | Fit to intended question |
|---|---|---|---|
| **A. Retain current equations as an illustrative software test** | Acceptable only for solver, serialization, and software-invariant tests if every parameter and closure stays labeled hypothetical. Not defensible for calibration, physiological interpretation, or prediction. | Minimal data and effort; no identifiability or physiological validation possible. | Useful as a code fixture, but does not answer the flux-identifiability question. |
| **B. Replace unsupported closures with externally specified measured fluxes** | Strongest immediate scientific option if the fluxes come from a protocol-specific, documented method with uncertainty. It tests a bounded glucose-pool balance without pretending the current insulin/action closures are established. | Requires access to serial glucose, tracer-derived meal appearance and HGP, and a justified disposal estimate; C-peptide kinetics are needed for secretion work. Data access/protocol feasibility is unresolved. Moderate effort after the data/protocol gate. | Best match to the proposed first question: whether measured fluxes support a conditional post-meal balance and what is identifiable. It does not predict absorption or provide a fully coupled forward simulator. |
| **C. Reproduce a published mechanistic model** | Potentially strongest model-level provenance if one exact model version, equations, parameter sources, inputs, and reference outputs are obtained and independently checked. | Highest transcription, unit audit, implementation, and benchmark effort; needs full article/supplement/code and matched data/protocol. Those are currently unavailable for R2. | Appropriate later if the goal shifts to faithful reproduction/benchmarking; not defensible to reconstruct Padova from its abstract. |

## Recommendation And Review Gate

Choose **B** for the next scientific phase, conditionally on obtaining a suitable flux-rich dataset or protocol. Begin with a measured-flux glucose-pool accounting analysis and propagate tracer uncertainty. Only retain a forward closure when its form is justified, its parameters have a data source, and the observation schedule can identify the parameters needed. Treat C-peptide as an external secretion-identification measurement until a C-peptide state/observation model is explicitly selected. Keep the current v1 run under A as a reproducible software fixture, not as a physiological baseline.

If suitable flux data cannot be accessed, do not calibrate the current equations. Resolve data feasibility or pursue the full-text/source-access gate for a published model. A separate scientific review must decide the glucose domain, renal-loss omission, effective-volume handling, secretion method, insulin kinetic information, disposal reference, and the allowable estimable parameter subset. This document does not select replacement equations or numeric values.

## Sources

- **R1.** Dalla Man C, Rizza RA, Cobelli C. “Meal Simulation Model of the Glucose-Insulin System.” *IEEE Transactions on Biomedical Engineering*. 2007;54(10):1740-1749. [DOI](https://doi.org/10.1109/TBME.2007.893506); [PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/17926672/).
- **R2.** Visentin R, Cobelli C, Dalla Man C. “The Padova Type 2 Diabetes Simulator from Triple-Tracer Single-Meal Studies: In Silico Trials Also Possible in Rare but Not-So-Rare Individuals.” *Diabetes Technology & Therapeutics*. 2020;22(12):892-903. [DOI](https://doi.org/10.1089/dia.2020.0110); [PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/32324063/).
- **R4.** Bergman RN, Ider YZ, Bowden CR, Cobelli C. “Quantitative estimation of insulin sensitivity.” *American Journal of Physiology*. 1979;236(6):E667-E677. [DOI](https://doi.org/10.1152/ajpendo.1979.236.6.E667); [Crossref abstract/metadata](https://api.crossref.org/works/10.1152/ajpendo.1979.236.6.E667).
- **R6.** Basu R, Di Camillo B, Toffolo G, et al. “Use of a novel triple-tracer approach to assess postprandial glucose metabolism.” *American Journal of Physiology-Endocrinology and Metabolism*. 2003;284(1):E55-E69. [DOI](https://doi.org/10.1152/ajpendo.00190.2001); [PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/12485809/).
- **R7.** Van Cauter E, Mestrez F, Sturis J, Polonsky KS. “Estimation of insulin secretion rates from C-peptide levels. Comparison of individual and standard kinetic parameters for C-peptide clearance.” *Diabetes*. 1992;41(3):368-377. [DOI](https://doi.org/10.2337/diab.41.3.368); [PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/1551497/).