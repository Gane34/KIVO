"""FastAPI routes for the PhysioTwin REST API.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from physiotwin.api.schemas import (
    AdverseRiskResponse,
    EvaluationResponse,
    ForecastRequest,
    ForecastResponse,
    HealthResponse,
    ObservationsResponse,
    SimulationRunRequest,
    SimulationRunResponse,
    SyntheticPatientDetail,
    SyntheticPatientSummary,
)
from physiotwin.engine import (
    ModelParameters,
    SimulationConfig,
    SolverSettings,
    simulate_model,
)
from physiotwin.evaluation import evaluate_forecast_vs_baselines
from physiotwin.forecast import run_forecast
from physiotwin.observations import generate_patient_observations
from physiotwin.risk import evaluate_adverse_risks
from physiotwin.synthetic import get_patient, list_patients

router = APIRouter(prefix="/api")


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        engine="physiotwin-reduced-order-3state",
        provenance="SYNTHETIC_RESEARCH_PROTOTYPE",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@router.get("/patients", response_model=List[SyntheticPatientSummary])
def get_patients() -> List[SyntheticPatientSummary]:
    patients = list_patients()
    return [
        SyntheticPatientSummary(
            id=p.id,
            name=p.name,
            age=p.age,
            sex=p.sex,
            bmi=p.bmi,
            diabetes_type=p.diabetes_type,
            hba1c_pct=p.hba1c_pct,
            fasting_glucose_mmol_L=p.fasting_glucose_mmol_L,
            basal_insulin_pmol_L=p.basal_insulin_pmol_L,
            medications=p.medications,
            phenotype_description=p.phenotype_description,
            provenance=p.provenance,
        )
        for p in patients
    ]


@router.get("/patients/{patient_id}", response_model=SyntheticPatientDetail)
def get_patient_detail(patient_id: str) -> SyntheticPatientDetail:
    try:
        p = get_patient(patient_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found.")

    return SyntheticPatientDetail(
        id=p.id,
        name=p.name,
        age=p.age,
        sex=p.sex,
        bmi=p.bmi,
        diabetes_type=p.diabetes_type,
        hba1c_pct=p.hba1c_pct,
        fasting_glucose_mmol_L=p.fasting_glucose_mmol_L,
        basal_insulin_pmol_L=p.basal_insulin_pmol_L,
        medications=p.medications,
        phenotype_description=p.phenotype_description,
        provenance=p.provenance,
        parameters=p.parameters.__dict__,
        solver_defaults=p.solver_defaults.__dict__,
    )


@router.get("/patients/{patient_id}/observations", response_model=ObservationsResponse)
def get_observations(
    patient_id: str,
    duration_min: float = Query(360.0, ge=30.0, le=1440.0),
    sampling_interval_min: float = Query(5.0, ge=1.0, le=30.0),
    seed: int = Query(42),
    noise_std: float = Query(0.15, ge=0.0, le=1.0),
) -> ObservationsResponse:
    try:
        patient = get_patient(patient_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found.")

    obs = generate_patient_observations(
        patient=patient,
        duration_min=duration_min,
        sampling_interval_min=sampling_interval_min,
        seed=seed,
        noise_std=noise_std,
    )
    return ObservationsResponse(
        patient_id=patient_id,
        duration_min=duration_min,
        sampling_interval_min=sampling_interval_min,
        seed=seed,
        noise_std=noise_std,
        provenance="SYNTHETIC_OBSERVATIONS_NOISY_CGM",
        observations=obs,
    )


@router.post("/simulation/run", response_model=SimulationRunResponse)
def run_simulation(req: SimulationRunRequest) -> SimulationRunResponse:
    if req.patient_id:
        try:
            patient = get_patient(req.patient_id)
            params = patient.parameters
            solver_defs = patient.solver_defaults
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Patient {req.patient_id} not found.")
    else:
        params = ModelParameters()
        solver_defs = SolverSettings()

    if req.parameter_overrides:
        merged = {**params.__dict__, **req.parameter_overrides}
        params = ModelParameters(**merged)

    solver = SolverSettings(
        method=solver_defs.method,
        rtol=solver_defs.rtol,
        atol=solver_defs.atol,
        dt=req.dt or 0.5,
        duration_min=req.duration_min or 360.0,
        initial_G_mmol_L=solver_defs.initial_G_mmol_L,
        initial_I_pmol_L=solver_defs.initial_I_pmol_L,
        initial_X_dimless=solver_defs.initial_X_dimless,
    )

    config = SimulationConfig(
        parameters=params,
        solver=solver,
        experiment_name=f"api_sim_{req.patient_id or 'custom'}",
    )
    result = simulate_model(config)
    trajectories = result.to_record_array()

    return SimulationRunResponse(
        patient_id=req.patient_id,
        trajectories=trajectories,
        diagnostics=result.diagnostics,
        provenance="SYNTHETIC_SIMULATION_3STATE_ODE",
    )


@router.post("/forecast", response_model=ForecastResponse)
def get_forecast(req: ForecastRequest) -> ForecastResponse:
    try:
        patient = get_patient(req.patient_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Patient {req.patient_id} not found.")

    meal_amt = req.meal_scenario.amount_mmol if req.meal_scenario else None
    result = run_forecast(
        patient=patient,
        observed_up_to_min=req.observed_up_to_min,
        forecast_horizon_min=req.forecast_horizon_min,
        meal_amount_mmol=meal_amt,
        uncertainty_level=req.uncertainty_level,
        num_ensemble=req.num_ensemble,
        seed=req.seed,
    )
    return ForecastResponse(**result)


@router.get("/evaluation/compare", response_model=EvaluationResponse)
def get_baseline_comparison(
    patient_id: str = Query("SYN-001"),
    split_point_min: float = Query(120.0, ge=20.0, le=300.0),
    forecast_horizon_min: float = Query(180.0, ge=15.0, le=240.0),
    seed: int = Query(42),
) -> EvaluationResponse:
    try:
        patient = get_patient(patient_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found.")

    res = evaluate_forecast_vs_baselines(
        patient=patient,
        split_point_min=split_point_min,
        forecast_horizon_min=forecast_horizon_min,
        seed=seed,
    )
    return EvaluationResponse(**res)


@router.get("/evaluation/adverse-risk", response_model=AdverseRiskResponse)
def get_adverse_risk(
    patient_id: str = Query("SYN-001"),
    split_point_min: float = Query(120.0, ge=20.0, le=300.0),
    forecast_horizon_min: float = Query(180.0, ge=15.0, le=240.0),
    seed: int = Query(42),
) -> AdverseRiskResponse:
    try:
        patient = get_patient(patient_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found.")

    res = evaluate_adverse_risks(
        patient=patient,
        split_point_min=split_point_min,
        forecast_horizon_min=forecast_horizon_min,
        seed=seed,
    )
    return AdverseRiskResponse(**res)
