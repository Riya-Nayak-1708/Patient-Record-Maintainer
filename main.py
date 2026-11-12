
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="Patient ID", example="1")]
    name: Annotated[str, Field(..., description="Patient name")]
    city: Annotated[str, Field(..., description="Patient city")]
    gender: Literal["male", "female", "others"]
    age: Annotated[int, Field(gt=0, description="Patient age")]
    weight_kg: Annotated[float, Field(gt=0, description="Weight in kg")]
    height_cm: Annotated[float, Field(gt=0, description="Height in cm")]

    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif self.bmi < 25:
            return "normal"
        elif self.bmi < 30:
            return "overweight"
        else:
            return "obese"
    
class PatientUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    gender: Literal["male", "female", "others"] | None = None
    age: int | None = Field(default=None, gt=0)
    weight_kg: float | None = Field(default=None, gt=0)
    height_cm: float | None = Field(default=None, gt=0)


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data


def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)


@app.get("/")
def hello():
    return {"message": "PATIENT RECORD MANAGER API"}


@app.get("/about")
def about():
    return {"message": "Here doctor can manage patient records easily"}


@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def patients(patient_id: str):
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(
        status_code=404,
        detail="Patient record not found"
    )


@app.post("/create")
def create_patient(patient: Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient already exists"
        )

    data[patient.id] = patient.model_dump()

    save_data(data)

    return {
        "message": "Patient added successfully",
        "patient": patient
    }



@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient: Patient):

    data = load_data()

    # Check whether patient exists
    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )


    if patient.id != patient_id:
        raise HTTPException(
            status_code=400,
            detail="Patient ID does not match"
        )

   
    data[patient_id] = patient.model_dump()

   
    save_data(data)

    return {
        "message": "Patient updated successfully",
        "patient": patient
    }



@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

   
    deleted_patient = data.pop(patient_id)

    # Save updated data
    save_data(data)

    return {
        "message": "Patient deleted successfully",
        "deleted_patient": deleted_patient
    }

@app.patch("/edit/{patient_id}")
def update_patient_partial(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    # Check patient exists
    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

   
    existing_patient = data[patient_id]
    update_data = patient_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    updated_patient = {**existing_patient, **update_data}

    validated_patient = Patient(**updated_patient)

    data[patient_id] = validated_patient.model_dump()

    save_data(data)

    return {
        "message": "Patient updated successfully",
        "patient": validated_patient
    }
