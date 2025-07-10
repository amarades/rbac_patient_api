from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import datetime

from db import Base, engine, SessionLocal
from models import User, Patient, Note
from rbac import get_current_user, require_role
from auth import authenticate_user
from token_1 import create_access_token
from auth import get_current_user, require_role


# ----------------------------
# Create and configure app
# ----------------------------
app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# ----------------------------
# Initialize DB tables
# ----------------------------
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
# Home Page
# ----------------------------
@app.get("/", response_class=HTMLResponse)
def index():
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read())

# ----------------------------
# Auth/Login Endpoint
# ----------------------------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# ----------------------------
# Who Am I Endpoint
# ----------------------------
# NEW (token-based)
@app.get("/whoami")
def who_am_i(user=Depends(get_current_user)):
    return {"username": user.username, "role": user.role}

# ----------------------------
# Add Patient (API)
# ----------------------------
@app.post("/patients")
def add_patient(name: str, age: int, db: Session = Depends(get_db)):
    patient = Patient(name=name, age=age)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return {"message": "Patient added", "patient_id": patient.id}

# ----------------------------
# Add Patient (via HTML Form)
# ----------------------------
@app.post("/patients/add")
def add_patient_ui(name: str = Form(...), age: int = Form(...), db: Session = Depends(get_db)):
    patient = Patient(name=name, age=age)
    db.add(patient)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# ----------------------------
# Add Note to Patient
# ----------------------------

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
# Delete Patient via UI
# ----------------------------
@app.post("/patients/{patient_id}/notes")
def add_note(patient_id: int, content: str, user=Depends(require_role("clinician")), db: Session = Depends(get_db)):
    note = Note(patient_id=patient_id, user_id=user.id, content=content, created_at=datetime.datetime.utcnow())
    db.add(note)
    db.commit()
    return {"message": "Note added"}

@app.post("/patients/delete")
def delete_patient_ui(patient_id: int = Form(...), user=Depends(require_role("admin")), db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

