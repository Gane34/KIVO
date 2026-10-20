import React from 'react';
import { BarChart3, ShieldCheck, Info } from 'lucide-react';
import { EvaluationResponse } from '../types';

interface BaselineComparisonPanelProps {
  evaluation: EvaluationResponse | null;
  isLoading: boolean;
}

export const BaselineComparisonPanel: React.FC<BaselineComparisonPanelProps> = ({
  evaluation,
  isLoading,
}) => {
  if (!evaluation) return null;

  const { twin_metrics, persistence_baseline_metrics, linear_trend_metrics, ground_truth_summary } =
    evaluation;

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-title">
          <BarChart3 size={18} color="#0284c7" />
          <span>Synthetic Forecast Method Comparison</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.72rem', color: '#16a34a' }}>
          <ShieldCheck size={14} />
          <span>Same-generator synthetic comparison</span>
        </div>
      </div>

      <p style={{ fontSize: '0.78rem', color: '#64748b', marginBottom: '12px' }}>
        Single synthetic profile: {ground_truth_summary.eval_points_count} future noisy CGM samples. ODE uses generator parameters and latent cutoff state; comparison is information-advantaged, not held-out validation.
      </p>

      <table className="metrics-table">
        <thead>
          <tr>
            <th>Model Approach</th>
            <th>RMSE (mM)</th>
            <th>MAE (mM)</th>
            <th>Forecast TIR (3.9–10 mM)</th>
            <th>Forecast TBR (&lt;3.9 mM)</th>
          </tr>
        </thead>
        <tbody>
          <tr className="highlight-row">
            <td>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span className="legend-dot" style={{ backgroundColor: '#7c3aed', width: '8px', height: '8px', borderRadius: '50%' }} />
                <strong>PhysioTwin (Mechanistic ODE)</strong>
              </div>
            </td>
            <td><strong>{twin_metrics.rmse_mmol_L.toFixed(2)}</strong></td>
            <td><strong>{twin_metrics.mae_mmol_L.toFixed(2)}</strong></td>
            <td>{twin_metrics.time_in_range_pct.toFixed(1)}%</td>
            <td>{twin_metrics.time_below_range_pct.toFixed(1)}%</td>
          </tr>
          <tr>
            <td>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span className="legend-dot" style={{ backgroundColor: '#64748b', width: '8px', height: '8px', borderRadius: '50%' }} />
                <span>Persistence Baseline (ZOH)</span>
              </div>
            </td>
            <td>{persistence_baseline_metrics.rmse_mmol_L.toFixed(2)}</td>
            <td>{persistence_baseline_metrics.mae_mmol_L.toFixed(2)}</td>
            <td>{persistence_baseline_metrics.time_in_range_pct.toFixed(1)}%</td>
            <td>{persistence_baseline_metrics.time_below_range_pct.toFixed(1)}%</td>
          </tr>
          <tr>
            <td>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span className="legend-dot" style={{ backgroundColor: '#f59e0b', width: '8px', height: '8px', borderRadius: '50%' }} />
                <span>Linear Trend Extrapolation</span>
              </div>
            </td>
            <td>{linear_trend_metrics.rmse_mmol_L.toFixed(2)}</td>
            <td>{linear_trend_metrics.mae_mmol_L.toFixed(2)}</td>
            <td>{linear_trend_metrics.time_in_range_pct.toFixed(1)}%</td>
            <td>{linear_trend_metrics.time_below_range_pct.toFixed(1)}%</td>
          </tr>
        </tbody>
      </table>

      <div style={{ marginTop: '12px', fontSize: '0.74rem', color: '#64748b', background: '#f8fafc', padding: '8px 10px', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '2px', fontWeight: 600, color: '#475569' }}>
          <Info size={12} />
          <span>Ground Truth Context (Continuous CGM Sensor):</span>
        </div>
        Mean: <strong>{ground_truth_summary.true_mean_cgm_mmol_L} mM</strong> | 
        Range: <strong>[{ground_truth_summary.true_min_cgm_mmol_L} – {ground_truth_summary.true_max_cgm_mmol_L} mM]</strong> | 
        True TIR: <strong>{ground_truth_summary.true_time_in_range_pct}%</strong>
      </div>
    </div>
  );
};
