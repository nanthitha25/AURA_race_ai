import React from "react";

function RadioMessage({ data }) {
  return (
    <div className="panel radio-panel">
      <h2>AURA RADIO</h2>
      <div className="radio-text">
        "{data.radio}"
      </div>
    </div>
  );
}

export default RadioMessage;
