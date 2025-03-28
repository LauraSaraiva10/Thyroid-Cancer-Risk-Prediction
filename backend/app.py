from fastapi import FastAPI
from routers.prediction import router as prediction_router

app = FastAPI(title="Thyroid Cancer Risk Predictor")

app.include_router(prediction_router, prefix="/predict", tags=["Prediction"])

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}