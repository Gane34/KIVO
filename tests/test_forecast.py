"""Tests for the forecast and evaluation modules.
"""

import numpy as np
import pytest

from physiotwin.evaluation import _calculate_metrics
from physiotwin.evaluation import evaluate_forecast_vs_baselines
from physiotwin.forecast import run_forecast
from physiotwin.observations import generate_patient_observations
from physiotwin.synthetic import get_patient


def test_observations_reproducibility():
    obs1 = generate_patient_observations("SYN-001", duration_min=60.0, seed=123)
    obs2 = generate_patient_observations("SYN-001", duration_min=60.0, seed=123)
    assert len(obs1) == len(obs2)
    for p1, p2 in zip(obs1, obs2):
        assert p1["cgm_glucose_mmol_L"] == pytest.approx(p2["cgm_glucose_mmol_L"], abs=1e-5)
        assert p1["true_glucose_mmol_L"] == pytest.approx(p2["true_glucose_mmol_L"], abs=1e-5)


def test_forecast_ensemble_and_uncalibrated_sensitivity_envelope():
    res = run_forecast("SYN-001", observed_up_to_min=90.0, forecast_horizon_min=90.0, num_ensemble=15, seed=42)
    forecast_pts = res["forecast_segment"]
    assert len(forecast_pts) > 0
    assert forecast_pts[0]["time_min"] == pytest.approx(90.0, abs=1.0)
    for pt in forecast_pts:
        assert pt["glucose_lower_bound"] <= pt["glucose_predicted"] <= pt["glucose_upper_bound"] + 1e-3
        assert pt["glucose_lower_bound"] >= 0.0
    assert res["forecast_basis"] == "SAME_GENERATOR_LATENT_STATE_CONTINUATION"
    assert res["uncertainty_interpretation"] == "UNCALIBRATED_PARAMETER_SENSITIVITY_ENVELOPE"
    assert "not a forecast estimated from the displayed CGM" in res["physiological_notes"]


def test_evaluation_discloses_information_advantage():
    res = evaluate_forecast_vs_baselines("SYN-001", split_point_min=100.0, forecast_horizon_min=100.0, seed=42)
    assert "information-advantaged same-generator" in res["methodology_notes"]
    assert "same future timestamps" in res["methodology_notes"]

    # Check metric values are valid numbers
    for m in (res["twin_metrics"], res["persistence_baseline_metrics"], res["linear_trend_metrics"]):
        assert np.isfinite(m["rmse_mmol_L"])
        assert np.isfinite(m["mae_mmol_L"])
        assert 0.0 <= m["time_in_range_pct"] <= 100.0


def test_forecast_metrics_use_consistent_mmol_per_liter_arithmetic():
    metrics = _calculate_metrics(
        y_true=np.asarray([4.0, 8.0]),
        y_pred=np.asarray([5.0, 12.0]),
        model_name="test",
    )
    assert metrics["mae_mmol_L"] == 2.5
    assert metrics["rmse_mmol_L"] == pytest.approx(np.sqrt(8.5), abs=0.001)
    assert metrics["time_in_range_pct"] == 50.0
    assert metrics["time_below_range_pct"] == 0.0
    assert metrics["time_above_range_pct"] == 50.0
