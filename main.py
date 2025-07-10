from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
import datetime
import os

from db import Base, engine, SessionLocal
from models import User, Patient, Note
from auth import authenticate_user, get_current_user, require_role
from token_1 import create_access_token

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/", response_class=HTMLResponse)
def index():
    path = os.path.join("frontend", "index.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>index.html not found</h1>", status_code=404)

Base.metadata.create_all(bind=engine)

# ----------------------------
# DB Dependency
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# Auth/Login Endpoint
# ----------------------------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ----------------------------
# Whoami Endpoint
# ----------------------------
@app.get("/whoami")
def whoami(user: User = Depends(get_current_user)):
    return {"username": user.username, "role": user.role}

# ----------------------------
# Add Patient (API with JSON Body)
# ----------------------------
class PatientInput(BaseModel):
    name: str
    age: int

@app.post("/patients")
def add_patient(data: PatientInput, db: Session = Depends(get_db)):
    patient = Patient(name=data.name, age=data.age)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return {"message": "Patient added", "patient_id": patient.id}

# ----------------------------
# Add Note to Patient
# ----------------------------
class NoteInput(BaseModel):
    content: str

@app.post("/patients/{patient_id}/notes")
def add_note(
    patient_id: int,
    data: NoteInput = Body(...),
    user=Depends(require_role("clinician")),
    db: Session = Depends(get_db)
):
    note = Note(
        patient_id=patient_id,
        user_id=user.id,
        content=data.content,
        created_at=datetime.datetime.utcnow()
    )
    db.add(note)
    db.commit()
    return {"message": "Note added"}

# ----------------------------
# List Patients + Notes
# ----------------------------
@app.get("/patients")
def list_patients_with_notes(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    response = []
    for p in patients:
        notes = db.query(Note).filter(Note.patient_id == p.id).all()
        note_data = [
            {
                "content": n.content,
                "created_at": n.created_at.strftime("%Y-%m-%d %H:%M"),
                "author": db.query(User).filter(User.id == n.user_id).first().username
            }
            for n in notes
        ]
        response.append({
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "notes": note_data
        })
    return response

# ----------------------------
# Delete Patient (API for JS)
# ----------------------------
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, user=Depends(require_role("admin")), db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted"}
