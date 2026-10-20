import React from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ReferenceArea,
} from 'recharts';
import { ObservationPoint, ForecastPoint } from '../types';

interface GlucoseChartProps {
  observedData: ObservationPoint[];
  forecastData: ForecastPoint[];
  splitPointMin: number;
  isLoading: boolean;
}

interface CombinedChartPoint {
  time_min: number;
  observed_cgm?: number;
  true_latent_g?: number;
  forecast_g?: number;
  forecast_lower?: number;
  forecast_upper?: number;
  forecast_ci_span?: number; // forecast_upper - forecast_lower
  insulin_predicted?: number;
  action_predicted?: number;
}

export const GlucoseChart: React.FC<GlucoseChartProps> = ({
  observedData,
  forecastData,
  splitPointMin,
  isLoading,
}) => {
  // Merge observed and forecast points into a single aligned time grid
  const pointMap = new Map<number, CombinedChartPoint>();

  observedData.forEach((obs) => {
    pointMap.set(obs.timestamp_min, {
      time_min: obs.timestamp_min,
      observed_cgm: obs.cgm_glucose_mmol_L,
      true_latent_g: obs.true_glucose_mmol_L,
    });
  });

  forecastData.forEach((fc) => {
    const existing = pointMap.get(fc.time_min) || { time_min: fc.time_min };
    existing.forecast_g = fc.glucose_predicted;
    existing.forecast_lower = fc.glucose_lower_bound;
    existing.forecast_upper = fc.glucose_upper_bound;
    existing.forecast_ci_span = Math.max(0, fc.glucose_upper_bound - fc.glucose_lower_bound);
    existing.insulin_predicted = fc.insulin_predicted;
    existing.action_predicted = fc.action_predicted;
    pointMap.set(fc.time_min, existing);
  });

  const chartData = Array.from(pointMap.values()).sort((a, b) => a.time_min - b.time_min);

  // Custom rich tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const dataPoint = payload[0].payload as CombinedChartPoint;
      const isPast = dataPoint.time_min <= splitPointMin;

      return (
        <div className="custom-tooltip">
          <div className="tooltip-title">Time: t = {dataPoint.time_min} min</div>

          {dataPoint.observed_cgm !== undefined && (
            <div style={{ color: '#38bdf8', marginBottom: '3px' }}>
              CGM Reading: <strong className="tooltip-val">{dataPoint.observed_cgm.toFixed(2)}</strong> mmol/L
            </div>
          )}

          {dataPoint.true_latent_g !== undefined && isPast && (
            <div style={{ color: '#94a3b8', fontSize: '0.72rem', marginBottom: '3px' }}>
              Latent True Glucose: {dataPoint.true_latent_g.toFixed(2)} mmol/L
            </div>
          )}

          {dataPoint.forecast_g !== undefined && !isPast && (
            <>
              <div style={{ color: '#c084fc', marginBottom: '3px' }}>
                Illustrative ODE continuation: <strong className="tooltip-val">{dataPoint.forecast_g.toFixed(2)}</strong> mmol/L
              </div>
              {dataPoint.forecast_lower !== undefined && dataPoint.forecast_upper !== undefined && (
                <div style={{ color: '#a855f7', fontSize: '0.72rem', marginBottom: '3px' }}>
                  Uncalibrated parameter-sensitivity envelope: [{dataPoint.forecast_lower.toFixed(2)} – {dataPoint.forecast_upper.toFixed(2)}]
                </div>
              )}
              {dataPoint.action_predicted !== undefined && (
                <div style={{ color: '#cbd5e1', fontSize: '0.72rem' }}>
                  Model Action X: {dataPoint.action_predicted.toFixed(2)} | Insulin: {dataPoint.insulin_predicted?.toFixed(1)} pmol/L
                </div>
              )}
            </>
          )}

          <div style={{ marginTop: '4px', fontSize: '0.68rem', color: '#94a3b8', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '3px' }}>
            {isPast ? '● Synthetic historical observation' : '◆ Same-generator ODE continuation'}
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="chart-card">
      <div className="chart-header">
        <div>
          <h2 style={{ fontSize: '1.05rem', fontWeight: 600, color: '#0f172a' }}>
            Synthetic Glucose Trajectory: ODE Continuation
          </h2>
          <p style={{ fontSize: '0.78rem', color: '#64748b' }}>
            Shaded envelope is an uncalibrated parameter-sensitivity display, not a predictive confidence interval. The ODE continuation uses the synthetic generator state, not CGM state estimation.
          </p>
        </div>

        <div className="legend-custom">
          <div className="legend-item">
            <span className="legend-dot" style={{ backgroundColor: '#0284c7' }} />
            <span>Synthetic CGM-like observations</span>
          </div>
          <div className="legend-item">
            <span className="legend-dot" style={{ backgroundColor: '#7c3aed' }} />
            <span>Same-generator ODE continuation (mean)</span>
          </div>
          <div className="legend-item">
            <span className="legend-dot" style={{ backgroundColor: '#c4b5fd' }} />
            <span>Uncalibrated sensitivity envelope</span>
          </div>
          <div className="legend-item">
            <span className="legend-dot" style={{ backgroundColor: '#10b981' }} />
            <span>Illustrative reference interval (3.9 – 10.0 mmol/L)</span>
          </div>
        </div>
      </div>

      <div className="chart-container-inner">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 20, right: 30, left: 10, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />

            {/* Target Glycemic Range 3.9 - 10.0 mmol/L */}
            <ReferenceArea y1={3.9} y2={10.0} fill="#10b981" fillOpacity={0.06} />

            {/* Clinical Alert Reference Lines */}
            <ReferenceLine
              y={3.9}
              stroke="#ef4444"
              strokeDasharray="4 4"
              strokeWidth={1.5}
              label={{ value: 'Reference line (3.9 mmol/L)', position: 'insideBottomLeft', fill: '#ef4444', fontSize: 11 }}
            />
            <ReferenceLine
              y={10.0}
              stroke="#f59e0b"
              strokeDasharray="4 4"
              strokeWidth={1.5}
              label={{ value: 'Reference line (10.0 mmol/L)', position: 'insideTopLeft', fill: '#d97706', fontSize: 11 }}
            />

            {/* Split Point: Current Time Line */}
            <ReferenceLine
              x={splitPointMin}
              stroke="#0f172a"
              strokeWidth={2}
              label={{ value: `t_now = ${splitPointMin} min`, position: 'top', fill: '#0f172a', fontWeight: 'bold', fontSize: 11 }}
            />

            {/* Meal Event Pin */}
            <ReferenceLine
              x={0}
              stroke="#0284c7"
              strokeDasharray="2 2"
              label={{ value: 'Meal Ingestion (t=0)', position: 'insideTopLeft', fill: '#0284c7', fontSize: 11 }}
            />

            <XAxis
              dataKey="time_min"
              type="number"
              domain={[0, 'dataMax']}
              stroke="#94a3b8"
              fontSize={12}
              tickFormatter={(t) => `${t}m`}
              label={{ value: 'Elapsed Simulation Time (minutes)', position: 'bottom', offset: 0, fill: '#64748b', fontSize: 12 }}
            />

            <YAxis
              domain={[0, 16]}
              stroke="#94a3b8"
              fontSize={12}
              label={{ value: 'Glucose Concentration (mmol/L)', angle: -90, position: 'insideLeft', offset: 0, fill: '#64748b', fontSize: 12 }}
            />

            <Tooltip content={<CustomTooltip />} />

            {/* Shaded Forecast Uncertainty Band */}
            <Area
              type="monotone"
              dataKey="forecast_upper"
              stroke="none"
              fill="#c4b5fd"
              fillOpacity={0.25}
              isAnimationActive={false}
            />

            {/* Historical CGM Readings: Solid line with dots */}
            <Line
              type="monotone"
              dataKey="observed_cgm"
              stroke="#0284c7"
              strokeWidth={2.5}
              dot={{ r: 3, fill: '#0284c7', strokeWidth: 1, stroke: '#ffffff' }}
              activeDot={{ r: 5 }}
              isAnimationActive={false}
              connectNulls={false}
            />

            {/* Mechanistic Twin Forecast: Dashed purple line */}
            <Line
              type="monotone"
              dataKey="forecast_g"
              stroke="#7c3aed"
              strokeWidth={2.5}
              strokeDasharray="6 4"
              dot={false}
              activeDot={{ r: 5, fill: '#7c3aed' }}
              isAnimationActive={false}
              connectNulls={false}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
