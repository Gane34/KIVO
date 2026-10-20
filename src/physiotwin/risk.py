"""Exploratory threshold checks for synthetic ODE projections.

The module does not estimate calibrated event probabilities. Its synthetic reference
indicator is generated from the same illustrative ODE and is not independent validation.
"""

from __future__ import annotations

from typing import Any, Dict
import numpy as np

from physiotwin.forecast import run_forecast
from physiotwin.observations import generate_patient_observations
from physiotwin.synthetic import SyntheticPatient, get_patient


def evaluate_adverse_risks(
    patient: SyntheticPatient | str,
    split_point_min: float = 120.0,
    forecast_horizon_min: float = 180.0,
    seed: int = 42,
) -> Dict[str, Any]:
    """Report mean-projection threshold crossings without assigning event probabilities."""
    if isinstance(patient, str):
        patient = get_patient(patient)

    # 1. Run forecast with ensemble
    forecast_data = run_forecast(
        patient=patient,
        observed_up_to_min=split_point_min,
        forecast_horizon_min=forecast_horizon_min,
        num_ensemble=30,
        seed=seed,
    )

    forecast_pts = forecast_data["forecast_segment"]
    predicted_g = np.array([pt["glucose_predicted"] for pt in forecast_pts])
    times = np.array([pt["time_min"] for pt in forecast_pts])
    predicted_x = np.array([pt["action_predicted"] for pt in forecast_pts])
    predicted_i = np.array([pt["insulin_predicted"] for pt in forecast_pts])

    # 2. Ground truth evaluation from full simulated observation stream
    total_duration = split_point_min + forecast_horizon_min
    all_obs = generate_patient_observations(
        patient=patient,
        duration_min=total_duration,
        sampling_interval_min=2.5,
        seed=seed,
    )
    future_obs = [obs for obs in all_obs if obs["timestamp_min"] > split_point_min]
    future_true_g = np.array([obs["true_glucose_mmol_L"] for obs in future_obs])

    # These are threshold checks on the ensemble mean, not probability estimates.
    hypo_threshold = 3.9
    hypo_nadir = float(np.min(predicted_g))
    nadir_idx = int(np.argmin(predicted_g))
    nadir_time = float(times[nadir_idx])
    hypo_crossing = bool(np.any(predicted_g < hypo_threshold))

    true_hypo_occurred = bool(np.any(future_true_g < hypo_threshold))

    # Mechanistic explanation
    nadir_x = predicted_x[nadir_idx]
    nadir_i = predicted_i[nadir_idx]
    hypo_explanation = (
        f"The illustrative ODE ensemble-mean trajectory reaches {hypo_nadir:.2f} mmol/L at "
        f"t={nadir_time:.0f} min (X={nadir_x:.2f}, I={nadir_i:.1f} pmol/L in the same model). "
        "This crossing follows the model's assumed closures and hypothetical parameters; it is not "
        "an independently supported physiological explanation or a calibrated event prediction."
    )

    hypo_assessment = {
        "risk_type": "Exploratory hypoglycemia threshold check",
        "target_definition": f"Any ensemble-mean sample < {hypo_threshold} mmol/L within {forecast_horizon_min:.0f} min; no duration rule",
        "predicted_probability": None,
        "probability_status": "NOT_CALIBRATED",
        "model_threshold_crossing": hypo_crossing,
        "threshold_mmol_L": hypo_threshold,
        "mean_projection_extreme_mmol_L": round(hypo_nadir, 2),
        "time_of_projection_extreme_min": round(nadir_time - split_point_min, 1),
        "alert_level": "EXPLORATORY MODEL CROSSING" if hypo_crossing else "NO MODEL CROSSING",
        "mechanistic_explanation": hypo_explanation,
    }

    # --- Hyperglycemia Evaluation ---
    hyper_threshold = 13.9
    hyper_peak = float(np.max(predicted_g))
    peak_idx = int(np.argmax(predicted_g))
    peak_time = float(times[peak_idx])

    hyper_crossing = bool(np.any(predicted_g > hyper_threshold))

    hyper_explanation = (
        f"The illustrative ODE ensemble-mean trajectory reaches {hyper_peak:.2f} mmol/L at "
        f"t={peak_time:.0f} min. This is a threshold check on hypothetical model output, not a "
        "validated physiological explanation or calibrated event prediction."
    )

    hyper_assessment = {
        "risk_type": "Exploratory hyperglycemia threshold check",
        "target_definition": f"Any ensemble-mean sample > {hyper_threshold} mmol/L within {forecast_horizon_min:.0f} min; no duration rule",
        "predicted_probability": None,
        "probability_status": "NOT_CALIBRATED",
        "model_threshold_crossing": hyper_crossing,
        "threshold_mmol_L": hyper_threshold,
        "mean_projection_extreme_mmol_L": round(hyper_peak, 2),
        "time_of_projection_extreme_min": round(max(peak_time - split_point_min, 0.0), 1),
        "alert_level": "EXPLORATORY MODEL CROSSING" if hyper_crossing else "NO MODEL CROSSING",
        "mechanistic_explanation": hyper_explanation,
    }

    disclaimer = (
        "EXPLORATORY SYNTHETIC MODEL OUTPUT ONLY: No calibrated event probability is produced. "
        "The reference event indicator is from the same illustrative ODE generator, not independent "
        "ground truth. This output is not clinical decision support or treatment advice."
    )

    return {
        "patient_id": patient.id,
        "evaluation_window_min": float(forecast_horizon_min),
        "split_point_min": float(split_point_min),
        "hypoglycemia_risk": hypo_assessment,
        "hyperglycemia_risk": hyper_assessment,
        "synthetic_reference_event_occurred": true_hypo_occurred,
        "evaluation_disclaimer": disclaimer,
    }
