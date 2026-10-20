# PhysioTwin Phase 1.3: Research-Design Decision

## Decision Summary

**Do not proceed with Option B as an implementation using currently accessible data.** This audit found no same-subject, time-aligned dataset with the glucose pool scale and fluxes needed for a complete balance. The repository has no physiological data; GSE153792 is transcriptomics; the relevant tracer and model papers do not expose the required participant-level data through the records checked.

**Primary path: Option C, a prospective flux-rich research protocol, conditional on feasibility, appropriate ethics review and qualified clinical oversight.** Before any study, lock the scientific question, domain, tracer/assay method, measurement schedule, volume/pool definition, uncertainty model and analysis plan. This is a proposal for scientific planning, not an approved or prescribed human experiment.

**Fallback: Option D, a source-access-gated reproduction of a documented published model, beginning with a full-text review of the Dalla Man et al. meal model (R1), not an abstract-based reconstruction of Padova.** If R1's full equations, required inputs, validation protocol and necessary reference data cannot be obtained, stop and select a model only after a separate provenance/access review. Option D changes the immediate question from measured-flux identifiability to model reproduction and cannot substitute for missing flux data.

Option A remains appropriate only for software regression tests. Option B can be reconsidered if data-use access to the original R1/R2/R6 cohorts or a new matched existing dataset is secured.

## Evidence Versus Inference

**Evidence:** NCBI's official GEO DataSets summary for GSE153792 lists 34 human high-throughput expression-profiling samples, a TXT supplementary-data type, SRA BioProject PRJNA644109, and publication PMID 32780768. It documents transcriptomics, not a same-subject meal tracer flux series. The cited R6 abstract reports a 12-subject triple-tracer method estimating meal appearance and endogenous glucose production; R1 describes triple-tracer-derived major fluxes in a large normal database and a smaller T2D database; R2 reports a 51-person T2D triple-tracer meal model. The checked publication/repository records do not provide accessible subject-level physiological time series, full protocols or linked supplements/data for these studies. The existing PhysioTwin time series is synthetic.

**Inference:** No complete measured-flux balance is currently constructible from verified accessible data. A glucose change combined with Ra and HGP alone leaves a cumulative combined removal residual. It cannot be uniquely assigned to peripheral disposal if renal or other fluxes are not measured/justified. Concentration cannot be converted to a glucose pool mass without an effective distribution-volume definition and uncertainty.

**Assumptions not accepted as facts:** The proposed triple-tracer protocol may be feasible at a capable site; access to investigators or institutional full text may become possible; R1 may offer a suitable reproduction path after full methods review. None of those access or ethics conditions is confirmed.

## Option Comparison

| Option | Scientific defensibility | Data/access | Burden and effort | Identifiability and validation | Decision |
|---|---|---|---|---|---|
| **A. Use an existing sufficiently matched dataset** | Strong if same-subject measurements and provenance are verified. | No qualifying dataset located. GSE153792 is unsuitable; PhysioTwin output is generated, not measured. | Low implementation burden if such data are found; current search/access gap is blocking. | Cannot assess any individual balance without aligned raw/derived fluxes, volume, uncertainty and missingness. | Not available now. Reopen if a concrete accession/data manifest is obtained. |
| **B. Reproduce a published experiment's documented balance** | Strong in principle when raw measurements, exact protocol, flux method and pool boundary are accessible. | R1/R2/R6 demonstrate relevant designs, but checked records expose abstracts, not the necessary participant-level data/schedules. | Moderate to high data-use/access and transcription burden. | Aggregate abstract results cannot reproduce subject-level balance or uncertainty; no independent validation set verified. | Do not proceed now. First seek formal data/full-text access; no implementation from published summary values. |
| **C. Design a future research protocol** | Can directly measure the missing, matched quantities if the protocol and boundary are designed around them. | Requires a qualified tracer-capable study site and approved protocol; no existing access assumed. | Highest measurement and operational burden: tracer infusions, serial assays, sample handling, specialized analysis, ethics and clinical oversight. | Can improve flux separation, but does not guarantee identifiability. Effective volume, Rd, renal loss and kinetic parameter estimation still need explicit methods and prospective analysis. | **Primary path**, conditional on feasibility review and ethics/clinical oversight. |
| **D. Reproduce a better-documented mechanistic model** | Strong for fidelity to a selected model if exact equations, parameters, code/reference outputs and matched validation conditions are obtained. | R1 is a meal-model precedent but full equation/data access remains to be verified; Padova R2 is restricted and not reproducible from abstract. R4 is an IV glucose-disappearance model in conscious dogs, not the target meal/T2D flux boundary. | High literature/source review and implementation effort; possibly lower than a new tracer study but still requires complete model materials. | Reproduction can validate transcription against reference behavior, not necessarily transportability or the measured-flux question. | **Fallback** if prospective data are infeasible, after a source-access gate and explicit scope decision. |
+
+## Minimum Data Design For Option C
+
+The minimum design objective is an interval pool balance, not a patient-specific simulator. A single meal study would need, for the same participants and visit:
+
+1. Serial systemic plasma/serum glucose with specimen, assay, unit, precision and actual timestamps.
+2. Tracer enrichments plus oral meal and intravenous tracer dosing/infusion records sufficient for a declared method to estimate $R_{a,m}(t)$ and HGP/EGP with uncertainty. Fluxes are derived/model-estimated, not direct assay readings.
+3. A documented definition and supported value/estimator for effective glucose distribution volume if reporting mmol pool mass. Otherwise restrict reporting to concentrations and fluxes without claiming an absolute mass balance.
+4. An independent method for total glucose disposal if the result is to name $R_d$. Do not define disposal as a residual and then call that residual independent confirmation.
+5. Timed urine glucose and urine volume if renal loss may be material in the declared domain; if omitted, justify the restricted domain and keep unmeasured losses in the residual.
+6. Meal composition/timing, actual observation schedule, protocol and assay metadata, source identifiers, uncertainty/covariance, missingness and data-use provenance.
+
+Serial insulin and C-peptide are additional measurements for secretion and insulin kinetics, not substitutes for glucose tracer fluxes. Secretion from C-peptide requires a cited kinetic/deconvolution method. Insulin extraction and systemic clearance remain separate kinetic questions. Sample frequency and study size must be selected from the chosen validated protocol and identifiability/power analysis; no values are invented here. Any human study requires appropriate ethics review, consent/governance and qualified clinical oversight.
+
+## Immediate Gates
+
+- Seek authorized access to participant-level R1/R2/R6 data, full methods, supplements and code; record responses and terms. Do not treat an unanswered or inaccessible source as available.
+- In parallel, obtain feasibility input from tracer/metabolism investigators for a protocol capable of the proposed flux estimates. This is planning only; it is not ethics approval.
+- Before implementation, lock the pool, effective-volume method, flux definitions, data alignment, uncertainty propagation and treatment of unresolved removal as specified in `phase1_3_measured_flux_specification.md`.
+- If neither a matched dataset nor suitable prospective protocol is feasible, pause Option B and perform an access-first model-selection review for Option D. Do not tune the current hypothetical ODE.
+
+## Sources
+
+- Official GEO record: [GSE153792](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE153792); NCBI DataSets summary ID `200153792`; SRA [PRJNA644109](https://www.ncbi.nlm.nih.gov/sra/?term=PRJNA644109); associated publication [PMID 32780768](https://pubmed.ncbi.nlm.nih.gov/32780768/).
+- Dalla Man C, Rizza RA, Cobelli C. 2007 meal model: [DOI 10.1109/TBME.2007.893506](https://doi.org/10.1109/TBME.2007.893506), [PMID 17926672](https://pubmed.ncbi.nlm.nih.gov/17926672/).
+- Visentin R, Cobelli C, Dalla Man C. 2020 Padova T2D simulator: [DOI 10.1089/dia.2020.0110](https://doi.org/10.1089/dia.2020.0110), [PMID 32324063](https://pubmed.ncbi.nlm.nih.gov/32324063/).
+- Basu R, Di Camillo B, Toffolo G, et al. 2003 triple-tracer method: [DOI 10.1152/ajpendo.00190.2001](https://doi.org/10.1152/ajpendo.00190.2001), [PMID 12485809](https://pubmed.ncbi.nlm.nih.gov/12485809/).
+- Van Cauter E, Mestrez F, Sturis J, Polonsky KS. 1992 C-peptide kinetics: [DOI 10.2337/diab.41.3.368](https://doi.org/10.2337/diab.41.3.368), [PMID 1551497](https://pubmed.ncbi.nlm.nih.gov/1551497/).
+- Bergman RN, Ider YZ, Bowden CR, Cobelli C. 1979 glucose disappearance model: [DOI 10.1152/ajpendo.1979.236.6.E667](https://doi.org/10.1152/ajpendo.1979.236.6.E667); accessible abstract/metadata via [Crossref](https://api.crossref.org/works/10.1152/ajpendo.1979.236.6.E667).
