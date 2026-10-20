# PhysioTwin
## Digital Twin Proof of Concept for Exploring Glucose Dynamics in Type 2 Diabetes

Developed under KIVO — Intelligent Digital Twins & AI

PhysioTwin is a research prototype that explores how a simplified glucose–insulin dynamics model, synthetic observations, simulation, and forecasting can be combined to study glucose behavior over time. The project integrates a reduced-order dynamical model with a FastAPI backend and a React frontend to provide an interactive dashboard for demonstration and research exploration.

> Research prototype only. This project uses synthetic data and hypothetical model assumptions. It has not been clinically validated and must not be used for diagnosis, treatment, or patient-care decisions.

---

## 1. Team Details

- Team Name: KIVO
- Project Title: PhysioTwin
- Team Leader: Ganesh Mandala
- Team Members: KIVO research team
- Contact Email: ganeshmandala108@gmail.com
- Contact Number: +91 6302496321

## 2. College / Institution Information

- Institution: A.M. Reddy Memorial College of Engineering and Technology
- Department: Cyber Security
- Location: Andhra Pradesh, India

## 3. Project Overview

Type 2 diabetes involves complex glucose regulation influenced by meals, insulin secretion, insulin action, and glucose utilization. A single glucose measurement does not sufficiently capture the time-dependent behavior of glucose metabolism.

PhysioTwin is designed to demonstrate a digital-twin-inspired workflow for investigating such dynamics in a transparent and reproducible manner. The system combines mechanistic modeling, synthetic observations, simulation, forecasting, and dashboard-based visualization to support educational and research-oriented analysis.

The goal is not to provide clinical guidance, but to establish a foundation for future work in personalized and validated physiological digital twins.

## 4. Problem Statement

A deeper understanding of glucose dynamics requires modeling the temporal evolution of key physiological states rather than relying only on snapshot measurements. However, building clinically reliable digital-twin systems requires careful parameterization, suitable data, and validation against real-world evidence.

PhysioTwin addresses this by providing a proof-of-concept environment in which model assumptions, synthetic trajectories, and forecast behavior can be explored in a structured and inspectable way.

## 5. Healthcare Use Case

Primary Condition: Type 2 Diabetes Mellitus (T2D)

Potential applications:
- Explore simulated glucose trajectories over time
- Investigate how model assumptions affect system behavior
- Generate exploratory short-term forecasts
- Compare model outputs against simple baseline predictors
- Visualize synthetic observations, forecasts, and risk-related indicators
- Support future research into more rigorous, calibrated digital-twin workflows

Intended users:
- Digital health researchers
- Biomedical engineering students
- Developers exploring physiological modeling systems
- Academic teams studying digital-twin concepts

Safety note:
PhysioTwin is not intended to diagnose diabetes, prescribe treatment, or provide clinical alerts. It is a research demonstration only.

## 6. Technical Stack

| Component | Technology |
|---|---|
| Backend API | Python, FastAPI |
| Numerical Computation | NumPy, SciPy |
| API Server | Uvicorn |
| Frontend | React, TypeScript, Vite |
| Visualization | Recharts |
| Testing | pytest |
| API Documentation | FastAPI OpenAPI / Swagger UI |
| Version Control | Git, GitHub |

## 7. Model and Data Methodology

The project uses a simplified three-state reduced-order physiological model representing:
- systemic glucose amount
- systemic insulin concentration
- delayed peripheral insulin action

The model is described by the following equations:

$$
\frac{dQ_G}{dt} = R_{a,m} + HGP - R_d
$$

$$
V_I \frac{dI}{dt} = (1 - E_H) S_\beta - CL_I I
$$

$$
\frac{dX}{dt} = k_X I - \frac{X}{\tau_X}
$$

Where:
- $Q_G$: modeled glucose amount
- $I$: modeled systemic insulin concentration
- $X$: delayed insulin-action state
- $R_{a,m}$: meal-related glucose appearance
- $HGP$: hepatic glucose production
- $R_d$: glucose disposal

The system is intentionally lightweight and transparent to support research exploration rather than clinical deployment. All demo data are synthetic, and model assumptions are hypothetical unless supported by appropriate calibration and scientific validation.

### Forecasting and Evaluation

The prototype includes:
- synthetic patient phenotypes and glucose observations
- forecast horizons of 30, 60, 120, and 180 minutes
- Monte Carlo ensemble forecasts
- persistence and linear-trend baseline comparisons
- MAE, RMSE, and Time in Range (TIR) metrics
- exploratory threshold-based risk flags

These outputs are intended for research and demonstration only and are not calibrated clinical confidence intervals or medical alerts.

### Data Methodology

This proof of concept uses synthetic patient profiles and synthetic glucose observations. No real-patient clinical validation is claimed or implied. Results generated from synthetic data demonstrate the workflow and the behavior of the model under a controlled experimental setting, but they do not establish real-world predictive accuracy or clinical validity.

## 8. System Architecture

The system follows a conceptual workflow:

1. Synthetic patient profiles and glucose observations
2. Physiological model and numerical simulation engine
3. Forecast generation and baseline comparison
4. FastAPI backend
5. React dashboard and chart visualization
6. Evaluation metrics and exploratory risk indicators

This architecture is designed to make the digital-twin concept accessible, reproducible, and easy to inspect.

## 9. Verified Status

The following checks were executed and passed in the current workspace:

- `python -m pytest -q` → 21 passed in 3.50s
- live API checks against the running FastAPI server → HTTP 200 for health, patient list, observations, simulation, and forecast endpoints
- `cd frontend && npm run build` → production build succeeded
- `cd frontend && npm run dev -- --host 127.0.0.1 --port 4173` → app served successfully at `http://127.0.0.1:4173`

## 10. Installation and Execution

### Prerequisites

- Python 3.10+
- Node.js and npm
- Git

### Backend Setup

From the repository root:

```bash
cd <path-to-project>
python -m pytest -q
python -m uvicorn physiotwin.api.app:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend Setup

Open a separate terminal:

```bash
cd frontend
npm install
npm run build
npm run dev -- --host 127.0.0.1 --port 4173
```

### API Documentation

Once the backend is running, open:

- `http://127.0.0.1:8000/docs`

## 11. Example API Requests

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/patients
curl "http://127.0.0.1:8000/api/patients/SYN-001/observations?duration_min=60&sampling_interval_min=5.0&seed=42"
curl -X POST http://127.0.0.1:8000/api/simulation/run -H "Content-Type: application/json" -d "{\"patient_id\":\"SYN-001\",\"duration_min\":60.0,\"dt\":1.0}"
curl -X POST http://127.0.0.1:8000/api/forecast -H "Content-Type: application/json" -d "{\"patient_id\":\"SYN-001\",\"observed_up_to_min\":120.0,\"forecast_horizon_min\":120.0,\"seed\":42}"
```

## 12. Demo Workflow

1. Start the backend.
2. Start the frontend.
3. Select a synthetic patient profile.
4. View the generated observation stream and simulation outputs.
5. Review forecast and evaluation metrics.
6. Evaluate limitations and responsible-use guidance before drawing conclusions.

## 13. Limitations and Responsible Use

- Synthetic data only; no real-patient calibration
- Model parameters are hypothetical and require scientific justification
- Forecast intervals are exploratory and not validated clinical confidence intervals
- Threshold-based risk flags are experimental and should not be treated as medical alerts
- The project does not provide medical advice, diagnosis, or treatment recommendations
- The system is not a clinically validated medical device

## 14. Repository Structure

```text
KIVO/
├── README.md
├── LICENSE
├── physiotwin/
├── tests/
├── frontend/
├── docs/
│   ├── architecture.pdf
│   ├── PhysioTwin_Presentation.pptx
│   ├── PhysioTwin_Presentation.pdf
│   ├── demo-script.md
│   └── verification-report.md
└── .gitignore
```

## 15. License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

## 16. Troubleshooting

- If backend imports fail, ensure the project root is on the Python path and dependencies are installed.
- If the frontend does not start, run `npm install` inside the `frontend` directory.
- If the app loads but API calls fail, confirm the backend is running on port `8000`.
- If command paths do not work on Windows, run the commands from the project root in PowerShell.

## 17. Disclaimer

PhysioTwin is an experimental research prototype developed for educational and technical exploration. It is not a medical device and must not be used to make patient-care decisions, diagnosis, or treatment recommendations.

---

**Project:** PhysioTwin  
**Technology Initiative:** KIVO  
**Public GitHub Repository:** https://github.com/Gane34/KIVO
