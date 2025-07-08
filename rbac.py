# rbac.py

from fastapi import Header, HTTPException

USERS = {
    "admin": {"name": "Alice", "role": "admin"},
    "clinician": {"name": "Bob", "role": "clinician"},
    "guest": {"name": "Gina", "role": "guest"},
}

def get_current_user(x_role: str = Header(...)):
    user = USERS.get(x_role.lower())
    if not user:
        raise HTTPException(status_code=401, detail="Invalid role")
    return user

def require_role(allowed_roles: list):
    def wrapper(x_role: str = Header(...)):
        user = get_current_user(x_role)
        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return wrapper

