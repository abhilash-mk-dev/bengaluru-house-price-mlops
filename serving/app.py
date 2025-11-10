# import mlflow
# from fastapi import FastAPI
# import pandas as pd

# app = FastAPI()

# # MLflow tracking to ngrok server
# mlflow.set_tracking_uri("https://enhancive-arrangeable-alvin.ngrok-free.dev")

# # always load staging model
# MODEL_NAME = "bengaluru_house_price_model"
# model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/Staging")

# # MODEL_PATH = "./model_artifact"
# # model = mlflow.pyfunc.load_model(MODEL_PATH)

# @app.get("/")
# def root():
#     return {"status": "model API is running"}

# @app.post("/predict")
# def predict(data: dict):
#     df = pd.DataFrame([data])
#     pred = model.predict(df)[0]
#     return {"prediction": float(pred)}

import mlflow
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# PUBLIC NGROK MLflow tracking URI
MLFLOW_NGROK = "https://enhancive-arrangeable-alvin.ngrok-free.dev"
mlflow.set_tracking_uri(MLFLOW_NGROK)

# LOAD MODEL FROM REGISTRY (Staging stage)
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


