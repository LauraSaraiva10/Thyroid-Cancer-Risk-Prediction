from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from models.base_model import Base

class ThyroidCancerTypePrediction(Base):
    __tablename__ = "thyroid_cancer_predictions"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    family_history = Column(String)
    radiation_exposure = Column(String)
    iodine_deficiency = Column(String)
    smoking = Column(String)
    obesity = Column(String)
    diabetes = Column(String)
    tsh_level = Column(Float)
    t3_level = Column(Float)
    t4_level = Column(Float)
    nodule_size = Column(Float)
    thyroid_cancer_risk = Column(String)
    prediction = Column(String)
    created_at = Column(DateTime, default=datetime.now())