# Architecture

## Overview

PhysioTwin is a Python/FastAPI backend paired with a React + TypeScript frontend. The system is intentionally framed as a research prototype and synthetic-data dashboard for Type 2 diabetes glucose dynamics.

## Components

### Backend engine
- [src/physiotwin/engine.py](../src/physiotwin/engine.py): defines the reduced-order 3-state glucose-insulin model, initial conditions, flux calculations, diagnostics, and output serialization.
- [src/physiotwin/forecast.py](../src/physiotwin/forecast.py): generates same-generator continuation forecasts and uncalibrated parameter-sensitivity envelopes.
- [src/physiotwin/evaluation.py](../src/physiotwin/evaluation.py): computes synthetic baseline comparison metrics using persistence and linear extrapolation.
- [src/physiotwin/risk.py](../src/physiotwin/risk.py): evaluates exploratory threshold crossings without claiming calibrated risk probabilities.

### Data and synthetic generation
- [src/physiotwin/synthetic.py](../src/physiotwin/synthetic.py): constructs synthetic patient profiles and scenario metadata.
- [src/physiotwin/observations.py](../src/physiotwin/observations.py): generates noisy CGM observations from the synthetic state trajectory.

### API layer
- [src/physiotwin/api/app.py](../src/physiotwin/api/app.py): application factory and FastAPI startup configuration.
- [src/physiotwin/api/routes.py](../src/physiotwin/api/routes.py): HTTP endpoints for health checks, patient data, observations, simulation, forecast, evaluation, and risk.
- [src/physiotwin/api/schemas.py](../src/physiotwin/api/schemas.py): request and response models used by the API.

### Frontend
- [frontend/src/App.tsx](../frontend/src/App.tsx): main dashboard and orchestration logic.
- [frontend/src/components](../frontend/src/components): UI panels for risk, patient selection, charting, summary cards, and stream controls.
- [frontend/src/services/api.ts](../frontend/src/services/api.ts): API client used by the dashboard.

## Runtime flow

1. Synthetic patient metadata is loaded from the Python model layer.
2. The backend generates noisy CGM observations for a selected profile.
3. The dashboard queries `/api/patients`, `/api/patients/{id}/observations`, and `/api/simulation/run`.
4. Forecast and evaluation endpoints operate on synthetic trajectories and not real patient data.
5. The React UI renders the returned metrics and risk flags for user-facing review.

## Limitations

- No clinical calibration or external validation has been established.
- Forecast uncertainty bands are synthetic sensitivity envelopes and not validated confidence intervals.
- The numerical engine is an illustrative research closure, not a validated patient model.

## Technology stack

- Python 3.10+
- FastAPI + Pydantic
- SciPy + NumPy
- React 18 + TypeScript + Vite
- Recharts
- pytest for automated verification
