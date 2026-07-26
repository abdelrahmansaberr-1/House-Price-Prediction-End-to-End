from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import json

app = FastAPI(title="House Price Prediction API", version="1.0")

model = joblib.load("house_price.pkl")

with open("locations.json", "r") as f:
    locations = json.load(f)

class HouseFeatures(BaseModel):
    carpet_area_sqft: float
    floor_num: float
    Bathroom: float
    Balcony: float
    location_grouped: str
    Furnishing: str
    Transaction: str
    Ownership: str
    facing: str

@app.get("/")
def read_root():
    return {"status": "API is up and running!", "model_loaded": True}

@app.post("/predict")
def predict_price(features: HouseFeatures):
    try:

        input_df = pd.DataFrame([features.dict()])
        
        pred_log = model.predict(input_df)
        
        pred_real = np.expm1(pred_log[0])
        
        return {
            "status": "success",
            "predicted_price_rupees": round(pred_real, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))