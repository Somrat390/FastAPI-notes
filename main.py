from fastapi import FastAPI , Path, HTTPException, Query
import json

app = FastAPI()

def load_json():
    with open("patient.json", 'r') as file:
        return json.load(file)

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