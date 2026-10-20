from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from physiotwin.engine import ModelParameters, SimulationConfig, SolverSettings, run_demonstration


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "experiments" / "phase1_initial" / "config.v1.json"


def load_experiment_config(config_path: str | Path) -> SimulationConfig:
    path = Path(config_path)
    raw_bytes = path.read_bytes()
    document: Any = json.loads(raw_bytes)
    if not isinstance(document, dict):
        raise ValueError("Experiment configuration must be a JSON object.")
    try:
        parameters = ModelParameters(**document["parameters"])
        solver = SolverSettings(**document["solver"])
        config = SimulationConfig(
            parameters=parameters,
            solver=solver,
            experiment_name=document["experiment_name"],
            experiment_version=document["experiment_version"],
            configuration_sha256=hashlib.sha256(raw_bytes).hexdigest(),
            provenance=document["provenance"],
            notes=document["notes"],
        )
    except (KeyError, TypeError) as error:
        raise ValueError(f"Invalid experiment configuration: {error}") from error
    config.validate()
    return config


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the deterministic Phase 1 illustrative experiment.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--output", type=Path, default=Path("outputs/phase1_initial_experiment"))
    args = parser.parse_args()
    config = load_experiment_config(args.config)
    paths = run_demonstration(args.output, config)
    for name, path in paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
