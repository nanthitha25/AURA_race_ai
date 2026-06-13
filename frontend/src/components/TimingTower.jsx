import React from 'react';

export default function TimingTower({ data }) {
  // Mock leaderboard showing the target opponent and the AURA driver
  const gap = data ? data.gap : "--";
  const driver = data ? data.driver : "VER";
  const opponent = data ? data.opponent : "NOR";
  const position = data ? data.race_forecast?.predicted_position?.replace("P", "") || "3" : "3";
  const oppPos = parseInt(position) - 1;

  return (
    <div className="mc-panel timing-tower">
      <h2 className="panel-title">LIVE POSITIONS</h2>
      
      <div className="tower-row">
        <span>P1 LEC</span>
        <span>-</span>
      </div>
      <div className="tower-row">
        <span>P2 SAI</span>
        <span>+2.4</span>
      </div>
      
      <div className="tower-row">
        <span>P{oppPos} {opponent}</span>
        <span>+6.1</span>
      </div>
      <div className="tower-row active">
        <span>P{position} {driver}</span>
        <span>+{gap}</span>
      </div>

      <div className="tower-row">
        <span>P{parseInt(position)+1} HAM</span>
        <span>+3.2</span>
      </div>
      
      <div style={{ marginTop: "auto", fontSize: "0.8rem", color: "var(--f1-text-dim)" }}>
        Predicted Finish: {data?.race_forecast?.predicted_position || "P2"} ({data?.race_forecast?.probability || 0}%)
      </div>
    </div>
  );
}
