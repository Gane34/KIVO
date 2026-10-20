# Research Scope

## Objective

Develop a reproducible, testable, conservation-based mechanistic simulation of glucose regulation in T2D. The long-term research objective is to support carefully bounded patient-specific research and treatment-response experiments. The current work is a research prototype, not a clinically validated medical device.

## Phase 0 question

What is the smallest defensible model boundary for a meal-related glucose response that includes circulating glucose, hepatic glucose production, pancreatic insulin secretion and clearance, and peripheral glucose uptake/action, without adding mechanisms for which the research question or evidence is not yet defined?

## Proposed initial boundary

Represent meal-derived glucose appearance into the systemic circulation, endogenous hepatic glucose production, circulating glucose, endogenous insulin secretion with hepatic first-pass extraction represented explicitly or as an unresolved effective term, systemic insulin clearance, and aggregate peripheral glucose uptake with delayed insulin action. The candidate equations and their limitations are in `physiology_specification.md`.

Meal appearance is an input in the first version, not a newly invented gastric-emptying subsystem. Hepatic glucose production and beta-cell secretion are explicit fluxes, but their functional forms and parameter values remain unresolved until an appropriate dataset and measurement protocol are selected.

## Included, deferred, and excluded

| Mechanism or data | Phase 0 decision | Reason |
|---|---|---|
| Meal-related glucose appearance | Include as a measured or declared input flux | Needed for a meal-response boundary; absorption kinetics need suitable observations before a mechanistic gut model can be selected. |
| Circulating glucose | Include as an amount/concentration state | Central conserved pool for the initial balance. |
| Hepatic glucose production | Include as an explicit source flux | Required physiological mechanism; insulin response form and non-insulin regulation are not yet identified. |
| Pancreatic insulin secretion | Include as an explicit glucose-responsive source term | Required mechanism; glucose-only stimulation is a proposed simplification, not a complete beta-cell model. |
| Insulin distribution and clearance | Include systemic clearance; resolve first-pass hepatic extraction from data or keep it explicitly lumped | Plasma insulin alone does not uniquely identify secretion and clearance. |
| Peripheral glucose uptake and insulin action | Include aggregate uptake and one delayed action state as a candidate | Meets the minimum scope while avoiding unsupported tissue-specific compartments. |
| Renal glucose loss | Defer from the initial equations; restrict interpretation to a range where omission is defensible or add it when supported | It can become important during marked hyperglycemia; omitting it is not valid for all T2D conditions. |
| Glucagon, incretins, counter-regulation, exercise, circadian effects, free fatty acids, glycogen stores, and tissue-specific uptake | Defer | Add only when a defined question and suitable evidence require them. Their absence limits interpretation. |
| GSE153792 transcriptomics | Exploratory evidence only; keep separate from physiological trajectories | Whole-blood expression and treatment-response labels are not meal glucose/insulin dynamics and cannot calibrate ODE time courses directly. |
| Padova T2D simulator | Benchmark for a later documented comparison | Its published model is a distinct, substantially larger model; no replication is claimed in Phase 0. |

## Evidence labels

- **Published evidence:** directly reported observations, model structures, or results in a cited source.
- **Proposed modeling choice:** a candidate mathematical closure made to define a tractable future model; it is not asserted as uniquely physiological.
- **Unresolved:** a question for which this phase does not have sufficient measurements or verified evidence to choose a function, value, or boundary.
- **Hypothesis:** a testable proposition that must be assessed against data; not a validated conclusion.

## Scope guardrails

Do not infer simulation parameters from transcriptomic expression without an independently justified mechanistic and measurement link. Do not merge transcriptomic samples with simulation rows. Do not claim Padova equivalence, patient-level predictive performance, clinical utility, or external validation before the relevant tests and comparisons have been completed.