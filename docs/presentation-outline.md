# Presentation outline

## 1. Problem statement
- Type 2 diabetes is a complex metabolic disease with large clinical burden.
- A transparent research prototype can explore model structure and forecast behavior.

## 2. Proposed solution
- Reduced-order mechanistic digital twin built from a glucose–insulin state system.
- Synthetic patient profiles and CGM-inspired observation streams highlight workflow and internal mechanics.

## 3. System architecture
- Python backend with FastAPI
- React dashboard frontend
- sciPy ODE solver and synthetic data generation
- forecast + baseline evaluation + risk threshold checks

## 4. Workflow
- Select synthetic patient
- Inspect data and observation stream
- Run simulation and forecast
- Compare with baseline metrics and risk flags

## 5. Results and evidence
- Backend tests pass
- API requests are successful
- Frontend build passes
- Demo app renders and serves successfully

## 6. Limitations
- Synthetic-only data
- No clinical calibration
- Uncalibrated uncertainty bands
- No medical decision support claim

## 7. Future work
- Fit to a real dataset
- Add formal validation and model-selection workflow
- Improve uncertainty and state estimation
- Expand the biological closure set with explicit evidence
