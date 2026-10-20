"""End-to-end automated demonstration script for PhysioTwin.

Executes the complete Digital Twin workflow:
1. System Health Check
2. Patient Cohort Selection (SYN-001)
3. Simulated Wearable CGM Stream Acquisition
4. Forward Mechanistic Forecast with Uncertainty Bounds
5. Same-Generator Synthetic Comparison (RMSE, MAE, predicted range occupancy)
6. Adverse-Event Risk Evaluation & Mechanistic Explanation
"""

import sys
import json
from fastapi.testclient import TestClient

from physiotwin.api.app import app

client = TestClient(app)

def run_workflow():
    print("=" * 70)
    print("  PHYSIOTWIN: END-TO-END DIGITAL TWIN DEMONSTRATION WORKFLOW")
    print("  Digital Twin Challenge 2026 | Research Prototype")
    print("=" * 70)

    # 1. Health Check
    print("\n[Step 1] Checking API Health and Engine Status...")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health = res.json()
    print(f"  [OK] Status: {health['status']} | Version: {health['version']}")
    print(f"  [OK] Engine: {health['engine']}")
    print(f"  [OK] Provenance: {health['provenance']}")

    # 2. Synthetic Patient Cohort
    print("\n[Step 2] Retrieving Synthetic Patient Cohort...")
    res = client.get("/api/patients")
    assert res.status_code == 200
    patients = res.json()
    print(f"  [OK] Found {len(patients)} synthetic phenotypes:")
    for p in patients:
        print(f"    - [{p['id']}] {p['name']} (HbA1c: {p['hba1c_pct']}%, Fasting: {p['fasting_glucose_mmol_L']} mM)")

    patient_id = "SYN-001"
    print(f"\n[Step 3] Selecting Patient: {patient_id} (Phase 1 Baseline Illustrative)...")
    res = client.get(f"/api/patients/{patient_id}")
    assert res.status_code == 200
    detail = res.json()
    print(f"  [OK] Phenotype: {detail['phenotype_description']}")
    print(f"  [OK] Medications: {', '.join(detail['medications'])}")
    print(f"  [OK] Parameters: V_G={detail['parameters']['V_G']}L, M_abs={detail['parameters']['M_abs']}mmol, S_X={detail['parameters']['S_X']}")

    # 4. Stream Observations
    print(f"\n[Step 4] Retrieving Simulated CGM Stream up to t=120 min...")
    res = client.get(f"/api/patients/{patient_id}/observations?duration_min=120&sampling_interval_min=5.0")
    assert res.status_code == 200
    obs_data = res.json()
    obs_points = obs_data["observations"]
    print(f"  [OK] Received {len(obs_points)} CGM samples (every 5 min)")
    print(f"  [OK] Reading at t=0 min: {obs_points[0]['cgm_glucose_mmol_L']} mmol/L (Meal event M_abs=70 mmol)")
    print(f"  [OK] Reading at t=60 min: {obs_points[12]['cgm_glucose_mmol_L']} mmol/L")
    print(f"  [OK] Reading at t=120 min: {obs_points[-1]['cgm_glucose_mmol_L']} mmol/L")

    # 5. Forward Forecast with Uncertainty
    print(f"\n[Step 5] Running 3-State Mechanistic Forecast from t=120 min across 180 min horizon...")
    payload = {
        "patient_id": patient_id,
        "observed_up_to_min": 120.0,
        "forecast_horizon_min": 180.0,
        "num_ensemble": 25,
        "seed": 42,
    }
    res = client.post("/api/forecast", json=payload)
    assert res.status_code == 200
    fc = res.json()
    fc_points = fc["forecast_segment"]
    print(f"  [OK] Generated {len(fc_points)} projected trajectory points")
    print(f"  [OK] Projection at t=180 min: {fc_points[24]['glucose_predicted']:.2f} mmol/L (uncalibrated sensitivity envelope: [{fc_points[24]['glucose_lower_bound']:.2f} - {fc_points[24]['glucose_upper_bound']:.2f}])")
    print(f"  [OK] Projection at t=240 min: {fc_points[48]['glucose_predicted']:.2f} mmol/L (uncalibrated sensitivity envelope: [{fc_points[48]['glucose_lower_bound']:.2f} - {fc_points[48]['glucose_upper_bound']:.2f}])")
    print(f"  [OK] Forecast basis: {fc['forecast_basis']}")
    print(f"  [OK] Uncertainty: {fc['uncertainty_interpretation']}")
    print(f"  [OK] Model Status: {fc['model_status']}")

    # 6. Baseline Comparison
    print(f"\n[Step 6] Comparing same-generator synthetic output against simple baselines...")
    res = client.get(f"/api/evaluation/compare?patient_id={patient_id}&split_point_min=120&forecast_horizon_min=180")
    assert res.status_code == 200
    ev = res.json()
    twin = ev["twin_metrics"]
    persistence = ev["persistence_baseline_metrics"]
    linear = ev["linear_trend_metrics"]
    print(f"  [OK] Evaluation over {ev['ground_truth_summary']['eval_points_count']} ground truth samples:")
    print(f"    - PhysioTwin Twin:    RMSE={twin['rmse_mmol_L']:.2f} mM | MAE={twin['mae_mmol_L']:.2f} mM | TIR={twin['time_in_range_pct']}%")
    print(f"    - Persistence (ZOH):  RMSE={persistence['rmse_mmol_L']:.2f} mM | MAE={persistence['mae_mmol_L']:.2f} mM | TIR={persistence['time_in_range_pct']}%")
    print(f"    - Linear Trend:       RMSE={linear['rmse_mmol_L']:.2f} mM | MAE={linear['mae_mmol_L']:.2f} mM | TIR={linear['time_in_range_pct']}%")
    print(f"    - Methodology: {ev['methodology_notes']}")

    # 7. Adverse-Event Risk Evaluation
    print(f"\n[Step 7] Evaluating Adverse-Event Risk Workflow...")
    res = client.get(f"/api/evaluation/adverse-risk?patient_id={patient_id}&split_point_min=120&forecast_horizon_min=180")
    assert res.status_code == 200
    rk = res.json()
    hypo = rk["hypoglycemia_risk"]
    print(f"  [OK] Target: {hypo['target_definition']}")
    probability_text = "not calibrated" if hypo["predicted_probability"] is None else f"{hypo['predicted_probability']*100:.0f}%"
    print(f"  [OK] Event probability: {probability_text} | Exploratory status: {hypo['alert_level']}")
    print(f"  [OK] Mean-curve minimum: {hypo['mean_projection_extreme_mmol_L']:.2f} mM at +{hypo['time_of_projection_extreme_min']:.0f} min from cutoff")
    print(f"  [OK] Mechanistic Explanation: {hypo['mechanistic_explanation']}")
    print(f"  [OK] Same-generator synthetic reference crossing: {'present' if rk['synthetic_reference_event_occurred'] else 'absent'}")

    print("\n" + "=" * 70)
    print("  DEMONSTRATION COMPLETE: ALL 7 STEPS EXECUTED SUCCESSFULLY")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    run_workflow()
