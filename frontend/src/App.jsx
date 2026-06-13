import { useEffect, useState } from "react";
import { connectAura } from "./websocket/auraSocket";
import Header from "./components/Header";
import TimingTower from "./components/TimingTower";
import SteeringWheel from "./components/SteeringWheel";
import AgentWarRoom from "./components/AgentWarRoom";
import RadioPanel from "./components/RadioPanel";
import StrategyPanel from "./components/StrategyPanel";
import "./styles/aura-f1.css";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const socket = connectAura((message) => {
      setData(message);
    });
    return () => socket.close();
  }, []);

  return (
    <div className="mc-container">
      <Header data={data} />
      
      {!data ? (
        <div style={{ textAlign: "center", marginTop: "50px", color: "var(--f1-red)" }}>
          <h2>INITIALIZING AURA RACE ENGINE...</h2>
          <p>Waiting for Telemetry Feed</p>
        </div>
      ) : (
        <div className="mc-grid">
          <TimingTower data={data} />
          <SteeringWheel data={data} />
          <AgentWarRoom data={data} />
          <StrategyPanel data={data} />
          <RadioPanel data={data} />
        </div>
      )}
    </div>
  );
}

export default App;
