from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import math
import joblib
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

final_features = ['age', 'chol_log', 'oldpeak_log', 'trestbps_log',
 'thalach_sq', 'sex_1', 'cp_1', 'cp_2', 'cp_3', 'fbs_1', 'restecg_1',
 'restecg_2', 'exang_1', 'slope_1', 'slope_2', 'ca_1', 'ca_2', 'ca_3',
 'thal_2', 'thal_3']

class InputData(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

model = joblib.load("../model/heart_disease_model.pkl")

def one_hot_encode(value, prefix, valid_vals):
    encoding = {}
    for v in valid_vals:
        key = f"{prefix}_{v}"
        encoding[key] = 1 if v == value else 0
    return encoding

@app.get('/')
def Hello():
    return {"message" : "Hello"}


@app.post("/predict")
def predict(data: InputData):
    print("Message")
    processed = {
        "age": data.age,
        "chol_log": math.log(data.chol + 1),
        "oldpeak_log": math.log(data.oldpeak + 1),
        "trestbps_log": math.log(data.trestbps + 1),
        "thalach_sq" : data.thalach ** 2,
    }

    processed.update(one_hot_encode(data.sex, "sex", [1]))
    processed.update(one_hot_encode(data.cp, "cp", [1, 2, 3]))
    processed.update(one_hot_encode(data.fbs, "fbs", [1]))
    processed.update(one_hot_encode(data.restecg, "restecg", [1, 2]))
    processed.update(one_hot_encode(data.exang, "exang", [1]))
    processed.update(one_hot_encode(data.slope, "slope", [1, 2]))
    processed.update(one_hot_encode(data.ca, "ca", [1, 2, 3]))
    processed.update(one_hot_encode(data.thal, "thal", [2, 3]))

    input_vector = []

    for feature in final_features:
        input_vector.append(processed.get(feature, 0))
    
    prediction = model.predict([input_vector])[0]

    return {"prediction": int(prediction), "input_vector": input_vector} 