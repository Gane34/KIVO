# Phase 1 Pre-Implementation Review and Illustrative Closures

## Decision boundary

This note defines the **software-testable illustrative closure** used by the first engine. It does not amend the evidence status of the candidate model in `physiology_specification.md`, resolve the research questions in `model_selection.md`, or claim a biologically identified functional form. The experiment is deterministic and hypothetical. Its parameter values are not published constants, patient data, or fitted values.

The written glucose-pool, systemic insulin, and action-state balances are sufficiently specified structurally to implement. Three constitutive/input functions are not specified by the literature audit or the parameter registry: the meal appearance time course, hepatic insulin response, and glucose-dependent beta-cell secretion. For an illustrative software test only, this note freezes those functions as below. They must be scientifically reviewed before the functions are treated as the approved physiological model.

## States and units

| State | Definition | Unit | Boundary interpretation |
|---|---|---|---|
| $Q_G$ | Amount of glucose in the effective systemic pool | mmol | $Q_G=V_GG$; not total-body glucose. |
| $I$ | Systemic insulin concentration | pmol/L | After a lumped portal/hepatic first-pass loss; not pancreatic secretion. |
| $X$ | Aggregate delayed peripheral insulin-action state | dimensionless | Latent mathematical state, not a measured concentration. |

Time is minutes. Glucose concentration is $G=Q_G/V_G$ in mmol/L. The pool boundary receives meal appearance and hepatic production, loses aggregate peripheral utilization, and sets renal loss to zero for this restricted illustrative scenario. No storage, oxidation, hepatic precursor, glucagon, incretin, gut, tissue, or C-peptide states are represented.

## Implemented candidate balances

$$\frac{dQ_G}{dt}=R_{a,m}(t)+HGP(t)-R_d(t), \qquad G=\frac{Q_G}{V_G}.$$

$$V_I\frac{dI}{dt}=(1-E_H)S_\beta(G)-CL_I I.$$

$$\frac{dX}{dt}=k_X I-\frac{X}{\tau_X}, \qquad R_d=(CL_G+S_X X)G.$$

All right-hand glucose fluxes have units mmol/min. $V_I dI/dt$, systemic insulin appearance, and clearance have units pmol/min. Both terms in $dX/dt$ have units min$^{-1}$.

## Explicit illustrative closures

### Meal appearance

Use a normalized shape-2 gamma forcing function:

$$q_m(t)=\begin{cases}\frac{t}{\tau_m^2}e^{-t/\tau_m},&t\geq0,\\0,&t<0,\end{cases} \qquad R_{a,m}(t)=M_{abs}q_m(t).$$

$q_m$ has units min$^{-1}$ and integrates to one over $[0,\infty)$. $M_{abs}$ is a hypothetical absorbed amount for this demonstration, not inferred from a meal label. A finite simulation horizon can leave a small tail unapplied; diagnostics report the integrated amount actually delivered. The gamma shape and time scale are convenient forcing assumptions, not a gastric or absorption mechanism established by R1/R2.

### Hepatic production

$$\phi_H(I)=\frac{1}{1+\max(I-I_{ref},0)/K_H}, \qquad HGP=HGP_0\phi_H(I).$$

Here $HGP_0$ is the production scale at or below the illustrative reference insulin $I_{ref}$; $K_H$ is a positive concentration scale. This closure is bounded in $(0,1]$ and nonincreasing in $I$. It is a deliberately simple shape chosen to satisfy the candidate qualitative constraint, not an equation or parameterization extracted from Padova or another source. The abrupt derivative change at $I=I_{ref}$ is an illustrative convenience, not a physiological threshold claim.

### Beta-cell secretion

$$S_\beta(G)=S_{\beta,0}+k_\beta\max(G-G_\beta,0).$$

$S_{\beta,0}$ has units pmol/min, $G_\beta$ has units mmol/L, and $k_\beta$ has units pmol L/(min mmol). This nonnegative thresholded affine rule is only a mathematical glucose-responsive closure. Its threshold, gain, lack of delay, and omission of incretin/neural regulation are not established physiology.

### Restricted initial conditions and admissible domain

Require all amounts/concentrations and flux-scale/gain parameters to be finite and nonnegative; volumes, time constants, and $K_H$ must be positive; $0\leq E_H<1$. For the illustrative scenario, initialize $X(0)=k_X I(0)\tau_X$, the steady state of the isolated action filter at the initial insulin concentration. This is a mathematical initialization rule, not a fasting measurement or inferred patient state.

With these constraints, $R_{a,m},HGP,R_d,S_\beta$ are nonnegative for nonnegative states. At $Q_G=0$, glucose uptake is zero and other glucose terms are nonnegative; at $I=0$, insulin appearance is nonnegative; at $X=0$, its derivative is nonnegative. Positivity is therefore expected in the continuous system on this domain, but numerical excursions are checked and never hidden by clipping.

## Evidence versus assumption

- **Evidence-supported at the level of need/measurement:** meal appearance, endogenous production, glucose utilization, insulin secretion, and postprandial glucose/insulin responses are reported measurable/modelled quantities in R1/R2. R6 supports triple-tracer measurement of meal appearance and endogenous production; R7 supports C-peptide kinetic estimation of secretion.
- **Structural balance choice:** the state balances conserve the modeled glucose pool and systemic insulin amount under the declared boundary. This accounting identity is a model structure, not proof that the omitted whole-body pools are conserved.
- **Illustrative assumptions:** gamma-2 meal forcing; reciprocal hinge hepatic response; thresholded affine beta secretion; constant effective distribution volumes; first-order systemic insulin clearance; one linear action filter; aggregate linear-in-glucose uptake; zero renal loss; no added hormone/drug/tissue mechanisms; hypothetical config values.
- **No traceable numeric source values:** no numerical parameter or concentration in the included illustrative configuration is represented as a published value. The initial $X$ is derived from the documented isolated-filter initialization rule; the initial glucose and insulin values are hypothetical scenario inputs and are not a steady-state claim.

## Dimensional audit

| Expression | Unit calculation | Result |
|---|---|---|
| $M_{abs}q_m$ | mmol x min$^{-1}$ | mmol/min |
| $V_GG$ | L x mmol/L | mmol |
| $R_{a,m}+HGP-R_d$ | mmol/min terms | mmol/min |
| $V_I dI/dt$ | L x pmol/(L min) | pmol/min |
| $CL_I I$ | L/min x pmol/L | pmol/min |
| $k_X I$ | L/(pmol min) x pmol/L | min$^{-1}$ |
| $X/\tau_X$ | dimensionless/min | min$^{-1}$ |
| $(CL_G+S_X X)G$ | L/min x mmol/L | mmol/min |
| $k_\beta(G-G_\beta)$ | pmol L/(min mmol) x mmol/L | pmol/min |

## Decisions still requiring scientific review

1. Are the gamma forcing, hepatic hinge, and beta-cell secretion functions acceptable at all, even for an illustrative reduced model, or should one/all remain injectable external functions until source data are available?
2. Should meal appearance be measured input only, or should the model include validated absorption kinetics?
3. Can an insulin-only driven $X$ state be identified separately from uptake gains under the proposed experiment?
4. Which distribution volumes and kinetic parameters can be independently measured or fixed without unsupported values?
5. What glucose range justifies omitting renal loss and other regulation?
6. Are the numerical display values in the illustrative configuration acceptable as arbitrary computational examples, clearly separated from physiological parameters?

Phase 1 should not silently promote these closures into the scientific specification. A review may retain, replace, or remove them before any calibration or patient-level interpretation.