"""Synthetic CGM observation and wearable data stream generator.

Generates realistic, noisy continuous glucose monitoring data from the
underlying mechanistic physiological twin, with reproducible seeds.
"""

from __future__ import annotations

from typing import List
import numpy as np

from physiotwin.engine import SimulationConfig, simulate_model
from physiotwin.synthetic import SyntheticPatient, get_patient


def generate_patient_observations(
    patient: SyntheticPatient | str,
    duration_min: float = 360.0,
    sampling_interval_min: float = 5.0,
    seed: int = 42,
    noise_std: float = 0.15,
) -> List[dict]:
    """Generates synthetic CGM observations with discrete 5-min sampling and sensor noise.

    Returns a list of dicts with:
    - timestamp_min
    - true_glucose_mmol_L (underlying latent physiology)
    - cgm_glucose_mmol_L (sensor reading with measurement noise)
    - sensor_noise_mmol_L
    - meal_marker_mmol
    - is_observed (True)
    """
    if isinstance(patient, str):
        patient = get_patient(patient)

    config = SimulationConfig(
        parameters=patient.parameters,
        solver=patient.solver_defaults,
        experiment_name=f"cgm_stream_{patient.id}",
    )
    # Ensure solver runs with the requested duration
    config.solver = patient.solver_defaults.__class__(
        method=patient.solver_defaults.method,
        rtol=patient.solver_defaults.rtol,
        atol=patient.solver_defaults.atol,
        dt=0.5,
        duration_min=duration_min,
        initial_G_mmol_L=patient.solver_defaults.initial_G_mmol_L,
        initial_I_pmol_L=patient.solver_defaults.initial_I_pmol_L,
        initial_X_dimless=patient.solver_defaults.initial_X_dimless,
    )

    sim_result = simulate_model(config)

    # Sample on discrete grid
    sample_times = np.arange(0.0, duration_min + 1e-6, sampling_interval_min)
    # Interpolate true glucose
    true_g = np.interp(sample_times, sim_result.time_min, sim_result.G_mmol_L)

    rng = np.random.default_rng(seed)
    noise = rng.normal(loc=0.0, scale=noise_std, size=len(sample_times))

    # CGM sensor measurements cannot be negative
    cgm_g = np.maximum(true_g + noise, 0.5)

    records = []
    for t, tg, cg, n in zip(sample_times, true_g, cgm_g, noise):
        # Meal event marker at t=0
        meal_marker = patient.parameters.M_abs if np.isclose(t, 0.0) else 0.0
        records.append({
            "timestamp_min": float(round(t, 2)),
            "true_glucose_mmol_L": float(round(tg, 3)),
            "cgm_glucose_mmol_L": float(round(cg, 3)),
            "sensor_noise_mmol_L": float(round(n, 3)),
            "meal_marker_mmol": float(round(meal_marker, 2)),
            "is_observed": True,
        })

    return records
