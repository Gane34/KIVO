# Evidence and Assumptions


## Evidence status

The references below were checked through bibliographic records and abstracts. They establish that relevant mechanistic models and data exist; they do not validate the candidate equations in this repository. In Phase 0.5, publisher and repository routes for the original Padova T2D paper were checked. The accessible abstract does not expose complete model equations or parameter values, and no verified code release was located. See `literature_audit.md` for access scope and limitations.

### Published evidence

- **R1 — Dalla Man C, Rizza RA, Cobelli C.** “Meal Simulation Model of the Glucose-Insulin System.” *IEEE Transactions on Biomedical Engineering*. 2007;54(10):1740-1749. DOI: [10.1109/TBME.2007.893506](https://doi.org/10.1109/TBME.2007.893506). The abstract describes a physiological post-meal model, subsystem decomposition, triple-tracer estimates of meal appearance, endogenous production, utilization, and insulin secretion; the strategy was extended to a smaller T2D database. It is a model precedent, not evidence that the simpler candidate equations here are adequate.
- **R2 — Visentin R, Cobelli C, Dalla Man C.** “The Padova Type 2 Diabetes Simulator from Triple-Tracer Single-Meal Studies: In Silico Trials Also Possible in Rare but Not-So-Rare Individuals.” *Diabetes Technology & Therapeutics*. 2020;22(12):892-903. DOI: [10.1089/dia.2020.0110](https://doi.org/10.1089/dia.2020.0110). The published abstract reports a 15-differential-equation, 39-parameter glucose/insulin/C-peptide meal model identified using data from 51 T2D subjects in a single triple-tracer mixed-meal study; it reports generating 100 virtual subjects and testing a virtual-drug case study. These are the paper's reported methods/results, not PhysioTwin results.
- **R3 — Visentin R, Schiavon M, Bonet J, Riz M, Wagenhuber B, Dalla Man C.** “Tailoring the Padova Type 2 Diabetes Simulator for Treatment Guidance in Target Populations.” *IEEE Transactions on Biomedical Engineering*. 2024;71(6):1780-1788. DOI: [10.1109/TBME.2024.3352153](https://doi.org/10.1109/TBME.2024.3352153). The abstract describes tailoring the simulator to insulin-naive T2D using published clinical data and comparing simulated treatment-initiation findings with clinical-trial outcomes. This illustrates that the simulator's domain depends on the source population and calibration; it is not evidence for universal transportability.
- **R4 — Bergman RN, Ider YZ, Bowden CR, Cobelli C.** “Quantitative estimation of insulin sensitivity.” *American Journal of Physiology*. 1979;236(6):E667-E677. DOI: [10.1152/ajpendo.1979.236.6.E667](https://doi.org/10.1152/ajpendo.1979.236.6.E667). The work is an early quantitative glucose-disappearance/insulin-sensitivity model precedent. Its experimental setting and model do not establish an individual T2D meal-model parameterization.
- **R5 — NCBI GEO, GSE153792.** “Whole-blood transcriptome profiling reveals signatures of metformin and its therapeutic response.” [GEO record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE153792). NCBI metadata identifies human whole-blood RNA-seq in drug-naive T2D volunteers, including longitudinal metformin-response profiling. The reported study concerns transcriptomic treatment response, not meal glucose fluxes or continuous glucose dynamics.
- **R6 — Basu R, Di Camillo B, Toffolo G, et al.** “Use of a novel triple-tracer approach to assess postprandial glucose metabolism.” *American Journal of Physiology-Endocrinology and Metabolism*. 2003;284(1):E55-E69. DOI: [10.1152/ajpendo.00190.2001](https://doi.org/10.1152/ajpendo.00190.2001); PMID: [12485809](https://pubmed.ncbi.nlm.nih.gov/12485809/). Triple-tracer method precedent for estimating meal glucose appearance and endogenous glucose production while reducing non-steady-state tracer error.
- **R7 — Van Cauter E, Mestrez F, Sturis J, Polonsky KS.** “Estimation of insulin secretion rates from C-peptide levels. Comparison of individual and standard kinetic parameters for C-peptide clearance.” *Diabetes*. 1992;41(3):368-377. DOI: [10.2337/diab.41.3.368](https://doi.org/10.2337/diab.41.3.368); PMID: [1551497](https://pubmed.ncbi.nlm.nih.gov/1551497/). Kinetic/deconvolution-method precedent; C-peptide concentration alone is not a secretion-rate observation.

### Padova benchmark investigation

The 2020 paper (R2) confirms a published Padova T2D simulator and reports 15 differential equations, 39 parameters, identification in 51 T2D subjects during one triple-tracer mixed meal, 100 generated virtual subjects, and plasma glucose/insulin/C-peptide results. The 2024 paper (R3) describes subsequent population tailoring. In Phase 0.5, publisher full-text/PDF/supplement routes and Europe PMC full-text/data metadata were checked; the article is marked restricted access and the checked routes did not expose equations, parameter tables, a supplement, dataset, or executable code. GitHub repository search did not locate a T2D implementation; authenticated code search was unavailable. This does not rule out institutional or author access.

Therefore:

- The Padova simulator is a planned benchmark, not a reproduced model.
- The 15-equation/39-parameter structure and single-meal triple-tracer cohort are reported by R2; they are not a template to copy without reading the full paper and supporting material.
- Benchmarking must first establish the exact model version, boundary, equations, units, parameterization, input protocol, and available reference outputs. The reduced candidate in this specification is not expected to match the Padova model merely because both represent glucose and insulin.

The abstract reports a glucose AUC comparison; this is a publication-reported result, not a PhysioTwin benchmark threshold. See `literature_audit.md` for the verified facts and access URLs.

The abstract reports a glucose AUC comparison; this is a publication-reported result, not a PhysioTwin benchmark threshold. See `literature_audit.md` for the verified facts and access URLs.

## Proposed modeling choices

1. Use systemic glucose amount as the conserved model pool and concentration as a derived variable at fixed effective volume.
2. Treat meal appearance as a normalized external input until meal/tracer data justify an absorption subsystem.
3. Include an explicit hepatic production flux with an insulin-response function, but leave its form and parameter values undecided.
4. Include glucose-responsive beta-cell secretion, a hepatic first-pass extraction fraction, and systemic insulin clearance. Glucose-only stimulation and first-order clearance are candidate closures, not complete physiology.
5. Represent peripheral insulin action with one delayed state and aggregate glucose clearance. This is a deliberately limited model hypothesis.
6. Omit renal glucose loss, glucagon, incretins, exercise, and tissue-specific compartments initially. This bounds the domain of validity and may be unacceptable for experiments that strongly engage those mechanisms.

## Unresolved evidence needs

- A chosen T2D dataset with raw-data access, measurement units, meal composition/timing, subject inclusion criteria, and provenance.
- Dense glucose and insulin observations plus C-peptide kinetic analysis and tracer measurements adequate to constrain secretion, clearance, meal appearance, hepatic production, and utilization. These measurements may still not uniquely separate all individual parameters.
- Full-text review of R1-R3 and any supplementary files before fixing the equations or defining benchmark acceptance criteria.
- A predeclared model domain, observation model, error model, and held-out protocol.

No physiological constants, uncertainty distributions, clinical outcomes, or validation claims are invented in the parameter registry.