import React, { useEffect, useState, useCallback, useRef } from 'react';
import {
  SyntheticPatientSummary,
  SyntheticPatientDetail,
  ForecastResponse,
  EvaluationResponse,
  AdverseRiskResponse,
  HealthResponse,
} from './types';
import {
  fetchHealth,
  fetchPatients,
  fetchPatientDetail,
  fetchForecast,
  fetchEvaluation,
  fetchAdverseRisk,
} from './services/api';
import { Header } from './components/Header';
import { PatientSelector } from './components/PatientSelector';
import { PatientSummaryCard } from './components/PatientSummaryCard';
import { StreamControls } from './components/StreamControls';
import { GlucoseChart } from './components/GlucoseChart';
import { AdverseRiskPanel } from './components/AdverseRiskPanel';
import { BaselineComparisonPanel } from './components/BaselineComparisonPanel';
import { ModelStatusPanel } from './components/ModelStatusPanel';

export const App: React.FC = () => {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [patients, setPatients] = useState<SyntheticPatientSummary[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string>('SYN-001');
  const [patientDetail, setPatientDetail] = useState<SyntheticPatientDetail | null>(null);

  // Time & Simulation controls
  const [observedTime, setObservedTime] = useState<number>(120);
  const [forecastHorizon, setForecastHorizon] = useState<number>(180);
  const [mealAmount, setMealAmount] = useState<number>(70);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);

  // Data payloads
  const [forecastData, setForecastData] = useState<ForecastResponse | null>(null);
  const [evaluationData, setEvaluationData] = useState<EvaluationResponse | null>(null);
  const [riskData, setRiskData] = useState<AdverseRiskResponse | null>(null);

  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // 1. Initial Load: Health & Cohort List
  useEffect(() => {
    async function init() {
      try {
        const [h, p] = await Promise.all([fetchHealth(), fetchPatients()]);
        setHealth(h);
        setPatients(p);
      } catch (err: any) {
        console.error('Initialization error:', err);
        setError(err.message || 'Failed to connect to PhysioTwin backend API.');
      }
    }
    init();
  }, []);

  // 2. Fetch Patient Detail on selection
  useEffect(() => {
    async function loadPatient() {
      if (!selectedPatientId) return;
      try {
        const detail = await fetchPatientDetail(selectedPatientId);
        setPatientDetail(detail);
      } catch (err: any) {
        console.error('Failed to load patient detail:', err);
      }
    }
    loadPatient();
  }, [selectedPatientId]);

  // 3. Fetch Forecast, Evaluation, and Risk data
  const refreshAnalytics = useCallback(async () => {
    if (!selectedPatientId) return;
    setIsLoading(true);
    setError(null);

    try {
      const [fc, ev, rk] = await Promise.all([
        fetchForecast({
          patientId: selectedPatientId,
          observedUpToMin: observedTime,
          forecastHorizonMin: forecastHorizon,
          mealAmountMmol: mealAmount,
        }),
        fetchEvaluation(selectedPatientId, observedTime, forecastHorizon),
        fetchAdverseRisk(selectedPatientId, observedTime, forecastHorizon),
      ]);

      setForecastData(fc);
      setEvaluationData(ev);
      setRiskData(rk);
    } catch (err: any) {
      console.error('Data refresh error:', err);
      setError(err.message || 'Failed to update simulation forecast.');
    } finally {
      setIsLoading(false);
    }
  }, [selectedPatientId, observedTime, forecastHorizon, mealAmount]);

  useEffect(() => {
    refreshAnalytics();
  }, [refreshAnalytics]);

  // 4. Stream Playback Loop
  useEffect(() => {
    if (isPlaying) {
      timerRef.current = setInterval(() => {
        setObservedTime((prev) => {
          if (prev >= 330) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 5;
        });
      }, 1500);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying]);

  return (
    <div className="app-container">
      <Header health={health} isLoading={isLoading} />

      {error && (
        <div style={{ background: '#fee2e2', borderBottom: '1px solid #ef4444', color: '#991b1b', padding: '10px 24px', fontSize: '0.85rem' }}>
          <strong>API Communication Error:</strong> {error}
        </div>
      )}

      <main className="dashboard-grid">
        {/* Left Sidebar */}
        <aside className="sidebar">
          <PatientSelector
            patients={patients}
            selectedPatientId={selectedPatientId}
            onSelectPatient={(id) => {
              setSelectedPatientId(id);
              setIsPlaying(false);
            }}
            isLoading={isLoading}
          />

          <PatientSummaryCard patient={patientDetail} />
        </aside>

        {/* Right Main Content */}
        <section>
          {/* Controls Bar */}
          <StreamControls
            isPlaying={isPlaying}
            onTogglePlay={() => setIsPlaying(!isPlaying)}
            onReset={() => {
              setIsPlaying(false);
              setObservedTime(30);
            }}
            onStepForward={() => {
              setIsPlaying(false);
              setObservedTime((prev) => Math.min(prev + 15, 330));
            }}
            observedTime={observedTime}
            maxTime={330}
            forecastHorizon={forecastHorizon}
            onSelectHorizon={(h) => setForecastHorizon(h)}
            mealAmount={mealAmount}
            onSelectMealAmount={(amt) => setMealAmount(amt)}
            isLoading={isLoading}
          />

          {/* Time Series Dual-Line Chart */}
          <GlucoseChart
            observedData={forecastData?.observed_segment || []}
            forecastData={forecastData?.forecast_segment || []}
            splitPointMin={observedTime}
            isLoading={isLoading}
          />

          {/* Analytics Panels */}
          <div className="analytics-grid">
            <AdverseRiskPanel riskData={riskData} isLoading={isLoading} />
            <BaselineComparisonPanel evaluation={evaluationData} isLoading={isLoading} />
            <ModelStatusPanel />
          </div>
        </section>
      </main>
    </div>
  );
};
