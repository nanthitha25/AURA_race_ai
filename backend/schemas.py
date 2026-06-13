from pydantic import BaseModel

class RaceSituation(BaseModel):
    driver: str
    opponent: str
    gap: float
    gap_closing_rate: float
    brake_variation: float
    throttle_variation: float
    speed_variation: float
    lap_time_loss: float
    driver_aggression: float
    driver_consistency: float
    tyre_advantage: bool
    drs: bool
    driver_advantage: bool

class LiveTelemetry(BaseModel):
    driver: str
    opponent: str
    speed: float
    throttle: float
    brake: float
    rpm: float
    gear: int
    drs: int
    gap: float
    tyre_age: int
    time: float
