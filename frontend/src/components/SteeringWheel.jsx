import React from 'react';

export default function SteeringWheel({ data }) {
  if (!data) return <div className="mc-panel steering-wheel">Loading Telemetry...</div>;

  const rpmPercent = Math.min(100, (data.rpm / 13000) * 100);

  return (
    <div className="mc-panel steering-wheel">
      <div className="wheel-display">
        
        <div className="rpm-bar">
          <div className="rpm-fill" style={{ width: `${rpmPercent}%` }}></div>
        </div>

        <div className="wheel-stat">
          <span className="wheel-val">{data.speed}</span>
          <span className="wheel-label">km/h</span>
        </div>

        <div className="wheel-stat">
          <span className="wheel-val">{data.gear}</span>
          <span className="wheel-label">GEAR</span>
        </div>

        <div className={`drs-indicator ${data.drs ? "active" : ""}`}>
          {data.drs ? "DRS ACTIVE" : "DRS OFF"}
        </div>
        
      </div>
      
      <div style={{ display: 'flex', justifyContent: 'space-around', marginTop: '15px' }}>
         <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--f1-text-dim)' }}>THROTTLE</div>
            <div style={{ fontWeight: 'bold', color: 'var(--f1-green)' }}>{data.throttle}%</div>
         </div>
         <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--f1-text-dim)' }}>BRAKE</div>
            <div style={{ fontWeight: 'bold', color: 'var(--f1-red)' }}>{data.brake}%</div>
         </div>
      </div>
    </div>
  );
}
