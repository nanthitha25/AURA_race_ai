import React from 'react';

export default function StrategyPanel({ data }) {
  if (!data || !data.decision || !data.decision.multi_stint_plans) {
    return <div className="mc-panel">Calculating Multi-Stint Options...</div>;
  }

  const plans = data.decision.multi_stint_plans;
  const bestPlan = plans[0];

  return (
    <div className="mc-panel strategy-panel">
      <h2 className="panel-title">AURA MULTI-STINT OPTIMIZER</h2>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        
        {/* Top 3 Strategic Options */}
        <div style={{ display: 'flex', gap: '10px', overflowX: 'auto', paddingBottom: '10px' }}>
          {plans.slice(0, 3).map((plan, i) => (
            <div key={i} style={{
              flex: 1, 
              border: `1px solid ${i === 0 ? 'var(--f1-green)' : '#333'}`,
              backgroundColor: '#1a1a1a',
              padding: '10px',
              minWidth: '140px'
            }}>
              <div style={{ fontSize: '0.8rem', color: i === 0 ? 'var(--f1-green)' : 'var(--f1-text-dim)', fontWeight: 'bold' }}>
                {plan.name.replace(/_/g, ' ')}
              </div>
              <div style={{ fontSize: '1.2rem', margin: '5px 0' }}>P{plan.expected_finish}</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--f1-yellow)' }}>{plan.confidence}% Conf</div>
            </div>
          ))}
        </div>

        {/* Detailed Stint Breakdown for Best Plan */}
        <div style={{ borderLeft: '3px solid var(--f1-red)', paddingLeft: '10px' }}>
          <div style={{ fontWeight: 'bold', marginBottom: '10px', color: 'var(--f1-text-dim)' }}>RECOMMENDED STINT PATH:</div>
          {bestPlan.stints.map((stint, idx) => (
            <div key={idx} style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              marginBottom: '5px',
              fontFamily: 'monospace'
            }}>
              <span style={{ 
                color: stint.compound === 'SOFT' ? '#ff3333' : 
                       stint.compound === 'MEDIUM' ? 'var(--f1-yellow)' : 
                       'white' 
              }}>
                {stint.compound}
              </span>
              <span>Laps: {stint.laps}</span>
              <span style={{ color: 'var(--f1-text-dim)' }}>Push: {stint.push_level * 100}%</span>
            </div>
          ))}
        </div>

        {/* Risks */}
        <div style={{ marginTop: 'auto', paddingTop: '10px', borderTop: '1px solid #333', display: 'flex', justifyContent: 'space-between' }}>
           <span style={{ color: 'var(--f1-text-dim)', fontSize: '0.9rem' }}>Traffic Risk Penalty:</span>
           <span style={{ color: bestPlan.traffic_risk > 0.4 ? 'var(--f1-red)' : 'var(--f1-green)' }}>
             {(bestPlan.traffic_risk * 100).toFixed(0)}%
           </span>
        </div>

      </div>
    </div>
  );
}
