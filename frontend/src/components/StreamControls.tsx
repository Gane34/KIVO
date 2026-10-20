import React from 'react';
import { Play, Pause, RotateCcw, FastForward, Clock, Utensils } from 'lucide-react';

interface StreamControlsProps {
  isPlaying: boolean;
  onTogglePlay: () => void;
  onReset: () => void;
  onStepForward: () => void;
  observedTime: number;
  maxTime: number;
  forecastHorizon: number;
  onSelectHorizon: (h: number) => void;
  mealAmount: number;
  onSelectMealAmount: (amt: number) => void;
  isLoading: boolean;
}

export const StreamControls: React.FC<StreamControlsProps> = ({
  isPlaying,
  onTogglePlay,
  onReset,
  onStepForward,
  observedTime,
  maxTime,
  forecastHorizon,
  onSelectHorizon,
  mealAmount,
  onSelectMealAmount,
  isLoading,
}) => {
  return (
    <div className="controls-container">
      {/* Stream Playback Controls */}
      <div className="control-group">
        <span className="control-label">Wearable CGM Stream:</span>
        <button
          className={`btn ${isPlaying ? 'btn-primary' : ''}`}
          onClick={onTogglePlay}
          disabled={isLoading || observedTime >= maxTime}
          title={isPlaying ? 'Pause streaming' : 'Replay simulated continuous CGM stream'}
        >
          {isPlaying ? <Pause size={14} /> : <Play size={14} />}
          <span>{isPlaying ? 'Streaming...' : 'Replay Stream'}</span>
        </button>

        <button
          className="btn"
          onClick={onStepForward}
          disabled={isLoading || isPlaying || observedTime >= maxTime}
          title="Advance observation stream by 15 minutes"
        >
          <FastForward size={14} />
          <span>+15m Step</span>
        </button>

        <button
          className="btn"
          onClick={onReset}
          disabled={isLoading}
          title="Reset stream to t=30 min"
        >
          <RotateCcw size={14} />
          <span>Reset</span>
        </button>

        <div style={{ marginLeft: '8px', fontSize: '0.8rem', fontWeight: 600, color: '#0f172a' }}>
          t<sub>now</sub>: <span className="code-pill">{observedTime.toFixed(0)} min</span>
        </div>
      </div>

      <div style={{ width: '1px', height: '24px', background: '#e2e8f0', margin: '0 8px' }} />

      {/* Forecast Horizon Selector */}
      <div className="control-group">
        <span className="control-label">
          <Clock size={14} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'middle' }} />
          Forecast Horizon:
        </span>
        <div className="btn-group">
          {[30, 60, 120, 180].map((h) => (
            <button
              key={h}
              className={`btn ${forecastHorizon === h ? 'active' : ''}`}
              onClick={() => onSelectHorizon(h)}
              disabled={isLoading}
            >
              {h}m
            </button>
          ))}
        </div>
      </div>

      <div style={{ width: '1px', height: '24px', background: '#e2e8f0', margin: '0 8px' }} />

      {/* Meal Challenge Selector */}
      <div className="control-group">
        <span className="control-label">
          <Utensils size={14} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'middle' }} />
          Meal Challenge:
        </span>
        <div className="btn-group">
          {[
            { label: 'Snack (35 mmol)', val: 35 },
            { label: 'Standard (70 mmol)', val: 70 },
            { label: 'High Carb (100 mmol)', val: 100 },
          ].map((m) => (
            <button
              key={m.val}
              className={`btn ${mealAmount === m.val ? 'active' : ''}`}
              onClick={() => onSelectMealAmount(m.val)}
              disabled={isLoading}
            >
              {m.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
