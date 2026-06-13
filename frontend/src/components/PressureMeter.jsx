import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

function PressureMeter({ history }) {
  return (
    <div className="panel chart-panel">
      <h2>PRESSURE HISTORY</h2>
      <div style={{ width: '100%', height: '200px' }}>
        <ResponsiveContainer>
          <LineChart data={history}>
            <XAxis dataKey="time" hide />
            <YAxis domain={[0, 100]} stroke="#666" />
            <Tooltip contentStyle={{ backgroundColor: '#111', border: '1px solid #333' }} />
            <Line 
                type="monotone" 
                dataKey="pressure" 
                stroke="#ff4444" 
                strokeWidth={3}
                dot={false}
                isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default PressureMeter;
