import React from 'react';

export default function AgentWarRoom({ data }) {
  if (!data || !data.agents) return <div className="mc-panel">Loading Agents...</div>;

  const agents = data.agents;

  return (
    <div className="mc-panel">
      <h2 className="panel-title">AI AGENT WAR ROOM</h2>
      <div className="agent-war-room">
        
        <div className="agent-card">
          <div className="agent-name">STRATEGY AGENT</div>
          <div className="agent-verdict" style={{ color: "var(--f1-yellow)" }}>
            {agents.strategy.action}
          </div>
          <div className="agent-conf">
            <span>Confidence</span>
            <span>{Number(agents.strategy.confidence).toFixed(1)}%</span>
          </div>
        </div>

        <div className="agent-card">
          <div className="agent-name">PSYCHOLOGY AGENT</div>
          <div className="agent-verdict" style={{ color: agents.psychology.status === "Vulnerable" ? "var(--f1-red)" : "var(--f1-green)" }}>
            {agents.psychology.status.toUpperCase()}
          </div>
          <div className="agent-conf">
            <span>Mistake Prob</span>
            <span>{Number(agents.psychology.confidence).toFixed(1)}%</span>
          </div>
        </div>

        <div className="agent-card">
          <div className="agent-name">OVERTAKE AGENT</div>
          <div className="agent-verdict">
            {agents.overtake.action}
          </div>
          <div className="agent-conf">
            <span>Success Prob</span>
            <span>{Number(agents.overtake.confidence).toFixed(1)}%</span>
          </div>
        </div>

        <div className="agent-card">
          <div className="agent-name">RISK AGENT</div>
          <div className="agent-verdict" style={{ color: agents.risk.status === "Approved" ? "var(--f1-green)" : "var(--f1-red)" }}>
            {agents.risk.status.toUpperCase()}
          </div>
          <div className="agent-conf">
            <span>Safety Margin</span>
            <span>{Number(agents.risk.confidence).toFixed(1)}%</span>
          </div>
        </div>

      </div>
    </div>
  );
}
