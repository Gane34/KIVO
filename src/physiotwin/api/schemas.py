"""Pydantic schemas for the PhysioTwin REST API.

All models adhere to Pydantic v2 conventions and clearly label synthetic provenance.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "0.1.0"
    engine: str = "physiotwin-reduced-order-3state"
    provenance: str = "SYNTHETIC_RESEARCH_PROTOTYPE"
    timestamp: str


class ModelParametersSchema(BaseModel):
    V_G: float = Field(12.0, description="Volume of glucose distribution (L)")
    V_I: float = Field(8.0, description="Volume of insulin distribution (L)")
    M_abs: float = Field(70.0, description="Absorbed meal glucose amount (mmol)")
    tau_m: float = Field(28.0, description="Meal appearance time constant (min)")
    HGP_0: float = Field(1.0, description="Basal hepatic glucose production (mmol/min)")
    I_ref: float = Field(150.0, description="Reference insulin for HGP suppression (pmol/L)")
    K_H: float = Field(40.0, description="HGP suppression sensitivity (pmol/L)")
    CL_G: float = Field(0.08, description="Basal glucose clearance (L/min)")
    S_X: float = Field(0.0025, description="Insulin action sensitivity gain (L/min)")
    k_X: float = Field(0.004, description="Action filter excitation gain (L/(pmol min))")
    tau_X: float = Field(48.0, description="Action filter time constant (min)")
    CL_I: float = Field(0.12, description="Systemic insulin clearance (L/min)")
    E_H: float = Field(0.35, description="Hepatic first-pass insulin extraction fraction")
    S_beta_0: float = Field(40.0, description="Basal beta-cell secretion (pmol/min)")
    G_beta: float = Field(4.5, description="Secretion glucose threshold (mmol/L)")
    k_beta: float = Field(30.0, description="Glucose-responsive secretion gain (pmol L/(min mmol))")


class SolverSettingsSchema(BaseModel):
    method: str = "LSODA"
    rtol: float = 1e-7
    atol: float = 1e-9
    dt: float = 0.5
    duration_min: float = 360.0
    initial_G_mmol_L: float = 5.5
    initial_I_pmol_L: float = 80.0
    initial_X_dimless: Optional[float] = None


class SyntheticPatientSummary(BaseModel):
    id: str
    name: str
    age: int
    sex: str
    bmi: float
    diabetes_type: str
    hba1c_pct: float
    fasting_glucose_mmol_L: float
    basal_insulin_pmol_L: float
    medications: List[str]
    phenotype_description: str
    provenance: str


class SyntheticPatientDetail(SyntheticPatientSummary):
    parameters: ModelParametersSchema
    solver_defaults: SolverSettingsSchema


class ObservationPoint(BaseModel):
    timestamp_min: float
    cgm_glucose_mmol_L: float
    true_glucose_mmol_L: float
    sensor_noise_mmol_L: float
    meal_marker_mmol: float = 0.0
    is_observed: bool = True


class ObservationsResponse(BaseModel):
    patient_id: str
    duration_min: float
    sampling_interval_min: float
    seed: int
    noise_std: float
    provenance: str = "SYNTHETIC_OBSERVATIONS_NOISY_CGM"
    observations: List[ObservationPoint]


class SimulationRunRequest(BaseModel):
    patient_id: Optional[str] = "SYN-001"
    parameter_overrides: Optional[Dict[str, float]] = None
    duration_min: Optional[float] = 360.0
    dt: Optional[float] = 0.5


class SimulationTrajectoryPoint(BaseModel):
    time_min: float
    Q_G_mmol: float
    G_mmol_L: float
    I_pmol_L: float
    X_dimless: float
    R_a_mmol_min: float
    HGP_mmol_min: float
    R_d_mmol_min: float
    S_beta_pmol_min: float


class SimulationRunResponse(BaseModel):
    patient_id: Optional[str]
    trajectories: List[SimulationTrajectoryPoint]
    diagnostics: Dict[str, Any]
    provenance: str


class MealScenario(BaseModel):
    amount_mmol: float = 70.0
    tau_m_min: float = 28.0


class ForecastRequest(BaseModel):
    patient_id: str = "SYN-001"
    observed_up_to_min: float = Field(120.0, ge=10.0, le=350.0)
    forecast_horizon_min: float = Field(180.0, ge=15.0, le=240.0)
    meal_scenario: Optional[MealScenario] = None
    uncertainty_level: float = Field(0.95, ge=0.5, le=0.99)
    num_ensemble: int = Field(25, ge=5, le=100)
    seed: int = 42


class ForecastPoint(BaseModel):
    time_min: float
    glucose_predicted: float
    glucose_lower_bound: float
    glucose_upper_bound: float
    insulin_predicted: float
    action_predicted: float
    is_forecast: bool = True


class ForecastResponse(BaseModel):
    patient_id: str
    observed_up_to_min: float
    forecast_horizon_min: float
    observed_segment: List[ObservationPoint]
    forecast_segment: List[ForecastPoint]
    model_status: str
    physiological_notes: str
    forecast_basis: str
    uncertainty_interpretation: str
    provenance: str = "SYNTHETIC_FORECAST_ENSEMBLE"


class ModelMetrics(BaseModel):
    model_name: str
    rmse_mmol_L: float
    mae_mmol_L: float
    time_in_range_pct: float
    time_below_range_pct: float
    time_above_range_pct: float


class EvaluationResponse(BaseModel):
    patient_id: str
    split_point_min: float
    forecast_horizon_min: float
    twin_metrics: ModelMetrics
    persistence_baseline_metrics: ModelMetrics
    linear_trend_metrics: ModelMetrics
    ground_truth_summary: Dict[str, Any]
    methodology_notes: str


class RiskAssessment(BaseModel):
    risk_type: str
    target_definition: str
    predicted_probability: Optional[float]
    probability_status: str
    model_threshold_crossing: bool
    threshold_mmol_L: float
    mean_projection_extreme_mmol_L: float
    time_of_projection_extreme_min: Optional[float]
    alert_level: str
    mechanistic_explanation: str


class AdverseRiskResponse(BaseModel):
    patient_id: str
    evaluation_window_min: float
    split_point_min: float
    hypoglycemia_risk: RiskAssessment
    hyperglycemia_risk: RiskAssessment
    synthetic_reference_event_occurred: bool
    evaluation_disclaimer: str
