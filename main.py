from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from rbac import get_current_user, require_role

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict to ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory patient store
class Patient(BaseModel):
    id: int
    name: str
    age: int

patients = [
    Patient(id=1, name="Alice", age=30),
    Patient(id=2, name="Bob", age=40)
]

# Check current user identity
@app.get("/whoami")
def who_am_i(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

# ✅ View all patients (all roles allowed)
@app.get("/patients", response_model=List[Patient])
def list_patients(current_user: dict = Depends(get_current_user)):
    return patients

# ✅ Add new patient (admin, clinician)
@app.post("/patients")
def add_patient(patient: Patient, current_user: dict = Depends(require_role(["admin", "clinician"]))):
    if any(p.id == patient.id for p in patients):
        raise HTTPException(status_code=400, detail="Patient ID already exists.")
    patients.append(patient)
    return {"message": f"Patient {patient.name} added."}

# ✅ Delete patient (admin only)
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, current_user: dict = Depends(require_role(["admin"]))):
    for patient in patients:
        if patient.id == patient_id:
            patients.remove(patient)
            return {"message": f"Patient {patient_id} deleted."}
    raise HTTPException(status_code=404, detail="Patient not found.")

# ✅ Get single patient detail
@app.get("/patients/{patient_id}")
def get_patient(patient_id: int, current_user: dict = Depends(get_current_user)):
    for patient in patients:
        if patient.id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found.")

# ✅ Clinician adds note (mocked)
@app.post("/patients/{patient_id}/notes")
def add_note(patient_id: int, current_user: dict = Depends(require_role(["clinician"]))):
    return {"message": f"Note added to patient {patient_id} by {current_user['name']}"}

# Only admin can delete patient
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, current_user: dict = Depends(require_role(["admin"]))):
    return {"message": f"Patient {patient_id} deleted by {current_user['name']}"}
