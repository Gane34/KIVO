from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import numpy as np
from scipy.integrate import solve_ivp


@dataclass(frozen=True)
class ModelParameters:
    """Illustrative reduced-order model parameters.

    These values are not published physiological constants. Their provenance is intentionally
    restricted to the Phase 1 illustrative closure in docs/phase1_model_closures.md.
    """

    V_G: float = 12.0
    V_I: float = 8.0
    M_abs: float = 70.0
    tau_m: float = 28.0
    HGP_0: float = 1.0
    I_ref: float = 150.0
    K_H: float = 40.0
    CL_G: float = 0.08
    S_X: float = 0.0025
    k_X: float = 0.004
    tau_X: float = 48.0
    CL_I: float = 0.12
    E_H: float = 0.35
    S_beta_0: float = 40.0
    G_beta: float = 4.5
    k_beta: float = 30.0

    def validate(self) -> None:
        for name, value in self.__dict__.items():
            if not np.isfinite(value):
                raise ValueError(f"Parameter {name} is not finite: {value!r}")

        positive_fields = [
            "V_G",
            "V_I",
            "tau_m",
            "HGP_0",
            "K_H",
            "CL_G",
            "S_X",
            "k_X",
            "tau_X",
            "CL_I",
            "S_beta_0",
            "G_beta",
            "k_beta",
        ]
        for field_name in positive_fields:
            if getattr(self, field_name) <= 0:
                raise ValueError(f"Parameter {field_name} must be positive.")

        if self.M_abs < 0:
            raise ValueError("Parameter M_abs must be nonnegative.")

        if not (0.0 <= self.E_H < 1.0):
            raise ValueError("E_H must be in [0, 1).")
        if self.I_ref < 0:
            raise ValueError("I_ref must be nonnegative.")


@dataclass(frozen=True)
class SolverSettings:
    method: str = "LSODA"
    rtol: float = 1e-7
    atol: float = 1e-9
    dt: float = 0.5
    duration_min: float = 360.0
    initial_G_mmol_L: float = 5.5
    initial_I_pmol_L: float = 80.0
    initial_X_dimless: float | None = None

    def validate(self) -> None:
        if self.duration_min <= 0 or self.dt <= 0:
            raise ValueError("duration_min and dt must be positive.")
        if self.rtol <= 0 or self.atol <= 0:
            raise ValueError("rtol and atol must be positive.")
        if self.initial_G_mmol_L <= 0 or self.initial_I_pmol_L <= 0:
            raise ValueError("Initial glucose and insulin concentrations must be positive.")


@dataclass
class SimulationConfig:
    parameters: ModelParameters = field(default_factory=ModelParameters)
    solver: SolverSettings = field(default_factory=SolverSettings)
    experiment_name: str = ""
    experiment_version: str = ""
    configuration_sha256: str = ""
    provenance: str = "illustrative_hypothetical" 
    notes: str = "Minimal reduced-order model; not patient-specific or clinically validated."

    def validate(self) -> None:
        self.parameters.validate()
        self.solver.validate()


@dataclass
class SimulationResult:
    time_min: np.ndarray
    Q_G_mmol: np.ndarray
    G_mmol_L: np.ndarray
    I_pmol_L: np.ndarray
    X_dimless: np.ndarray
    R_a_mmol_min: np.ndarray
    HGP_mmol_min: np.ndarray
    R_d_mmol_min: np.ndarray
    S_beta_pmol_min: np.ndarray
    diagnostics: Dict[str, Any]

    def to_record_array(self) -> List[Dict[str, float]]:
        return [
            {
                "time_min": float(t),
                "Q_G_mmol": float(qg),
                "G_mmol_L": float(g),
                "I_pmol_L": float(i),
                "X_dimless": float(x),
                "R_a_mmol_min": float(ra),
                "HGP_mmol_min": float(hgp),
                "R_d_mmol_min": float(rd),
                "S_beta_pmol_min": float(sb),
            }
            for t, qg, g, i, x, ra, hgp, rd, sb in zip(
                self.time_min,
                self.Q_G_mmol,
                self.G_mmol_L,
                self.I_pmol_L,
                self.X_dimless,
                self.R_a_mmol_min,
                self.HGP_mmol_min,
                self.R_d_mmol_min,
                self.S_beta_pmol_min,
            )
        ]


DEFAULT_CONFIG = SimulationConfig()


def meal_appearance_rate(t: np.ndarray | float, params: ModelParameters) -> np.ndarray | float:
    t_array = np.asarray(t, dtype=float)
    q = np.zeros_like(t_array, dtype=float)
    mask = t_array >= 0.0
    if np.any(mask):
        q[mask] = (t_array[mask] / (params.tau_m ** 2)) * np.exp(-t_array[mask] / params.tau_m)
    return q * params.M_abs


def hepatic_glucose_production(I: np.ndarray | float, params: ModelParameters) -> np.ndarray | float:
    I_array = np.asarray(I, dtype=float)
    hgp_response = 1.0 / (1.0 + np.maximum(I_array - params.I_ref, 0.0) / params.K_H)
    return params.HGP_0 * hgp_response


def beta_cell_secretion(G: np.ndarray | float, params: ModelParameters) -> np.ndarray | float:
    G_array = np.asarray(G, dtype=float)
    return params.S_beta_0 + params.k_beta * np.maximum(G_array - params.G_beta, 0.0)


def compute_fluxes(y: np.ndarray, params: ModelParameters) -> Dict[str, np.ndarray]:
    Q_G, I, X = y[:, 0], y[:, 1], y[:, 2]
    G = Q_G / params.V_G
    R_a = meal_appearance_rate(y[:, 0] * 0.0 + np.arange(y.shape[0]) * 0.0, params)  # placeholder to be replaced by time-based input
    return {
        "Q_G_mmol": Q_G,
        "G_mmol_L": G,
        "I_pmol_L": I,
        "X_dimless": X,
        "R_a_mmol_min": R_a,
        "HGP_mmol_min": hepatic_glucose_production(I, params),
        "R_d_mmol_min": (params.CL_G + params.S_X * X) * G,
        "S_beta_pmol_min": beta_cell_secretion(G, params),
    }


def rhs(t: float, y: np.ndarray, params: ModelParameters, time_input: np.ndarray | None = None) -> np.ndarray:
    Q_G, I, X = y
    G = Q_G / params.V_G
    # Use the true continuous meal appearance function in time rather than the nearest
    # sample on the output grid. The nearest-grid lookup made the ODE numerically
    # sensitive to solver tolerances and subtly violated the model's conservation checks.
    R_a = meal_appearance_rate(np.asarray([t], dtype=float), params)[0]
    HGP = hepatic_glucose_production(I, params)
    R_d = (params.CL_G + params.S_X * X) * G
    S_beta = beta_cell_secretion(G, params)
    dQ_G = R_a + HGP - R_d
    dI = ((1.0 - params.E_H) * S_beta - params.CL_I * I) / params.V_I
    dX = params.k_X * I - X / params.tau_X
    return np.asarray([dQ_G, dI, dX], dtype=float)


def initial_state(config: SimulationConfig) -> np.ndarray:
    params = config.parameters
    solver = config.solver
    if solver.initial_X_dimless is None:
        x0 = params.k_X * solver.initial_I_pmol_L * params.tau_X
    else:
        x0 = solver.initial_X_dimless
    qg0 = params.V_G * solver.initial_G_mmol_L
    return np.asarray([qg0, solver.initial_I_pmol_L, x0], dtype=float)


def simulate_model(config: SimulationConfig | None = None) -> SimulationResult:
    config = DEFAULT_CONFIG if config is None else config
    config.validate()
    params = config.parameters
    solver = config.solver
    times = np.arange(0.0, solver.duration_min + solver.dt / 2.0, solver.dt, dtype=float)
    y0 = initial_state(config)

    def function_for_solve(_, state):
        return rhs(_, state, params, times)

    solution = solve_ivp(
        function_for_solve,
        t_span=(0.0, solver.duration_min),
        y0=y0,
        t_eval=times,
        method=solver.method,
        rtol=solver.rtol,
        atol=solver.atol,
    )
    if not solution.success:
        raise RuntimeError(f"Solver failed: {solution.message}")

    y = solution.y.T
    Q_G = y[:, 0]
    I = y[:, 1]
    X = y[:, 2]
    G = Q_G / params.V_G
    R_a = np.asarray([meal_appearance_rate(np.asarray([t], dtype=float), params)[0] for t in times], dtype=float)
    HGP = hepatic_glucose_production(I, params)
    R_d = (params.CL_G + params.S_X * X) * G
    S_beta = beta_cell_secretion(G, params)

    mass_balance = np.trapezoid(R_a + HGP - R_d, times) - (Q_G[-1] - Q_G[0])
    insulin_balance = np.trapezoid((1.0 - params.E_H) * S_beta - params.CL_I * I, times) - (params.V_I * (I[-1] - I[0]))

    diagnostics = {
        "solver_status": solution.status,
        "solver_message": solution.message,
        "mass_balance_residual_glucose_mmol": float(mass_balance),
        "insulin_balance_residual_pmol": float(insulin_balance),
        "integrated_meal_input_mmol": float(np.trapezoid(R_a, times)),
        "integrated_glucose_production_mmol": float(np.trapezoid(HGP, times)),
        "integrated_glucose_utilization_mmol": float(np.trapezoid(R_d, times)),
        "integrated_beta_cell_secretion_pmol": float(np.trapezoid((1.0 - params.E_H) * S_beta, times)),
        "integrated_systemic_clearance_pmol": float(np.trapezoid(params.CL_I * I, times)),
        "provenance": config.provenance,
        "notes": config.notes,
    }

    return SimulationResult(
        time_min=times,
        Q_G_mmol=Q_G,
        G_mmol_L=G,
        I_pmol_L=I,
        X_dimless=X,
        R_a_mmol_min=R_a,
        HGP_mmol_min=HGP,
        R_d_mmol_min=R_d,
        S_beta_pmol_min=S_beta,
        diagnostics=diagnostics,
    )


def save_results_csv(result: SimulationResult, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "time_min",
        "Q_G_mmol",
        "G_mmol_L",
        "I_pmol_L",
        "X_dimless",
        "R_a_mmol_min",
        "HGP_mmol_min",
        "R_d_mmol_min",
        "S_beta_pmol_min",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(",".join(fields) + "\n")
        for record in result.to_record_array():
            handle.write(
                ",".join(str(record[field]) for field in fields) + "\n"
            )
    return output_path


def save_metadata_json(config: SimulationConfig, result: SimulationResult, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "software_version": "0.1.0",
        "experiment_name": config.experiment_name,
        "experiment_version": config.experiment_version,
        "configuration_sha256": config.configuration_sha256,
        "provenance": config.provenance,
        "notes": config.notes,
        "solver": {
            "method": config.solver.method,
            "rtol": config.solver.rtol,
            "atol": config.solver.atol,
            "dt": config.solver.dt,
            "duration_min": config.solver.duration_min,
        },
        "parameters": {
            key: float(value)
            for key, value in config.parameters.__dict__.items()
        },
        "diagnostics": result.diagnostics,
    }
    import json
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
    return output_path


def plot_state_trajectories(result: SimulationResult, output_path: str | Path) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)
    axes = axes.flatten()

    axes[0].plot(result.time_min, result.G_mmol_L, label="G")
    axes[0].set_title("Systemic glucose concentration")
    axes[0].set_xlabel("Time (min)")
    axes[0].set_ylabel("mmol/L")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(result.time_min, result.I_pmol_L, label="I")
    axes[1].set_title("Systemic insulin")
    axes[1].set_xlabel("Time (min)")
    axes[1].set_ylabel("pmol/L")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(result.time_min, result.X_dimless)
    axes[2].set_title("Aggregate action state")
    axes[2].set_xlabel("Time (min)")
    axes[2].set_ylabel("dimensionless")
    axes[2].grid(True, alpha=0.3)

    axes[3].plot(result.time_min, result.R_a_mmol_min, label="meal")
    axes[3].plot(result.time_min, result.HGP_mmol_min, label="HGP")
    axes[3].plot(result.time_min, result.R_d_mmol_min, label="utilization")
    axes[3].set_title("Flux comparison")
    axes[3].set_xlabel("Time (min)")
    axes[3].set_ylabel("mmol/min")
    axes[3].grid(True, alpha=0.3)
    axes[3].legend(loc="best")

    fig.savefig(output_path, dpi=200)
    return output_path


def run_demonstration(
    output_dir: str | Path = "outputs/phase1_demo",
    config: SimulationConfig | None = None,
) -> Dict[str, Path]:
    if config is None:
        config = SimulationConfig(
            provenance="illustrative_hypothetical",
            notes="Deterministic example using the documented Phase 1 illustrative closure only.",
        )
    result = simulate_model(config)
    output_root = Path(output_dir)
    csv_path = save_results_csv(result, output_root / "phase1_result.csv")
    metadata_path = save_metadata_json(config, result, output_root / "phase1_metadata.json")
    plot_path = plot_state_trajectories(result, output_root / "phase1_state_trajectories.png")
    return {
        "results_csv": csv_path,
        "metadata_json": metadata_path,
        "plot_png": plot_path,
    }
