from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

@app.get("/")
def hello():
    return {"message": "Hello World!"}

@app.get("/about")
def about():
    return {"message": "This is a simple FastAPI application."}

@app.get("/view")
def patients():
    data = load_data()
    return data


@app.get("/patient/{patient_id}")
def patient(patient_id: str = Path(..., description="Patient ID", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail= "Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Field to sort by height, weight, bmi"), order: str = Query("asc", description="Sort in ascending or descending order")):
    valid_sort_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. {valid_sort_fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Use 'asc' or 'desc'.")
    data = load_data()
    sort_order = true if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse = sort_order)
    return sorted_data     
    