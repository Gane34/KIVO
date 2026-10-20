import {
  AdverseRiskResponse,
  EvaluationResponse,
  ForecastResponse,
  HealthResponse,
  SyntheticPatientDetail,
  SyntheticPatientSummary,
} from '../types';

const API_BASE = '/api';

export async function fetchHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return res.json();
}

export async function fetchPatients(): Promise<SyntheticPatientSummary[]> {
  const res = await fetch(`${API_BASE}/patients`);
  if (!res.ok) throw new Error(`Failed to fetch patients: ${res.statusText}`);
  return res.json();
}

export async function fetchPatientDetail(patientId: string): Promise<SyntheticPatientDetail> {
  const res = await fetch(`${API_BASE}/patients/${encodeURIComponent(patientId)}`);
  if (!res.ok) throw new Error(`Failed to fetch patient detail: ${res.statusText}`);
  return res.json();
}

export async function fetchForecast(params: {
  patientId: string;
  observedUpToMin: number;
  forecastHorizonMin: number;
  mealAmountMmol?: number;
  uncertaintyLevel?: number;
}): Promise<ForecastResponse> {
  const payload = {
    patient_id: params.patientId,
    observed_up_to_min: params.observedUpToMin,
    forecast_horizon_min: params.forecastHorizonMin,
    meal_scenario: params.mealAmountMmol
      ? { amount_mmol: params.mealAmountMmol, tau_m_min: 28.0 }
      : undefined,
    uncertainty_level: params.uncertaintyLevel ?? 0.95,
    num_ensemble: 25,
    seed: 42,
  };

  const res = await fetch(`${API_BASE}/forecast`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errorBody = await res.text();
    throw new Error(`Forecast request failed: ${res.status} - ${errorBody}`);
  }
  return res.json();
}

export async function fetchEvaluation(
  patientId: string,
  splitPointMin: number,
  forecastHorizonMin: number
): Promise<EvaluationResponse> {
  const query = new URLSearchParams({
    patient_id: patientId,
    split_point_min: splitPointMin.toString(),
    forecast_horizon_min: forecastHorizonMin.toString(),
    seed: '42',
  });
  const res = await fetch(`${API_BASE}/evaluation/compare?${query.toString()}`);
  if (!res.ok) throw new Error(`Evaluation comparison failed: ${res.statusText}`);
  return res.json();
}

export async function fetchAdverseRisk(
  patientId: string,
  splitPointMin: number,
  forecastHorizonMin: number
): Promise<AdverseRiskResponse> {
  const query = new URLSearchParams({
    patient_id: patientId,
    split_point_min: splitPointMin.toString(),
    forecast_horizon_min: forecastHorizonMin.toString(),
    seed: '42',
  });
  const res = await fetch(`${API_BASE}/evaluation/adverse-risk?${query.toString()}`);
  if (!res.ok) throw new Error(`Adverse risk request failed: ${res.statusText}`);
  return res.json();
}
