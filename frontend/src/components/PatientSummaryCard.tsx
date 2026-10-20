import React from 'react';
import { User, Pill, FileText, Activity } from 'lucide-react';
import { SyntheticPatientDetail } from '../types';

interface PatientSummaryCardProps {
  patient: SyntheticPatientDetail | null;
}

export const PatientSummaryCard: React.FC<PatientSummaryCardProps> = ({ patient }) => {
  if (!patient) return null;

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-title">
          <User size={18} color="#0284c7" />
          <span>Patient Profile & Metadata</span>
        </div>
        <span className="code-pill">{patient.id}</span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div>
          <div style={{ fontSize: '1rem', fontWeight: 700, color: '#0f172a' }}>
            {patient.name}
          </div>
          <div style={{ fontSize: '0.78rem', color: '#64748b' }}>
            {patient.age}y • {patient.sex} • BMI {patient.bmi} kg/m² • {patient.diabetes_type}
          </div>
        </div>

        <div style={{ background: '#f8fafc', padding: '10px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px', fontSize: '0.78rem' }}>
            <div>
              <span style={{ color: '#64748b' }}>Fasting Glucose:</span>
              <div style={{ fontWeight: 600, color: '#0f172a' }}>{patient.fasting_glucose_mmol_L} mmol/L</div>
            </div>
            <div>
              <span style={{ color: '#64748b' }}>Basal Insulin:</span>
              <div style={{ fontWeight: 600, color: '#0f172a' }}>{patient.basal_insulin_pmol_L} pmol/L</div>
            </div>
            <div>
              <span style={{ color: '#64748b' }}>HbA1c:</span>
              <div style={{ fontWeight: 600, color: '#0f172a' }}>{patient.hba1c_pct} %</div>
            </div>
            <div>
              <span style={{ color: '#64748b' }}>Meal Glucose M_abs:</span>
              <div style={{ fontWeight: 600, color: '#0f172a' }}>{patient.parameters.M_abs} mmol</div>
            </div>
          </div>
        </div>

        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', fontWeight: 600, color: '#475569', marginBottom: '4px' }}>
            <Pill size={14} />
            <span>Current Medications:</span>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {patient.medications.map((med, idx) => (
              <span
                key={idx}
                style={{
                  fontSize: '0.72rem',
                  background: '#f1f5f9',
                  border: '1px solid #cbd5e1',
                  padding: '2px 8px',
                  borderRadius: '4px',
                  color: '#334155',
                }}
              >
                {med}
              </span>
            ))}
          </div>
        </div>

        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', fontWeight: 600, color: '#475569', marginBottom: '4px' }}>
            <FileText size={14} />
            <span>Phenotype & Pathophysiology:</span>
          </div>
          <p style={{ fontSize: '0.78rem', color: '#475569', lineHeight: 1.45, background: '#f8fafc', padding: '8px', borderRadius: '6px' }}>
            {patient.phenotype_description}
          </p>
        </div>

        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', fontWeight: 600, color: '#475569', marginBottom: '4px' }}>
            <Activity size={14} />
            <span>Key Kinetic Parameters:</span>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '4px', fontSize: '0.7rem' }}>
            <div className="code-pill">V_G: {patient.parameters.V_G} L</div>
            <div className="code-pill">S_X: {patient.parameters.S_X}</div>
            <div className="code-pill">k_beta: {patient.parameters.k_beta}</div>
            <div className="code-pill">HGP_0: {patient.parameters.HGP_0}</div>
            <div className="code-pill">CL_I: {patient.parameters.CL_I}</div>
            <div className="code-pill">tau_m: {patient.parameters.tau_m} m</div>
          </div>
        </div>
      </div>
    </div>
  );
};
