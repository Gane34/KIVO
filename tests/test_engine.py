import numpy as np
import pytest

from physiotwin.engine import (
    DEFAULT_CONFIG,
    ModelParameters,
    SimulationConfig,
    SolverSettings,
    rhs,
    simulate_model,
)


def test_state_dimension_and_validation():
    config = DEFAULT_CONFIG
    result = simulate_model(config)
    assert result.Q_G_mmol.shape == result.G_mmol_L.shape == result.I_pmol_L.shape == result.X_dimless.shape
    assert result.Q_G_mmol.shape[0] > 0

    bad = ModelParameters(V_G=-1.0)
    try:
        bad.validate()
        raise AssertionError("Expected validation error for negative V_G.")
    except ValueError:
        pass

    config_bad = SimulationConfig(
        solver=SolverSettings(duration_min=-1.0, dt=0.5),
    )
    try:
        config_bad.validate()
        raise AssertionError("Expected validation error for invalid solver settings.")
    except ValueError:
        pass


def test_solver_returns_finite_outputs():
    result = simulate_model(DEFAULT_CONFIG)
    assert np.all(np.isfinite(result.time_min))
    assert np.all(np.isfinite(result.Q_G_mmol))
    assert np.all(np.isfinite(result.G_mmol_L))
    assert np.all(np.isfinite(result.I_pmol_L))
    assert np.all(np.isfinite(result.X_dimless))
    assert result.diagnostics["solver_status"] == 0


def test_positivity_for_valid_domain():
    result = simulate_model(DEFAULT_CONFIG)
    assert np.all(result.G_mmol_L >= 0.0)
    assert np.all(result.I_pmol_L >= 0.0)
    assert np.all(result.X_dimless >= 0.0)
    assert np.all(result.R_a_mmol_min >= 0.0)
    assert np.all(result.HGP_mmol_min >= 0.0)
    assert np.all(result.R_d_mmol_min >= 0.0)
    assert np.all(result.S_beta_pmol_min >= 0.0)


def test_mass_balance_residual_is_small():
    result = simulate_model(DEFAULT_CONFIG)
    assert abs(result.diagnostics["mass_balance_residual_glucose_mmol"]) < 1e-2
    assert abs(result.diagnostics["insulin_balance_residual_pmol"]) < 2e-2


def test_zero_input_has_stable_behavior():
    config = SimulationConfig(
        parameters=ModelParameters(M_abs=0.0),
        solver=SolverSettings(duration_min=180.0, dt=0.25),
    )
    result = simulate_model(config)
    assert np.all(result.R_a_mmol_min >= 0.0)
    assert np.all(np.isfinite(result.G_mmol_L))
    assert np.all(result.I_pmol_L >= 0.0)
    assert np.all(result.X_dimless >= 0.0)


def test_reproducibility():
    result_1 = simulate_model(DEFAULT_CONFIG)
    result_2 = simulate_model(DEFAULT_CONFIG)
    np.testing.assert_allclose(result_1.G_mmol_L, result_2.G_mmol_L, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(result_1.I_pmol_L, result_2.I_pmol_L, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(result_1.X_dimless, result_2.X_dimless, rtol=1e-12, atol=1e-12)


def test_tolerance_sensitivity():
    config_loose = SimulationConfig(solver=SolverSettings(rtol=1e-4, atol=1e-6))
    config_tight = SimulationConfig(solver=SolverSettings(rtol=1e-7, atol=1e-9))
    loose = simulate_model(config_loose)
    tight = simulate_model(config_tight)
    assert np.max(np.abs(loose.G_mmol_L - tight.G_mmol_L)) < 1e-2
    assert np.max(np.abs(loose.I_pmol_L - tight.I_pmol_L)) < 1e-1


def test_rhs_uses_time_continuous_meal_forcing():
    params = ModelParameters(M_abs=70.0, tau_m=28.0)
    # The meal forcing should be evaluated at the actual time, not a nearest-grid sample.
    t = 13.5
    y = np.array([params.V_G * 5.5, 80.0, params.k_X * 80.0 * 48.0], dtype=float)
    deriv = rhs(t, y, params, time_input=np.linspace(0.0, 360.0, 721))
    assert np.isfinite(deriv).all()
    assert deriv[0] > 0.0
    assert deriv[2] == pytest.approx(params.k_X * 80.0 - y[2] / params.tau_X)
