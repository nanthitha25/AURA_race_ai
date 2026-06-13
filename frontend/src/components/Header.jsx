import React from 'react';

export default function Header({ data }) {
  return (
    <header className="mc-header">
      <h1>AURA RACE AI</h1>
      <div className="mc-header-stats">
        <span>LAP 52/78</span>
        <span>RACE: MONACO GP</span>
        {data && (
          <span style={{ color: "var(--f1-red)", fontWeight: "bold" }}>
            {data.driver} → {data.decision?.action || "STANDBY"}
          </span>
        )}
      </div>
    </header>
  );
}
