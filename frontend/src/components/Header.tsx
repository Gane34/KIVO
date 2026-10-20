import React from 'react';
import { Activity, ShieldAlert, Cpu } from 'lucide-react';
import { HealthResponse } from '../types';

interface HeaderProps {
  health: HealthResponse | null;
  isLoading: boolean;
}

export const Header: React.FC<HeaderProps> = ({ health, isLoading }) => {
  return (
    <header>
      <div className="disclaimer-banner">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="banner-badge">Synthetic Research Prototype</span>
          <span>
            Digital Twin Challenge 2026: Mechanistic glucose regulation simulator. Not approved for clinical use.
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', opacity: 0.85 }}>
          <ShieldAlert size={14} />
          <span>Strict Synthetic Data Separation Active</span>
        </div>
      </div>

      <div className="main-header">
        <div className="brand-wrapper">
          <div className="brand-icon">
            <Activity size={24} />
          </div>
          <div>
            <div className="brand-title">
              PhysioTwin
              <span style={{ fontSize: '0.75rem', fontWeight: 500, color: '#0284c7', background: '#e0f2fe', padding: '2px 8px', borderRadius: '4px' }}>
                v0.1.0-research
              </span>
            </div>
            <div className="brand-subtitle">
              Mechanistic T2D Glucose Regulation & Predictive Digital Twin Dashboard
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div className="system-status-pill">
            <div className={`status-dot ${isLoading ? 'loading' : ''}`} />
            <span>
              Engine: {health ? health.engine : 'Connecting...'}
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', color: '#64748b' }}>
            <Cpu size={14} />
            <span>LSODA Stiff Solver</span>
          </div>
        </div>
      </div>
    </header>
  );
};
