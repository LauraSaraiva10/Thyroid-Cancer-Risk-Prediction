from pydantic import BaseModel

class PredictionRequest(BaseModel):
    age: int
    gender: str
    family_history: str
    radiation_exposure: str
    iodine_deficiency: str
    smoking: str
    obesity: str
    diabetes: str
    tsh_level: float
    t3_level: float
    t4_level: float
    nodule_size: float
    thyroid_cancer_risk: str