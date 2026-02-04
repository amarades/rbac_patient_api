"""
create_users.py - Script to create initial admin and clinician users in the database.
"""

from db import SessionLocal, engine, Base
from models import User
from passlib.context import CryptContext

# ----------------------------
# Password Hashing Setup
# ----------------------------
pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ----------------------------
# Database Session Initialization
# ----------------------------
# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ----------------------------
# Create Admin and Clinician Users
# ----------------------------
try:
    print("Hashing admin password...")
    admin_pw = pwd.hash("adminpass")
    print("Hashing clinician password...")
    clinician_pw = pwd.hash("clinicianpass")
    
    admin = User(username="admin", hashed_password=admin_pw, role="admin")
    clinician = User(username="clinician", hashed_password=clinician_pw, role="clinician")
except Exception as e:
    print(f"Error during hashing or user creation: {e}")
    raise e

db.add_all([admin, clinician])
db.commit()
db.close()

print("✅ Admin and Clinician created.")
