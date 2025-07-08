from fastapi import FastAPI , Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import List, Dict, Annotated,Literal
import json

app = FastAPI()



class Patient(BaseModel):
    id: Annotated[str, Field(...,description="Id of the patient", example="P001")]
    name: Annotated[str,Field(...,description="Name of the patient", examples=["John Doe"])]
    city: Annotated[str,Field(...,description="City of the paitent", examples=["New York"])]
    age: Annotated[int, Field(...,gt=0, lt=120, description="Age of the patient", examples=[30])]
    gender : Annotated[Literal['Male','Female', 'Other'], Field(..., description="Gender of the Paitent")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in m", examples=[1.70])]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg", examples=[70.5])]

    @computed_field
    @property
    def BMI(self)-> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.BMI < 18.5:
            return "Underweight"
        elif 18.5 <= self.BMI < 24.9:
            return "Normal weight"
        elif 25 <= self.BMI < 29.9:
            return "Overweight"
        else:
            return "Obesity"


def load_json():
    with open("patient.json", 'r') as file:
        return json.load(file)

def save_data(data):
    with open("patient.json", 'w') as file:
        json.dump(data, file)

@app.get("/")
def hello():
    return {"message":"Patient Management System API"}

@app.get("/about")
def about():
    return {"message":"A fully functional API for managing patient data, appointments, and medical records."}

@app.get("/view")
def view_patients():
    patients = load_json()
    return {"patients": patients}

@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient in the database", example="P001")):
    patient = load_json()
    if patient_id in patient:
        return patient[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found", headers={"X-Error": "Patient ID not found"})

@app.get("/sort")
def sort_patient(sort_by: str = Query(..., description="Sort by height,weight,BMI"), order: str = Query("asc", description="Order of sorting: asc or desc")):
    valid_fields = ["height", "weight", "BMI"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail= f"Invalid field select from {valid_fields}")
    
    data = load_json()

    sort_order = True if order == "dsc" else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


@app.post("/create")
def add_patient(patient: Patient):
    ## load data from json file
    data = load_json()
    ## check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists", headers={"X-Error": "Duplicate ID"})
    ## add patient to data
    data[patient.id] = patient.model_dump(exclude=['id'])

    ## save data to json file
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient added successfully"})