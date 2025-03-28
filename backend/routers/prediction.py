import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.prediction import PredictionRequest
from database.database import get_db
from models.thyroid_cancer_data import ThyroidCancerTypePrediction
from services.prediction_service import make_prediction

router = APIRouter()

@router.post("")
def predict_thyroid_cancer_type(data: PredictionRequest, db: Session = Depends(get_db)):
    try:
        input_data = np.array([[
            data.age, data.gender, data.family_history, data.radiation_exposure,
            data.iodine_deficiency, data.smoking, data.obesity, data.diabetes,
            data.tsh_level, data.t3_level, data.t4_level, data.nodule_size, data.thyroid_cancer_risk
        ]])

        input_data = pd.DataFrame(input_data, columns=[
            "Age", "Gender", "Family_History", "Radiation_Exposure",
            "Iodine_Deficiency", "Smoking", "Obesity", "Diabetes",
            "TSH_Level", "T3_Level", "T4_Level", "Nodule_Size", "Thyroid_Cancer_Risk"
        ])

        input_data["Age"] = pd.to_numeric(input_data["Age"], errors="coerce")
        input_data["TSH_Level"] = pd.to_numeric(input_data["TSH_Level"], errors="coerce")
        input_data["T3_Level"] = pd.to_numeric(input_data["T3_Level"], errors="coerce")
        input_data["T4_Level"] = pd.to_numeric(input_data["T4_Level"], errors="coerce")
        input_data["Nodule_Size"] = pd.to_numeric(input_data["Nodule_Size"], errors="coerce")

        prediction = make_prediction(input_data)

        prediction_label = "Malignant" if prediction == 1 else "Benign"

        db_record = ThyroidCancerTypePrediction(
            age=data.age,
            gender=data.gender,
            family_history=data.family_history,
            radiation_exposure=data.radiation_exposure,
            iodine_deficiency=data.iodine_deficiency,
            smoking=data.smoking,
            obesity=data.obesity,
            diabetes=data.diabetes,
            tsh_level=data.tsh_level,
            t3_level=data.t3_level,
            t4_level=data.t4_level,
            nodule_size=data.nodule_size,
            thyroid_cancer_risk=data.thyroid_cancer_risk,
            prediction=prediction_label
        )
        db.add(db_record)
        db.commit()

        return {"prediction": prediction_label}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def get_prediction_history(db: Session = Depends(get_db)):
    records = db.query(ThyroidCancerTypePrediction).order_by(ThyroidCancerTypePrediction.created_at.desc()).limit(10).all()
    return records