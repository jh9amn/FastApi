from fastapi import FastAPI, HTTPException, Path, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Optional, Literal
from fastapi.responses import JSONResponse

app = FastAPI()


class Patient(BaseModel):
    
    id: Annotated[str, Field(description="Id of the patient", examples=["P001", "P002"])]
    name: Annotated[str, Field(description="Name of the patient")]
    city: Annotated[str, Field(description="City of the patient")]
    age: Annotated[int, Field(description="Age of the patient", ge=0)]
    gender: Annotated[Literal["male", "female", "others"], Field(description="Gender of the patient")]
    height: Annotated[float, Field(description="Height of the patient in mtrs")]
    weight: Annotated[float, Field(description="Weight of the patient in kgs")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        
        if self.bmi < 18.5:
            return "Underweight"
        
        elif self.bmi < 25:
            return "Normal"
        
        else: return "Overweight"
    
    

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    
def load_data():
    # Simulate loading data from a file or database
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data
        
def save_data(data):
    # Simulate saving data to a file or database
    with open("patients.json", "w") as f:
        json.dump(data, f)

@app.get("/")
def hell0():
    return {"message" : "Hello World"}

@app.get("/about")
def get_about():
    return {"message" : "I am a FastAPI application"}

@app.get("/patients")
def get_patients():
    data = load_data()
    return data


# Path parameter to get a specific patient by ID
@app.get("/patients/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

# Query parameter to sort patients by age
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi") , order : str =  Query("asc", description="Order of sorting")):
    
    valid_fields = ["height", "weight", "bmi"]
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Valid orders are: asc, desc")
    
    sort_order = 1 if order == "asc" else -1
    data = load_data()
    
    sorted_patients = sorted(data.values(), key=lambda x: x[sort_by], reverse=(sort_order == -1))
    
    return sorted_patients


## Add a new patient to the data
@app.post("/create")
def create_patient(patient: Patient):
    
    # Load existing data
    data = load_data()
    
    # Check if the patient ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    
    # Add the new patient to the data
    data[patient.id] = patient.model_dump(exclude=["bmi", "verdict", "id"])
    
    save_data(data)
    
    return JSONResponse(content={"message": "Patient created successfully", "Patient ID": patient.id}, status_code=201)



@app.put("/update/{patient_id}")
# def update_patient(patient_id: str, patient_update: PatientUpdate):

#     data = load_data()

#     if patient_id not in data:
#         raise HTTPException(status_code=404, detail="Patient not found")

#     existing_patient_data = data[patient_id]

#     # only provided fields
#     update_patient_data = patient_update.model_dump(exclude_unset=True, exclude_none=True)

#     # update data
#     existing_patient_data.update(update_patient_data)

#     # validate + recalc BMI
#     patient_pydantic_obj = Patient(**existing_patient_data)

#     # convert back to dict
#     updated_data = patient_pydantic_obj.model_dump()

#     # save
#     data[patient_id] = updated_data
#     save_data(data)

#     return JSONResponse(
#         content={
#             "message": "Patient updated successfully",
#             "Patient ID": patient_id,
#             "data": updated_data
#         },
#         status_code=200
#     )

def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})



@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(content={"message": "Patient deleted successfully",
                                "Patient ID": patient_id}, status_code=200 )
        