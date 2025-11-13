from typing import List, Optional, Annotated
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, StringConstraints, conint, field_validator
from datetime import date
 
app = FastAPI(description="Data validation using Pydantic v2+", version="1.0")
 
 
class Patient(BaseModel):
    patient_id: Annotated[str, StringConstraints(pattern=r"^PAT\d{4}$")] = Field(description="Must start with 'PAT' followed by 4 digits")
    name: Annotated[str, StringConstraints(min_length=3)] = Field(description="Minimum 3 characters")
    age: Annotated[int, Field(ge=1, le=120)] = Field(description="Age must be between 1 and 120")
    date_of_birth: date = Field(..., description="Date of birth (must not be in the future)")
    email: EmailStr = Field(description="Valid email address")
    blood_group: Annotated[str, StringConstraints(pattern=r"^(A|B|AB|O)[+-]$")] = Field(description="Valid blood group like A+, O-, etc.")
    contact_number: Annotated[str, StringConstraints(pattern=r"^[6-9]\d{9}$")] = Field(description="Indian mobile number (10 digits, starts with 6-9)")
 
     # Custom validation for DOB only
    @field_validator("date_of_birth")
    @classmethod
    def dob_not_in_future(cls, dob: date) -> date:
        today = date.today()
        if dob > today:
            raise ValueError("Date of birth cannot be in the future.")
        return dob
 
@app.post("/patients", response_model=Patient)
def create_patient(data: Patient):
    if data:
        return data
    raise HTTPException(status_code=400, detail="Internal Server error")
 
 
@app.get("/api/health")
def health():
    return {"message": "API is healthy"}
 