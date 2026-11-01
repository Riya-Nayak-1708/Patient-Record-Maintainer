from fastapi import FastAPI
import json 
app = FastAPI()


def load_data():
    with open("patients.jason.json","r") as f:
        data = json.load(f)
    return data
@app.get("/")
def hello():
    return {'message':'PATIENT RECORD MAGAER API'}
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