# Repository Audit: PhysioTwin

**Date:** 2026-10-19  
**Reviewer:** Senior Full-Stack Engineer & Scientific Digital-Twin Architect  
**Project:** PhysioTwin (Digital Twin Challenge 2026)  
**Baseline Status:** Phase 0.5 - Phase 1.3 Research Prototype  

---

## 1. Repository Inventory & File Structure

```
d:/Ganesh/digitaltwin/
├── README.md                                 # Project overview, commitments, dev commands
├── pyproject.toml                            # Python package metadata (physiotwin 0.1.0)
├── docs/                                     # Scientific audit, physiology, & planning docs
│   ├── data_dictionary.md                   # Data conventions, units, GSE153792 handling
│   ├── evidence_and_assumptions.md          # Reference registry & assumptions breakdown
│   ├── initial_experiment.md                # Proposed triple-tracer protocol & criteria
│   ├── literature_audit.md                  # Padova T2D audit & accessibility status
│   ├── model_selection.md                   # Rationale for reduced-order candidate model
│   ├── parameter_registry.csv               # Formal parameter definitions & missingness
│   ├── phase1_2_model_review.md             # Review of candidate equations
│   ├── phase1_3_dataset_audit.md            # Audit of available datasets (GSE153792, etc.)
│   ├── phase1_3_measured_flux_specification.md # Mass-balance flux requirements
│   ├── phase1_3_research_design_decision.md # Design decisions on prospective vs retrospective
│   ├── phase1_initial_experiment_interpretation.md # Caveats of the illustrative experiment
│   ├── phase1_model_closures.md             # Freezing of illustrative closures
│   ├── physiology_specification.md          # Candidate 3-state ODE equations & units
│   ├── research_scope.md                    # Research question & model boundary
│   └── validation_plan.md                   # Invariant, mass-balance, and limiting checks
├── experiments/
│   └── phase1_initial/
│       └── config.v1.json                   # Deterministic baseline configuration
├── outputs/
│   └── phase1_initial_experiment/
│       ├── results.csv                      # Baseline ODE simulation trajectory (721 points)
│       ├── run_metadata.json                # Execution metadata and solver diagnostics
│       └── state_trajectories.png           # 4-panel trajectory and flux plot
├── reports/
│   └── phase1_1_diagnostics.md              # Detailed diagnosis of baseline glucose dip
├── src/
│   └── physiotwin/
│       ├── __init__.py                      # Package entrypoint (version 0.1.0)
│       ├── engine.py                        # ODE RHS, solvers, fluxes, diagnostics, runner
│       └── experiment.py                    # Experiment loader and CLI runner
└── tests/
    ├── test_engine.py                       # 9 tests: tolerances, balances, limits, dimensions
    └── test_package.py                      # 1 test: import verification
```

---

## 2. Test Suite Execution & Verification

### Command Executed
```powershell
python -m pytest -v
```
Using: Python 3.14.4 (`C:\Users\USER\AppData\Local\Python\pythoncore-3.14-64\python.exe`), `pytest-9.1.1`, `numpy-2.4.4`, `scipy-1.17.1`.

### Results
```
tests/test_engine.py::test_state_dimension_and_validation PASSED         [ 10%]
tests/test_engine.py::test_solver_returns_finite_outputs PASSED          [ 20%]
tests/test_engine.py::test_positivity_for_valid_domain PASSED            [ 30%]
tests/test_engine.py::test_pool_balances_close_and_internal_fluxes_are_accounted PASSED [ 40%]
tests/test_engine.py::test_zero_input_and_zero_action_match_analytic_limits PASSED [ 50%]
tests/test_engine.py::test_meal_input_normalization_and_time_based_flux PASSED [ 60%]
tests/test_engine.py::test_versioned_configuration_and_reproducibility PASSED [ 70%]
tests/test_engine.py::test_declared_equation_dimensions_balance PASSED   [ 80%]
tests/test_engine.py::test_tolerance_sensitivity PASSED                  [ 90%]
tests/test_package.py::test_package_imports PASSED                       [100%]
====================== 10 passed, 310 warnings in 5.10s =======================
```
All 10 tests passed without errors.

---

## 3. Inventory of Features: Implemented, Partial, Broken, Missing

| Feature | Status | Notes |
|---|---|---|
| **Core 3-State ODE Engine** | **Implemented** | $Q_G$ (glucose pool), $I$ (systemic insulin), $X$ (insulin action). Scipy `solve_ivp` with LSODA, dimensional checking, conservation balance residuals. |
| **Baseline Experiment Runner** | **Implemented** | Reruns `config.v1.json` deterministically, outputs CSV, JSON metadata, and PNG plot. |
| **Mass Balance Accounting** | **Implemented** | Independent quadrature of meal appearance, HGP, disposal, and insulin fluxes confirms mass-balance residual $< 10^{-5}$ mmol. |
| **Synthetic Patient Profiles** | **Missing** | Only single hypothetical configuration (`config.v1.json`) exists. No cohort of diverse clinical phenotypes (e.g. insulin resistant, impaired beta-cell secretion, lean normal, controlled T2D). |
| **Time-Series Wearable / CGM Stream** | **Missing** | No continuous stream generator, no observation noise model, no distinction between sensor readings and latent physiological state. |
| **Forecast Engine & Uncertainty** | **Missing** | Current engine is a batch integrator from $t=0$ to $360$ min. No state estimation (e.g., rolling window / forward projection from intermediate observations) or parameter uncertainty cones. |
| **Adverse Event Risk Workflow** | **Missing** | No explicit, mathematically defined risk model for hypoglycemia ($G < 3.9$ mmol/L) or severe hyperglycemia ($G > 13.9$ mmol/L) with defensible ground truth and metric evaluation. |
| **Simple Baseline Comparator** | **Missing** | No non-leaking baseline (e.g., historical persistence or autoregressive/linear extrapolation) to benchmark the twin against. |
| **Evaluation Metrics (RMSE, MAE, Risk)** | **Missing** | No formal evaluation pipeline computing forecast accuracy against ground truth. |
| **REST API (Backend)** | **Missing** | No FastAPI server or endpoints exist. |
| **Frontend Web Application** | **Missing** | No React / Vite / TypeScript dashboard exists. |

---

## 4. Physiological Limitations & Scientific Integrity Audit

1. **Illustrative Closures vs. True Biology:**
   - **Meal Appearance ($R_{a,m}$):** Uses a shape-2 gamma forcing function ($q_m(t) = \frac{t}{\tau_m^2} e^{-t/\tau_m}$). This is an empirical input curve, not gastric emptying or intestinal absorption physiology.
   - **Hepatic Glucose Production ($HGP$):** Modeled via a reciprocal-hinge function $\frac{HGP_0}{1 + \max(I - I_{ref}, 0)/K_H}$. While qualitatively non-increasing with insulin, the hard hinge at $I = 150$ pmol/L is an illustrative software assumption.
   - **Beta-Cell Secretion ($S_\beta$):** Modeled as affine-thresholded $S_{\beta,0} + k_\beta \max(G - G_\beta, 0)$. It lacks delay, biphasic secretion dynamics, incretin effects (GLP-1), or glucose-rate sensitivity. It also has a basal secretion floor ($S_{\beta,0} = 40$ pmol/min) that never drops to zero even when glucose is dangerously low.
2. **The "Hypoglycemic Dip" in Baseline Simulation:**
   - As documented in `reports/phase1_1_diagnostics.md`, simulated glucose falls to $1.57$ mmol/L at $t=248$ min.
   - **Root Cause:** Persistent baseline insulin secretion + delayed action $X$ + uncalibrated hypothetical parameter gains ($S_X, CL_G, CL_I$). Modeled utilization exceeds input by $44.58$ mmol over the run.
   - **Integrity Requirement:** We must NOT disguise this or artificially clip the trajectory. The user interface must explicitly label the model status, explain this known behavior, and distinguish illustrative hypothetical parameter sets from clinical reality.
3. **Absence of Clinical Validation:**
   - All parameters in `config.v1.json` are hypothetical. No real human cohort data or clinical trial data are fitted.
   - No claim of reproducing the full Padova Type 2 Diabetes Simulator can be made because Padova's proprietary equations and subject parameter distributions are restricted.
4. **Data Separation:**
   - GSE153792 (transcriptomic RNA-seq dataset from human muscle biopsies) must never be merged with continuous time-series CGM data. All patient records in the application must be synthetic, transparently labeled, and generated with known seeds.

---

## 5. Preservation Guarantees

The existing baseline files:
- `src/physiotwin/engine.py`
- `src/physiotwin/experiment.py`
- `experiments/phase1_initial/config.v1.json`
- `outputs/phase1_initial_experiment/results.csv`
- `outputs/phase1_initial_experiment/run_metadata.json`
- `outputs/phase1_initial_experiment/state_trajectories.png`
- `tests/test_engine.py` and `tests/test_package.py`

will remain fully functional, unaltered in their core equations, and verified by regression tests throughout the full-stack development process.
