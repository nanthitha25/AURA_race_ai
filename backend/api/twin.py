from fastapi import APIRouter
from models.digital_twin.digital_driver import DigitalDriver

router = APIRouter()

@router.post("/predict")
def predict_driver_behavior(data: dict):
    driver = data.get("driver", "NOR")
    situation = {
        "pressure": data.get("pressure", "HIGH"),
        "corner": data.get("corner", "T10")
    }
    
    twin = DigitalDriver(driver)
    prediction = twin.predict_reaction(situation)
    return prediction
