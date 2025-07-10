"""
token_1.py - JWT token creation and decoding utilities for the RBAC API.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

# ------------------------------
# JWT Configuration
# ------------------------------
SECRET_KEY = "secretkeyformyapi123"  # Replace with a strong key (e.g., secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ------------------------------
# Create Access Token
# ------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token with given payload and expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ------------------------------
# Decode Access Token
# ------------------------------
def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode a JWT token and return the payload if valid.
    Returns None if token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

