# PhysioTwin Competition MVP Plan

## Purpose And Boundaries

This plan targets a reproducible, end-to-end Digital Twin Challenge 2026 demonstration. The immediate deliverable is a working competition prototype and submission package; a research paper is out of scope until after the prototype. This is a planning document only: it does not change the engine, baseline configuration, parameters, or saved outputs, and it does not authorize a human study or clinical use.

PhysioTwin is not currently a patient-specific or clinically validated digital twin. Its current ODE is an illustrative three-state software fixture. The recorded baseline reaches a glucose minimum of 1.572 mmol/L at 248 minutes; its own diagnosis attributes this to hypothetical values and unvalidated closures, not to a measured patient response. Do not present that curve as a credible clinical forecast or hide the low value. Hypoglycemia prediction is excluded from the initial MVP unless an independently justified model domain and suitable ground truth are approved.

## Requirements And Acceptance Criteria

The requirements below combine the supplied challenge brief with acceptance criteria for a reproducible implementation. The repository does not currently contain an authoritative challenge notice or confirm the requested video duration. Treat the requirement for a video of at least 20 minutes as supplied by the project owner and verify it against the official challenge source before submission. No additional challenge rule is assumed.

| Requirement | MVP acceptance criterion |
|---|---|
| Static patient data | Load a versioned synthetic profile with explicit synthetic provenance and a stable synthetic ID. If permitted open data are later used, include source/accession, license/terms, retrieval date, checksum, transformation lineage and permitted use. No real patient data are assumed available. |
| Dynamic wearable/IoT stream | Ingest timestamped glucose observations from a deterministic fixture; validate ordering, units, duplicates, missing intervals and provenance. A real sensor connection is optional and must not be implied without a verified device/data source. |
| Bounded state estimation and simulation | Expose the observed glucose estimate and a declared short-horizon forecast with uncertainty. Do not infer hidden insulin, hepatic production, insulin action or other latent physiological states from glucose alone. Keep the current ODE disconnected from forecasts until it passes review. |
| One adverse-event task | Predict a defined synthetic sustained-hyperglycemia event within a fixed forecast horizon. Use a locked synthetic-only label definition and separately implemented past-only predictor. Do not label or predict hypoglycemia in the initial demo. |
| Doctor-facing dashboard | Show patient/source status, latest observations and timestamps, glucose history, forecast and uncertainty, event probability/alert state, and a concise evidence-based explanation of the alert. Every view identifies synthetic or open-data provenance and states that it is not for clinical decisions. |
| Baseline comparison | Evaluate the selected predictor against a simple persistence baseline using subject/scenario-held-out data and discrimination, calibration, event-detection and false-alert measures. Publish the split and per-scenario results. |
| Reproducibility | A committed experiment configuration and deterministic seed reproduce the data, split, model, metrics and dashboard demo; outputs contain code/config hashes, software versions and data provenance. Re-running must not overwrite the protected Phase 1 output directory. |
| Submission package | Public GitHub repository; README; architecture document; presentation PDF; an explicit open-source license; and a demonstration video meeting the official duration rule. Verify public access and license compatibility before release. |
| Demonstration | A clean setup can regenerate the fixture and metrics, start the app, show a normal period and the forecast/alert case, explain uncertainty and limitations, and finish with the reproducibility and submission artifacts. |

## Current Capability Inventory

| Area | Present capability | Gap / constraint |
|---|---|---|
| Scientific documentation | Physiology specification, parameter registry, evidence audit, model review, dataset audit, measured-flux contract and prospective validation plan. These consistently distinguish evidence from assumptions. | No accepted competition data source, prediction task, observation model or submission architecture is selected. |
| Engine | `src/physiotwin/engine.py` implements a deterministic ODE for glucose-pool amount, systemic insulin and an aggregate action state. It checks domains, solver output, balances and meal-input normalization. | Constitutive closures and all configured numeric values are illustrative and unsupported. No patient calibration, observation model, uncertainty propagation, stream input or event prediction exists. The baseline glucose trajectory is implausibly low and is not clinically validated. |
| Experiment runner | Versioned JSON configuration, configuration SHA-256, deterministic simulation, CSV/metadata/plot outputs and software-version recording. | Only one hypothetical experiment exists; no dataset manifest, held-out evaluation, prediction metrics or generated patient/event cohort exists. |
| Tests | `pytest` tests package import, parameter validation, numerical behavior, positivity, balances, normalization, reproducibility, dimensions and tolerance sensitivity. | Tests are software invariants, not physiology or event-prediction validation. No frontend, ingestion, schema, alert, leakage or evaluation tests exist. |
| Data | The repository contains no raw physiological data. The checked audit reports GSE153792 is transcriptomics, not a meal/CGM flux series; no permitted matched glucose/flux cohort is verified. | Do not describe open patient data or live sensors as available. Synthetic inputs are the feasible initial route. Any external dataset requires a fresh access, license, privacy and suitability review. |
| Runtime/package | Python 3.10+; NumPy, SciPy and Matplotlib; pytest optional dependency. | No dashboard or API framework, frontend build, pinned environment/lock file, license, architecture document, presentation PDF or demo video is present in the inspected workspace. |

The inspected repository includes the root README and `pyproject.toml`, all existing `docs/` files, engine and experiment runner, tests, Phase 1 JSON config, generated CSV/JSON/PNG, and the Phase 1 diagnostic report. The image, CSV and metadata agree with the documented hypothetical baseline. No repository code or baseline artifact is modified by this plan.

## Measurement And Output Semantics

- **Observed measurement:** A timestamped value presented as measured by an identified assay/device in a documented source dataset. In the initial demo there are no real observations; do not use this label for generated values.
- **Synthetic input:** A value created by the deterministic scenario generator, including a synthetic profile or simulated CGM-like reading. Carry an explicit `synthetic` provenance flag and generator/config version.
- **Model estimate:** A quantity computed from available observations using a named estimator. MVP state estimation is limited to a filtered glucose level and recent trend; it does not claim estimates of unobserved physiological states or fluxes.
- **Forecast:** A future glucose trajectory or event probability computed only from information available at the forecast time. Show forecast horizon, uncertainty, model/version and data cutoff. A forecast is not an observation or a clinical recommendation.
- **Alert:** A thresholded presentation of a forecast probability under a declared demo policy. It is not a diagnosis, alarm validated for care, or action recommendation. Preserve probability and uncertainty, not only a colored badge.

## Proposed Minimum Architecture And Data Flow

Use one Python application for the first vertical slice: a Streamlit dashboard as the presentation layer, calling small, testable Python modules in `src/physiotwin/` in-process. Avoid a separate API service and JavaScript frontend until a verified challenge requirement makes that split necessary. This minimizes build/deployment dependencies while keeping clean interfaces that can later be exposed through an API.

Logical modules:

1. **Source and provenance:** Versioned synthetic profile/stream fixtures now; a future open-data adapter only after access and terms review. Normalize into a documented timestamped observation schema without mutating raw source files.
2. **Validation and alignment:** Validate IDs, timestamps, units, duplicates, missingness and sensor/source metadata. Retain invalid/missing flags instead of silently filling gaps.
3. **State estimation:** Estimate only current glucose from recent valid observations (for example, a predeclared robust smoother) and a trend summary. The displayed state is observation-derived, not a hidden physiological state.
4. **Forecast and event scoring:** Run a transparent, separately versioned predictor on past-only features. Produce a glucose/event forecast and uncertainty from training data or a predeclared synthetic ensemble. Do not call the existing ODE here.
5. **Evaluation and experiment runner:** Use a committed config, deterministic seeds, subject/scenario-level splits and metric outputs. Save each run to a new experiment directory with hashes and package versions.
6. **Dashboard:** Show source/provenance and data quality, current observations, state estimate, forecast interval, event probability/alert, and a concise explanation such as recent level, trend, data coverage and model version. Display synthetic/demo and non-clinical status persistently.

Data flow: source fixture or permitted source -> immutable raw record -> validated/aligned stream -> past-only state/features -> forecast and event probability -> alert policy -> dashboard and reproducible run artifacts. Labels and future measurements are evaluation-only and never enter the live scoring path. The current mechanistic engine remains a separate research component until review gates below pass.

## Event Task And Leakage Controls

The demo task is to predict whether a synthetic stream will enter the scenario-defined sustained-hyperglycemia event within the next 60 minutes. The exact label window and threshold belong in `demo_scenario.md`; they are fixture rules, not diagnostic criteria. Choose this rather than hypoglycemia because the existing engine reaches an unsupported low glucose and has no validated low-glucose operating domain or counter-regulatory model.

Generate synthetic streams and labels before fitting the predictor. Define the event from future generated observations, but build predictor features exclusively from observations at or before the forecast timestamp. Do not include generator event flags, event injection time, future values, label-threshold state, or scenario metadata that reveals the outcome. The predictor must not reproduce the label rule directly. Split whole synthetic subjects/scenarios before window extraction; keep every window from one trajectory in one split. Fit preprocessing and model selection on training scenarios only. Test on held-out scenario templates/seed groups, including no-event and varied event trajectories. Document that synthetic performance is a software demonstration and does not establish clinical performance.

## Evaluation Plan

Compare a predeclared, past-only trained event predictor to a simple persistence baseline on identical held-out synthetic trajectories. The baseline carries forward the last observed glucose over the prediction horizon and applies the same declared event scoring/alert policy; it is not trained on future samples. Do not tune thresholds on the test split.

Report event prevalence and confusion matrix at the frozen alert threshold; sensitivity/recall, specificity, precision/positive predictive value, false alerts per simulated day, lead time for detected events, AUROC and AUPRC, and Brier score with a reliability/calibration plot. AUPRC and alert burden matter for imbalanced event sets; no single metric is sufficient. For continuous glucose forecasts, if provided, report MAE and interval coverage/width separately. Bootstrap uncertainty by synthetic subject/scenario, not by overlapping time window. Report performance by held-out scenario family and note when a metric is undefined. Synthetic acceptance is successful reproduction, no leakage, valid timestamp/units handling, non-degenerate predictions, and transparent baseline comparison; no clinical performance threshold is invented here.

Add focused tests for schema validation, timestamp ordering and gaps, deterministic generation, train/test subject isolation, feature cutoff, label/predictor separation, reproducible metrics, alert threshold behavior, and dashboard empty/error states. Preserve the existing engine tests as regression tests; they do not validate the event pipeline.

## Engine Review Or Replace Gate

Before connecting the ODE to the competition forecast, scientific/model review must at minimum:

- Revisit the thresholded-affine beta-cell secretion floor and its persistent systemic insulin source, the instantaneous systemic-insulin hepatic closure, aggregate uptake/action dynamics, meal forcing, zero renal loss, and initial state assumptions. These closures contribute to the baseline's low glucose trajectory.
- Establish a defensible glucose operating domain, input and observation model, supported parameter/initial-condition sources, and uncertainty representation. Current configuration values are hypothetical; passing solver and balance tests does not establish physiology.
- Confirm whether the equations, parameterization and state meaning can represent the demo task. The current engine consumes a prescribed meal forcing; it does not consume timestamped CGM and does not estimate patient-specific parameters.
- Test numerical convergence, positivity, balances and limiting cases under any proposed domain, then compare predictions with independent, permissioned measurements and a simple baseline using subject-held-out evaluation. Hypoglycemia would require a supported low-glucose model and independently defined ground truth before it could be considered.
- If these gates cannot be met on the challenge schedule, retain the ODE only as a clearly marked research fixture and use a bounded synthetic stream estimator/event forecaster for the competition demonstration. Do not rename that forecaster as a validated physiological twin.

No equation, parameter, config, or baseline output is proposed for modification in this planning task.

## Milestones And Dependencies

| Order | Milestone / exit criterion | Dependency |
|---|---|---|
| 0 | Verify official challenge source, submission artifacts, video duration and any data/privacy rules; record URLs and decision. | Access to official challenge materials; the 20-minute minimum currently comes from the user brief, not an inspected repository source. |
| 1 | Lock the synthetic event definition, stream schema, provenance fields, forecast horizon, split policy and metric protocol. Review the scenario document. | Milestone 0; scientific/competition review of fixture-only label threshold. |
| 2 | Build the earliest vertical slice: deterministic fixture -> validation -> simple state estimate and persistence forecast -> dashboard plot/event state -> reproducible run manifest. A viewer can follow one synthetic case end to end. | Milestone 1; no real data or current ODE needed. |
| 3 | Add the separately trained predictor, held-out scenario evaluation, uncertainty and baseline comparison; demonstrate leakage tests pass. | Stable schema and scenario generator from Milestone 2. |
| 4 | Review the current ODE against the stated demo domain. Connect it only if the review and independent evidence gates pass; otherwise document it as not used for prediction. | Scientific reviewer and suitable independent data; may be a stop/defer gate. |
| 5 | Harden usability, provenance and failure states; freeze configs/results; prepare README, architecture document, license and presentation PDF. | Stable vertical slice and evaluation; license/terms and public release review. |
| 6 | Record and review the complete demonstration video; verify required duration and repository links; run clean-environment reproduction. | Submission guidance verified; release artifacts ready. |

The schedule dates and staffing are unresolved because no official calendar or team capacity was found in the inspected repository. Preserve this dependency order; do not let a presentation deadline imply a scientific validation claim.

## Video Demonstration Plan

Target a recording of at least 20 minutes, following the user-supplied duration requirement until verified against official challenge materials. Keep a run-of-show and record the exact runtime. Suggested content: project boundary and synthetic provenance; architecture and data distinctions; deterministic generation and schema checks; dashboard walkthrough through baseline and event windows; forecast uncertainty and explanation; predictor versus persistence evaluation and held-out split; reproducible config/results and clean rerun; current ODE's low-baseline warning and explicit reason it is not used as a clinical predictor; repository, license, README and architecture artifact. Do not pad with unsupported physiology or claim real sensors/patient data. Include an on-screen non-clinical disclaimer and leave time to inspect the uncertainty/alert behavior.

## Risks And Unresolved Decisions

- **Challenge rules and schedule:** official source, exact video duration/format, repository submission requirements and dates are not recorded locally. Confirm before final packaging.
- **Data:** no suitable accessible patient/CGM stream or sensor is verified. Open-data candidate, license, consent/privacy implications, and whether its labels support the event task remain unresolved.
- **Synthetic-to-real gap:** strong synthetic results can reflect the generator and must not be presented as patient-level validation or clinical utility.
- **Label policy:** event threshold/duration and alert policy are fixture-level choices; an authoritative clinical/scientific source and domain review are required before any real-data or clinical interpretation.
- **Engine validity:** current equations/parameters are illustrative; baseline low glucose and structural identifiability concerns block its use as a patient forecast.
- **Uncertainty:** synthetic forecast uncertainty may be generator-based and not calibrated for real people. State its source and assess calibration on held-out synthetic cases only.
- **Public release:** verify data redistribution rights, software license compatibility, generated artifacts, secrets, and repository visibility before publishing.
- **Scope and time:** frontend polish, a real device integration, model replacement and paper writing could displace the working slice. The paper and unverified integrations remain out of scope for this MVP plan.

## First Implementation Task

After review of this plan and the scenario, begin with Milestone 1's locked stream/label contract, then implement only the deterministic synthetic fixture and its schema/temporal validation. Use a new experiment/output location. The first demonstrable vertical slice should be a single reproducible trajectory visible in the dashboard with a persistence forecast and provenance; add a trained predictor only after the label and split leakage tests are in place.