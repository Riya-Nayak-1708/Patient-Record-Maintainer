from fastapi import FastAPI, Path, HTTPException, Query  
from pydantic import basemodel, Field 
from typing import Annotated, Literal
import json 
app = FastAPI()

class Petient(basemodel):
    id: Annotated[str, Field(..., description='this is the id section', exapmle='1,2')]
    name: Annotated[str, Field(..., description='name of the patient should be written in this section', example='Riya ')]
    city: Annotated[str, Field(..., description='city of the patient',example='barielly') ]
    gender: Annotated[Literal['male','female,''others'],[Field(..., description='gender of the patient')]]
    age: Annotated[int, Field(..., lt=0, description='age of the patient')]
    weight_kg: Annotated[float, Field(..., lt=0, description='weight of the patient')]
    height_cm: Annotated[float, Field(..., description='height of the patient')]
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.wieght/(self.weight**2),2)
        return bmi 

    @computed_field
    @property
    def verdict(self) -> str;
        if self.bmi<18.5:
            return "underweight"
        elif self.bmi <25:
            return "normal"
        elif self.bmi <30:
            return "nromal"
        else:
            return "obbese"


def load_data():
    with open("patients.jason.json","r") as f:
        data = json.load(f)
    return data
@app.get("/")
def hello():
    return {'message':'PATIENT RECORD MANAGER API'}
@app.get("/about")
def about():
    return {'message':'here doctor can manage patients record easily'}
@app.get("/view")
def view():
    data = load_data()
    return data
@app.get('/patient/{patient_id}')
def patients(patient_id:int):
    data = load_data

    if patient_id in data:
        return data[patient_id]
    return{'message':'patient record not found'}