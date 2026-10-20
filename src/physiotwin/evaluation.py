"""Single-profile synthetic comparison and forecast metrics for PhysioTwin.

Compares an information-advantaged same-generator ODE continuation against simple baselines:
1. Zero-Order Hold (Persistence): assumes glucose remains at the last observed value.
2. Linear Extrapolation: projects recent rate of change over the preceding 15 minutes.

The persistence and linear baselines use only history through split_point_min. The ODE
continuation uses the generator's exact parameters and hidden state and is not an equal-information comparator.
"""

from __future__ import annotations

from typing import Any, Dict, List
import numpy as np

from physiotwin.forecast import run_forecast
from physiotwin.observations import generate_patient_observations
from physiotwin.synthetic import SyntheticPatient, get_patient


def _calculate_metrics(
    y_true: np.ndarray, y_pred: np.ndarray, model_name: str
) -> Dict[str, Any]:
    """Calculates RMSE, MAE, TIR, TBR, and TAR on the evaluation horizon."""
    errors = y_pred - y_true
    rmse = float(np.sqrt(np.mean(errors ** 2)))
    mae = float(np.mean(np.abs(errors)))

    # Reference-range occupancy of predictions, not accuracy against the target.
    n_total = len(y_pred)
    if n_total == 0:
        tir = tbr = tar = 0.0
    else:
        tir = float(np.sum((y_pred >= 3.9) & (y_pred <= 10.0)) / n_total * 100.0)
        tbr = float(np.sum(y_pred < 3.9) / n_total * 100.0)
        tar = float(np.sum(y_pred > 10.0) / n_total * 100.0)

    return {
        "model_name": model_name,
        "rmse_mmol_L": round(rmse, 3),
        "mae_mmol_L": round(mae, 3),
        "time_in_range_pct": round(tir, 1),
        "time_below_range_pct": round(tbr, 1),
        "time_above_range_pct": round(tar, 1),
    }


def evaluate_forecast_vs_baselines(
    patient: SyntheticPatient | str,
    split_point_min: float = 120.0,
    forecast_horizon_min: float = 180.0,
    seed: int = 42,
) -> Dict[str, Any]:
    """Runs twin forecast, calculates baselines, and computes rigorous performance metrics."""
    if isinstance(patient, str):
        patient = get_patient(patient)

    total_duration = split_point_min + forecast_horizon_min

    # 1. Ground truth observation stream across entire span
    all_observations = generate_patient_observations(
        patient=patient,
        duration_min=total_duration,
        sampling_interval_min=5.0,
        seed=seed,
    )

    # Historical observations available at prediction time (<= split_point_min)
    history = [obs for obs in all_observations if obs["timestamp_min"] <= split_point_min + 1e-4]
    # Future ground truth to evaluate against (> split_point_min)
    future = [obs for obs in all_observations if obs["timestamp_min"] > split_point_min + 1e-4]

    if not future:
        raise ValueError("Evaluation horizon contains no future observation points.")

    eval_times = np.array([obs["timestamp_min"] for obs in future])
    y_true_cgm = np.array([obs["cgm_glucose_mmol_L"] for obs in future])
    # 2. Mechanistic Twin Forecast
    twin_res = run_forecast(
        patient=patient,
        observed_up_to_min=split_point_min,
        forecast_horizon_min=forecast_horizon_min,
        num_ensemble=20,
        seed=seed,
    )
    # Interpolate twin predictions onto the evaluation timestamps
    forecast_points = twin_res["forecast_segment"]
    f_times = np.array([pt["time_min"] for pt in forecast_points])
    f_glucose = np.array([pt["glucose_predicted"] for pt in forecast_points])
    y_pred_twin = np.interp(eval_times, f_times, f_glucose)

    # 3. Persistence Baseline (Zero-Order Hold): G(t) = G(t_split)
    last_observed_g = history[-1]["cgm_glucose_mmol_L"]
    y_pred_persistence = np.full_like(eval_times, fill_value=last_observed_g)

    # 4. Linear Extrapolation Baseline: extrapolate recent 15 min slope, bounded [2.0, 20.0]
    if len(history) >= 4:
        # 15 minutes of history is 3 intervals of 5 min
        recent_dx = history[-1]["timestamp_min"] - history[-4]["timestamp_min"]
        recent_dy = history[-1]["cgm_glucose_mmol_L"] - history[-4]["cgm_glucose_mmol_L"]
        slope = recent_dy / max(recent_dx, 1.0)
    else:
        slope = 0.0

    dt_from_split = eval_times - split_point_min
    y_pred_linear = np.clip(last_observed_g + slope * dt_from_split, 2.0, 25.0)

    # Compute metrics against ground-truth CGM observations
    twin_metrics = _calculate_metrics(y_true_cgm, y_pred_twin, "Same-generator ODE continuation")
    persistence_metrics = _calculate_metrics(y_true_cgm, y_pred_persistence, "Persistence Baseline (ZOH)")
    linear_metrics = _calculate_metrics(y_true_cgm, y_pred_linear, "Linear Trend Extrapolation")

    # True range metrics
    ground_truth_tir = float(np.sum((y_true_cgm >= 3.9) & (y_true_cgm <= 10.0)) / len(y_true_cgm) * 100.0)

    methodology = (
        f"Single synthetic profile and cutoff; evaluation over [{split_point_min:.0f}, "
        f"{total_duration:.0f}] min ({len(future)} noisy synthetic CGM points). "
        "Errors are in mmol/L and all models are scored on the same future timestamps. "
        "Persistence and trend use only history through the cutoff. The ODE continuation uses "
        "the generator's exact parameters and latent cutoff state, so this is an information-"
        "advantaged same-generator consistency check, not a fair or subject-held-out forecast benchmark. "
        "Reported range occupancy is calculated from predictions, not agreement with observed range occupancy."
    )

    return {
        "patient_id": patient.id,
        "split_point_min": float(split_point_min),
        "forecast_horizon_min": float(forecast_horizon_min),
        "twin_metrics": twin_metrics,
        "persistence_baseline_metrics": persistence_metrics,
        "linear_trend_metrics": linear_metrics,
        "ground_truth_summary": {
            "eval_points_count": len(future),
            "true_mean_cgm_mmol_L": round(float(np.mean(y_true_cgm)), 2),
            "true_time_in_range_pct": round(ground_truth_tir, 1),
            "true_min_cgm_mmol_L": round(float(np.min(y_true_cgm)), 2),
            "true_max_cgm_mmol_L": round(float(np.max(y_true_cgm)), 2),
        },
        "methodology_notes": methodology,
    }
