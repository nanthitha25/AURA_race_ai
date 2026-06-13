# 🏎️ AURA-Race AI: F1 Pit-Wall Engineering System

AURA-Race AI is an advanced, multi-agent Formula 1 race engineering and strategy simulator. It transitions traditional motorsport data analytics from static telemetry dashboards into an active, predictive **Mission Control AI**. 

By leveraging the `FastF1` library to ingest real-world Formula 1 telemetry, AURA acts as an autonomous Race Engineer—predicting opponent mistakes under pressure, analyzing real-time overtake opportunities, and projecting multi-stint pit strategies.

---

## 🌟 Key Capabilities
1. **Psychological Memory Engine**: Predicts the exact probability of an opponent making a mistake (e.g. late braking) based on dynamic pressure from the trailing car.
2. **Adaptive Overtake Forecasting**: Doesn't just calculate *if* an overtake is possible, but predicts *when* (e.g., "Attack T10 on Lap 46").
3. **Multi-Stint Race Optimizer**: Evaluates thousands of race paths (Undercuts, Overcuts, Push Stints) factoring in Tyre Degradation and Pit Lane traffic risk.
4. **Mission Control Dashboard**: A highly authentic, dark-mode React interface streaming WebSocket telemetry at 10Hz, rendering F1 digital steering wheels, timing towers, and live Multi-Agent decision confidences.

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[FastF1 API] -->|Real Race Telemetry| B(Backend Collector)
    B --> C(Feature Extraction)
    
    subgraph AURA Multi-Agent Brain
        C --> D[Strategy Agent]
        C --> E[Psychology Agent]
        C --> F[Overtake Agent]
        C --> G[Risk Agent]
        
        D & E & F & G --> H{Aura Decision Engine}
    end
    
    H -->|Multi-Stint & Action Predictions| I(WebSocket Server)
    I -->|JSON Data Stream| J[React V2 Mission Control Cockpit]
```

---

## 👤 Use Case Diagram

```mermaid
graph TD
    RE([Race Engineer])
    DR([Driver])

    subgraph AURA System
        UC1(Monitor Live Telemetry)
        UC2(Predict Opponent Mistake)
        UC3(Forecast Best Attack Window)
        UC4(Optimize Pit Strategy)
    end

    RE --> UC1
    RE --> UC2
    RE --> UC3
    RE --> UC4
    UC3 -.->|Relay Radio Commands| DR
    UC4 -.->|Call to Box| DR
```

---

## 🔄 Sequence Diagram: Live Telemetry Flow

```mermaid
sequenceDiagram
    participant F1 as FastF1 API
    participant BE as FastAPI Backend
    participant AE as AURA Decision Engine
    participant WS as WebSocket Broadcaster
    participant UI as React Mission Control

    UI->>WS: Connect to ws://localhost:8000/live
    WS-->>UI: Connection Accepted

    loop Every 100ms (10Hz)
        F1->>BE: Fetch Lap Telemetry Row
        BE->>AE: Pass Speed, Brake, Gap, RPM
        AE->>AE: Run Psychological Memory
        AE->>AE: Simulate Multi-Stint Optimization
        AE-->>BE: Return JSON payload (Strategy, Risk, Action)
        BE->>WS: Broadcast Data
        WS->>UI: Render Steering Wheel & Agents
    end
```

---

## 📦 Class Diagram: Multi-Agent Core

```mermaid
classDiagram
    class MasterRaceAgent {
        +decision_engine
        +process(telemetry, features)
    }

    class AuraDecisionEngine {
        +memory: PsychologicalMemory
        +knowledge: OpponentKnowledgeGraph
        +overtake_ai: OvertakePredictor
        +decide(driver, opponent, gap)
    }

    class MultiStintSimulator {
        +tyre_model: TyreDegradationModel
        +pit_model: PitStrategyOptimizer
        +simulate(current_lap, total_laps)
    }

    class OpportunityEngine {
        +scorer: OvertakeOpportunityScore
        +evaluate(current_state, weakness)
    }

    MasterRaceAgent --> AuraDecisionEngine
    AuraDecisionEngine --> MultiStintSimulator
    AuraDecisionEngine --> OpportunityEngine
```

---

## ⚡ Activity Diagram: Multi-Stint Strategy Evaluation

```mermaid
stateDiagram-v2
    [*] --> GenerateStintPermutations
    GenerateStintPermutations --> EvaluateStint
    
    state EvaluateStint {
        [*] --> ComputeBaseLapTime
        ComputeBaseLapTime --> ApplyTyreDegradation
        ApplyTyreDegradation --> ApplyPitLossPenalty
        ApplyPitLossPenalty --> ApplyTrafficRiskPenalty
        ApplyTrafficRiskPenalty --> [*]
    }
    
    EvaluateStint --> ScoreTotalRaceTime
    ScoreTotalRaceTime --> RankStrategies
    RankStrategies --> [*]
```

---

## 🚀 Running the Project

### 1. Start the Backend (Uvicorn / FastAPI)
The core engine runs on a FastAPI WebSocket server.
```bash
# Navigate to project root
source .venv/bin/activate
uvicorn backend.main:app --reload --port 8000
```

### 2. Start the Frontend (React / Vite)
The UI simulates a trackside engineering pit-wall.
```bash
cd frontend
npm run dev
```

Visit `http://localhost:5173` to view the Live Telemetry Dashboard.
