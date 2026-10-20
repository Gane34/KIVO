# Limitations and Responsible Use

## Scientific limitations

1. The current model is a synthetic, illustrative prototype. It is not a clinically validated digital twin.
2. Parameters are hypothetical and not fitted to real patient cohorts.
3. The model is not intended for medical decision support or treatment planning.
4. Risk outputs are exploratory threshold checks only, not calibrated event probabilities.
5. Forecast uncertainty is an uncalibrated sensitivity envelope created by parameter perturbation, not a validated 95% confidence interval.

## Methodological limitations

- The model does not include explicit gastric emptying, glucagon dynamics, renal compensation, exercise, or tissue-specific uptake.
- Meal forcing uses a simplified gamma-like appearance function with a fixed closure choice.
- Error reporting and synthetic CGM streams are generated from the same model, so they are not independent validation data.
- The comparison metrics are informative for a same-generator consistency check, but they do not represent held-out clinical performance.

## Responsible use

This project must be used only for research, education, and demo workflows. It must not be used to assess real patient risk, drive treatment decisions, or replace clinician judgment.

## TODOs for future validation

- Fit model parameters to real study data.
- Validate against independent external cohorts.
- Separate model uncertainty from observation noise and state-estimation error.
- Perform prospective evaluation with clinically meaningful endpoints.
