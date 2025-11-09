import mlflow
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# CONNECT MLflow
mlflow.set_tracking_uri("http://172.17.0.1:5000")

# LOAD MODEL FROM REGISTRY (STAGING)
MODEL_NAME = "bengaluru_house_price_model"
model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/Staging")


@app.get("/")
def root():
    return {"status": "model API is running"}


@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    pred = model.predict(df)[0]
    return {"prediction": float(pred)}
