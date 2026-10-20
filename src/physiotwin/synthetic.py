"""Synthetic patient cohort generator and registry for PhysioTwin.

All patient records generated here are strictly synthetic and illustrative.
They do not correspond to any real individuals or clinical trial participants.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List, Optional
import numpy as np

from physiotwin.engine import ModelParameters, SolverSettings, SimulationConfig


@dataclass(frozen=True)
class SyntheticPatient:
    id: str
    name: str
    age: int
    sex: str
    bmi: float
    diabetes_type: str
    hba1c_pct: float
    fasting_glucose_mmol_L: float
    basal_insulin_pmol_L: float
    medications: List[str]
    phenotype_description: str
    provenance: str
    parameters: ModelParameters
    solver_defaults: SolverSettings

    def to_dict(self) -> Dict:
        data = asdict(self)
        data["parameters"] = asdict(self.parameters)
        data["solver_defaults"] = asdict(self.solver_defaults)
        return data


COHORT: Dict[str, SyntheticPatient] = {
    "SYN-001": SyntheticPatient(
        id="SYN-001",
        name="Cohort Profile A (Baseline Illustrative)",
        age=58,
        sex="Male",
        bmi=28.4,
        diabetes_type="Type 2 Diabetes (Illustrative Model Default)",
        hba1c_pct=7.6,
        fasting_glucose_mmol_L=5.5,
        basal_insulin_pmol_L=80.0,
        medications=["Metformin 500mg BID"],
        phenotype_description="Exact baseline matching Phase 1 config.v1. Demonstrates the documented illustrative closures and postprandial trajectory.",
        provenance="SYNTHETIC_HYPOTHETICAL — generated from Phase 1 illustrative baseline configuration",
        parameters=ModelParameters(
            V_G=12.0,
            V_I=8.0,
            M_abs=70.0,
            tau_m=28.0,
            HGP_0=1.0,
            I_ref=150.0,
            K_H=40.0,
            CL_G=0.08,
            S_X=0.0025,
            k_X=0.004,
            tau_X=48.0,
            CL_I=0.12,
            E_H=0.35,
            S_beta_0=40.0,
            G_beta=4.5,
            k_beta=30.0,
        ),
        solver_defaults=SolverSettings(
            duration_min=360.0,
            dt=0.5,
            initial_G_mmol_L=5.5,
            initial_I_pmol_L=80.0,
        ),
    ),
    "SYN-002": SyntheticPatient(
        id="SYN-002",
        name="Cohort Profile B (Severe Insulin Resistance)",
        age=63,
        sex="Female",
        bmi=34.1,
        diabetes_type="Type 2 Diabetes (High Insulin Resistance)",
        hba1c_pct=8.8,
        fasting_glucose_mmol_L=7.2,
        basal_insulin_pmol_L=140.0,
        medications=["Metformin 1000mg BID", "Glipizide 5mg daily"],
        phenotype_description="Marked peripheral insulin resistance (S_X lowered by 50%) and elevated basal hepatic glucose production (HGP_0=1.4 mmol/min).",
        provenance="SYNTHETIC_HYPOTHETICAL — simulated insulin-resistant phenotype",
        parameters=ModelParameters(
            V_G=14.0,
            V_I=9.5,
            M_abs=70.0,
            tau_m=32.0,
            HGP_0=1.4,
            I_ref=160.0,
            K_H=55.0,
            CL_G=0.06,
            S_X=0.0012,
            k_X=0.0035,
            tau_X=55.0,
            CL_I=0.11,
            E_H=0.30,
            S_beta_0=60.0,
            G_beta=5.0,
            k_beta=35.0,
        ),
        solver_defaults=SolverSettings(
            duration_min=360.0,
            dt=0.5,
            initial_G_mmol_L=7.2,
            initial_I_pmol_L=140.0,
        ),
    ),
    "SYN-003": SyntheticPatient(
        id="SYN-003",
        name="Cohort Profile C (Impaired Beta-Cell Secretion)",
        age=67,
        sex="Male",
        bmi=25.2,
        diabetes_type="Type 2 Diabetes (Insulinopenic)",
        hba1c_pct=8.2,
        fasting_glucose_mmol_L=6.8,
        basal_insulin_pmol_L=45.0,
        medications=["Metformin 850mg BID", "Sitagliptin 100mg daily"],
        phenotype_description="Blunted beta-cell responsiveness (k_beta reduced by 60%, S_beta_0=25 pmol/min). Pronounced prolonged postprandial hyperglycemia.",
        provenance="SYNTHETIC_HYPOTHETICAL — simulated secretome-deficient phenotype",
        parameters=ModelParameters(
            V_G=12.5,
            V_I=8.0,
            M_abs=70.0,
            tau_m=28.0,
            HGP_0=1.1,
            I_ref=140.0,
            K_H=38.0,
            CL_G=0.075,
            S_X=0.0022,
            k_X=0.004,
            tau_X=45.0,
            CL_I=0.13,
            E_H=0.40,
            S_beta_0=25.0,
            G_beta=5.2,
            k_beta=12.0,
        ),
        solver_defaults=SolverSettings(
            duration_min=360.0,
            dt=0.5,
            initial_G_mmol_L=6.8,
            initial_I_pmol_L=45.0,
        ),
    ),
    "SYN-004": SyntheticPatient(
        id="SYN-004",
        name="Cohort Profile D (Controlled Postprandial)",
        age=52,
        sex="Female",
        bmi=26.8,
        diabetes_type="Type 2 Diabetes (Lifestyle & Metformin Controlled)",
        hba1c_pct=6.5,
        fasting_glucose_mmol_L=5.1,
        basal_insulin_pmol_L=65.0,
        medications=["Metformin 500mg daily"],
        phenotype_description="Preserved peripheral sensitivity and modest hepatic overproduction. Demonstrates tight glycemic control within target range.",
        provenance="SYNTHETIC_HYPOTHETICAL — simulated controlled glycemic phenotype",
        parameters=ModelParameters(
            V_G=11.5,
            V_I=7.8,
            M_abs=60.0,
            tau_m=30.0,
            HGP_0=0.85,
            I_ref=130.0,
            K_H=30.0,
            CL_G=0.09,
            S_X=0.0032,
            k_X=0.0045,
            tau_X=42.0,
            CL_I=0.14,
            E_H=0.38,
            S_beta_0=45.0,
            G_beta=4.2,
            k_beta=38.0,
        ),
        solver_defaults=SolverSettings(
            duration_min=360.0,
            dt=0.5,
            initial_G_mmol_L=5.1,
            initial_I_pmol_L=65.0,
        ),
    ),
}


def get_patient(patient_id: str) -> SyntheticPatient:
    if patient_id not in COHORT:
        raise KeyError(f"Synthetic patient '{patient_id}' not found in cohort.")
    return COHORT[patient_id]


def list_patients() -> List[SyntheticPatient]:
    return list(COHORT.values())
