# PhysioTwin Deterministic Demo Scenario

## Status And Purpose

This is a proposed software test fixture for the competition MVP, not a patient record, sensor export, clinical protocol, or physiological ground truth. It creates CGM-like timestamped synthetic observations so the ingestion, state-estimation, forecast, event alert, dashboard, and evaluation path can be demonstrated end to end. The scenario's numeric values and event definition are benchmark-fixture choices only; they are not diagnostic or treatment thresholds.

The existing three-state engine is not used to generate these observations or forecasts. Its saved illustrative run reaches 1.572 mmol/L and is not clinically validated. Keeping the stream generator independent prevents that low trajectory from being silently treated as a realistic patient course. The proposed generator is a deterministic signal fixture, not a replacement physiology model.

## Synthetic Profile And Stream Contract

Use one demo profile in the dashboard and a larger reproducible set of synthetic trajectories for training/evaluation.

| Field | Example / rule | Meaning |
|---|---|---|
| `subject_id` | `SYN-DEMO-001` | Synthetic identity only; never a real or pseudonymized person. |
| `source_type` | `synthetic` | Required source/provenance value; must remain visible in the UI and output manifest. |
| `scenario_id` | `sustained_high_v1` | Generator/config identifier; not available to the predictor as a feature. |
| `time_min` | Integer elapsed minutes from scenario start | Monotone, timezone-independent fixture clock. |
| `glucose_mmol_L` | Deterministically generated value | CGM-like synthetic observation; not a measured concentration. |
| `quality_flag` | `valid`, with explicit `missing`/`invalid` test cases in other fixtures | Synthetic stream quality state; missing points are not silently interpolated. |
| `generator_version`, `seed`, `config_sha256` | Fixed and recorded | Enough information to reproduce the generated stream and its labels. |

For the demo trajectory, generate 24 hours at 5-minute intervals, including both endpoints (289 nominal timestamps). Use elapsed time, not local wall-clock time. A deterministic fixture can be expressed as a smooth background signal plus a seeded, bounded measurement perturbation, with a separate scripted excursion waveform. Keep the waveform parameters, seed and missingness pattern in a versioned configuration. The event script and its metadata are generator-only; the dashboard and predictor receive only observations available at the scoring timestamp. Make a second no-event trajectory and at least one altered event shape for evaluation so the predictor is not assessed only on the displayed example.

Static fields must not masquerade as clinical covariates. The profile contains only synthetic identity, scenario/config provenance and stream/device-simulation metadata. Do not invent age, sex, medication, diagnosis history, sensor manufacturer or treatment data. If static covariates are later needed, add them only with a stated synthetic-generation rationale and explicit feature review.

## Target Event And Label Generation

**Task:** At each valid scoring time, predict whether the synthetic trajectory will satisfy the scenario's sustained-high event definition at any point in the next 60 minutes.

**Fixture event definition:** A future event is positive when at least six consecutive valid 5-minute future samples are at or above 13.9 mmol/L. If timestamps are missing or irregular, do not count six rows as six consecutive intervals; the label is unresolved for that window unless the elapsed-time and missingness policy can establish the full 30-minute interval. The value 13.9 mmol/L and 30-minute duration are chosen for a deterministic software fixture only. They are not asserted to be the applicable clinical definition for any cohort or to be an official challenge threshold.

Generate the ground truth from the complete generated future glucose series after the stream is frozen. Assign label 1 if the event begins within `(t, t + 60 min]`, otherwise 0. A positive event must meet the sustained-duration rule; an isolated high sample is not positive. Mark windows whose future range is truncated or whose required samples are missing as ineligible rather than negative. Store labels in an evaluation-only table joined by synthetic subject and scoring timestamp; never merge them into the live observation stream.

The predictor is independent of this label procedure. It can use only a predeclared summary of past observations (for example: latest valid value, recent robust slope, recent variability and observed-data coverage) and be trained on training scenarios. It must not use the event script, future samples, label table, scenario ID, injection time, generator phase or the exact label calculation as a feature or prediction rule. Use a simple persistence comparator that carries the latest observed value forward over the horizon, then applies the same event policy to that forecast; it does not inspect future observations. This baseline may perform poorly, which is useful information rather than a reason to change the held-out labels.

## Determinism, Splits And Leakage Prevention

Version and hash the generator configuration, code version, seed, stream schema, label policy, split manifest, predictor configuration and metric configuration. Repeated generation with the same version and seed must produce byte-equivalent normalized rows and labels. Use fixed, recorded seeds for a family of synthetic trajectories. Change event timing, amplitude/shape, background level and no-event status across scenarios while keeping the task definition fixed. These variations are test-fixture diversity, not physiological mechanisms.

Assign complete synthetic subjects and scenario families to train, validation and test before extracting overlapping forecast windows. Never split time windows from a single trajectory across sets. Reserve held-out generator seeds and waveform variants for test; do not select features, thresholds, smoothing or hyperparameters after inspecting test results. Any scaler, imputer or fitted transformation is trained only on training scenarios. Keep generator-only metadata and future labels out of the feature matrix. Add automated checks that each subject/scenario appears in one split only and that every feature timestamp is at or before its forecast origin.

Because synthetic labels necessarily come from synthetic future values, they cannot establish real-world event performance. The nontriviality safeguard is that the label is computed by a future duration-and-threshold test while the predictor is a trained past-only model, not the same direct threshold rule; the test set also changes trajectory templates. Report this limitation plainly.

## Expected Dashboard Behavior

1. The page identifies `SYN-DEMO-001` and labels the entire view “Synthetic demonstration.” It shows the last observation timestamp, valid-data coverage and any gap/quality warnings.
2. The current glucose observation is visually distinct from the filtered model estimate. The estimate is limited to recent valid glucose measurements; no insulin, meal, HGP, tissue uptake or latent action state is implied.
3. The timeline distinguishes past synthetic observations from the future forecast. The forecast shows a central trajectory or risk probability, an uncertainty interval, the 60-minute horizon and the last data timestamp used. No future generated samples are shown as if observed.
4. As the scripted excursion approaches, event probability may increase and the demo alert state changes only according to a predeclared alert threshold. Show the probability, threshold/version and event horizon with the alert; the threshold is a demo policy and not a care recommendation.
5. The explanation states the observable reasons available to the predictor, such as the recent level, direction/rate of change, recent variability, data coverage and model version. It must not claim that an intervention or a physiological mechanism caused the event. If data are stale, missing or out of the declared range, show “insufficient data” rather than a confident alert.
6. A clear disclaimer says the scenario and alert are synthetic, are not medical advice, and have not been clinically validated.

## Evaluation Outputs

Produce a run manifest, normalized stream CSV, evaluation-only label table, split manifest and machine-readable metric results in a new experiment directory. Record source type, scenario/generator version, config and code hashes, random seeds, feature set, predictor and persistence-baseline versions, forecast horizon, label policy and software versions. Do not overwrite `outputs/phase1_initial_experiment/`.

Compare predictor and persistence baseline on exactly the same held-out subjects/scenarios. Report event prevalence, confusion matrix at the locked alert threshold, recall/sensitivity, specificity, precision, false alerts per synthetic day, detected-event lead time, AUROC, AUPRC and Brier score; include calibration/reliability and uncertainty by resampling whole synthetic subjects/scenarios. Report each held-out scenario family and undefined metrics. If continuous glucose forecasts are implemented, report MAE and prediction interval coverage/width separately. Do not convert synthetic metric values into claims about patient care or clinical validity.

## Open Decisions Before Implementation

- Confirm the event threshold/duration with the scientific owner as a synthetic fixture policy; select an authoritative definition before any permitted real-data task.
- Confirm the forecast probability alert threshold and acceptable demo alert behavior before viewing test-set outcomes.
- Select exact waveform family, generator seed set, quality/missingness cases and train/validation/test scenario counts in a versioned config. No physiological interpretation is attached to the waveform.
- Decide whether the dashboard forecast includes a glucose-valued trend projection in addition to event probability. If included, define the estimator and uncertainty separately from event classification.
- Verify official challenge requirements for video duration, public repository and deliverable format before recording or release.
- Use no open dataset, real participant data or sensor connection until source availability, license/terms, privacy and matching event labels are verified.