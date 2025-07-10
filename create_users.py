"""
create_users.py - Script to create initial admin and clinician users in the database.
"""

from db import SessionLocal
from models import User
from passlib.context import CryptContext

# ----------------------------
# Password Hashing Setup
# ----------------------------
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------------------
# Database Session Initialization
# ----------------------------
db = SessionLocal()

# ----------------------------
# Create Admin and Clinician Users
# ----------------------------
admin = User(username="admin", hashed_password=pwd.hash("adminpass"), role="admin")
clinician = User(username="clinician", hashed_password=pwd.hash("clinicianpass"), role="clinician")

db.add_all([admin, clinician])
db.commit()
db.close()

print("✅ Admin and Clinician created.")
