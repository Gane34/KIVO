# PhysioTwin

PhysioTwin is a research prototype for a synthetic Type 2 diabetes glucose-dynamics dashboard. It combines a reduced-order ODE engine with a FastAPI backend and a React frontend for demonstration, forecast comparison, and exploratory risk review. The project is not clinically validated and is intended only for research and educational use.

## Project goal

This project demonstrates a mechanistic digital-twin concept for glucose regulation in a synthetic T2D scenario. It is designed to be reproducible and transparent, with model assumptions, uncertainty notes, and synthetic-only provenance clearly labeled.

## Intended use case

- Educational demonstration of glucose-insulin dynamics
- API and frontend verification for a prototype research workflow
- Synthetic simulation and forecast comparison against simple baselines
- Scientific review of model assumptions and limitations

## Team and institution

- Team: TODO
- Institution: TODO
- Contact: TODO

## Technology stack

- Python 3.10+
- FastAPI
- Pydantic
- SciPy and NumPy
- React 18
- TypeScript
- Vite
- Recharts
- pytest

## Model and data methodology

The model is a three-state reduced-order system representing systemic glucose amount, systemic insulin concentration, and delayed insulin action. All patient data used in the demo are synthetic and illustrative. The forecast workflow is a same-generator continuation and its uncertainty envelope is not a clinically validated confidence interval.

## Verified status

The following checks were executed and passed in the current workspace:

- `python -m pytest -q` → 21 passed in 3.50s
- live API checks against the running FastAPI server → HTTP 200 for health, patient list, observations, simulation, and forecast endpoints
- `cd frontend && npm run build` → production build succeeded
- `cd frontend && npm run dev -- --host 127.0.0.1 --port 4173` → app served successfully at http://127.0.0.1:4173

## Installation and execution

### Python backend

```powershell
cd D:\Ganesh\digitaltwin
python -m pytest -q
python -m uvicorn physiotwin.api.app:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend

```powershell
cd D:\Ganesh\digitaltwin\frontend
npm install
npm run build
npm run dev -- --host 127.0.0.1 --port 4173
```

### API docs

Once the backend is running, visit:

- http://127.0.0.1:8000/docs

## Example API requests

```powershell
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/patients
curl "http://127.0.0.1:8000/api/patients/SYN-001/observations?duration_min=60&sampling_interval_min=5.0&seed=42"
curl -X POST http://127.0.0.1:8000/api/simulation/run -H "Content-Type: application/json" -d "{\"patient_id\":\"SYN-001\",\"duration_min\":60.0,\"dt\":1.0}"
curl -X POST http://127.0.0.1:8000/api/forecast -H "Content-Type: application/json" -d "{\"patient_id\":\"SYN-001\",\"observed_up_to_min\":120.0,\"forecast_horizon_min\":120.0,\"seed\":42}"
```

## Demo workflow

1. Start the backend.
2. Start the frontend.
3. Select a synthetic patient profile.
4. View the generated observation stream and simulation outputs.
5. Review forecast and evaluation metrics.
6. Read the scientific limitations and responsible-use disclaimer before drawing conclusions.

## Known limitations

- Synthetic data only; no real-patient calibration.
- Parameter assumptions are hypothetical.
- Forecast intervals are synthetic sensitivity envelopes, not validated clinical confidence intervals.
- This project does not provide medical advice, diagnosis, or treatment recommendations.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).

## Troubleshooting

- If backend imports fail, ensure the project root is on the Python path and dependencies are installed.
- If the frontend does not start, run `npm install` inside [frontend](frontend).
- If the app serves but requests fail, confirm the backend is running on port 8000.
- If a command uses a Windows path mismatch, run it from the project root in PowerShell.

## Responsible-use disclaimer

This repository is a research prototype. It is not a clinically validated device and must not be used for real medical decisions, diagnosis, or treatment planning.
