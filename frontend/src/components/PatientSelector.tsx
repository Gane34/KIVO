import React from 'react';
import { Users, CheckCircle2 } from 'lucide-react';
import { SyntheticPatientSummary } from '../types';

interface PatientSelectorProps {
  patients: SyntheticPatientSummary[];
  selectedPatientId: string;
  onSelectPatient: (patientId: string) => void;
  isLoading: boolean;
}

export const PatientSelector: React.FC<PatientSelectorProps> = ({
  patients,
  selectedPatientId,
  onSelectPatient,
  isLoading,
}) => {
  return (
    <div className="card">
      <div className="card-header">
        <div className="card-title">
          <Users size={18} color="#0284c7" />
          <span>Synthetic Patient Cohort</span>
        </div>
        <span style={{ fontSize: '0.72rem', color: '#64748b' }}>
          {patients.length} Phenotypes
        </span>
      </div>

      <div className="patient-list">
        {patients.map((patient) => {
          const isSelected = patient.id === selectedPatientId;
          return (
            <button
              key={patient.id}
              className={`patient-card-item ${isSelected ? 'active' : ''}`}
              onClick={() => onSelectPatient(patient.id)}
              disabled={isLoading}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="patient-item-id">{patient.id}</span>
                {isSelected && <CheckCircle2 size={16} color="#0284c7" />}
              </div>
              <div className="patient-item-name">{patient.name}</div>
              <div className="patient-item-meta">
                <span>HbA1c: <strong>{patient.hba1c_pct}%</strong></span>
                <span>Fasting: <strong>{patient.fasting_glucose_mmol_L} mM</strong></span>
                <span>BMI: <strong>{patient.bmi}</strong></span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
