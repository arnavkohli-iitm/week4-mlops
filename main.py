# File: main.py
import os
import uvicorn
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow

from predict import load_model, format_features, make_prediction

# MLflow Server Configuration
MLFLOW_TRACKING_URI = "http://34.67.236.227:8081"

os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI) # Also set it for the predict.py import

app = FastAPI(title="Iris ML API", description="API for Iris species prediction")

# Load the model once at startup
try:
    print(f"Loading model from MLflow at {MLFLOW_TRACKING_URI}...")
    model = load_model() # This function is from predict.py
    if model:
        print("Model loaded successfully.")
    else:
        print("Model loading returned None. Check MLflow server.")
except Exception as e:
    print(f"FATAL: Could not load model at startup. {e}")
    print("Is the MLflow server running at the correct IP?")
    model = None


# Define the input data model using Pydantic
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    class Config:
        # This allows using example values in the FastAPI docs
        schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }

# Define the output data model
class Prediction(BaseModel):
    prediction: str


@app.get("/", summary="Health check endpoint")
def read_root():
    """Health check: Returns status and model load status."""
    model_status = "loaded" if model is not None else "load_failed"
    return {"status": "ok", "model_status": model_status}


@app.post("/predict", summary="Make a single prediction", response_model=Prediction)
def get_prediction(features: IrisFeatures):
    """
    Make a prediction on a single set of Iris features.
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not available. Check server logs."
        )
    
    # Convert Pydantic model to list of strings, just like your CLI app
    feature_list = [
        str(features.sepal_length),
        str(features.sepal_width),
        str(features.petal_length),
        str(features.petal_width)
    ]
    
    try:
        # Use your existing functions from predict.py
        data_df = format_features(feature_list)
        if data_df is None:
            raise ValueError("Feature formatting failed.")
            
        prediction_value = make_prediction(model, data_df)
        
        if prediction_value is None:
             raise ValueError("Model prediction failed.")
        
        return {"prediction": prediction_value}
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Prediction error: {e}"
        )

if __name__ == "__main__":
    print("--- Starting Uvicorn server for local testing ---")
    print(f"Connect to MLflow at: {MLFLOW_TRACKING_URI}")
    uvicorn.run(app, host="0.0.0.0", port=8000)