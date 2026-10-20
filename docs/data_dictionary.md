# Data Dictionary and Provenance

## Physiological model quantities

| Name | Type | Units | Meaning / provenance requirement |
|---|---|---|---|
| `time_min` | independent variable | min | Elapsed time from a documented experiment origin; retain original timestamps and conversion. |
| `glucose_mmol_L` | observation/state-derived output | mmol/L | Systemic glucose concentration; record specimen type, assay/device, calibration, and conversion from source units. |
| `glucose_amount_mmol` | model state | mmol | $Q_G=V_GG$ in the specified effective pool; depends on declared $V_G$. |
| `insulin_pmol_L` | observation/state | pmol/L | Systemic plasma insulin; preserve original assay units and assay metadata. It is not secretion rate. |
| `insulin_secretion_pmol_min` | latent/model flux | pmol/min | Pancreatic secretion estimate; record whether measured, tracer/C-peptide-inferred, or model-predicted. |
| `c_peptide` | optional observation | source-specific; normalize only with method recorded | May inform endogenous secretion; assay units, conversion, and kinetic model must be declared. Not currently a model state. |
| `meal_absorbable_glucose_mmol` | input quantity | mmol | Requires meal composition and a justified absorbed fraction or tracer-derived appearance basis. |
| `meal_appearance_rate_mmol_min` | input flux | mmol/min | Measured or explicitly estimated meal-derived rate of appearance; preserve its source and uncertainty. |
| `hepatic_glucose_production_mmol_min` | latent/model flux | mmol/min | Distinguish measured/tracer-estimated values from model predictions. |
| `peripheral_utilization_mmol_min` | latent/model flux | mmol/min | Aggregate removal from systemic pool; not directly observed unless supported by a flux protocol. |
| `renal_glucose_loss_mmol_min` | optional flux | mmol/min | Omitted in the initial candidate; if later included, preserve urine collection/time-window and measurement basis. |
| `subject_id` | identifier | none | Stable pseudonymous key from source data; do not use row number as identity. Keep linkage key separately under approved controls. |
| `condition_id` | identifier | none | Explicit meal, treatment, visit, and protocol identifier; encode repeated measures without flattening them. |
| `source_record_id` | identifier | none | Original sample or measurement ID retained through transformations. |

## Transcriptomic source: GSE153792

NCBI GEO accession **GSE153792**, titled “Whole-blood transcriptome profiling reveals signatures of metformin and its therapeutic response,” is a human whole-blood RNA-seq study of drug-naive T2D volunteers with longitudinal metformin-response analysis. GEO record: <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE153792>.

Use it only as exploratory evidence about systemic transcriptional changes and metformin response. Preserve original count/expression files and GEO sample metadata unchanged; create separately versioned derived objects with recorded normalization and filtering. Do not merge its sample rows with simulated or measured physiological time points, infer glucose kinetic parameters from expression alone, or use it as direct calibration data for meal appearance, hepatic production, insulin secretion, or uptake.

Before analysis, record the accession and file URLs, retrieval date, checksums, platform/library details, sample-to-subject mapping as supplied by GEO, treatment/visit metadata, response definitions, and any missingness or exclusions. Verify those fields against the source record and associated publication; do not infer pairing from accession order.

## Raw and derived data policy

- Keep raw downloads byte-for-byte unchanged; store transformations outside the raw-data location.
- Maintain a manifest containing source, accession/URL, retrieval timestamp, checksum, license/terms, software version, and transformation command/configuration.
- Carry subject, condition, time, and source-record identifiers into derived data. Document unit conversions and never overwrite source values.
- Store simulator-generated output separately from observations and label it as simulated, including model/version, parameter source, solver, tolerances, and random seed if applicable.
- No dataset has been downloaded into this repository during Phase 0.