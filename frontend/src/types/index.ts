export interface SyntheticPatientSummary {
  id: string;
  name: string;
  age: number;
  sex: string;
  bmi: number;
  diabetes_type: string;
  hba1c_pct: number;
  fasting_glucose_mmol_L: number;
  basal_insulin_pmol_L: number;
  medications: string[];
  phenotype_description: string;
  provenance: string;
}

export interface ModelParameters {
  V_G: number;
  V_I: number;
  M_abs: number;
  tau_m: number;
  HGP_0: number;
  I_ref: number;
  K_H: number;
  CL_G: number;
  S_X: number;
  k_X: number;
  tau_X: number;
  CL_I: number;
  E_H: number;
  S_beta_0: number;
  G_beta: number;
  k_beta: number;
}

export interface SolverSettings {
  method: string;
  rtol: number;
  atol: number;
  dt: number;
  duration_min: number;
  initial_G_mmol_L: number;
  initial_I_pmol_L: number;
  initial_X_dimless: number | null;
}

export interface SyntheticPatientDetail extends SyntheticPatientSummary {
  parameters: ModelParameters;
  solver_defaults: SolverSettings;
}

export interface ObservationPoint {
  timestamp_min: number;
  cgm_glucose_mmol_L: number;
  true_glucose_mmol_L: number;
  sensor_noise_mmol_L: number;
  meal_marker_mmol: number;
  is_observed: boolean;
}

export interface ForecastPoint {
  time_min: number;
  glucose_predicted: number;
  glucose_lower_bound: number;
  glucose_upper_bound: number;
  insulin_predicted: number;
  action_predicted: number;
  is_forecast: boolean;
}

export interface ForecastResponse {
  patient_id: string;
  observed_up_to_min: number;
  forecast_horizon_min: number;
  observed_segment: ObservationPoint[];
  forecast_segment: ForecastPoint[];
  model_status: string;
  physiological_notes: string;
  forecast_basis: string;
  uncertainty_interpretation: string;
  provenance: string;
}

export interface ModelMetrics {
  model_name: string;
  rmse_mmol_L: number;
  mae_mmol_L: number;
  time_in_range_pct: number;
  time_below_range_pct: number;
  time_above_range_pct: number;
}

export interface EvaluationResponse {
  patient_id: string;
  split_point_min: number;
  forecast_horizon_min: number;
  twin_metrics: ModelMetrics;
  persistence_baseline_metrics: ModelMetrics;
  linear_trend_metrics: ModelMetrics;
  ground_truth_summary: {
    eval_points_count: number;
    true_mean_cgm_mmol_L: number;
    true_time_in_range_pct: number;
    true_min_cgm_mmol_L: number;
    true_max_cgm_mmol_L: number;
  };
  methodology_notes: string;
}

export interface RiskAssessment {
  risk_type: string;
  target_definition: string;
  predicted_probability: number | null;
  probability_status: string;
  model_threshold_crossing: boolean;
  threshold_mmol_L: number;
  mean_projection_extreme_mmol_L: number;
  time_of_projection_extreme_min: number | null;
  alert_level: string;
  mechanistic_explanation: string;
}

export interface AdverseRiskResponse {
  patient_id: string;
  evaluation_window_min: number;
  split_point_min: number;
  hypoglycemia_risk: RiskAssessment;
  hyperglycemia_risk: RiskAssessment;
  synthetic_reference_event_occurred: boolean;
  evaluation_disclaimer: string;
}

export interface HealthResponse {
  status: string;
  version: string;
  engine: string;
  provenance: string;
  timestamp: string;
}
