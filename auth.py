"""
auth.py - Handles authentication and role-based access control for the RBAC API.
"""

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from token_1 import decode_access_token
from db import SessionLocal
from models import User
from passlib.context import CryptContext

# ----------------------------
# Password Hashing Setup
# ----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------------------
# OAuth2 Scheme for JWT Bearer Token
# ----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ----------------------------
# Password Verification
# ----------------------------
def verify_password(plain, hashed):
    """
    Verifies a plain password against a hashed password.
    """
    return pwd_context.verify(plain, hashed)

# ----------------------------
# User Authentication
# ----------------------------
def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticates a user by username and password.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# ----------------------------
# Database Dependency
# ----------------------------
def get_db():
    """
    Provides a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# Get Current User from JWT
# ----------------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieves the current user from the JWT token.
    """
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ----------------------------
# Role-Based Access Dependency
# ----------------------------
def require_role(required_role: str):
    """
    Dependency to require a specific user role.
    """
    def role_dependency(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_dependency

