# Model Revision Record

## Revision 0 — Scientific Forecast Audit

**Date:** 2026-10-19  
**Purpose:** Record the current implementation audit and separate supported software corrections from unsupported physiological retuning.

### Preserved reference

The following files are immutable reference artifacts for this revision:

- `src/physiotwin/engine.py`
- `experiments/phase1_initial/config.v1.json`
- `outputs/phase1_initial_experiment/results.csv`
- `outputs/phase1_initial_experiment/run_metadata.json`
- `outputs/phase1_initial_experiment/state_trajectories.png`

Pre-change SHA-256 hashes:

| File | SHA-256 |
|---|---|
| `experiments/phase1_initial/config.v1.json` | `31b9b894bfe41848e439ce2d271896b4c863118da40eb755259a0243e8b979a8` |
| `src/physiotwin/engine.py` | `2af1209920bf67edcc0a1c6d6e61ca3d1b1cb249eeaeddce18b6efeec757dd2` |
| `outputs/phase1_initial_experiment/results.csv` | `5ec1dbd8e604521785b09a147ac77d76b2fb086e222630849570b98b01d8088e` |
| `outputs/phase1_initial_experiment/run_metadata.json` | `61cb90191495a99ef3a24cd9b0b16e5d03b7758c37e862dd4c71aafc00608c24` |
| `outputs/phase1_initial_experiment/state_trajectories.png` | `052968521b003acc628e37c847f59ca1103c1f3bf8a2c4bf2fde385fbfd106ea` |

Before code edits, `python -m pytest -q` passed 21 tests (652 environment deprecation warnings). The baseline was rerun to a temporary directory using the checked-in configuration; 721 glucose samples matched the saved CSV exactly. `python scripts/run_demo.py` reproduced the single-profile synthetic metrics (RMSE 0.12 mmol/L, MAE 0.10 mmol/L) and the heuristic 100% hypoglycemia probability.

### Findings that block physiological model changes

The current parameter values have no traceable numeric data source; no suitable T2D time series, tracer data, insulin/C-peptide series, independent validation cohort or verified data-use license is present. The checked Padova audit found insufficient accessible equations, parameter tables and participant-level data for faithful reproduction. The baseline low glucose is stable numerically, but the configured initial state is not a coupled fasting equilibrium and the model's meal-free equilibrium is about 2.038 mmol/L. Therefore no physiology equation, parameter or initial-condition adjustment is authorized by this evidence. Clipping or visual retuning would conceal rather than resolve these issues.

### Implemented supported software/display corrections

The deterministic nadir-distance formulas in `risk.py` do not estimate probabilities; remove numeric event probabilities and present only exploratory model threshold-crossing status until an independent labeled evaluation supports probabilistic outputs. Rename the synthetic comparison's “ground truth verified” wording so it cannot be mistaken for external validation. Describe the current ensemble bounds as an uncalibrated parameter-sensitivity envelope, not a 95% confidence/predictive interval. State explicitly that `run_forecast` continues a same-generator ODE using its hidden cutoff state and does not estimate state from the observation stream.

Implemented in this revision: event probabilities are returned as null with `NOT_CALIBRATED`; threshold crossings are labeled exploratory; the synthetic reference flag no longer says “ground truth verified”; forecast responses identify same-generator latent-state continuation and an uncalibrated parameter-sensitivity envelope; evaluation methodology discloses the information advantage and removes the hard-coded leakage assertion; dashboard, README and demo wording match these semantics. Regression tests assert the revised API contract. These changes do not alter ODE equations, parameter configuration or saved baseline artifacts, and do not improve physiological forecasting.

### Verification record after corrections

- Confirm preserved reference hashes are unchanged and reproduce the baseline outside its protected output directory.
- `python -m pytest tests/test_api.py::test_api_adverse_risk -q`: passed after revising the risk response.
- `python -m pytest tests/test_forecast.py tests/test_api.py -q`: 11 passed after revising forecast/evaluation metadata.
- `python scripts/run_demo.py`: completed; reports probability `not calibrated`, exploratory crossing and same-generator reference status. RMSE remains 0.12 mmol/L for the same non-independent synthetic example.
- `Push-Location frontend; npm run build; Pop-Location`: passed after API/UI updates; Vite reports the existing >500 kB bundle advisory.
- Full test suite and final baseline hashes are pending at the time of this record update.

Files changed by the supported correction: `src/physiotwin/risk.py`, `src/physiotwin/forecast.py`, `src/physiotwin/evaluation.py`, `src/physiotwin/api/schemas.py`, `tests/test_api.py`, `tests/test_forecast.py`, `scripts/run_demo.py`, `frontend/src/types/index.ts`, `frontend/src/components/AdverseRiskPanel.tsx`, `frontend/src/components/GlucoseChart.tsx`, `frontend/src/components/BaselineComparisonPanel.tsx`, and `README.md`. The three audit documents are `docs/scientific_forecast_audit.md`, `docs/forecast_validation_protocol.md` and this file.

### Claims status after this revision

| Claim level | Status |
|---|---|
| 1. Numerically functioning declared model | Demonstrated for the fixed software fixture, with solver/accounting limitations documented. |
| 2. Physiologically plausible model | Not established; implausible modeled low glucose and basal equilibrium remain unresolved. |
| 3. Predicts held-out measurements | Not established; no suitable measured cohort or leakage-free subject-held-out result exists. |
| 4. Clinically validated forecasting system | Not established; no clinical validation has been performed. |