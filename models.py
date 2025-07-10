from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base

# ----------------------------
# User Table
# ----------------------------
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # Store hashed password
    role = Column(String, nullable=False)  # E.g., "admin", "clinician", etc.

    # One-to-many: User -> Notes
    notes = relationship("Note", back_populates="user")


# ----------------------------
# Patient Table
# ----------------------------
class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    # One-to-many: Patient -> Notes
    notes = relationship("Note", back_populates="patient")


# ----------------------------
# Note Table
# ----------------------------
class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="notes")
    user = relationship("User", back_populates="notes")
