import React from 'react';
import { HelpCircle, AlertCircle, CheckCircle2, ShieldCheck } from 'lucide-react';

export const ModelStatusPanel: React.FC = () => {
  return (
    <div className="card">
      <div className="card-header">
        <div className="card-title">
          <HelpCircle size={18} color="#0284c7" />
          <span>Model Assumptions & Scientific Status</span>
        </div>
        <span className="code-pill">Phase 1 Reduced-Order</span>
      </div>

      <div className="assumptions-list">
        <div className="assumption-item">
          <CheckCircle2 size={16} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div>
            <strong>Coupled 3-State Balances:</strong> Glucose pool amount (<span className="code-pill">Q_G</span>), systemic insulin (<span className="code-pill">I</span>), and delayed action (<span className="code-pill">X</span>). Preserves declared mass balances to solver accuracy (&lt; 10⁻⁵ mmol).
          </div>
        </div>

        <div className="assumption-item">
          <AlertCircle size={16} color="#f59e0b" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div>
            <strong>Illustrative Constitutive Closures:</strong> Uses shape-2 gamma meal forcing (<span className="code-pill">tau_m=28m</span>), reciprocal-hinge hepatic extraction (<span className="code-pill">I_ref=150</span>), and thresholded affine beta-cell secretion (<span className="code-pill">G_beta=4.5</span>). These are software-testable illustrative closures, not verified human biology.
          </div>
        </div>

        <div className="assumption-item">
          <AlertCircle size={16} color="#f59e0b" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div>
            <strong>Postprandial Nadir Behavior:</strong> As documented in <span className="code-pill">reports/phase1_1_diagnostics.md</span>, persistent basal secretion floor combined with delayed action produces net pool depletion over 360 min. This behavior is faithfully preserved from the baseline and not artificially clipped.
          </div>
        </div>

        <div className="assumption-item">
          <ShieldCheck size={16} color="#0284c7" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div>
            <strong>Research Data Boundary:</strong> 100% synthetic cohort data. Does not access or misjoin transcriptomic samples (GSE153792). No clinical validation is claimed; parameters are hypothetical.
          </div>
        </div>
      </div>
    </div>
  );
};
