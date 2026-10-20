# Validation Plan

Validation is prospective. No physiology engine exists yet, so none of the checks below has been run and no physiological validation is claimed. Tests should be added alongside implementation and should fail loudly when a required invariant is violated.

## Required checks

| Check | Method | Pass criterion / failure signal |
|---|---|---|
| Units and dimensional consistency | Encode units for state, parameter, and flux definitions; independently review each right-hand-side term and meal integral. Add automated checks where the implementation's unit library and equation structure make them reliable. | Every equation is dimensionally consistent; no unit conversion is implicit. Any mismatch blocks release. |
| Glucose pool mass balance | Compute cumulative initial amount + integrated sources - integrated sinks versus final amount using solver output and independently integrated fluxes. | Residual converges toward numerical tolerance as tolerances/step sizes tighten; report tolerance and scale. |
| Insulin balance | Apply the same integrated-source/sink residual check to insulin amount, secretion, hepatic extraction, and clearance. | Accounting closes to stated numerical tolerance; secreted, extracted, and cleared insulin are not conflated. |
| Positivity and admissible domains | Test nonnegative glucose, insulin, meal appearance, secretion, production, uptake, and extraction bounds across normal and stress cases; inspect solver excursions. | No negative physical amount/concentration or flux outside its defined constraints; no post hoc clipping that hides instability. Signed deviations, if introduced, must be explicitly classified. |
| Solver convergence and stability | Compare stiff-capable and reference solvers where appropriate; refine tolerances and maximum step; compare trajectories and integrated fluxes. | Outputs change less than a predeclared numerical error budget and remain finite/admissible. Choose tolerances before reviewing validation outcomes. |
| Limiting cases | Zero meal input; zero secretion; zero insulin action; no insulin clearance; zero hepatic production; long fasting relaxation; vanishing action time constant; and limiting parameter values that simplify to analytically checkable equations. | Results agree with derived expected behavior and do not produce sign, singularity, or conservation errors. |
| Physiological challenge tests | Simulate a documented meal input, graded glucose challenge, and insulin perturbation only when corresponding data and boundary conditions are available. Compare direction, timing, and flux response with measured outcomes. | Predeclared qualitative and quantitative metrics are met; do not treat plausible-looking curves as evidence. Include hypoglycemia/hyperglycemia only if model boundary supports those regimes. |
| Parameter identifiability | Structural analysis of equations; practical identifiability via profile likelihood or equivalent; sensitivity and parameter-correlation analysis under the planned observation schedule. | Report which parameters are estimable, uncertainty intervals, correlations, and failed identifiability. Do not report a unique patient parameter when alternatives fit equivalently. |
| Padova benchmark comparison | After full-text/supplement/source inspection, match version, initial conditions, meal input, units, outputs, and parameterization; compare only shared quantities using published reference data or verified executable outputs. | Record protocol and numerical discrepancies. Do not claim reproduction from architecture resemblance or abstract-reported results alone. |
| Held-out validation | Hold out subjects and, where supported, meals/conditions before fitting. Preserve subject-level separation and predefine metrics. Report calibration and held-out performance separately, with uncertainty and data provenance. | No leakage across split; held-out result meets a criterion defined before examining the holdout. If data are insufficient, label validation unperformed. |

## Validation hierarchy

1. Verify equation dimensions, state/flux semantics, and code-level unit conversions.
2. Verify solver-independent invariants, mass-balance accounting, positivity, limiting cases, and convergence.
3. Establish parameter identifiability for the actual experiment before fitting individuals.
4. Fit only to a documented training dataset with preserved provenance.
5. Test physiological challenges and compare the declared outputs on held-out subjects/conditions.
6. Conduct a separate, documented Padova benchmark comparison after the reference model is inspected.

## Data separation and reproducibility

Keep raw source files immutable. Record source URL/accession, retrieval date, checksum, license/terms, file names, transformations, and code version in a manifest when data are acquired. Derived tables must retain sample/subject identifiers and transformation lineage. Transcriptomic rows and physiological time-series rows have different experimental units and must not be joined by row order or treated as paired without a verified shared identifier and design.