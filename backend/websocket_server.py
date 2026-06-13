import asyncio
import time
import random
from fastapi import WebSocket
from backend.telemetry_processor import process_telemetry

async def telemetry_stream(websocket: WebSocket, master_agent):
    await websocket.accept()
    
    while True:
        try:
            # Simulate Live Telemetry Stream instead of waiting for a client to send it
            telemetry = {
                "time": time.time(),
                "driver": "VER",
                "opponent": "NOR",
                "speed": random.randint(250, 330),
                "throttle": random.randint(70, 100),
                "brake": random.randint(0, 80),
                "rpm": random.randint(9000, 12000),
                "gear": random.randint(5, 8),
                "drs": random.randint(0, 1),
                "gap": round(random.uniform(0.1, 1.5), 2),
                "tyre_age": 15,
                "weather": "dry"
            }
            
            features = process_telemetry(telemetry)
            response = master_agent.process(telemetry, features)
            
            await websocket.send_json(response)
            await asyncio.sleep(1)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"WebSocket Error: {e}")
            break
