from fastapi import FastAPI, Depends
from rbac import get_current_user, require_role

app = FastAPI()

@app.get("/whoami")
def who_am_i(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

# Public for all valid users
@app.get("/patients/{patient_id}")
def get_patient_info(patient_id: int, current_user: dict = Depends(get_current_user)):
    return {"patient_id": patient_id, "info": f"Visible to {current_user['role']}"}

# Only clinician can add notes
@app.post("/patients/{patient_id}/notes")
def add_note(patient_id: int, current_user: dict = Depends(require_role(["clinician"]))):
    return {"message": f"Note added to patient {patient_id} by {current_user['name']}"}

# Only admin can delete patient
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, current_user: dict = Depends(require_role(["admin"]))):
    return {"message": f"Patient {patient_id} deleted by {current_user['name']}"}
