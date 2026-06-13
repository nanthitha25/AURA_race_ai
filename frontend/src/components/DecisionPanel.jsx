import React from "react";

function DecisionPanel({ data }) {
  const isAttack = data.decision.action === "ATTACK";
  
  return (
    <div className={`panel decision-panel ${isAttack ? 'attack-mode' : ''}`}>
      <h2>RECOMMENDATION</h2>
      <h1 className="action-text">
          {isAttack ? "🔥 ATTACK" : data.decision.action}
      </h1>
      <div className="decision-details">
          <div className="stat">
              <span className="label">Confidence</span>
              <span className="value">{data.decision.confidence}%</span>
          </div>
      </div>
    </div>
  );
}

export default DecisionPanel;
