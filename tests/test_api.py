"""Integration tests for the PhysioTwin REST API.
"""

import pytest
from fastapi.testclient import TestClient

from physiotwin.api.app import app

client = TestClient(app)


def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"
    assert "physiotwin" in data["engine"]
    assert "timestamp" in data


def test_api_patients_list():
    response = client.get("/api/patients")
    assert response.status_code == 200
    patients = response.json()
    assert len(patients) >= 4
    patient_ids = [p["id"] for p in patients]
    assert "SYN-001" in patient_ids
    assert "SYN-002" in patient_ids
    assert "SYN-003" in patient_ids
    assert "SYN-004" in patient_ids

    # Check synthetic provenance label
    for p in patients:
        assert "SYNTHETIC" in p["provenance"]


def test_api_patient_detail():
    response = client.get("/api/patients/SYN-001")
    assert response.status_code == 200
    p = response.json()
    assert p["id"] == "SYN-001"
    assert "parameters" in p
    assert p["parameters"]["V_G"] == 12.0
    assert p["parameters"]["M_abs"] == 70.0
    assert "solver_defaults" in p

    # Test not found
    err_response = client.get("/api/patients/NON-EXISTENT")
    assert err_response.status_code == 404


def test_api_patient_observations():
    response = client.get("/api/patients/SYN-001/observations?duration_min=180&sampling_interval_min=5.0&seed=42")
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == "SYN-001"
    assert len(data["observations"]) == 37  # 0 to 180 step 5 = 37 points
    first_pt = data["observations"][0]
    assert first_pt["timestamp_min"] == 0.0
    assert "cgm_glucose_mmol_L" in first_pt
    assert "true_glucose_mmol_L" in first_pt
    assert first_pt["is_observed"] is True


def test_api_simulation_run():
    payload = {
        "patient_id": "SYN-001",
        "duration_min": 60.0,
        "dt": 1.0,
    }
    response = client.post("/api/simulation/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["trajectories"]) > 0
    assert "diagnostics" in data
    assert "mass_balance_residual_glucose_mmol" in data["diagnostics"]


def test_api_forecast():
    payload = {
        "patient_id": "SYN-001",
        "observed_up_to_min": 120.0,
        "forecast_horizon_min": 120.0,
        "num_ensemble": 10,
        "seed": 42,
    }
    response = client.post("/api/forecast", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["observed_segment"]) > 0
    assert len(data["forecast_segment"]) > 0
    # First forecast point should be at or near 120.0
    assert abs(data["forecast_segment"][0]["time_min"] - 120.0) < 1.0

    for pt in data["forecast_segment"]:
        assert pt["glucose_lower_bound"] <= pt["glucose_upper_bound"]
        assert pt["glucose_lower_bound"] >= 0.0

    assert "model_status" in data
    assert "physiological_notes" in data
    assert data["forecast_basis"] == "SAME_GENERATOR_LATENT_STATE_CONTINUATION"
    assert data["uncertainty_interpretation"] == "UNCALIBRATED_PARAMETER_SENSITIVITY_ENVELOPE"


def test_api_evaluation_compare():
    response = client.get("/api/evaluation/compare?patient_id=SYN-001&split_point_min=120.0&forecast_horizon_min=120.0")
    assert response.status_code == 200
    data = response.json()
    assert "twin_metrics" in data
    assert "persistence_baseline_metrics" in data
    assert "linear_trend_metrics" in data

    twin = data["twin_metrics"]
    persistence = data["persistence_baseline_metrics"]

    assert twin["rmse_mmol_L"] >= 0.0
    assert persistence["rmse_mmol_L"] >= 0.0
    assert "same-generator consistency check" in data["methodology_notes"]


def test_api_adverse_risk():
    response = client.get("/api/evaluation/adverse-risk?patient_id=SYN-001&split_point_min=120.0&forecast_horizon_min=180.0")
    assert response.status_code == 200
    data = response.json()
    assert "hypoglycemia_risk" in data
    assert "hyperglycemia_risk" in data

    hypo = data["hypoglycemia_risk"]
    assert "target_definition" in hypo
    assert hypo["predicted_probability"] is None
    assert hypo["probability_status"] == "NOT_CALIBRATED"
    assert hypo["model_threshold_crossing"] is True
    assert len(hypo["mechanistic_explanation"]) > 0
    assert data["synthetic_reference_event_occurred"] in (True, False)
    assert "not independent" in data["evaluation_disclaimer"]
