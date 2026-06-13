import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from backend.schemas import RaceSituation
from backend.ai_service import aura_ai
from backend.websocket_server import telemetry_stream
from backend.api import twin
from agents.master_agent import MasterRaceAgent

app = FastAPI(title="AURA Race AI API")

# Add CORS for React Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Twin API
app.include_router(twin.router, prefix="/twin")

# Instantiate the Monolithic Master Agent
master_agent = MasterRaceAgent(aura_ai)

@app.get("/")
def home():
    return {"system": "AURA Race AI Online", "status": "Running"}

@app.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    await telemetry_stream(websocket, master_agent)
