import React from 'react';
import { AlertTriangle, TrendingDown, TrendingUp, HelpCircle } from 'lucide-react';
import { AdverseRiskResponse } from '../types';

interface AdverseRiskPanelProps {
  riskData: AdverseRiskResponse | null;
  isLoading: boolean;
}

export const AdverseRiskPanel: React.FC<AdverseRiskPanelProps> = ({ riskData, isLoading }) => {
  if (!riskData) return null;

  const hypo = riskData.hypoglycemia_risk;
  const hyper = riskData.hyperglycemia_risk;

  const getAlertClass = (level: string) => {
    if (level === 'EXPLORATORY MODEL CROSSING') return 'risk-moderate';
    return 'risk-low';
  };

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-title">
          <AlertTriangle size={18} color="#ef4444" />
          <span>Exploratory Model Threshold Checks</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ fontSize: '0.72rem', color: '#64748b' }}>
            Horizon: {riskData.evaluation_window_min} min
          </span>
          <span className="code-pill">Seed: 42</span>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {/* Hypoglycemia Risk Card */}
        <div style={{ border: '1px solid #fee2e2', borderRadius: '8px', padding: '12px', background: '#fffaf0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <TrendingDown size={16} color="#ef4444" />
              <strong style={{ fontSize: '0.88rem', color: '#991b1b' }}>{hypo.risk_type}</strong>
            </div>
            <span className={`risk-badge ${getAlertClass(hypo.alert_level)}`}>
              {hypo.alert_level}
            </span>
          </div>

          <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '2px' }}>
            Target: {hypo.target_definition}
          </div>

          <div className="risk-stat-grid">
            <div>
              <div className="stat-box-label">Calibrated probability</div>
              <div className="stat-box-val" style={{ color: hypo.model_threshold_crossing ? '#ef4444' : '#0f172a' }}>
                {hypo.predicted_probability === null ? 'Unavailable' : `${(hypo.predicted_probability * 100).toFixed(0)}%`}
              </div>
            </div>
            <div>
              <div className="stat-box-label">Mean-curve minimum</div>
              <div className="stat-box-val">
                {hypo.mean_projection_extreme_mmol_L.toFixed(2)} mM
              </div>
            </div>
            <div>
              <div className="stat-box-label">Time to Nadir</div>
              <div className="stat-box-val">
                {hypo.time_of_projection_extreme_min !== null ? `+${hypo.time_of_projection_extreme_min.toFixed(0)}m` : 'N/A'}
              </div>
            </div>
          </div>

          <div className="explanation-text">
            <strong>Model explanation:</strong> {hypo.mechanistic_explanation}
          </div>
        </div>

        {/* Hyperglycemia Risk Card */}
        <div style={{ border: '1px solid #fef3c7', borderRadius: '8px', padding: '12px', background: '#fffbeb' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <TrendingUp size={16} color="#d97706" />
              <strong style={{ fontSize: '0.88rem', color: '#92400e' }}>{hyper.risk_type}</strong>
            </div>
            <span className={`risk-badge ${getAlertClass(hyper.alert_level)}`}>
              {hyper.alert_level}
            </span>
          </div>

          <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '2px' }}>
            Target: {hyper.target_definition}
          </div>

          <div className="risk-stat-grid">
            <div>
              <div className="stat-box-label">Calibrated probability</div>
              <div className="stat-box-val">
                {hyper.predicted_probability === null ? 'Unavailable' : `${(hyper.predicted_probability * 100).toFixed(0)}%`}
              </div>
            </div>
            <div>
              <div className="stat-box-label">Mean-curve maximum</div>
              <div className="stat-box-val">
                {hyper.mean_projection_extreme_mmol_L.toFixed(2)} mM
              </div>
            </div>
            <div>
              <div className="stat-box-label">Time to Peak</div>
              <div className="stat-box-val">
                {hyper.time_of_projection_extreme_min !== null ? `+${hyper.time_of_projection_extreme_min.toFixed(0)}m` : 'N/A'}
              </div>
            </div>
          </div>

          <div className="explanation-text" style={{ borderLeftColor: '#f59e0b' }}>
            <strong>Model explanation:</strong> {hyper.mechanistic_explanation}
          </div>
        </div>

        {/* Ground Truth Validation Status */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.75rem', background: '#f8fafc', padding: '8px 12px', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <HelpCircle size={14} color="#64748b" />
            <span>Same-generator synthetic reference crossing: <strong>{riskData.synthetic_reference_event_occurred ? 'Present' : 'Absent'}</strong></span>
          </div>
          <span style={{ color: '#64748b' }}>Not independent validation or care guidance</span>
        </div>
      </div>
    </div>
  );
};
