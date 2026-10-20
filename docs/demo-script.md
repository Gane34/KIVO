# Demo script

## 5-7 minute live demo outline

1. Problem framing: Type 2 diabetes forecasting and the need for a transparent mechanistic prototype.
2. Architecture overview: Flask? No — FastAPI backend, React frontend, same-generator forecast, risk thresholds.
3. Synthetic patient selection: choose a patient profile, explain that all patients are synthetic and illustrative.
4. Observation stream: show CGM generation and meal markers without claiming real patient monitoring.
5. Simulation: run a simulation end-to-end and visualize glucose, insulin, and action state trajectories.
6. Forecast and metrics: show baseline comparison metrics and the uncalibrated prediction envelope.
7. Responsible-use disclaimer: explain that the system is for research demonstration only and not clinical support.

## 20-25 minute recording outline

### 00:00-03:00 Introduction and motivation
- Define the problem and target user problem.
- Explain synthetic-data scope and limitations.

### 03:00-06:00 Architecture walkthrough
- Show backend, frontend, ODE engine, data generation, and evaluation modules.
- Reference actual files and endpoints.

### 06:00-11:00 Live API demonstration
- Show `/api/health`, patient listing, observations, simulation, and forecast endpoints.
- Include exact command examples and status codes.

### 11:00-16:00 Frontend walk-through
- Select patient, explain synthetic profile, review charts and metrics.
- Show forecast and risk panels.

### 16:00-20:00 Scientific honesty and limitations
- Describe synthetic status, parameter assumptions, and uncertainty disclaimers.
- Explain why the model is not clinical-grade.

### 20:00-25:00 Final summary and next steps
- Explain validation results and future work.

## Manual recording procedure

1. Open the frontend at http://127.0.0.1:4173.
2. Use OBS Studio or a similar screen recorder.
3. Record at 1080p with microphone narration.
4. Capture terminal commands and the UI in separate scenes.
5. Keep the final edit under 20-25 minutes and include the scientific limitations disclaimer.

Do not claim a completed recording unless the video file actually exists and was checked.
