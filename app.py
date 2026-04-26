from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

# Importing the model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
    
    
    
app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad"]

tier_2_cities = [
    "Surat", "Jaipur", "Lucknow", "Kanpur", "Nagpur", 
    "Indore", "Thane", "Bhopal", "Visakhapatnam", "Patna", 
    "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik", 
    "Faridabad", "Meerut", "Rajkot", "Varanasi", "Srinagar", 
    "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai", "Prayagraj", 
    "Ranchi", "Jabalpur", "Gwalior", "Coimbatore", "Vijayawada", 
    "Jodhpur", "Madurai", "Raipur", "Kota", "Guwahati", 
    "Chandigarh", "Solapur", "Hubli-Dharwad", "Tiruchirappalli", "Bareilly"
]

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age must be between 1 and 119")]
    weight: Annotated[float, Field(..., gt=0, description="Weight must be a positive number")]
    height: Annotated[float, Field(..., gt=0, description="Height must be a positive number")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Income must be a positive number")]
    smoker : Annotated[bool, Field(..., description="Is user a smoker?")]
    city: Annotated[str, Field(..., description="City of residence")]
    occupation: Annotated[Literal['retired', 'unemployed', 'business_owner', 'government_job'], Field(..., description="Occupation type")]
    
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    
    @computed_field
    @property
    def lifestyle(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 30:
            return "young"
        elif self.age < 60:
            return "adult"
        else:
            return "senior"
        
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
        
@app.post("/predict")
def predict(data: UserInput):
    
    input_df = pd.DataFrame([{
        
            "bmi": data.bmi,
            "age_group": data.age_group,
            "lifestyle": data.lifestyle_risk,
            "income_lpa": data.income_lpa,
            "city_tier": data.city_tier,
            "occupation": data.occupation
        
    }])
    prediction = model.predict(input_df)[0]
    
    return JSONResponse(content={"predicted_premium": prediction}, status_code=200)
    