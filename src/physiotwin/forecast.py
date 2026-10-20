"""Physiological forecasting engine for PhysioTwin.

Generates forward mechanistic projections and parameter uncertainty bands
from an observation cutoff time, using the underlying 3-state ODE model.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import numpy as np
from scipy.integrate import solve_ivp

from physiotwin.engine import (
    ModelParameters,
    SimulationConfig,
    SolverSettings,
    compute_fluxes,
    rhs,
    simulate_model,
)
from physiotwin.observations import generate_patient_observations
from physiotwin.synthetic import SyntheticPatient, get_patient


def run_forecast(
    patient: SyntheticPatient | str,
    observed_up_to_min: float = 120.0,
    forecast_horizon_min: float = 180.0,
    meal_amount_mmol: Optional[float] = None,
    uncertainty_level: float = 0.95,
    num_ensemble: int = 25,
    seed: int = 42,
) -> Dict[str, Any]:
    """Return a same-generator ODE continuation and an uncalibrated sensitivity envelope.

    The generated observation segment is not assimilated. The forecast is initialized from
    the synthetic model's latent state at the cutoff, so it is not observation-conditioned.
    """
    if isinstance(patient, str):
        patient = get_patient(patient)

    # Total timeline duration
    total_duration = observed_up_to_min + forecast_horizon_min

    # 1. Generate full ground-truth observation stream up to observed_up_to_min
    all_observations = generate_patient_observations(
        patient=patient,
        duration_min=total_duration,
        sampling_interval_min=5.0,
        seed=seed,
    )
    observed_segment = [
        obs for obs in all_observations if obs["timestamp_min"] <= observed_up_to_min + 1e-4
    ]

    # 2. Run deterministic reference simulation from t=0 to total_duration
    base_params = patient.parameters
    if meal_amount_mmol is not None:
        # User specified custom meal override
        base_params = ModelParameters(
            **{**patient.parameters.__dict__, "M_abs": float(meal_amount_mmol)}
        )

    base_config = SimulationConfig(
        parameters=base_params,
        solver=SolverSettings(
            duration_min=total_duration,
            dt=0.5,
            initial_G_mmol_L=patient.solver_defaults.initial_G_mmol_L,
            initial_I_pmol_L=patient.solver_defaults.initial_I_pmol_L,
        ),
    )
    base_result = simulate_model(base_config)

    # Find the index closest to observed_up_to_min
    split_idx = np.argmin(np.abs(base_result.time_min - observed_up_to_min))
    t0_forecast = float(base_result.time_min[split_idx])
    y0_forecast = np.array([
        base_result.Q_G_mmol[split_idx],
        base_result.I_pmol_L[split_idx],
        base_result.X_dimless[split_idx],
    ], dtype=float)

    # 3. Forecast time grid (every 2.5 minutes for smooth visualization)
    t_eval_forecast = np.arange(t0_forecast, total_duration + 1e-6, 2.5)

    # 4. Generate Ensemble for uncertainty quantification
    rng = np.random.default_rng(seed)
    ensemble_trajectories = []

    # Include the base model first
    param_variations = [base_params]
    for _ in range(num_ensemble - 1):
        # Sample relative perturbations
        perturb_sx = rng.normal(1.0, 0.08)
        perturb_tau = rng.normal(1.0, 0.06)
        perturb_cli = rng.normal(1.0, 0.06)
        perturbed_p = ModelParameters(
            V_G=base_params.V_G,
            V_I=base_params.V_I,
            M_abs=base_params.M_abs,
            tau_m=float(np.clip(base_params.tau_m * perturb_tau, 15.0, 60.0)),
            HGP_0=base_params.HGP_0,
            I_ref=base_params.I_ref,
            K_H=base_params.K_H,
            CL_G=base_params.CL_G,
            S_X=float(np.clip(base_params.S_X * perturb_sx, 0.0005, 0.008)),
            k_X=base_params.k_X,
            tau_X=base_params.tau_X,
            CL_I=float(np.clip(base_params.CL_I * perturb_cli, 0.05, 0.25)),
            E_H=base_params.E_H,
            S_beta_0=base_params.S_beta_0,
            G_beta=base_params.G_beta,
            k_beta=base_params.k_beta,
        )
        param_variations.append(perturbed_p)

    for p in param_variations:
        sol = solve_ivp(
            fun=lambda t, y: rhs(t, y, p),
            t_span=(t0_forecast, total_duration),
            y0=y0_forecast,
            t_eval=t_eval_forecast,
            method="LSODA",
            rtol=1e-6,
            atol=1e-8,
        )
        if sol.success:
            g_traj = sol.y[0] / p.V_G
            ensemble_trajectories.append({
                "G": g_traj,
                "I": sol.y[1],
                "X": sol.y[2],
            })

    if not ensemble_trajectories:
        raise RuntimeError("Ensemble forecast integration failed.")

    g_matrix = np.array([traj["G"] for traj in ensemble_trajectories])
    i_matrix = np.array([traj["I"] for traj in ensemble_trajectories])
    x_matrix = np.array([traj["X"] for traj in ensemble_trajectories])

    # Quantiles
    alpha = (1.0 - uncertainty_level) / 2.0
    g_lower = np.percentile(g_matrix, alpha * 100, axis=0)
    g_upper = np.percentile(g_matrix, (1.0 - alpha) * 100, axis=0)
    g_mean = np.mean(g_matrix, axis=0)
    i_mean = np.mean(i_matrix, axis=0)
    x_mean = np.mean(x_matrix, axis=0)

    forecast_points = []
    for idx, t in enumerate(t_eval_forecast):
        forecast_points.append({
            "time_min": float(round(t, 2)),
            "glucose_predicted": float(round(g_mean[idx], 3)),
            "glucose_lower_bound": float(round(max(g_lower[idx], 0.0), 3)),
            "glucose_upper_bound": float(round(g_upper[idx], 3)),
            "insulin_predicted": float(round(i_mean[idx], 2)),
            "action_predicted": float(round(x_mean[idx], 3)),
            "is_forecast": True,
        })

    # Model status notes
    min_predicted_g = float(np.min(g_mean))
    if min_predicted_g < 3.9:
        status = "EXPLORATORY MODEL OUTPUT: The illustrative mean trajectory falls below 3.9 mmol/L; this is not a clinical risk alert."
    elif min_predicted_g > 10.0:
        status = "EXPLORATORY MODEL OUTPUT: The illustrative mean trajectory exceeds 10.0 mmol/L; this is not a clinical risk alert."
    else:
        status = "ILLUSTRATIVE MODEL OUTPUT: No threshold crossing in the mean trajectory; physiological validity is not established."

    notes = (
        "This is a same-generator ODE continuation, not a forecast estimated from the displayed CGM observations. "
        f"The cutoff state and parameters come from the synthetic model. The central {int(uncertainty_level*100)}% "
        f"parameter-sensitivity envelope uses {num_ensemble} arbitrary perturbation draws; it is uncalibrated "
        "and excludes observation, state-estimation, model-form, and parameter-covariance uncertainty. "
        "All parameter values are hypothetical; no clinical calibration or validation is available."
    )

    return {
        "patient_id": patient.id,
        "observed_up_to_min": float(observed_up_to_min),
        "forecast_horizon_min": float(forecast_horizon_min),
        "observed_segment": observed_segment,
        "forecast_segment": forecast_points,
        "model_status": status,
        "physiological_notes": notes,
        "forecast_basis": "SAME_GENERATOR_LATENT_STATE_CONTINUATION",
        "uncertainty_interpretation": "UNCALIBRATED_PARAMETER_SENSITIVITY_ENVELOPE",
        "provenance": "SYNTHETIC_FORECAST_ENSEMBLE",
    }
