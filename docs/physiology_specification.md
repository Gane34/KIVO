# Physiology Specification

## Status and notation

This is a candidate specification, not an implemented or validated model. A fixed-volume, well-mixed systemic glucose pool and a systemic insulin concentration are proposed abstractions. Published literature supports the existence and measurable importance of meal appearance, endogenous glucose production, glucose utilization, insulin secretion, and insulin action; the particular closures below are not established by that evidence. No parameter values are assigned.

Concentrations use mmol/L for glucose and pmol/L for insulin; time uses minutes; amounts use mmol or pmol. All rates are per minute. Volumes are effective distribution volumes, not asserted anatomical measurements. Symbols are listed in `parameter_registry.csv`.

## System boundary

The modeled glucose pool is systemic circulating glucose. Its boundary receives glucose from meal appearance and hepatic endogenous production and loses glucose through aggregate peripheral utilization and, when modeled, renal excretion. The model does not explicitly conserve total-body glucose: hepatic production draws on unmodeled glycogen/gluconeogenic substrates, and peripheral uptake is not followed into tissue stores or oxidation. Therefore, the balance is a pool balance, not a whole-body carbon balance.

The insulin subsystem represents pancreatic secretion into portal blood, a lumped hepatic first-pass extraction fraction, and systemic plasma insulin clearance. A single delayed action state represents aggregate peripheral insulin action. Direct hepatic suppression by systemic insulin is an instantaneous candidate closure; portal insulin exposure and hepatic signaling delay are not separately resolved.

## Candidate states

| State | Definition | Units | Biological interpretation / caveat |
|---|---|---|---|
| $Q_G$ | $V_G G$ | mmol | Amount of glucose in the effective systemic glucose pool; $G$ is derived concentration and $V_G$ is assumed fixed. |
| $I$ | systemic insulin concentration | pmol/L | Circulating insulin after portal delivery and hepatic extraction; it is not a direct measurement of secretion. |
| $X$ | aggregate peripheral insulin-action state | dimensionless | Positive delayed action signal driven by systemic insulin. It is an abstract model state, not a directly measured biological concentration. |

Candidate initial conditions are measured fasting values for $G$ and $I$ and a defined consistent initialization for $X$. They must not be assigned arbitrary defaults. Whether fasting steady state can determine $X$ and the basal fluxes is a calibration question.

## Candidate fluxes

| Flux | Sign in glucose pool | Units | Definition / status |
|---|---:|---|---|
| $R_{a,m}(t)$ | + | mmol/min | Meal-derived rate of appearance into systemic circulation. Supplied from a justified measurement/model input; no gastric-emptying mechanism is chosen here. |
| $HGP(t)$ | + | mmol/min | Endogenous hepatic glucose production. Proposed to be modulated by insulin; exact response function is unresolved. |
| $R_d(t)$ | - | mmol/min | Aggregate peripheral glucose utilization, including basal and insulin-action-dependent components. Tissue-specific partition is deferred. |
| $R_{renal}(t)$ | - | mmol/min | Renal glucose loss. Set to zero only for a stated use domain where this omission is justified; otherwise it is an omitted boundary flux. |
| $S_\beta(t)$ | source to insulin | pmol/min | Pancreatic insulin secretion into portal blood; glucose is the only candidate input in v1. Incretin, neural, and other regulation are omitted. |
| $CL_I I$ | sink from insulin | pmol/min | First-order systemic insulin clearance candidate; $CL_I$ is an effective clearance, not a fixed literature constant. |

## Candidate governing equations

**1. Meal appearance input.** A dose-normalized forcing function is one possible representation:

$$R_{a,m}(t) = M_{abs} q_m(t), \qquad q_m(t) \ge 0, \qquad \int_{t_0}^{t_1} q_m(t)\,dt = 1.$$

$M_{abs}$ is the absorbable meal-derived glucose amount in mmol and $q_m$ has units min$^{-1}$. This preserves the declared absorbed amount over the modeled interval. Neither the absorbable fraction nor the time course may be guessed; use tracer-derived appearance or document the source of the forcing input. A mechanistic gut model is deferred.

**2. Systemic glucose amount balance.**

$$\frac{dQ_G}{dt} = R_{a,m}(t) + HGP(t) - R_d(t) - R_{renal}(t), \qquad G = \frac{Q_G}{V_G}.$$

Each term on the right is mmol/min. For the narrowly scoped initial candidate, $R_{renal}=0$ is an explicit assumption, not a universal physiological fact. A nonzero renal term requires a justified relationship and data, particularly for marked hyperglycemia.

**3. Hepatic glucose production.**

$$HGP(t) = HGP_0\,\phi_H(I(t);\theta_H).$$

$HGP_0$ is a basal scale in mmol/min. As candidate constraints, $0\leq\phi_H\leq1$ and $\partial\phi_H/\partial I\leq0$ over the modeled domain; the intended qualitative hypothesis is that increasing insulin does not increase hepatic production over that domain. The function form, parameters, and whether systemic insulin is an adequate proxy for portal/hepatic exposure are unresolved. This equation is a proposed closure, not a directly established law.

**4. Pancreatic insulin and systemic clearance.**

$$V_I\frac{dI}{dt} = (1-E_H)S_\beta(G(t);\theta_\beta) - CL_I I(t).$$

$V_I dI/dt$ and both fluxes have units pmol/min. $S_\beta$ is pancreatic secretion into portal blood (pmol/min); $E_H$ is a dimensionless hepatic first-pass extraction fraction; $CL_I$ has units L/min. The proposed glucose-only secretion function must be nonnegative and glucose-responsive in the intended range. Its baseline, response shape, delay, and dependence on other regulators are unresolved. If data cannot identify $E_H$ and secretion separately, an effective systemic insulin appearance term may be used instead, but must not be mislabeled as direct pancreatic secretion.

**5. Peripheral insulin action and utilization.**

$$\frac{dX}{dt} = k_X I - \frac{X}{\tau_X}, \qquad R_d(t) = \bigl(CL_G + S_X X(t)\bigr)G(t).$$

$X$ is dimensionless; $k_X$ has units L/(pmol min); $\tau_X$ has units min; $CL_G$ and $S_X$ have units L/min. Consequently $R_d$ is mmol/min. This is a proposed one-state delay and linear-in-glucose aggregate uptake closure, inspired by established glucose-insulin modeling practice but not selected as a uniquely correct T2D mechanism. Positivity of $X$, uptake, and glucose must be established by the implemented solver/model domain rather than assumed from the equation alone.

## Dimensional and conservation checks

- Glucose balance: mmol/min on both sides; $V_GG$ is mmol.
- Insulin balance: pmol/min on both sides; $V_II$ is pmol; $CL_I I$ is pmol/min.
- Action equation: each term is min$^{-1}$ because $X$ is dimensionless.
- Uptake: (L/min)(mmol/L) = mmol/min.
- Meal appearance: (mmol)(min$^{-1}$) = mmol/min and integrates to $M_{abs}$ under the stated normalization.
- Pool conservation residual must equal input fluxes minus output fluxes. It does not prove whole-body glucose conservation because storage, oxidation, and hepatic precursor pools are outside the boundary.

## Assumptions and unresolved questions

1. Are tracer-measured meal appearance and endogenous production available for a T2D population and the meal conditions of interest?
2. Which glucose-stimulated beta-cell secretion function can be identified from insulin plus C-peptide data, and how should hepatic first-pass extraction be represented?
3. Is a single systemic insulin-driven action state sufficient for the target time scale, or do data require separate hepatic and peripheral insulin-action states?
4. Can hepatic production be modeled as an instantaneous function of systemic insulin, or is portal insulin and/or delayed action needed?
5. What is the intended glucose range, and when must renal glucose loss be included?
6. Which parameters can be practically identified from the intended observation schedule? Concentration-only observations may not separate fluxes that contribute similarly to net change.
7. Which external data define the meal input, basal conditions, measurement error, and individual parameter estimates without importing unsupported priors?

## Scope exclusions

No glucagon, incretin, exercise, circadian, renal, explicit gastric, glucose-distribution, tissue-specific, glycogen, or drug-effect subsystem is implemented or silently implied. Add a mechanism only with a question, evidence, observable implication, and validation plan.