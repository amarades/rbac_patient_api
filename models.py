"""
models.py - SQLAlchemy ORM models for the RBAC API.
Defines User, Patient, and Note tables and their relationships.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base

# ----------------------------
# User Table
# ----------------------------
class User(Base):
    """
    User model/table.
    Fields:
        - id: Primary key
        - username: Unique username
        - hashed_password: Hashed password for authentication
        - role: User role (e.g., "admin", "clinician")
    Relationships:
        - notes: One-to-many relationship to Note
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # One-to-many: User -> Notes
    notes = relationship("Note", back_populates="user")


# ----------------------------
# Patient Table
# ----------------------------
class Patient(Base):
    """
    Patient model/table.
    Fields:
        - id: Primary key
        - name: Patient's name
        - age: Patient's age
    Relationships:
        - notes: One-to-many relationship to Note
    """
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
    """
    Note model/table.
    Fields:
        - id: Primary key
        - patient_id: Foreign key to Patient
        - user_id: Foreign key to User (author)
        - content: Note content
        - created_at: Timestamp of note creation
    Relationships:
        - patient: Many-to-one relationship to Patient
        - user: Many-to-one relationship to User
    """
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="notes")
    user = relationship("User", back_populates="notes")
