import React from "react";

function TelemetryCard({ data }) {
  return (
    <div className="panel telemetry-panel">
      <h2>TELEMETRY</h2>
      <div className="telemetry-grid">
        <div className="stat">
            <span className="label">Speed</span>
            <span className="value">{data.speed} km/h</span>
        </div>
        <div className="stat">
            <span className="label">Brake</span>
            <span className="value">{data.brake}%</span>
        </div>
        <div className="stat">
            <span className="label">Throttle</span>
            <span className="value">{data.throttle}%</span>
        </div>
      </div>
      
      <div className="analysis-section">
          <h2>AI ANALYSIS</h2>
          <div className="stat highlight">
              <span className="label">Pressure</span>
              <span className="value">{data.mistake_probability > 50 ? "HIGH" : "MEDIUM"}</span>
          </div>
          <div className="stat highlight">
              <span className="label">Mistake Probability</span>
              <span className="value">{data.mistake_probability}%</span>
          </div>
      </div>
    </div>
  );
}

export default TelemetryCard;
