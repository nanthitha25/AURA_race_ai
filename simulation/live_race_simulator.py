import websocket
import json
import time
import random

def simulate():
    try:
        ws = websocket.create_connection("ws://localhost:8000/live")
        print("Connected to AURA Real-Time Simulator.")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    while True:
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
            "tyre_age": 15
        }

        try:
            ws.send(json.dumps(telemetry))
            response = ws.recv()
            data = json.loads(response)
            
            print("\nAURA ANALYSIS:")
            print(f"Gap: {telemetry['gap']}s | Speed: {telemetry['speed']} km/h")
            print(f"Mistake Probability: {data['mistake_probability']}%")
            print(f"Decision: {data['decision']['action']} (Confidence: {data['decision']['confidence']}%)")
            print(f"Radio: {data['radio']}")
            
            time.sleep(0.5)
        except Exception as e:
            print(f"Connection lost: {e}")
            break

if __name__ == "__main__":
    simulate()
