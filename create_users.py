from db import SessionLocal
from models import User
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

admin = User(username="admin", hashed_password=pwd.hash("adminpass"), role="admin")
clinician = User(username="clinician", hashed_password=pwd.hash("clinicianpass"), role="clinician")

db.add_all([admin, clinician])
db.commit()
db.close()
print("✅ Admin and Clinician created.")
